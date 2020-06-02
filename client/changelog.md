### Performance Farm Benchmarks: bug fixing and change log

##### 01.06.2020

Key points: the code is not supposed to be run using an existing personal Postgres installation. There is also a list of important branches, and the script should clone and run benchmarks on each one separately. 

- System cannot find directory BIN_PATH, that being BUILD_PATH + 'bin'.
  BUILD_PATH is set by default as '/tmp/bin-postgres', for some reason the OS cannot create two directories at the same time, an additional mkdir is imposed to first create bin-postgres and then bin.
- Found another bug: the directory gets somehow cancelled during the process, and not after it is over.
- The whole cloning and installing system is a mess, I plan to make a gradual switch to another Python module of git and let it handle everything.
- Call is being replaced with run within subprocess module, since it works better on later versions of Python.
- Found additional requirements for make: bison, flex (Debian).
- Error during make should be logged, but otherwise the git cloning and installing works.
- Killing processes is now embedded into a try-catch statement, so that if the postmaster.pid file is not found, the program does not break.



##### Files and folders

* perffarm-client.py: takes care of coordinating the setup of benchmarks, and when everything is initialized runs collectors;
* Benchmarks:
  * pgbench.py:
  * runner.py: 
* Collectors:
  * collectd.py: runs collectd to gather system and database statistics;
  * collector.py: combines other collectors and calls them;
  * linux.py: contains a collection of shell commands to extract system information such as CPU usage, kernel configuration and memory;
  * postgres.py: manly a function that connects to Postgres and selects its settings;
* Post example: 
  * upload.py: takes the output file and sends it to the API;
* Utils: 
  * cluster.py: 
  * git.py: hand-written module to extract information from a git repository;
  * locking.py: ensures locking of files;
  * logging.py: prints nice logging;
  * misc.py: connects to database and returns available RAM.

