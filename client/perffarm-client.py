#!/usr/bin/env python2.7

import argparse
import json
import os

from benchmarks.pgbench import PgBench
from benchmarks.runner import BenchmarkRunner

from collectors.collectd import CollectdCollector
from collectors.linux import LinuxCollector
from collectors.postgres import PostgresCollector
from collectors.collector import MultiCollector

from utils.locking import FileLock
from utils.git import GitRepository
from utils.cluster import PgCluster
from utils import logging

from settings import *

if __name__ == '__main__':

    if os.path.exists(OUTPUT_DIR):
        print "output directory '%s' already exists" % OUTPUT_DIR
        sys.exit(1)

    with FileLock('.lock') as lock:

        # clone repository and build the sources

        repository = GitRepository(url=GIT_URL, path=REPOSITORY_PATH)

        repository.clone_or_update()
        repository.build_and_install(path=BUILD_PATH)

        # build and start a postgres cluster

        cluster = PgCluster(OUTPUT_DIR, bin_path=BIN_PATH,
                            data_path=DATADIR_PATH)

        # create collectors

        collectors = MultiCollector()

        system = os.popen("uname").readlines()[0].split()[0]
        if system == 'Linux':
            collectors.register('linux', LinuxCollector(OUTPUT_DIR))

        collectors.register('collectd',
                            CollectdCollector(OUTPUT_DIR, DATABASE_NAME, ''))

        pg_collector = PostgresCollector(OUTPUT_DIR, dbname=DATABASE_NAME,
                                         bin_path=('%s/bin' % (BUILD_PATH)))
        collectors.register('postgres', pg_collector)

        runner = BenchmarkRunner(OUTPUT_DIR, cluster, collectors)

        # register the three tests we currently have

        runner.register_benchmark('pgbench', PgBench)

        # register one config for each benchmark (should be moved to a config
        # file)

        PGBENCH_CONFIG['results_dir'] = OUTPUT_DIR
        runner.register_config('pgbench-basic',
                               'pgbench',
                               dbname=DATABASE_NAME,
                               bin_path=('%s/bin' % (BUILD_PATH,)),
                               postgres_config=POSTGRES_CONFIG,
                               **PGBENCH_CONFIG)

        # check configuration and report all issues
        issues = runner.check()

        if issues:
            # print the issues
            for k in issues:
                for v in issues[k]:
                    print k, ':', v
        else:
            runner.run()
