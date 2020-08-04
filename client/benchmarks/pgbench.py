import math
import os
import os.path
import re
import time
import psutil

from multiprocessing import cpu_count
from utils.logging import log
from utils.misc import available_ram, run_cmd

from settings import *
from settings_local import *
import folders

class PgBench(object):
    'a simple wrapper around pgbench, running TPC-B-like workload by default'

    # TODO allow running custom scripts, not just the default
    #      read-write/read-only tests
    # TODO allow running 'prepared' mode

    def __init__(self, bin_path, dbname, scale, clients, iterations, duration, read_only, results_dir=None):
        '''
        bin_path   - path to PostgreSQL binaries (dropdb, createdb, psql
                     commands)
        dbname     - name of the database to use
        duration   - duration of each execution
        iterations       - number of iterations (for each client count)
        out_dir    - output directory
        '''

        self._bin = bin_path
        self._dbname = dbname
        self._duration = duration
        self._outdir = results_dir
        self._iterations = iterations
        self._scale = scale
        self._clients = clients
        self._read_only = read_only

        self._env = os.environ
        self._env['PATH'] = ':'.join([bin_path, self._env['PATH']])


    def _init(self, scale):
        """
        recreate the database (drop + create) and populate it with given scale
        """

        # initialize results for this dataset scale
        
        log("recreating '%s' database" % (self._dbname,))
        run_cmd(['dropdb', '-h', folders.SOCKET_PATH, '--if-exists', self._dbname], env=self._env)
        run_cmd(['createdb', '-h', folders.SOCKET_PATH, self._dbname], env=self._env)

        log("initializing pgbench '%s' with scale %s" % (self._dbname, scale))

        r = run_cmd(['pgbench', '-i', '-s', str(scale), '-h', folders.SOCKET_PATH, '-p', '5432', self._dbname], env=self._env, cwd=self._outdir)

        with open(folders.LOG_PATH + '/pgbench_log.txt', 'w+') as file:
            file.write("pgbench log: \n")
            file.write(r[1].decode("utf-8"))

        # remember the init duration
        self._pgbench_init = r[2]
        

    @staticmethod
    def _parse_results(data):
        'extract results (including parameters) from the pgbench output'

        data = data.decode('utf-8')

        with open(folders.LOG_PATH + '/pgbench_log.txt', 'a+') as file:
            file.write(data)

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
        r = re.search('latency average = ([0-9\.]+) ms', data)
        if r:
            latency = r.group(1)

        tps = -1
        r = re.search('tps = ([0-9]+\.[0-9]+) \(excluding connections '
                      'establishing\)', data)
        if r:
            tps = r.group(1)

        statement_latencies = -1
        r = re.search('statement latencies in milliseconds:([\s\S]+)', data)

        if r:
            statement_latencies = r.group(1)

        return {'mode': mode,
                'clients': clients,
                'threads': threads,
                'latency': latency,
                'statement_latencies' : statement_latencies,
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
            issues.append("duration (%s) needs to be an integer" % self._duration)
        elif not self._duration >= 1:
            issues.append("duration (%s) needs to be >= 1" % (self._duration,))

        if type(self._iterations) is not int:
            issues.append("iterations (%s) needs to be an integer" % self._duration)
        elif not self._iterations >= 1:
            issues.append("iterations (%s) needs to be >= 1" % (self._iterations,))

        if type(self._clients) is not list:
            issues.append("clients (%s) needs to be an array" % self._clients)
        else:
            for client in self._clients:
                if not client >= 1:
                    issues.append("client (%s) needs to be >= 1" % (client))

        return issues

    def _run(self, run, scale, duration, pgbench_init, read_only, nclients=1, njobs=1, aggregate=True):
        'run pgbench on the database (either a warmup or actual benchmark run)'

        # add -r here
        args = ['pgbench', '-r', '-h', folders.SOCKET_PATH, '-c', str(nclients), '-j', str(njobs), '-T',
                str(duration)]

        if read_only:
            rtag = "ro"
        else:
            rtag = "rw"

        prefix = "pgbench-%s-%d-%d-%d-%s-" % (rtag, scale, duration, nclients, str(run))

        # aggregate on per second resolution
        if aggregate:
            args.extend(['-l', '--aggregate-interval', '1', '--log-prefix', prefix])

        if read_only:
            args.extend(['-S'])

        args.extend([self._dbname])

        # do an explicit checkpoint before each run
        run_cmd(['psql', '-h', folders.SOCKET_PATH, self._dbname, '-c', 'checkpoint'], env=self._env)

        log("pgbench: clients=%d, jobs=%d, aggregate=%s, read-only=%s, "
            "duration=%d" % (nclients, njobs, aggregate, read_only, duration))

        start = time.time()
        r = run_cmd(args, env=self._env, cwd=folders.LOG_PATH)
        end = time.time()

        r = PgBench._parse_results(r[1])
        r.update({'init': pgbench_init})
        r.update({'start': start, 'end': end})

        return r

    def run_tests(self):
        """
        execute the whole benchmark, including initialization, warmup and
        benchmark iterations
        """
        results = []
        result = {}
        tmp = {}

        j = 0
        info = {}

        info['clients'] = self._clients
        scale = self._scale

        # init for the dataset scale and warmup
        self._init(scale)

        if self._read_only:
            tag = "read-only"
        else:
            tag = "read-write"

        for i in range(0, self._iterations):
            log("pgbench: %s iteration=%d" % (tag, i))

            for clients in self._clients:
                if clients not in results:
                    result['clients'] = clients

                self._init(scale)
                r = self._run(i, scale, self._duration, self._pgbench_init, self._read_only, clients, clients, True)

                r.update({'iteration': i})
                results.append(r)

        info['scale'] = scale
        info['iterations'] = results
        info['duration'] = self._duration
        info['read_only'] = self._read_only

        return info
