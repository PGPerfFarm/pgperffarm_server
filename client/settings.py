import os
import sys

# global configuration
REUSE_REPO = True
UPDATE = True
REMOVE_AFTERWARDS = True

# default url: master branch
GIT_URL = 'https://github.com/postgres/postgres.git'
GIT_PATH = '/tmp' 
BUILD_PATH = '/tmp/build'
INSTALL_PATH = '/tmp/install'
BIN_PATH = os.path.join(INSTALL_PATH, 'bin')
LOG_PATH = '/tmp' # choose an existing directory

# be careful with changing this, might compromise existing external Postgres processes
# furthermore, make sure that a non-superuser can access this folder
DATADIR_PATH = '/tmp/data-postgres'

API_URL = 'http://140.211.168.111:8080/'
MACHINE_SECRET = 'CHANGEME'
# test secret

POSTGRES_CONFIG = {
    'shared_buffers': '1GB',
    'work_mem': '64MB',
    'maintenance_work_mem': '128MB',
    'min_wal_size': '2GB',
    'max_wal_size': '4GB',
    'log_line_prefix': '%t [%p]: [%l-1] db=%d,user=%u,app=%a,client=%h ',
    'log_checkpoints': 'on',
    'log_autovacuum_min_duration': '0',
    'log_temp_files': '32',
    'checkpoint_timeout': '30min',
    'checkpoint_completion_target': '0.9',
}

DATABASE_NAME = 'perf'

OUTPUT_DIR = '/tmp/perf-output'

# configuration for PgBench
# runs - number of repetitions (including test for all client counts)
# duration - duration (in seconds) of a single benchmark (per client count)
PGBENCH_CONFIG = {
    'runs': 3,
    'duration': 600,
    'csv': False
}

# ignore missing file with local config
try:
    from settings_local import *
except Exception as e:
    print (sys.stderr, "ERROR: local configuration (settings_local.py) " \
                         "not found")
    sys.exit(1)
