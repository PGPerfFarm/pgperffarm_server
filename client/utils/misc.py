import os
import psycopg2
import psycopg2.extras
import time

from subprocess import call, STDOUT
from tempfile import TemporaryFile


def available_ram():
	'determine amount of RAM in the system (in megabytes)'

	return int(os.popen("free -m").readlines()[1].split()[1])


def run_cmd(args, env=None, cwd=None):
	'run command (a subprocess.call wrapper)'

	with TemporaryFile() as strout:

		start = time.time()
		retcode = call(args, env=env, cwd=cwd, stdout=strout, stderr=STDOUT)

		strout.seek(0)
		return (retcode, strout.read(), (time.time() - start))


def connect(dbname, conn, cursor, nretries = 60, delay = 1.0):
	'''Try opening a connection and a cursor. If it does not succeed (e.g.
	when the database is performing recovery after a crash, retry multiple
	times (as specified by nretries and delay in seconds).
	'''

	# if we already have connection and a cursor, return it
	if conn and cursor:
		return (conn, cursor)

	# we'll try repeatedly, with delays between the attempts
	i = 0
	while i < nretries:

		i += 1

		try:
			conn = psycopg2.connect('host=localhost dbname=%s' % (dbname,))
			# TODO do we actually need autocommit?
			conn.autocommit = True
			cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

			return (conn, cursor)
		except:
			# connection failure - sleep for a while, then try again
			time.sleep(delay)

	return (None, None)


def disconnect(conn, cursor):
	'''Make sure we're disconnected (but prevent exceptions)'''

	try:
		cursor.close()
	except:
		pass

	try:
		conn.close()
	except:
		pass
