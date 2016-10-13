import os
import sys

# global configuration
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

OUTPUT_DIR = '/home/user/tmp/perf-output'

# configuration for PgBench
#
# runs     - number of repetitions (including test for all client counts)
# duration - duration (in seconds) of a single benchmark (per client count)
#
PGBENCH_CONFIG = {
	'runs' : 3,
	'duration' : 60,	# duration of per-client-count benchmark
	'csv' : False
}

# ignore missing file with local config
try:
	from settings_local import *
except:
	print >> sys.stderr, "ERROR: local configuration (settings_local.py) not found"
	sys.exit(1)
