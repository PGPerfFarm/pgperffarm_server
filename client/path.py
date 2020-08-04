import os
import folders

def create_path(BRANCH_PATH):

	folders.BUILD_PATH = os.path.join(BRANCH_PATH, 'build')
	folders.INSTALL_PATH = os.path.join(BRANCH_PATH, 'install')
	folders.BIN_PATH = os.path.join(folders.INSTALL_PATH, 'bin')
	folders.OUTPUT_PATH = os.path.join(BRANCH_PATH, 'output')
	folders.REPOSITORY_PATH = os.path.join(BRANCH_PATH, 'postgresql')
	folders.DATADIR_PATH = os.path.join(BRANCH_PATH, 'data')
	folders.SOCKET_PATH = os.path.join(BRANCH_PATH, 'socket')
	folders.LOG_PATH = os.path.join(BRANCH_PATH, 'log')