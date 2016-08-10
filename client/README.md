PostgreSQL performance farm client
==================================

A client integrating several database benchmarks intended for regular testing
of PostgreSQL during development, and reporting the results back to a server.
You can think of this as another buildfarm, but running performance tests
instead of regression tests. Also, this is written in Python and not Perl.

Currently there are three benchmarks available:

* pgbench (TPC-B-like, testing OLTP workload)


Limitations
-----------

The current client has a number of limitations - firstly, it only works on
Linux (and perhaps other unix-like operating systems - Solaris, BSD, ...).
If you're interested in making it work on Windows, let me know.


pgbench
-------

Requires no extra setup, everything is handled by the code (including data
generation etc.).


Statistics
----------

The client also collects various system-level statistics, useful when analyzing
the results and investigating performance regressions or differences between
systems. This includes:

* various data from /proc (cpuinfo, meminfo, ...)
* PostgreSQL statistics (bgwriter, databases, tables and indexes)
* sar statistics
