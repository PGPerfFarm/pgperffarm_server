import csv
import multiprocessing
import os
import psycopg2
import psycopg2.extras
import time

from multiprocessing import Process, Queue
from utils.logging import log

class PostgresCollector(object):
	'collects basic PostgreSQL-level statistics (bgwriter, databases, tables, indexes)'

	def __init__(self, dbname):
		self._dbname = dbname


	def start(self):
		self._in_queue = Queue()
		self._out_queue = Queue()
		self._worker = Process(target=run_collector, args=(self._in_queue, self._out_queue, self._dbname))
		self._worker.start()


	def stop(self):

		# signal the worker process to stop by writing a value into the queue
		self._in_queue.put(True)

		log("stopping the PostgreSQL statistics collector")

		# Wait for collector to place result into the output queue. This needs
		# to happen before calling join() otherwise it causes a deadlock.
		log("waiting for collector result in a queue")
		self._result = self._out_queue.get()

		# And wait for the worker to terminate. This should be pretty fast as
		# the collector places result into the queue right before terminating.
		log("waiting for collector process to terminate")
		self._worker.join()

		self._worker = None
		self._in_queue = None
		self._out_queue = None


	def result(self):
		return self._result


def run_collector(in_queue, out_queue, dbname, interval=1.0):
	'collector code for a separate process, communicating through a pair of queues'

	bgwriter_log = None
	tables_log = None
	indexes_log = None
	database_log = None

	# get current timestamp
	ts = time.time()

	while True:

		# wait until the next tick
		ts += interval

		# if we're behind, skip forward
		if ts < time.time():
			continue

		# sleep (but only for the remaining time, to prevent drift)
		time.sleep(ts - time.time())

		# if we've received message in the input queue (not empty), terminate
		if not in_queue.empty():
			log("PostgreSQL collector received request to terminate")
			break

		# open connection to the benchmark database (if can't open, continue)
		# notice this is intentionally after the wait, so we'll wait before
		# next connection attempt
		try:
			conn = psycopg2.connect('host=localhost dbname=%s' % (dbname,))
			cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		except Exception as ex:
			continue

		# background writer stats
		cur.execute('SELECT EXTRACT(EPOCH FROM now()) AS ts, * FROM pg_stat_bgwriter')

		# on the first iteration, construct the CSV files
		if not bgwriter_log:
			fields = [desc[0] for desc in cur.description]
			bgwriter_log = csv.DictWriter(open('bgwriter.csv', 'w'), fields)
			bgwriter_log.writeheader()

		bgwriter_log.writerows(cur.fetchall())

		# TODO we can assume statistics for most objects (tables, indexes) won't
		# change every second, so we can optimize the amount of data by detecting
		# changes and only keeping the two rows next to it

		# table statistics
		cur.execute('SELECT EXTRACT(EPOCH FROM now()) AS ts, * FROM pg_stat_all_tables JOIN pg_statio_all_tables USING (relid, schemaname, relname)')

		# on the first iteration, construct the CSV files
		if not tables_log:
			fields = [desc[0] for desc in cur.description]
			tables_log = csv.DictWriter(open('tables.csv', 'w'), fields)
			tables_log.writeheader()

		tables_log.writerows(cur.fetchall())

		# index statistics
		cur.execute('SELECT EXTRACT(EPOCH FROM now()) AS ts, * FROM pg_stat_all_indexes JOIN pg_statio_all_indexes USING (relid, indexrelid, schemaname, relname, indexrelname)')

		# on the first iteration, construct the CSV files
		if not indexes_log:
			fields = [desc[0] for desc in cur.description]
			indexes_log = csv.DictWriter(open('indexes.csv', 'w'), fields)
			indexes_log.writeheader()

		indexes_log.writerows(cur.fetchall())

		# database statistics
		cur.execute('SELECT EXTRACT(EPOCH FROM now()) AS ts, * FROM pg_stat_database')

		# on the first iteration, construct the CSV files
		if not database_log:
			fields = [desc[0] for desc in cur.description]
			database_log = csv.DictWriter(open('database.csv', 'w'), fields)
			database_log.writeheader()

		database_log.writerows(cur.fetchall())

		conn.close()

	log("PostgreSQL collector generates CSV results")

	# close the CSV writers
	bgwriter_log = None
	tables_log = None
	indexes_log = None
	database_log = None

	result = {}

	with open('bgwriter.csv', 'r') as f:
		result.update({'bgwriter' : f.read()})

	with open('tables.csv', 'r') as f:
		result.update({'tables' : f.read()})

	with open('indexes.csv', 'r') as f:
		result.update({'indexes' : f.read()})

	with open('database.csv', 'r') as f:
		result.update({'database' : f.read()})

	# remove the files
	os.remove('bgwriter.csv')
	os.remove('tables.csv')
	os.remove('indexes.csv')
	os.remove('database.csv')

	out_queue.put(result)

	log("PostgreSQL collector put results into output queue and terminates")
