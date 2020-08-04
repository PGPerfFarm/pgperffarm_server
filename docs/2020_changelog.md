### Performance Farm Benchmarks: bug fixing and change log



#### TODO LIST

* Benchmarks:
  * Fix the collectd part (script for installing collectd to run further tests);
  * Remove unnecessary fields from JSON;
  * Pull pg_stat_statement data;
  * Allow logging of build/install even with an empty result;
* API:
  * Collectd tables when that is implemented;
  * Table log_logentry (id int, timestamp timestamptz, machine, level, logmessage, acknowledged);
  * Email the user if a machine changes kernel;
  * os_kernl_id_id in systems_knownsysctlinfo should be defined as UNIQUE (move that list into systems_kernel and get rid of the knownsysctlinfo table);
* Website:
  * Use authentication from https://git.postgresql.org/gitweb/?p=pglister.git;a=blob;f=web/pglister/auth.py;h=87ffb0b2adbcd45d956b7f625dc9ae29c7807bfa;hb=HEAD;
  * Display data within the same branches and maybe also within all branches;
  * Add possibility to download further files;
  * Add automatic update of list of branches;
  * Pages to fix:
    * Single machine: still to do;
    * Benchmarks: check if ordering works
    * Add machine: temporarily disabled;
    * Login: temporarily disabled;
    * My machines: temporarily disabled;
    * Homepage: to revamp;
    * User profile: temporarily disabled.

+ Documentation:
  + add missing tables to docs;
  + database of client must exist;
  + add cronjob (user);
  + Add script to load data;


