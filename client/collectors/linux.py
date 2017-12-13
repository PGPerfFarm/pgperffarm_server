import os.path

from datetime import datetime, timedelta, time
from utils.logging import log
from utils.misc import run_cmd


class LinuxCollector(object):
    'Collect various Linux-specific statistics (cpuinfo, mounts)'

    def __init__(self, outdir):
        self._outdir = outdir

        # Hard code all possible places a packager might install sysctl.
        self._env = os.environ
        self._env['PATH'] = ':'.join(['/usr/sbin/', '/sbin/', self._env['PATH']])

    def start(self):
        pass

    def stop(self):
        pass

    def result(self):
        'build the results'

        r = {'sysctl': self._collect_sysctl()}

        r.update(self._collect_system_info())

        return r

    def _collect_sysctl(self):
        'collect kernel configuration'

        log("collecting sysctl")
        r = run_cmd(['sysctl', '-a'], env=self._env)

        return r[1]

    def _collect_system_info(self):
        'collect cpuinfo, meminfo, mounts'

        system = {}

        with open('/proc/cpuinfo', 'r') as f:
            system['cpuinfo'] = f.read()

        with open('/proc/meminfo', 'r') as f:
            system['meminfo'] = f.read()

        with open('/proc/mounts', 'r') as f:
            system['mounts'] = f.read()

        return system
