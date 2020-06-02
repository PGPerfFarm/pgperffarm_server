import os
import shutil
import subprocess

from multiprocessing import cpu_count
from tempfile import TemporaryFile
from utils.logging import log

def build(git_path, build_path, install_path):

    log("Building repository...")

    with TemporaryFile() as strout:
        log("Configuring sources in '%s' with prefix '%s'" %
            (git_path, build_path))
        subprocess.run([git_path + '/configure', '--prefix', install_path], cwd=build_path,
             capture_output=True)

    with TemporaryFile() as strout:
        log("Building sources and installing into '%s'" % (install_path,))

            # cleanup and build using multiple cpus
        subprocess.run(['make', '-s', 'clean'], cwd=build_path, capture_output=True)
        subprocess.run(['make', '-s', '-j', str(cpu_count()), 'install'],
            cwd=build_path, capture_output=True)

        # various things needs to be installed because of various changes
        # between releases.  Take a systematic approach and check
        # if the directory exist, then try to install it.

        '''
        print("Installing additional tools...")

        items = [
                'src/bin/initdb',
                'src/bin/pg_ctl',
                'src/bin/scripts',
                'src/bin/psql',
                'src/bin/pgbench'                     
                'contrib/pgbench',
            ]
        for item in items:
            srcdir = ''.join([git_path, '/', item])

            if os.path.isdir(srcdir):
                subprocess.run(['make', '-s', '-j', str(cpu_count()), 'install'],
                cwd=srcdir, capture_output=True)
        '''
