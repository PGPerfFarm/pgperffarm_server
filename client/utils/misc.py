import os
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
