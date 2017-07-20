import json
import os

from utils.logging import log
from multiprocessing import Process, Queue


class BenchmarkRunner(object):
    'manages runs of all the benchmarks, including cluster restarts etc.'

    def __init__(self, out_dir, cluster, collector):
        ''

        self._output = out_dir  # where to store output files
        self._benchmarks = {}  # bench name => class implementing the benchmark
        self._configs = {}  # config name => (bench name, config)
        self._cluster = cluster
        self._collector = collector

    def register_benchmark(self, benchmark_name, benchmark_class):
        ''

        # FIXME check if a mapping for the same name already exists
        self._benchmarks.update({benchmark_name: benchmark_class})

    def register_config(self, config_name, benchmark_name, postgres_config,
                        **kwargs):
        ''

        # FIXME check if a mapping for the same name already exists
        # FIXME check that the benchmark mapping already exists
        self._configs.update({config_name: {'benchmark': benchmark_name,
                                            'config': kwargs,
                                            'postgres': postgres_config}})

    def _check_config(self, config_name):
        ''

        log("checking benchmark configuration '%s'" % (config_name,))

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

        if os.path.exists(self._output):
            issues['global'] = ["output directory '%s' already exists" %
                                (self._output,)]

        for config_name in self._configs:
            t = self._check_config(config_name)
            if t:
                issues[config_name] = t

        return issues

    def _run_config(self, config_name):
        ''

        log("running benchmark configuration '%s'" % (config_name,))

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
        if config['benchmark']['csv']:
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

        # read the postgres log
        with open('pg.log', 'r') as f:
            r['postgres-log'] = f.read()

        r['meta'] = {'benchmark': config['benchmark'],
                     'name': config_name}

        os.remove('pg.log')

        with open('%s/%s.json' % (self._output, config_name), 'w') as f:
            f.write(json.dumps(r, indent=4))

    def run(self):
        'run all the configured benchmarks'

        os.mkdir(self._output)

        for config_name in self._configs:
            self._run_config(config_name)


def csv_collect_results(bench_name, queue):
    'collect results into a CSV files (through a queue)'

    with open("%s.csv" % (bench_name,), 'w') as results_file:

        # collect data from the queue - once we get a plain string (instead of
        # a list), it's a sign to terminate the collector
        while True:

            v = queue.get()

            # if we got a string, it means 'terminate'
            if isinstance(v, str):
                log("terminating CSV result collector")
                return

            v = [str(x) for x in v]

            # otherwise we expect the value to be a list, and we just print it
            results_file.write(bench_name + "\t" + "\t".join(v) + "\n")
            results_file.flush()
