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

GIT_URL = 'git@github.com:postgres/postgres.git'
REPOSITORY_PATH = '/home/user/tmp/git-postgres'
BUILD_PATH = '/home/user/tmp/bin-postgres'
BIN_PATH = os.path.join(BUILD_PATH, 'bin')
DATADIR_PATH = '/home/user/tmp/data-postgres'

POSTGRES_CONFIG = {'shared_buffers' : '1GB',
				   'work_mem' : '64MB',
				   'maintenance_work_mem' : '128MB',
				   'min_wal_size' : '2GB',
				   'max_wal_size' : '4GB',
				   'log_line_prefix' : '%n %t ',
				   'log_checkpoints' : 'on',
				   'log_autovacuum_min_duration' : '0',
				   'log_temp_files' : '32',
				   'checkpoint_timeout' : '15min',
				   'checkpoint_completion_target' : '0.9'}

DATABASE_NAME = 'perf'

OUTPUT_DIR = '/home/user/perf-output'


if __name__ == '__main__':

	with FileLock('.lock') as lock:

		# clone repository and build the sources

		repository = GitRepository(url = GIT_URL, path = REPOSITORY_PATH)

		repository.clone_or_update()
		repository.build_and_install(path = BUILD_PATH)

		# build and start a postgres cluster

		cluster = PgCluster(bin_path = BIN_PATH, data_path = DATADIR_PATH)

		# create collectors

		collectors = MultiCollector()

		collectors.register('system', LinuxCollector())
		collectors.register('postgres', PostgresCollector(dbname=DATABASE_NAME))

		runner = BenchmarkRunner(OUTPUT_DIR, cluster, collectors)

		# register the three tests we currently have

		runner.register_benchmark('pgbench', PgBench)

		# register one config for each benchmark (should be moved to a config file)

		runner.register_config('pgbench-basic', 'pgbench', dbname = DATABASE_NAME,
								bin_path = ('%s/bin' % (BUILD_PATH,)),
								postgres_config = POSTGRES_CONFIG)

		runner.run()
