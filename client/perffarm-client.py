#!/usr/bin/env python2.7

import argparse
import json
import os

from benchmarks.pgbench import PgBench
from benchmarks.runner import BenchmarkRunner

from collectors.linux import LinuxCollector
from collectors.postgres import PostgresCollector
from collectors.collector import MultiCollector

from utils.locking import FileLock
from utils.git import GitRepository
from utils.cluster import PgCluster
from utils import logging

from settings import *

if __name__ == '__main__':

    with FileLock('.lock') as lock:

        # clone repository and build the sources

        repository = GitRepository(url=GIT_URL, path=REPOSITORY_PATH)

        repository.clone_or_update()
        repository.build_and_install(path=BUILD_PATH)

        # build and start a postgres cluster

        cluster = PgCluster(bin_path=BIN_PATH, data_path=DATADIR_PATH)

        # create collectors

        collectors = MultiCollector()

        collectors.register('system', LinuxCollector())
        collectors.register('postgres',
                            PostgresCollector(dbname=DATABASE_NAME))

        runner = BenchmarkRunner(OUTPUT_DIR, cluster, collectors)

        # register the three tests we currently have

        runner.register_benchmark('pgbench', PgBench)

        # register one config for each benchmark (should be moved to a config
        # file)

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
