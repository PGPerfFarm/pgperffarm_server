#!/usr/bin/env python3

import argparse
import json
import os
import git
import pathlib
import shutil
import psutil
import logging
from datetime import datetime

from benchmarks.pgbench import PgBench
from benchmarks.runner import BenchmarkRunner

from collectors.collectd import CollectdCollector
from collectors.system import SystemCollector
from collectors.postgres import PostgresCollector
from collectors.collector import MultiCollector

from utils.locking import FileLock
from utils.build import build
from utils.cluster import PgCluster
from utils.logging import log
from utils.upload import upload

from settings import *
from settings_local import * 
from folders import *

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':

    
    
    if (AUTOMATIC_UPLOAD):
        upload(API_URL, OUTPUT_PATH, MACHINE_SECRET)
    '''

    
    with FileLock('.lock') as lock:

        git_pull_runtime = None
        git_clone_runtime = None

        build_runtime = None
        install_runtime = None
        configure_runtime = None

        # run received time
        run_received_time = datetime.now()

        # first of all, creating base path
        if (not (os.path.exists(BASE_PATH))):
            os.mkdir(BASE_PATH)

        log("Starting client...")

        # checking for local installation
        if (os.path.exists(REPOSITORY_PATH)):

            # an existing installation has been found
            # avoid rebuilding and reinstalling

            # cleaning socket path
            if (os.path.exists(SOCKET_PATH)):
                shutil.rmtree(SOCKET_PATH)
                os.mkdir(SOCKET_PATH)

            # cleaning log path
            if (os.path.exists(LOG_PATH)):
                shutil.rmtree(LOG_PATH)
                os.mkdir(LOG_PATH)

            log("Existing installation found...")

            branch = (git.Repo(REPOSITORY_PATH)).active_branch
            commit = (git.Repo(REPOSITORY_PATH)).head.commit

            if (UPDATE):
                # call git pull
                log("Updating repository...")
                git_pull_start_time = datetime.now()
                a = git.Git(REPOSITORY_PATH).pull()

                with open(LOG_PATH + '/git_pull_log.txt', 'w+') as file:
                    file.write("git pull log: \n")
                    file.write(a)

                git_pull_end_time = datetime.now()
                git_pull_runtime = str(git_pull_end_time - git_pull_start_time)

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

                    configure_runtime, build_runtime, install_runtime = build()

                else:
                    log("Repository is up to date. ")

        else:
            # remove build and install path just to be sure
            if (os.path.exists(BUILD_PATH)):
                shutil.rmtree(BUILD_PATH)
            os.mkdir(BUILD_PATH)

            if (os.path.exists(INSTALL_PATH)):
                shutil.rmtree(INSTALL_PATH)
            os.mkdir(INSTALL_PATH)

            if (os.path.exists(SOCKET_PATH)):
                shutil.rmtree(SOCKET_PATH)
            os.mkdir(SOCKET_PATH)

            if (os.path.exists(LOG_PATH)):
                shutil.rmtree(LOG_PATH)
            os.mkdir(LOG_PATH)

            # and finally, clone
            log("Cloning repository...")
            git_clone_start_time = datetime.now()

            try:
                a = git.Git(BASE_PATH).clone(GIT_URL)

                git_clone_end_time = datetime.now()
                git_clone_runtime = str(git_clone_end_time - git_clone_start_time)

                # and build
                configure_runtime, build_runtime, install_runtime = build()

            except Exception as e: # any exception
                with open(LOG_PATH + '/git_clone_log.txt', 'w+') as file:
                    file.write("git clone log: \n")
                    file.write(e.stderr)
                    log("Error while cloning, check logs.")
                    sys.exit(1)

        # get (or rewrite) current branch and commit
        # string because it must be JSON serializable
        repository = git.Repo(REPOSITORY_PATH)
        branch = str(repository.active_branch)
        commit = str(repository.head.commit)

        # build and start a postgres cluster

        cluster = PgCluster(OUTPUT_PATH, bin_path=BIN_PATH, data_path=DATADIR_PATH)

        # create collectors
        collectors = MultiCollector()

        system = os.popen("uname").readlines()[0].split()[0]

        if system == 'Linux':
            collectors.register('linux', SystemCollector(OUTPUT_PATH))

        if system == 'Darwin':
            collectors.register('osx', SystemCollector(OUTPUT_PATH))

        collectors.register('collectd',
                            CollectdCollector(OUTPUT_PATH, DATABASE_NAME, ''))

        pg_collector = PostgresCollector(OUTPUT_PATH, dbname=DATABASE_NAME, bin_path=('%s/bin' % (BUILD_PATH)))

        collectors.register('postgres', pg_collector)

        runner = BenchmarkRunner(OUTPUT_PATH, API_URL, MACHINE_SECRET, cluster, collectors)

        # register the three tests we currently have
        runner.register_benchmark('pgbench', PgBench)

        # register one config for each benchmark (should be moved to a config file)
        PGBENCH_CONFIG['results_dir'] = OUTPUT_PATH
        POSTGRES_CONFIG['listen_addresses'] = ''
        POSTGRES_CONFIG['unix_socket_directories'] = SOCKET_PATH
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
            # run start time
            run_start_time = datetime.now()
            runner.run()
            run_end_time = datetime.now()

        # remove the data directory
        try:
            cleanup_start_time = datetime.now()
            if os.path.exists(DATADIR_PATH):
                shutil.rmtree(DATADIR_PATH)
            cleanup_end_time = datetime.now()
            cleanup_runtime = str(cleanup_end_time - cleanup_start_time)

        except Exception as e: # any exception
            with open(LOG_PATH + '/cleanup_log.txt', 'w+') as file:
                file.write(e.stderr)
                log("Error while cleaning directories, check logs.")
                sys.exit(1)


        runtime = {
            'run_received_time': run_received_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'run_start_time': run_start_time.strftime("%Y-%m-%dT%H:%M:%S"), 
            'run_end_time': run_end_time.strftime("%Y-%m-%dT%H:%M:%S"), 
            'git_clone_runtime': git_clone_runtime,
            'git_pull_runtime': git_pull_runtime,
            'configure_runtime': configure_runtime,
            'build_runtime': build_runtime, 
            'install_runtime': install_runtime, 
            'cleanup_runtime': cleanup_runtime
        }

        # saving times in a text file
        with open(LOG_PATH + '/runtime_log.txt', 'w+') as file:
            file.write(json.dumps(runtime))


        if (AUTOMATIC_UPLOAD):
            upload(API_URL, OUTPUT_PATH, MACHINE_SECRET)

        else:
            log("Benchmark completed, check results in '%s'" % (OUTPUT_PATH, ))
    '''
    