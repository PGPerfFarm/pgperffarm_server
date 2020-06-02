#!/usr/bin/env python3

import argparse
import json
import os
import git
import pathlib
import shutil

from benchmarks.pgbench import PgBench
from benchmarks.runner import BenchmarkRunner

from collectors.collectd import CollectdCollector
from collectors.linux import LinuxCollector
from collectors.postgres import PostgresCollector
from collectors.collector import MultiCollector

from utils.locking import FileLock
from utils.build import build
from utils.cluster import PgCluster
from utils.logging import log

from settings_local import *

if __name__ == '__main__':

    with FileLock('.lock') as lock:

        log("Starting client...")

        REPOSITORY_PATH = os.path.join(GIT_PATH, 'postgres')

        # checking for local installation
        if (os.path.exists(REPOSITORY_PATH)):

            if (not REUSE_REPO):
                shutil.rmtree(REPOSITORY_PATH)

                if (os.path.exists(BUILD_PATH)):
                    shutil.rmtree(BUILD_PATH)
                os.mkdir(BUILD_PATH)

                if (os.path.exists(INSTALL_PATH)):
                    shutil.rmtree(INSTALL_PATH)
                os.mkdir(INSTALL_PATH)

                # clone and build
                log("Removing existing repository and reinitializing...")
                git.Git(GIT_PATH).clone(GIT_URL)
                build(REPOSITORY_PATH, BUILD_PATH, INSTALL_PATH)

            else:
                branch = (git.Repo(REPOSITORY_PATH)).active_branch
                commit = (git.Repo(REPOSITORY_PATH)).head.commit

                if (UPDATE):
                    # call git pull
                    log("Updating repository...")
                    git.Git().pull()

                    latest_branch = (git.Repo(REPOSITORY_PATH)).active_branch
                    latest_commit = (git.Repo(REPOSITORY_PATH)).head.commit

                    if (latest_commit != commit or latest_branch != branch):
                        log("Rebuilding repository to apply updates...")

                        if (os.path.exists(BUILD_PATH)):
                            shutil.rmtree(BUILD_PATH)
                        os.mkdir(BUILD_PATH)

                        if (os.path.exists(INSTALL_PATH)):
                            shutil.rmtree(INSTALL_PATH)
                        os.mkdir(INSTALL_PATH)

                        build(REPOSITORY_PATH, BUILD_PATH, INSTALL_PATH)

                    log("Repository is up to date. ")

                else:
                    if (not (os.path.exists(BUILD_PATH))):
                        # build
                        build(REPOSITORY_PATH, BUILD_PATH, INSTALL_PATH)

                    # if it exists, proceed to run tests

        else:
            # remove build and install path just to be sure
            if (os.path.exists(BUILD_PATH)):
                shutil.rmtree(BUILD_PATH)
            os.mkdir(BUILD_PATH)

            if (os.path.exists(INSTALL_PATH)):
                shutil.rmtree(INSTALL_PATH)
            os.mkdir(INSTALL_PATH)

            # and finally, clone
            log("Cloning repository...")
            git.Git(GIT_PATH).clone(GIT_URL)
            # and build
            build(REPOSITORY_PATH, BUILD_PATH, INSTALL_PATH)

        # get (or rewrite) current branch and commit
        # string because it must be JSON serializable
        repository = git.Repo(REPOSITORY_PATH)
        branch = str(repository.active_branch)
        commit = str(repository.head.commit)

        # build and start a postgres cluster
        cluster = PgCluster(OUTPUT_DIR, bin_path=BIN_PATH, data_path=DATADIR_PATH)

        # create collectors
        collectors = MultiCollector()

        system = os.popen("uname").readlines()[0].split()[0]
        if system == 'Linux':
            collectors.register('linux', LinuxCollector(OUTPUT_DIR))

        # add mac?

        collectors.register('collectd',
                            CollectdCollector(OUTPUT_DIR, DATABASE_NAME, ''))

        pg_collector = PostgresCollector(OUTPUT_DIR, dbname=DATABASE_NAME,
                                         bin_path=('%s/bin' % (BUILD_PATH)))
        collectors.register('postgres', pg_collector)

        runner = BenchmarkRunner(OUTPUT_DIR, API_URL, MACHINE_SECRET, cluster, collectors)

        # register the three tests we currently have
        runner.register_benchmark('pgbench', PgBench)

        # register one config for each benchmark (should be moved to a config file)
        PGBENCH_CONFIG['results_dir'] = OUTPUT_DIR
        runner.register_config('pgbench-basic',
                               'pgbench',
                               branch,
                               commit,
                               dbname=DATABASE_NAME,
                               bin_path=BIN_PATH,
                               postgres_config=POSTGRES_CONFIG,
                               **PGBENCH_CONFIG)

        # check configuration and report all issues
        issues = runner.check()

        if issues:
            # print the issues
            for k in issues:
                for v in issues[k]:
                    print (k, ':', v)
        else:
            runner.run()

        # cleanup
        if (REMOVE_AFTERWARDS):
            shutil.rmtree(REPOSITORY_PATH)
            shutil.rmtree(BUILD_PATH)
            shutil.rmtree(INSTALL_PATH)
