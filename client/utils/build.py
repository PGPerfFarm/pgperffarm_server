import os
import shutil
import subprocess
import sys

from datetime import datetime
from multiprocessing import cpu_count
from tempfile import TemporaryFile
from utils.logging import log

def build(git_path, build_path, install_path, log_path):

    log("Building repository...")

    with TemporaryFile() as strout:

        log("Configuring sources in '%s' with prefix '%s'" % (git_path, build_path))

        configure_start_time = datetime.now()
        a = subprocess.run([git_path + '/configure', '--prefix', install_path], cwd=build_path,
                 capture_output=True, text=True)
        configure_end_time = datetime.now()
        configure_runtime = configure_end_time - configure_start_time

    with TemporaryFile() as strout:
        log("Building sources and installing into '%s'" % (install_path,))

        # cleanup and build using multiple cpus
        build_start_time = datetime.now()
        b = subprocess.run(['make', '-s', 'clean'], cwd=build_path, capture_output=True, text=True)
        build_end_time = datetime.now()
        build_runtime = build_end_time - build_start_time

        install_start_time = datetime.now()
        c = subprocess.run(['make', '-s', '-j', str(cpu_count()), 'install'],
                cwd=build_path, capture_output=True, text=True)
        install_end_time = datetime.now()
        install_runtime = install_end_time - install_start_time
            
    with open(log_path + '/build_log.txt', 'w+') as file:

        file.write("configure error: \n")
        file.write(a.stderr)

        file.write("\nmake clean error: \n")
        file.write(b.stderr)

        file.write("\nmake install error: \n")
        file.write(c.stderr)

        d = subprocess.run(['/tmp/perffarm/install/bin/psql'], capture_output=True, text=True)
        print("XXXXXXX")
        print(d)
        print(d.stderr)

        if (a.stderr != '' or b.stderr != '' or c.stderr != ''):
            log("Errors have been found while installing, please check build_log.txt in '%s'" % (log_path,))

            sys.exit()



