import json
import os
import codecs
import requests
import csv
import shutil
import psutil

from multiprocessing import Process, Queue
from time import gmtime, strftime
from subprocess import check_output
import simplejson as json

from utils.logging import log
from utils.misc import run_cmd

from settings import *
from settings_local import *


class BenchmarkRunner(object):
	'manages iterations of all the benchmarks, including cluster restarts etc.'

	def __init__(self, out_dir, url, secret, cluster, collector):
		''
		self._output = out_dir  # where to store output files
		self._benchmarks = {}  # bench name => class implementing the benchmark
		self._configs = {}  # config name => (bench name, config)
		self._cluster = cluster
		self._collector = collector
		self._url = url
		self._secret = secret


	def register_benchmark(self, benchmark_name, benchmark_class):
		

		self._benchmarks.update({benchmark_name: benchmark_class})


	def register_config(self, config_name, benchmark_name, branch, commit,
						postgres_config, **kwargs):
		
		self._configs.update({config_name: {'benchmark': benchmark_name, 'config': kwargs, 'branch': branch, 'commit': commit, 'postgres': postgres_config}})


	def _check_config(self, config_name):
		''

		log("Checking benchmark configuration '%s'" % (config_name,))

		# construct the benchmark class for the given config name
		config = self._configs[config_name]
		bench = self._benchmarks[config['benchmark']]

		# expand the attribute names
		bench = bench(**config['config'])

		# run the tests
		return bench.check_config()


	def check(self):
		'check configurations for all benchmarks'

		issues = {}

		for config_name in self._configs:
			t = self._check_config(config_name)
			if t:
				issues[config_name] = t

		return issues


	def _run_config(self, config_name):

		log("Running benchmark configuration '%s'" % (config_name,))

		# construct the benchmark class for the given config name
		config = self._configs[config_name]
		bench = self._benchmarks[config['benchmark']]

		# expand the attribute names
		bench = bench(**config['config'])

		self._cluster.start(config=config['postgres'])

		# start collector(s) of additional info
		self._collector.start()

		# if requested output to CSV, create a queue and collector process
		csv_queue = None
		csv_collector = None
		if 'csv' in config['config'] and config['config']['csv']:
			csv_queue = Queue()
			csv_collector = Process(target=csv_collect_results,
									args=(config_name, csv_queue))
			csv_collector.start()

		# run the tests
		r = bench.run_tests(csv_queue)

		# notify the result collector to end and wait for it to terminate
		if csv_queue:
			csv_queue.put("STOP")
			csv_collector.join()

		# stop the cluster and collector
		log("terminating collectors")
		self._collector.stop()
		self._cluster.stop()

		# merge data from the collectors into the JSON document with results
		r.update(self._collector.result())

		r['meta'] = {
			'benchmark': config['benchmark'],
			'date': strftime("%Y-%m-%d %H:%M:%S.000000+00", gmtime()),
			'name': config_name,
		}

		r['git'] = {
				'branch': config['branch'],
				'commit': config['commit'],
				'remote': GIT_URL
		}

		r['kernel'] = {
			'uname_s': check_output(['uname', '-s']).rstrip(),
			'uname_r': check_output(['uname', '-r']).rstrip(),
			'uname_m': check_output(['uname', '-m']).rstrip(),
			'uname_v': check_output(['uname', '-v']).rstrip(),
		}

		uname = os.popen("uname").readlines()[0].split()[0]

		if uname == 'Linux':
			r['os_information'] = {
				'distributor': check_output(['lsb_release', '-i']).rstrip(),
				'description': check_output(['lsb_release', '-d']).rstrip(),
				'release': check_output(['lsb_release', '-r']).rstrip(),
				'codename': check_output(['lsb_release', '-c']).rstrip()
			}

		if uname == 'Darwin':
			r['os_information'] = {
				'distributor': check_output(['sw_vers', '-productName']).rstrip(),
				'description': 'not available',
				'release': check_output(['sw_vers', '-productVersion']).rstrip(),
				'codename': check_output(['sw_vers', '-buildVersion']).rstrip()
			}

		with open('%s/%s' % (self._output, 'results.json'), 'w+') as f:
			f.write(json.dumps(r, indent=4))


	def run(self):
		'run all the configured benchmarks'
		
		try:
			os.mkdir(self._output)
		except OSError as e:
			log("Output directory already exists: %s" % self._output)

		for config_name in self._configs:
			self._run_config(config_name)


def csv_collect_results(bench_name, queue):
	'collect results into a CSV file (through a queue)'

	with open("%s.csv" % (bench_name,), 'w') as results_file:

		# collect data from the queue - once we get a plain string (instead of
		# a list), it's a sign to terminate the collector
		while True:

			v = queue.get()

			# if we got a string, it means 'terminate'
			if isinstance(v, str):
				log("Terminating CSV result collector...")
				return

			v = [str(x) for x in v]

			# otherwise we expect the value to be a list, and we just print it
			results_file.write(bench_name + "\t" + "\t".join(v) + "\n")
			results_file.flush()
