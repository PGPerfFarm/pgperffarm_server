import os
import shutil
import time

from multiprocessing import cpu_count, Process, Queue
from subprocess import call, STDOUT
from tempfile import TemporaryFile
from utils.logging import log

from folders import *

class PgCluster(object):
    'basic manipulation of postgres cluster (init, start, stop, destroy)'

    def __init__(self, outdir, bin_path, data_path):
        self._outdir = outdir
        self._bin = bin_path
        self._data = data_path

        self._env = os.environ
        self._env['PATH'] = ':'.join([bin_path, self._env['PATH']])
        
        #self._env['USER'] = "postgres"
        #self._env['USERNAME'] = "postgres"
        #self._env['LOGNAME'] = "postgres"
        
        #self._env['PGUSER'] = "postgres"
        
        self._env['PGDATABASE'] = "postgres"

        #print(self._env)

        self._options = ""

    def _initdb(self):
        'initialize the data directory'

        with TemporaryFile() as strout:
            log("initializing cluster into '%s'" % (self._data,))
            r = call(['pg_ctl', '-D', self._data, 'init'], env=self._env,
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
            log("killing postgres processes")
            try: 
                pidfile = open(''.join([self._outdir, '/postmaster.pid']), 'r')
                pid = pidfile.readline().strip()
                run_cmd(['kill', '-9', pid])
                log("found postmaster.pid")
            except FileNotFoundError:
                log("postmaster.pid not found")
        
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

            cmd = ['pg_ctl', '-D', self._data, '-l',
                   ''.join([self._outdir, '/pg.log']), '-w']
            if len(self._options) > 0:
                cmd.extend(['-o', self._options])
            cmd.append('start')
            call(cmd, env=self._env, stdout=strout, stderr=STDOUT)

    def stop(self, destroy=True):
        'stop the cluster'

        with TemporaryFile() as strout:
            log("stopping cluster in '%s' using '%s' binaries" %
                (self._data, self._bin))
            call(['pg_ctl', '-D', self._data, '-w', '-t', '60', 'stop'],
                 env=self._env, stdout=strout, stderr=STDOUT)

        # kill any remaining processes, remove the data dir
        if destroy:
            self._destroy()
