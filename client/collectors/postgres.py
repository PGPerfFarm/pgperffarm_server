import csv
import multiprocessing
import os
import psycopg2
import psycopg2.extras
import time

from multiprocessing import Process, Queue
from utils.logging import log
from utils.misc import run_cmd


class PostgresCollector(object):
    """
    collects basic PostgreSQL-level statistics (bgwriter, databases, tables,
    indexes)
    """

    def __init__(self, outdir, dbname, bin_path):
        self._outdir = outdir
        self._dbname = dbname
        self._bin_path = bin_path

    def start(self):
        log("saving postgres settings")
        try:
            conn = psycopg2.connect('host=localhost dbname=%s' % self._dbname)
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(
                'SELECT name, setting, source '
                'FROM pg_settings ORDER BY lower(name)'
            )
            fields = [desc[0] for desc in cur.description]
            filename = ''.join([self._outdir, '/settings.csv'])
            settings_log = csv.DictWriter(open(filename, 'w'), fields,
                                          lineterminator='\n')
            settings_log.writeheader()
            settings_log.writerows(cur.fetchall())
            settings_log.close()
            conn.close()
        except Exception as ex:
            pass

    def stop(self):
        pass

    def result(self):
        return {}


def run_collector(in_queue, out_queue, dbname, bin_path, outdir, interval=1.0):
    pass
