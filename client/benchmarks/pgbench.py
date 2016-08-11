import math
import os
import os.path
import re
import time

from multiprocessing import cpu_count
from utils.logging import log
from utils.misc import available_ram, run_cmd


class PgBench(object):
	'a simple wrapper around pgbench, running TPC-B-like workload by default'

	# TODO allow running custom scripts, not just the default read-write/read-only tests
	# TODO allow running 'prepared' mode

	def __init__(self, bin_path, dbname, runs = 3, duration = 60):
		'''
		bin_path   - path to PostgreSQL binaries (dropdb, createdb, psql commands)
		dbname     - name of the database to use
		runs       - number of runs (for each client count)
		duration   - duration of each execution
		'''

		self._bin = bin_path
		self._dbname = dbname
		self._results = {}
		self._duration = duration
		self._runs = runs


	@staticmethod
	def _configure(cpu_count, ram_mbs):
		'derive the configurations to benchmark from CPU count and RAM size'

		config = []

		# TODO allow overriding this from a global config

		# scales: 10 (small), 50% of RAM, 200% of RAM
		#for s in [10, ram_mbs/15/2, ram_mbs*2/15]:
		for s in [10]:
			config.append({'scale' : int(math.ceil(s/10)*10),
						   'clients' : [1, cpu_count, 2*cpu_count]})

		return config


	def _init(self, scale):
		'recreate the database (drop + create) and populate it with given scale'

		# initialize results for this dataset scale
		self._results[scale] = {'init' : None, 'warmup' : None, 'runs' : []}

		log("recreating '%s' database" % (self._dbname,))
		run_cmd(['dropdb', '--if-exists', self._dbname], env={'PATH' : self._bin})
		run_cmd(['createdb', self._dbname], env={'PATH' : self._bin})

		log("initializing pgbench '%s' with scale %s" % (self._dbname, scale))
		r = run_cmd(['pgbench', '-i', '-s', str(scale), self._dbname], env={'PATH' : self._bin})

		# remember the init duration
		self._results[scale]['init'] = r[2]


	@staticmethod
	def _parse_results(data):
		'extract results (including parameters) from the pgbench output'

		scale = -1
		r = re.search('scaling factor: ([0-9]+)', data)
		if r:
			scale = r.group(1)

		mode = -1
		r = re.search('query mode: (.+)', data)
		if r:
			mode = r.group(1)

		clients = -1
		r = re.search('number of clients: ([0-9]+)', data)
		if r:
			clients = r.group(1)

		threads = -1
		r = re.search('number of threads: ([0-9]+)', data)
		if r:
			threads = r.group(1)

		duration = -1
		r = re.search('duration: ([0-9]+) s', data)
		if r:
			duration = r.group(1)

		latency = -1
		r = re.search('latency average: ([0-9\.]+) ms', data)
		if r:
			latency = r.group(1)

		tps = -1
		r = re.search('tps = ([0-9]+\.[0-9]+) \(excluding connections establishing\)', data)
		if r:
			tps = r.group(1)

		return {'scale' : scale,
				'mode' : mode,
				'clients' : clients,
				'threads' : threads,
				'duration' : duration,
				'latency' : latency,
				'tps' : tps}


	@staticmethod
	def _merge_logs():
		'merge log files produced by pgbench threads (aggregated per second)'

		r = {}

		# find pgbench transaction logs in current directory
		logs = [v for v in os.listdir(os.getcwd()) if re.match('pgbench_log.[0-9]+(\.[0-9]+)?', v)]

		# parse each transaction log, and merge it into the existing results
		for l in logs:
			worker_log = open(l, 'r')
			for row in worker_log:
				values = row.split(' ')

				timestamp = values[0]
				tps = int(values[1])
				lat_sum = long(values[2])
				lat_sum2 = long(values[3])
				lat_min = int(values[4])
				lat_max = int(values[5])

				# if first record for the timestamp, store it, otherwise merge
				if timestamp not in r:
					r[timestamp] = {'tps' : tps,
									'lat_sum' : lat_sum, 'lat_sum2' : lat_sum2,
									'lat_min' : lat_min, 'lat_max' : lat_max}
				else:
					r[timestamp]['tps'] += int(tps)
					r[timestamp]['lat_sum'] += long(lat_sum)
					r[timestamp]['lat_sum2'] += long(lat_sum2)
					r[timestamp]['lat_min'] = min(r[timestamp]['lat_min'], int(lat_min))
					r[timestamp]['lat_max'] = max(r[timestamp]['lat_max'], int(lat_max))

			os.remove(l)

		# now produce a simple text log sorted by the timestamp
		o = []
		for t in sorted(r.keys()):
			o.append('%s %d %d %d %d %d' % (t, r[t]['tps'], r[t]['lat_sum'], r[t]['lat_sum2'], r[t]['lat_min'], r[t]['lat_max']))

		return '\n'.join(o)


	def check_config(self):
		'check pgbench configuration (existence of binaries etc.)'

		issues = []

		if not os.path.isdir(self._bin):
			issues.append("bin_dir='%s' does not exist" % (self._bin,))
		elif not os.path.exists('%s/pgbench' % (self._bin,)):
			issues.append("pgbench not found in bin_dir='%s'" % (self._bin,))
		elif not os.path.exists('%s/createdb' % (self._bin,)):
			issues.append("createdb not found in bin_dir='%s'" % (self._bin,))
		elif not os.path.exists('%s/dropdb' % (self._bin,)):
			issues.append("dropdb not found in bin_dir='%s'" % (self._bin,))
		elif not os.path.exists('%s/psql' % (self._bin,)):
			issues.append("psql not found in bin_dir='%s'" % (self._bin,))

		if type(self._duration) is not int:
			issues.append("duration (%s) needs to be an integer" % (self._duration,))
		elif not self._duration >= 1:
			issues.append("duration (%s) needs to be >= 1" % (self._duration,))

		if type(self._runs) is not int:
			issues.append("runs (%s) needs to be an integer" % (self._duration,))
		elif not self._runs >= 1:
			issues.append("runs (%s) needs to be >= 1" % (self._runs,))

		return issues


	def _run(self, duration, nclients=1, njobs=1, read_only=False, aggregate=True):
		'run pgbench on the database (either a warmup or actual benchmark run)'

		args = ['pgbench', '-c', str(nclients), '-j', str(njobs), '-T', str(duration)]

		# aggregate on per second resolution
		if aggregate:
			args.extend(['-l', '--aggregate-interval', '1'])

		if read_only:
			args.extend(['-S'])

		args.extend([self._dbname])

		# do an explicit checkpoint before each run
		run_cmd(['psql', self._dbname, '-c', 'checkpoint'], env={'PATH' : self._bin})

		log("pgbench : clients=%d, jobs=%d, aggregate=%s, read-only=%s, duration=%d" % (nclients, njobs, aggregate, read_only, duration))

		start = time.time()
		r = run_cmd(args, env={'PATH' : self._bin})
		end = time.time()

		r = PgBench._parse_results(r[1])
		r.update({'read-only' : read_only})

		if aggregate:
			r.update({'transaction-log' : PgBench._merge_logs()})

		r.update({'start' : start, 'end' : end})

		return r


	def run_tests(self):
		'execute the whole benchmark, including initialization, warmup and benchmark runs'

		# derive configuration for the CPU count / RAM size
		configs = PgBench._configure(cpu_count(), available_ram())

		for config in configs:

			# init for the dataset scale and warmup
			self._init(config['scale'])

			warmup = self._run(self._duration, cpu_count(), cpu_count())
			results = []

			for run in range(self._runs):

				log("pgbench : run=%d" % (run,))

				for clients in config['clients']:

					# read-only
					r = self._run(self._duration, clients, clients, True)
					r.update({'run' : run})
					results.append(r)

					# read-write
					r = self._run(self._duration, clients, clients, False)
					r.update({'run' : run})
					results.append(r)

			self._results[config['scale']] = {
				'warmup' : warmup,
				'runs' : results
			}

		return self._results
