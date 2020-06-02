import os
import shutil
import subprocess
import sys

from multiprocessing import cpu_count
from tempfile import TemporaryFile
from utils.logging import log

def build(git_path, build_path, install_path, log_path):

    log("Building repository...")

    with TemporaryFile() as strout:

        log("Configuring sources in '%s' with prefix '%s'" % (git_path, build_path))
        a = subprocess.run([git_path + '/configure', '--prefix', install_path], cwd=build_path,
                 capture_output=True, text=True)

    with TemporaryFile() as strout:
        log("Building sources and installing into '%s'" % (install_path,))

        # cleanup and build using multiple cpus
        b = subprocess.run(['make', '-s', 'clean'], cwd=build_path, capture_output=True, text=True)

        c = subprocess.run(['make', '-s', '-j', str(cpu_count()), 'install'],
                cwd=build_path, capture_output=True, text=True)
            
    if (a.stderr != '' or b.stderr != '' or c.stderr != ''):
        with open(log_path + '/log.txt', 'w+') as file:

            file.write("configure error: \n")
            file.write(b.stderr)

            file.write("\nmake clean error: \n")
            file.write(b.stderr)

            file.write("\nmake install error: \n")
            file.write(c.stderr)

            log("Errors have been found while installing, please check log.txt in '%s'" % (log_path,))

            sys.exit()



