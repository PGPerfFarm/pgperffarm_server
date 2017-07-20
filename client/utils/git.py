import os
import shutil

from multiprocessing import cpu_count
from subprocess import call, STDOUT
from tempfile import TemporaryFile
from utils.logging import log


class GitRepository(object):
    'a simple management of a git repository / source building'

    def __init__(self, url, path):
        'url - repository URL, path - local directory for the clone'

        self._url = url
        self._path = path

    def _exists(self):
        'check that a local repository clone exists'

        # TODO verify that the repository uses the proper upstream url
        return os.path.exists(self._path)

    def _clone(self):
        ''
        log("cloning repository '%s' to '%s'" % (self._url, self._path))

        with TemporaryFile() as strout:
            call(['git', 'clone', self._url, self._path], stdout=strout,
                 stderr=STDOUT)

    def _update(self):
        'update an existing repository clone'

        log("updating repository '%s' from '%s'" % (self._path, self._url))

        # simply call git-pull and redirect stdout/stderr
        # FIXME should verify that the repository uses the proper upstream url
        with TemporaryFile() as strout:
            call(['git', 'pull'], cwd=self._path, stdout=strout, stderr=STDOUT)

    def current_commit(self):
        'returns current commit hash'

        with TemporaryFile() as strout:
            call(['git', 'rev-parse', 'HEAD'], cwd=self._path, stdout=strout,
                 stderr=STDOUT)
            strout.seek(0)
            return strout.read().strip()

    def clone_or_update(self):
        'refreshes the repository (either clone from scratch or refresh)'

        if self._exists():
            self._update()
        else:
            self._clone()

        log("current commit '%s'" % (self.current_commit(),))

    def build_and_install(self, path, remove=True):
        'builds and installs the sources'

        # TODO collect output of configure and make commands
        if os.path.exists(path):
            shutil.rmtree(path)

        with TemporaryFile() as strout:
            log("configuring sources in '%s' with prefix '%s'" %
                (self._path, path))
            call(['./configure', '--prefix', path], cwd=self._path,
                 stdout=strout, stderr=STDOUT)

        with TemporaryFile() as strout:
            log("building sources and installing into '%s'" % (path,))

            # cleanup and build using multiple cpus
            call(['make', '-s', 'clean'], cwd=self._path, stdout=strout,
                 stderr=STDOUT)
            call(['make', '-s', '-j', str(cpu_count()), 'install'],
                 cwd=self._path, stdout=strout, stderr=STDOUT)
