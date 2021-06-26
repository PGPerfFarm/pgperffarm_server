import os
import csv
import shutil

import folders
from utils.logging import log
from utils.misc import run_cmd
from settings_local import *

COLLECTD_CONFIG = '/tmp/.collectd.conf'
COLLECTD_PIDFILE = '/tmp/.collectd.pid'


class CollectdCollector(object):
    """
    Collect basic system and database statistics using collectd.
    """

    def __init__(self, outdir, dbname):
        self._outdir = '%s/stats' % outdir

        # Hard code all possible places a packager might install collectd.
        self._env = os.environ
        self._env['PATH'] = ':'.join(['/usr/sbin/', '/sbin/', self._env['PATH']])

        # get partition being used by postgres
        r = run_cmd(['df', '.'], cwd=BASE_PATH)
        partition = r[1].decode('utf-8').split('\n')[1].split(' ')[0]
        disk = partition.replace('/dev/', '')

        # Assume collectd.conf.in file to be in the same directory as this
        # file.
        cwd = os.path.dirname(os.path.realpath(__file__))

        modules = (
            'LoadPlugin aggregation\n'
            'LoadPlugin contextswitch\n'
            'LoadPlugin cpu\n'
            'LoadPlugin csv\n'
            'LoadPlugin disk\n'
            'LoadPlugin memory\n'
            'LoadPlugin postgresql\n'
            'LoadPlugin processes\n'
            'LoadPlugin swap\n'
        )

        system = os.popen("uname").readlines()[0].split()[0]

        if system == 'Linux':
            modules += (
                'LoadPlugin ipc\n'
                'LoadPlugin vmem\n'
            )

        config_template = open('%s/collectd.conf.in' % cwd, 'r')
        config = open(COLLECTD_CONFIG, 'w')
        config.write(config_template.read() % {'database': dbname,
                                               'disk': disk,
                                               'datadir': self._outdir,
                                               'modules': modules,
                                               'pghost': folders.SOCKET_PATH,
                                               'pguser': self._env['USER']})
        config.close()
        config_template.close()

        # TODO: Use collectd to test config act exit appropriately.

    def start(self):
        log("starting collectd")
        cmd = 'collectd -C %s -P %s' % (COLLECTD_CONFIG, COLLECTD_PIDFILE)
        run_cmd(cmd.split(' '), env=self._env)

    def stop(self):
        log("stopping collectd")

        try:
            pidfile = open(COLLECTD_PIDFILE, 'r')
            pid = pidfile.read().strip()
            run_cmd(['kill', pid])
        except FileNotFoundError:
            log('collectd pid not found - processes may still be running')

        # remove outdir
        if os.path.exists(self._outdir):
            shutil.rmtree(self._outdir)

    def result(self):
        r = {}
        r.update(self._collect_collectd_csv())

        return r

    def _collect_collectd_csv(self):
        collectd = {}

        for name in os.listdir(self._outdir):
            collectd[name] = {}
            for plugin in os.listdir(''.join([self._outdir, '/', name])):
                collectd[name][plugin] = {}
                for file in os.listdir(''.join([self._outdir, '/', name, '/', plugin])):
                    csv_file = ''.join([self._outdir, '/', name, '/', plugin, '/', file])
                    with open(csv_file, 'r') as csv_file_open:
                        reader = csv.DictReader(csv_file_open)
                        rows = []
                        for row in reader:
                            rows.append(row)
                        collectd[name][plugin][file] = rows

        return collectd
