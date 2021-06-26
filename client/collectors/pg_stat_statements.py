import psycopg2
import psycopg2.extras

import folders
from utils.logging import log


class PgStatStatementsCollector(object):
    """
    collects pg_stat_statements query results
    """

    def __init__(self, dbname):
        self._dbname = dbname
        self.r = None

    def start(self):
        log("collecting pg_stat_statements")

        conn = psycopg2.connect('host=%s dbname=%s' % (folders.SOCKET_PATH, self._dbname))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute(
            'CREATE EXTENSION pg_stat_statements;'
            'SELECT * FROM pg_stat_statements;'
        )

        self.r = cur.fetchall()

        conn.close()

    def stop(self):
        pass

    def result(self):
        return self.r
