import os.path

from datetime import datetime, timedelta, time
from utils.logging import log
from utils.misc import run_cmd


class LinuxCollector(object):
    'collects various Linux-specific statistics (cpuinfo, mounts, sar)'

    def __init__(self, sar_path='/var/log/sa'):
        self._start_ts = None
        self._end_ts = None
        self._sar = sar_path

    def start(self):
        self._start_ts = datetime.now()

    def stop(self):
        self._end_ts = datetime.now()

    def result(self):
        'build the results'

        r = {'sysctl': self._collect_sysctl()}

        # ignore sar if we've not found it
        sar = self._collect_sar_stats()
        if sar:
            r['sar'] = sar

        r.update(self._collect_system_info())

        return r

    def _collect_sar_stats(self):
        'extracts all data available in sar, filters by timestamp range'

        sar = {}
        log("collecting sar stats")

        d = self._start_ts.date()
        while d <= self._end_ts.date():

            # FIXME maybe skip if the file does not exist
            filename = '%(path)s/sa%(day)s' % {'path': self._sar,
                                               'day': d.strftime('%d')}

            # if the sar file does not exist, skip it
            if os.path.isfile(filename):

                log("extracting sar data from '%s'" % (filename,))

                # need to use the right combination of start/end timestamps
                s = self._start_ts.strftime('%H:%M:%S')
                e = self._end_ts.strftime('%H:%M:%S')

                if d == self._start_ts.date() and d == self._end_ts.date():
                    r = run_cmd(['sar', '-A', '-p', '-s', s, '-e', e, '-f',
                                 filename])
                elif d == self._start_ts.date():
                    r = run_cmd(['sar', '-A', '-p', '-s', s, '-f', filename])
                elif d == self._end_ts.date():
                    r = run_cmd(['sar', '-A', '-p', '-e', e, '-f', filename])
                else:
                    r = run_cmd(['sar', '-A', '-p', '-f', filename])

                sar[str(d)] = r[1]

            else:

                log("file '%s' does not exist, skipping" % (filename,))

            # proceed to the next day
            d += timedelta(days=1)

        if not sar:
            return None

        return sar

    def _collect_sysctl(self):
        'collect kernel configuration'

        log("collecting sysctl")
        r = run_cmd(['/usr/sbin/sysctl', '-a'])

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
