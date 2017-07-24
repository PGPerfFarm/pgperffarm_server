import os
import shutil
import time

from multiprocessing import cpu_count, Process, Queue
from subprocess import call, STDOUT
from tempfile import TemporaryFile
from utils.logging import log


class PgCluster(object):
    'basic manipulation of postgres cluster (init, start, stop, destroy)'

    def __init__(self, bin_path, data_path):
        self._bin = bin_path
        self._data = data_path

        self._options = ""

    def _initdb(self):
        'initialize the data directory'

        with TemporaryFile() as strout:
            log("initializing cluster into '%s'" % (self._data,))
            call(['pg_ctl', '-D', self._data, 'init'], env={'PATH': self._bin},
                 stdout=strout, stderr=STDOUT)

    def _configure(self, config):
        'build options list to use with pg_ctl'

        for k in config:
            self._options += ''.join([" -c ", k, "='", str(config[k]), "'"])

    def _destroy(self):
        """
        forced cleanup of possibly existing cluster processes and data
        directory
        """

        with TemporaryFile() as strout:
            log("killing all existing postgres processes")
            call(['killall', 'postgres'], stdout=strout, stderr=STDOUT)

        # remove the data directory
        if os.path.exists(self._data):
            shutil.rmtree(self._data)

    def start(self, config, destroy=True):
        'init, configure and start the cluster'

        # cleanup any previous cluster running, remove data dir if it exists
        if destroy:
            self._destroy()

        self._initdb()
        self._configure(config)

        with TemporaryFile() as strout:
            log("starting cluster in '%s' using '%s' binaries" %
                (self._data, self._bin))
            cmd = ['pg_ctl', '-D', self._data, '-l', 'pg.log', '-w']
            if len(self._options) > 0:
                cmd.extend(['-o', self._options])
            cmd.append('start')
            call(cmd, env={'PATH': self._bin}, stdout=strout, stderr=STDOUT)

    def stop(self, destroy=True):
        'stop the cluster'

        with TemporaryFile() as strout:
            log("stopping cluster in '%s' using '%s' binaries" %
                (self._data, self._bin))
            call(['pg_ctl', '-D', self._data, '-w', '-t', '60', 'stop'],
                 env={'PATH': self._bin}, stdout=strout, stderr=STDOUT)

        # kill any remaining processes, remove the data dir
        if destroy:
            self._destroy()
