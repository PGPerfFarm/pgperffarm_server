# file to declare folders
# to be imported globally in every script

import os

from settings import BASE_PATH
from settings_local import BASE_PATH

BUILD_PATH = os.path.join(BASE_PATH, 'build')
INSTALL_PATH = os.path.join(BASE_PATH, 'install')
BIN_PATH = os.path.join(INSTALL_PATH, 'bin')
OUTPUT_DIR = os.path.join(BASE_PATH, 'output')
REPOSITORY_PATH = os.path.join(BASE_PATH, 'postgres')
DATADIR_PATH = os.path.join(BASE_PATH, 'data')
SOCKET_PATH = os.path.join(BASE_PATH, 'socket')
LOG_PATH = os.path.join(BASE_PATH, 'log')