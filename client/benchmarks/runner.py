import json
import os

from utils.logging import log


class BenchmarkRunner(object):
	'manages runs of all the benchmarks, including cluster restarts etc.'

	def __init__(self, out_dir, cluster, collector):
		''

		self._output = out_dir	# where to store output files
		self._benchmarks = {}	# bench name => class implementing the benchmark
		self._configs = {}		# config name => (bench name, config)
		self._cluster = cluster
		self._collector = collector


	def register_benchmark(self, benchmark_name, benchmark_class):
		''

		# FIXME check if a mapping for the same name already exists
		self._benchmarks.update({benchmark_name : benchmark_class})


	def register_config(self, config_name, benchmark_name, postgres_config, **kwargs):
		''

		# FIXME check if a mapping for the same name already exists
		# FIXME check that the benchmark mapping already exists
		self._configs.update({config_name : {'benchmark' : benchmark_name, 'config' : kwargs, 'postgres' : postgres_config}})


	def _run_config(self, config_name):
		''

		log("running benchmark configuration '%s'" % (config_name,))

		# construct the benchmark class for the given config name
		config = self._configs[config_name]
		bench = self._benchmarks[config['benchmark']]

		# expand the attribute names
		bench = bench(**config['config'])

		self._cluster.start(config = config['postgres'])

		# start collector(s) of additional info
		self._collector.start()

		# run the tests
		r = bench.run_tests()

		# stop the cluster and collector
		self._collector.stop()
		self._cluster.stop()

		# merge data from the collectors into the JSON document with results
		r.update(self._collector.result())

		# read the postgres log
		with open('pg.log', 'r') as f:
			r['postgres-log'] = f.read()

		r['meta'] = {'benchmark' : config['benchmark'],
					 'name' : config_name}

		os.remove('pg.log')

		with open('%s/%s.json' % (self._output, config_name), 'w') as f:
			f.write(json.dumps(r, indent=4))


	def run(self):
		'run all the configured benchmarks'

		# FIXME check that the directory does not exist
		os.mkdir(self._output)

		for config_name in self._configs:
			self._run_config(config_name)
