### Performance Farm Benchmarks: bug fixing and change log



#### TODO LIST

* Benchmarks:
  * Installing collectd to run further tests (?);
  * Adding more tests or more options to pgbench, or automated testing (?);
  * Reviewing process shutdown;
  * Add list of branches;
  * Portability tests;
  * Allow overriding of default scaling and clients;
  * Allow logging of build/install even with an empty result;
  * -r 
* API:
  * Whole refactoring of the code, especially the serializing of JSON output, since its structure will change and right now code is not really clean;
  * Handle credentials;
  * Speed up the whole thing with more compact information and less requests from the website;
  * Drop alias table, so that a person can use their own;
  * Make machine secret larger (128);
  * Add approved flag in place of status;
  * Add benchmark table;
  * Calculate hash string of configuration;
* Website:
  * Improve displaying of results compatible with the new JSON structure;
  * Add possibility to download further files;
  * Add automatic update of list of branches;
  * Fix login and permissions (compatible with Postgres web infrastructure);
  * Style changes, general bug fixes;
* Server:
  * Updating all Python versions, Node, all software being used;
  * Cleaning existing databases with old test data;
  * Setting up automatic benchmarks.

+ Documentation:
  + Detailed explanation of JSON fields;
  + Update README and installation procedure;
  + Update requirements (in progress).



##### Week 1

Key points: the code is not supposed to be run using an existing personal Postgres installation. There is also a list of important branches, and the script should clone and run benchmarks on each one separately. 

- System cannot find directory BIN_PATH, that being BUILD_PATH + 'bin'.
  BUILD_PATH is set by default as '/tmp/bin-postgres', for some reason the OS cannot create two directories at the same time, an additional mkdir is imposed to first create bin-postgres and then bin.
- Found another bug: the directory gets somehow cancelled during the process, and not after it is over.
- The whole cloning and installing system is a mess, I plan to make a gradual switch to another Python module of git and let it handle everything.
- Call is being replaced with run within subprocess module, since it works better on later versions of Python.
- Found additional requirements for make: bison, flex (Debian).
- Error during make should be logged, but otherwise the git cloning and installing works.
- Killing processes is now embedded into a try-catch statement, so that if the postmaster.pid file is not found, the program does not break.

* After defining a deterministic workflow for cloning, pulling and building the repository, the process is complete.
* The git custom written functions have been completely replaced by gitpython.
* Still missing a bit of refactoring, especially within the part of killing processes and deleting folders.
* Now next goal is trying to improve JSON output results, so that they can be parsed and displayed better. First thing to focus on is "linux", next is understanding why "collectd" is always empty;
* Then it is time to find out where Linux specifics are generated:
  * Part of it is in misc.py, launching a "free -m" command;
  * Mostly in linux.py, which is composed by "sysctl", "meminfo" etc.

* Continuing the process of removing walls of text in the output and gradually switching them with JSON parameters, trying to replace as much as possible;
* Integration with 3 Python modules able to collect statistics in a much more portable and readable way;
* Redefining the whole JSON structure;



##### Week 2

* Added log messages and files for git operations;
* Removed unnecessary nesting of JSON, adding "mode" and "scale" parameters as values specific to the result;
* Added all times to build, clone, install etc;
* Patched pgbench and cluster scripts to be able to execute in different environments without conflicting with existing processes;
* Code refactoring;
* Added a better folder structure;
* Fixed a bug in logging where the regular expression could not match because of a semicolon;



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
* Post example (removed in later versions): 
  * upload.py: takes the output file and sends it to the API;
* Utils: 
  * cluster.py: 
  * git.py: hand-written module to extract information from a git repository (deleted and replaced by build.py);
  * build.py: module which takes care of executing a build from source from a git repository;
  * locking.py: ensures locking of files;
  * logging.py: prints nice logging;
  * misc.py: connects to database and returns available RAM.

