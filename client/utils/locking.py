import fcntl
import os


class FileLock():
    'a simple wrapper around file lock'

    def __init__(self, filename):
        self._file = open(filename, 'w')

    def __enter__(self):
        'locks the file and writes the PID of the current process into it'
        fcntl.flock(self._file, fcntl.LOCK_EX)
        self._file.write(str(os.getpid()))
        self._file.flush()

        return self._file

    def __exit__(self, type, value, traceback):
        'unlock the file'
        fcntl.flock(self._file, fcntl.LOCK_UN)
