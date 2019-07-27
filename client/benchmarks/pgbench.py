import math
import os
import os.path
import re
import time

from numpy import mean, median, std

from multiprocessing import cpu_count
from utils.logging import log
from utils.misc import available_ram, run_cmd


class PgBench(object):
    'a simple wrapper around pgbench, running TPC-B-like workload by default'

    # TODO allow running custom scripts, not just the default
    #      read-write/read-only tests
    # TODO allow running 'prepared' mode

    def __init__(self, bin_path, dbname, runs=3, duration=60, csv=False,
                 results_dir=None):
        '''
        bin_path   - path to PostgreSQL binaries (dropdb, createdb, psql
                     commands)
        dbname     - name of the database to use
        duration   - duration of each execution
        runs       - number of runs (for each client count)
        out_dir    - output directory
        '''

        self._bin = bin_path
        self._csv = csv
        self._dbname = dbname
        self._duration = duration
        self._outdir = results_dir
        self._runs = runs

        self._env = os.environ
        self._env['PATH'] = ':'.join([bin_path, self._env['PATH']])

        self._results = {}

    @staticmethod
    def _configure(cpu_count, ram_mbs):
        'derive the configurations to benchmark from CPU count and RAM size'

        config = []

        # TODO allow overriding this from a global config

        # scales: 10 (small), 50% of RAM, 200% of RAM
        # for s in [10, ram_mbs/15/2, ram_mbs*2/15]:
        for s in [10]:
            config.append({'scale': int(math.ceil(s / 10) * 10),
                           'clients': [1, cpu_count, 2 * cpu_count]})

        return config

    def _init(self, scale):
        """
        recreate the database (drop + create) and populate it with given scale
        """

        # initialize results for this dataset scale
        self._results['results'] = {
            'init': None,
            'runs': [],
            'warmup': None,
        }

        log("recreating '%s' database" % (self._dbname,))
        run_cmd(['dropdb', '--if-exists', self._dbname], env=self._env)
        run_cmd(['createdb', self._dbname], env=self._env)

        log("initializing pgbench '%s' with scale %s" % (self._dbname, scale))
        r = run_cmd(['pgbench', '-i', '-s', str(scale), self._dbname],
                    env=self._env, cwd=self._outdir)

        # remember the init duration
        self._results['results']['init'] = r[2]

    @staticmethod
    def _parse_results(data):
        'extract results (including parameters) from the pgbench output'

        data = data.decode('utf-8')

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
        r = re.search('tps = ([0-9]+\.[0-9]+) \(excluding connections '
                      'establishing\)', data)
        if r:
            tps = r.group(1)

        return {'scale': scale,
                'mode': mode,
                'clients': clients,
                'threads': threads,
                'duration': duration,
                'latency': latency,
                'tps': tps}

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
            issues.append("duration (%s) needs to be an integer" %
                          self._duration)
        elif not self._duration >= 1:
            issues.append("duration (%s) needs to be >= 1" % (self._duration,))

        if type(self._runs) is not int:
            issues.append("runs (%s) needs to be an integer" % self._duration)
        elif not self._runs >= 1:
            issues.append("runs (%s) needs to be >= 1" % (self._runs,))

        return issues

    def _run(self, run, scale, duration, nclients=1, njobs=1, read_only=False,
             aggregate=True, csv_queue=None):
        'run pgbench on the database (either a warmup or actual benchmark run)'

        # Create a separate directory for each pgbench run
        if read_only:
            rtag = "ro"
        else:
            rtag = "rw"
        rdir = "%s/pgbench-%s-%d-%d-%s" % (self._outdir, rtag, scale, nclients,
                                           str(run))
        os.mkdir(rdir)

        args = ['pgbench', '-c', str(nclients), '-j', str(njobs), '-T',
                str(duration)]

        # aggregate on per second resolution
        if aggregate:
            args.extend(['-l', '--aggregate-interval', '1'])

        if read_only:
            args.extend(['-S'])

        args.extend([self._dbname])

        # do an explicit checkpoint before each run
        run_cmd(['psql', self._dbname, '-c', 'checkpoint'], env=self._env)

        log("pgbench: clients=%d, jobs=%d, aggregate=%s, read-only=%s, "
            "duration=%d" % (nclients, njobs, aggregate, read_only, duration))

        start = time.time()
        r = run_cmd(args, env=self._env, cwd=rdir)
        end = time.time()

        r = PgBench._parse_results(r[1])
        r.update({'read-only': read_only})

        r.update({'start': start, 'end': end})

        if csv_queue is not None:
            csv_queue.put([start, end, r['scale'], nclients, njobs, mode,
                           duration, latency, tps])

        return r

    def run_tests(self, csv_queue):
        """
        execute the whole benchmark, including initialization, warmup and
        benchmark runs
        """

        # derive configuration for the CPU count / RAM size
        configs = PgBench._configure(cpu_count(), available_ram())

        results = {'ro': {}, 'rw': {}}
        j = 0
        for config in configs:
            scale = config['scale']

            if scale not in results['ro']:
                results['ro'][scale] = {}
            if scale not in results['rw']:
                results['rw'][scale] = {}

            # init for the dataset scale and warmup
            self._init(scale)

            warmup = self._run('w%d' % j, scale, self._duration, cpu_count(),
                               cpu_count())
            j += 1

            # read-only & read-write
            for ro in [True, False]:
                if ro:
                    tag = 'ro'
                else:
                    tag = 'rw'

                for i in range(self._runs):
                    log("pgbench: %s run=%d" % (tag, i))

                    for clients in config['clients']:
                        if clients not in results[tag][scale]:
                            results[tag][scale][clients] = {}
                            results[tag][scale][clients]['results'] = []

                        r = self._run(i, scale, self._duration, clients,
                                      clients, ro, True, csv_queue)
                        r.update({'run': i})
                        results[tag][scale][clients]['results'].append(r)

                        tps = []
                        for result in results[tag][scale][clients]['results']:
                            tps.append(float(result['tps']))
                        results[tag][scale][clients]['metric'] = mean(tps)
                        results[tag][scale][clients]['median'] = median(tps)
                        results[tag][scale][clients]['std'] = std(tps)

        self._results['pgbench'] = results
        return self._results
