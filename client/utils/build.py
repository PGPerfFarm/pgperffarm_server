import os
import shutil
import subprocess
import sys

from datetime import datetime
from multiprocessing import cpu_count
from tempfile import TemporaryFile
from utils.logging import log

import folders

def build():

    log("Building repository...")

    with TemporaryFile() as strout:

        log("Configuring sources in '%s' with prefix '%s'" % (folders.REPOSITORY_PATH, folders.BUILD_PATH))

        configure_start_time = datetime.now()
        a = subprocess.run([folders.REPOSITORY_PATH + '/configure', '--prefix', folders.INSTALL_PATH], cwd=folders.BUILD_PATH,
                 capture_output=True, text=True)
        configure_end_time = datetime.now()
        configure_runtime = configure_end_time - configure_start_time

    with TemporaryFile() as strout:
        log("Building sources and installing into '%s'" % (folders.INSTALL_PATH,))

        # cleanup and build using multiple cpus
        build_start_time = datetime.now()
        b = subprocess.run(['make', '-s', 'clean'], cwd=folders.BUILD_PATH, capture_output=True, text=True)
        build_end_time = datetime.now()
        build_runtime = build_end_time - build_start_time

        install_start_time = datetime.now()
        c = subprocess.run(['make', '-s', '-j', str(cpu_count()), 'install'],
                cwd=folders.BUILD_PATH, capture_output=True, text=True)
        install_end_time = datetime.now()
        install_runtime = install_end_time - install_start_time
            
    with open(folders.LOG_PATH + '/configure_log.txt', 'w+') as file:
        file.write(a.stderr)

    with open(folders.LOG_PATH + '/build_log.txt', 'w+') as file:
        file.write(b.stderr)

    with open(folders.LOG_PATH + '/install_log.txt', 'w+') as file:
        file.write(c.stderr)

    if (a.stderr != '' or b.stderr != '' or c.stderr != ''):
        log("Anomalies have been found while installing, please check logs in '%s'" % (folders.LOG_PATH,))

    return str(configure_runtime), str(build_runtime), str(install_runtime)





