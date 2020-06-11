import os
import shutil
import subprocess
import sys

from datetime import datetime
from multiprocessing import cpu_count
from tempfile import TemporaryFile
from utils.logging import log

from folders import *

def build():

    log("Building repository...")

    with TemporaryFile() as strout:

        log("Configuring sources in '%s' with prefix '%s'" % (REPOSITORY_PATH, BUILD_PATH))

        configure_start_time = datetime.now()
        a = subprocess.run([REPOSITORY_PATH + '/configure', '--prefix', INSTALL_PATH], cwd=BUILD_PATH,
                 capture_output=True, text=True)
        configure_end_time = datetime.now()
        configure_runtime = configure_end_time - configure_start_time

    with TemporaryFile() as strout:
        log("Building sources and installing into '%s'" % (INSTALL_PATH,))

        # cleanup and build using multiple cpus
        build_start_time = datetime.now()
        b = subprocess.run(['make', '-s', 'clean'], cwd=BUILD_PATH, capture_output=True, text=True)
        build_end_time = datetime.now()
        build_runtime = build_end_time - build_start_time

        install_start_time = datetime.now()
        c = subprocess.run(['make', '-s', '-j', str(cpu_count()), 'install'],
                cwd=BUILD_PATH, capture_output=True, text=True)
        install_end_time = datetime.now()
        install_runtime = install_end_time - install_start_time
            
    with open(LOG_PATH + '/build_log.txt', 'w+') as file:

        file.write("configure error: \n")
        file.write(a.stderr)

        file.write("\nmake clean error: \n")
        file.write(b.stderr)

        file.write("\nmake install error: \n")
        file.write(c.stderr)

        if (a.stderr != '' or b.stderr != '' or c.stderr != ''):
            log("Errors have been found while installing, please check build_log.txt in '%s'" % (LOG_PATH,))

            sys.exit()

    return configure_runtime, build_runtime, install_runtime





