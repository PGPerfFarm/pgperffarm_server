import csv
import multiprocessing
import os
import psycopg2
import psycopg2.extras
import time

from multiprocessing import Process, Queue
from utils.logging import log
from utils.misc import run_cmd

from folders import *

class PostgresCollector(object):
    """
    collects basic PostgreSQL-level statistics (bgwriter, databases, tables,
    indexes)
    """

    def __init__(self, outdir, dbname, bin_path):
        self._outdir = outdir
        self._dbname = dbname
        self._bin_path = bin_path

        self._env = os.environ
        self._env['PATH'] = ':'.join([bin_path, self._env['PATH']])
 
        self._env['PGDATABASE'] = "postgres"

    def start(self):
        log("saving postgres settings")
        try:

            conn = psycopg2.connect('host=%s dbname=%s' % (SOCKET_PATH, self._dbname))
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(
                'SELECT name, setting, source '
                'FROM pg_settings ORDER BY lower(name)'
            )

            fields = [desc[0] for desc in cur.description]

            with open(LOG_PATH + '/postgres_settings.csv', 'w+') as file:

                r = csv.DictWriter(file, fields)
                r.writeheader()
                r.writerows(cur.fetchall())

            conn.close()

        except Exception as ex:
            with open(LOG_PATH + '/pg_settings_log.txt', 'a+') as file:
                    file.write(e.stderr)
                    log("Error while extracting Postgres configuration, check logs.")

    def stop(self):
        pass

    def result(self):
        return {}


def run_collector(in_queue, out_queue, dbname, bin_path, outdir, interval=1.0):
    pass
