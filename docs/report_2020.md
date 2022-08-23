# Google Summer of Code 2020 - report

The Performance Farm is a project aimed to highlight the performance of Postgres as changes are being made, running benchmarks and displaying their results in a website. 

The project consists of three main parts:

* A client script, in charge of retrieving latest version of Postgres, building and installing it, and running PgBench to then collect results in JSON format;
* An API which receives results, parses them and stores them in a database while exposing endpoints for them to be fetched;
* A website, which takes parsed and aggregates results from the API and displays them through tables, plots and textual information.

The Performance Farm has been a Google Summer of Code project for a few years, therefore the work of 2020 consisted in improving and extending the current version, rather than rewriting it from scratch; however, a lot of functions have completely been changed since the project has been adapted to be more solid and with a coherent database structure.



### Client script

The 2019 version was functioning, yet had some flaws and bugs that could not be overlooked: the client script was not portable, had quite a few outdated packages and was lacking exception handling and logging. 

It has been improved with a better definition of folders and paths, creating a fixed structure and a dedicated socket folder to avoid conflict with existing processes, and it has been extensively tested to find additional requirements and potential bugs. If anything goes wrong, there are several files containing logs for each step of the procedure and only faulty files are deleted, avoiding to repeat computationally heavy operations.

Furthermore, the previous version relied on raw Bash commands to extract informations: this has been replaced with high-level Python packages which take care of Git commands and collecting system details. All operational times are calculated and get uploaded together with PgBench results, as well as logs and warning messages. 

There is now a predefined list of branches which get cloned, built and configured: each execution of the script performs benchmarks on all of them, and saves the result in a dedicated folder under the base path.

The script does not remove folders afterwards unless requested in the settings, so that the cloning operation is not performed every time: if an existing folder is found, the script just performs a pull operation and rebuilds if something has changed. 

Postgres is ran with custom data directories and socket path, to have a clean installation without processes interfering with existing setups. For each iteration, the database gets now dropped and recreated. 

PgBench commands have also been extended with more options to generate additional information which is then saved in the database. 

The set of configurations for PgBench has been revisited as well, removing the CSV option and allowing multiple sets of different configurations, with respective control for correctness. 

The JSON result is now much more cleaner and human readable.



### API and database

The API has for the most part been rewritten: the database has completely been redesigned, therefore the previous structure needed to be changed.

The database now holds information about:

* Runs (executions of the client script);
* Benchmarks (results, logs, statements and configurations);
* Hardware, compilers and system information;
* Postgres configuration;
* Repositories and branches;
* Machines;
* Users (fetched by the main Postgres authentication system).

All information filling these tables is obtained by the result from the client script and saved in an atomic way, after checking that the user has permission to upload (i. e. the machine has been approved by an admin). 

The API does not depend on Django-REST anymore, it is now written only using Django with a custom middleware, basic cookie handling and authentication from the Postgres website. 

To remove the Django-REST dependency, more checks have been added (fields validation, correctness, existence, size limit) both on the database and the API with Django validators.

Serializers and viewsets have also been removed and replaced with simple views which return a JSON response with related data. 

The requirements list has now been extremely trimmed down to mainly rely on Python packages maintained by Debian developers to be hosted on the Postgres machines.



### Website

The website was subject to changes mainly on the Javascript part: it naturally needed to be adapted to fetch results in the new format, and the current functionalities have been extended to also display the additional information being collected. Component-wise, the major improvements have been:

* A Trend page, displaying scatter plots and aggregated information about trends of latency and TPS from PgBench results for each commit;
* Run and benchmark results pages;
* History pages, highlighting changes in system parameters and Postgres configuration. 

In addition, bugs have been fixed and there has been some minor style changes. 

Webpack has been added instead of Vue-Loader to optimise compilation and code size, splitting heavy modules and loading them dynamically. 