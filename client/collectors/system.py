import os.path
import platform
import psutil
from cpuinfo import get_cpu_info_json, get_cpu_info

from datetime import datetime, timedelta, time
from utils.logging import log
from utils.misc import run_cmd

class SystemCollector(object):
    'Collect various Linux-specific statistics (cpuinfo, mounts)'

    def __init__(self, outdir):
        self._outdir = outdir

        # hard code all possible places a packager might install sysctl.
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

        return "tbd"


    def _collect_system_info(self):
        'collect cpuinfo, meminfo, mounts'

        log("Collecting system info")

        system = {}
        system['cpu'] = {}
        system['os'] = {}
        system['memory'] = {}
        system['disk'] = {}
        system['process'] = {}
        system['compiler'] = {}

        system['compiler']['make'] = run_cmd(['make', '--version'], env=self._env)
        system['compiler']['gcc'] = run_cmd(['gcc', '--version'], env=self._env)

        system['cpu']['information'] = get_cpu_info()
        system['cpu']['number'] = psutil.cpu_count()
        system['cpu']['times'] = psutil.cpu_times(percpu=False)
        system['cpu']['percent'] = psutil.cpu_times_percent(percpu=False)
        system['cpu']['stats'] = psutil.cpu_stats()
        system['cpu']['load_avg'] = psutil.getloadavg()

        system['os']['architecture'] = platform.architecture()
        system['os']['processor'] = platform.processor()
        system['os']['release'] = platform.release()
        system['os']['version'] = platform.version()
        system['os']['libc'] = platform.libc_ver()

        system['memory']['virtual'] = psutil.virtual_memory()
        system['memory']['swap'] = psutil.swap_memory()
        system['memory']['mounts'] = psutil.disk_partitions()

        system['disk']['usage'] = psutil.disk_usage('/')
        system['disk']['io'] = psutil.disk_io_counters(perdisk=False, nowrap=True)

        process = psutil.Process()
        system['process']['io'] = process.io_counters()
        system['process']['context_switches'] = process.num_ctx_switches()
        system['process']['cpu_times'] = process.cpu_times()
        system['process']['threads'] = process.num_threads()
        system['process']['cpu_percent'] = process.cpu_percent()
        system['process']['memory'] = process.memory_info()
        system['process']['memory_percent'] = process.memory_percent()


        # files to be uploaded and saved somewhere
        '''
        with open('/proc/cpuinfo', 'r') as f:
            system['cpuinfo'] = f.read()

        with open('/proc/meminfo', 'r') as f:
            system['meminfo'] = f.read()

        with open('/proc/mounts', 'r') as f:
            system['mounts'] = f.read()
        '''

        return system
