#!/usr/bin/env python3

import argparse
import json
import os
import git
import pathlib
import shutil
import psutil
import pydriller
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
from branches import *

import folders
from path import create_path


if __name__ == '__main__':


	def run(branch_name, BRANCH_PATH):
		
		'''
		if (AUTOMATIC_UPLOAD):
			upload(API_URL, folders.OUTPUT_PATH, MACHINE_SECRET)
		'''

		
		with FileLock('.lock') as lock:

			git_pull_runtime = None
			git_clone_runtime = None

			build_runtime = None
			install_runtime = None
			configure_runtime = None

			# run received time
			run_received_time = datetime.now()

			log("Starting client for branch '%s'..." % (branch_name, ))

			# checking for local installation
			if (os.path.exists(folders.REPOSITORY_PATH)):

				# an existing installation has been found
				# avoid rebuilding and reinstalling

				# cleaning socket path
				if (os.path.exists(folders.SOCKET_PATH)):
					shutil.rmtree(folders.SOCKET_PATH)
					os.mkdir(folders.SOCKET_PATH)

				# cleaning log path
				if (os.path.exists(folders.LOG_PATH)):
					shutil.rmtree(folders.LOG_PATH)
					os.mkdir(folders.LOG_PATH)

				log("Existing installation found...")

				branch = (git.Repo(folders.REPOSITORY_PATH)).active_branch
				commit = (git.Repo(folders.REPOSITORY_PATH)).head.commit

				if (UPDATE):
					# call git pull
					log("Updating repository...")
					git_pull_start_time = datetime.now()
					a = git.Git(folders.REPOSITORY_PATH).pull()

					with open(folders.LOG_PATH + '/git_pull_log.txt', 'w+') as file:
						file.write(a)

					git_pull_end_time = datetime.now()
					git_pull_runtime = str(git_pull_end_time - git_pull_start_time)

					latest_branch = (git.Repo(folders.REPOSITORY_PATH)).active_branch
					latest_commit = (git.Repo(folders.REPOSITORY_PATH)).head.commit

					if (latest_commit != commit or latest_branch != branch):
						log("Rebuilding repository to apply updates...")

						if (os.path.exists(folders.BUILD_PATH)):
							shutil.rmtree(folders.BUILD_PATH)
						os.mkdir(folders.BUILD_PATH)

						if (os.path.exists(folders.INSTALL_PATH)):
							shutil.rmtree(folders.INSTALL_PATH)
						os.mkdir(folders.INSTALL_PATH)

						configure_runtime, build_runtime, install_runtime = build()

					else:
						log("Repository is up to date. ")

			else:
				# remove build and install path just to be sure
				if (os.path.exists(folders.BUILD_PATH)):
					shutil.rmtree(folders.BUILD_PATH)
				os.mkdir(folders.BUILD_PATH)

				if (os.path.exists(folders.INSTALL_PATH)):
					shutil.rmtree(folders.INSTALL_PATH)
				os.mkdir(folders.INSTALL_PATH)

				if (os.path.exists(folders.SOCKET_PATH)):
					shutil.rmtree(folders.SOCKET_PATH)
				os.mkdir(folders.SOCKET_PATH)

				if (os.path.exists(folders.LOG_PATH)):
					shutil.rmtree(folders.LOG_PATH)
				os.mkdir(folders.LOG_PATH)

				# and finally, clone
				log("Cloning repository...")
				git_clone_start_time = datetime.now()

				try:
					a = git.Git(BRANCH_PATH).clone(GIT_URL)

					git_clone_end_time = datetime.now()
					git_clone_runtime = str(git_clone_end_time - git_clone_start_time)

					# and build
					configure_runtime, build_runtime, install_runtime = build()

				except Exception as e: # any exception
					with open(folders.LOG_PATH + '/git_clone_log.txt', 'w+') as file:
						file.write("git clone log: \n")
						file.write(e.stderr)
						log("Error while cloning, check logs.")
						sys.exit(1)

			# get (or rewrite) current branch and commit
			# string because it must be JSON serializable
			repository = git.Repo(folders.REPOSITORY_PATH)
			branch = str(repository.active_branch)
			commit = str(repository.head.commit)
			author = pydriller.GitRepository(folders.REPOSITORY_PATH).get_commit(commit).author.name


			# build and start a postgres cluster

			cluster = PgCluster(folders.OUTPUT_PATH, bin_path=folders.BIN_PATH, data_path=folders.DATADIR_PATH)

			# create collectors
			collectors = MultiCollector()

			system = os.popen("uname").readlines()[0].split()[0]

			if system == 'Linux':
				collectors.register('linux', SystemCollector(folders.OUTPUT_PATH))

			if system == 'Darwin':
				collectors.register('osx', SystemCollector(folders.OUTPUT_PATH))

			collectors.register('collectd',
								CollectdCollector(folders.OUTPUT_PATH, DATABASE_NAME, ''))

			pg_collector = PostgresCollector(folders.OUTPUT_PATH, dbname=DATABASE_NAME, bin_path=('%s/bin' % (folders.BUILD_PATH)))

			collectors.register('postgres', pg_collector)

			runner = BenchmarkRunner(folders.OUTPUT_PATH, API_URL, MACHINE_SECRET, cluster, collectors)

			# register the three tests we currently have
			runner.register_benchmark('pgbench', PgBench)

			# register one config for each benchmark (should be moved to a config file)
			PGBENCH_CONFIG['results_dir'] = folders.OUTPUT_PATH
			POSTGRES_CONFIG['listen_addresses'] = ''
			POSTGRES_CONFIG['unix_socket_directories'] = folders.SOCKET_PATH
			runner.register_config('pgbench-basic',
								   'pgbench',
								   branch,
								   commit,
								   author,
								   dbname=DATABASE_NAME,
								   bin_path=folders.BIN_PATH,
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
				if os.path.exists(folders.DATADIR_PATH):
					shutil.rmtree(folders.DATADIR_PATH)
				cleanup_end_time = datetime.now()
				cleanup_runtime = str(cleanup_end_time - cleanup_start_time)

			except Exception as e: # any exception
				with open(folders.LOG_PATH + '/cleanup_log.txt', 'w+') as file:
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
			with open(folders.LOG_PATH + '/runtime_log.txt', 'w+') as file:
				file.write(json.dumps(runtime))


			if (AUTOMATIC_UPLOAD):
				upload(API_URL, folders.OUTPUT_PATH, MACHINE_SECRET)
				log("Run complete. Uploading...")

			else:
				log("Run complete, check results in '%s'" % (folders.OUTPUT_PATH, ))

		return

	# end of function

	# first of all, creating base path
	if (not (os.path.exists(BASE_PATH))):
		os.mkdir(BASE_PATH)


	for branch in branches:

		folders.init()

		BRANCH_PATH = os.path.join(BASE_PATH, branch['branch_name'])

		if (not (os.path.exists(BRANCH_PATH))):
			os.mkdir(BRANCH_PATH)

		# calculate child directories
		create_path(BRANCH_PATH)

		run(branch['branch_name'], BRANCH_PATH)
		