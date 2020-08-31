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

The JSON result is now much more cleaner and human readable: since 



### API

The API has for the most part been rewritten: the database has completely been redesigned, therefore the previous structure needed to be changed.



### Website

The website was subject to changes mainly on the Javascript part: it naturally needed to be adapted to fetch results in the new format, and the current functionalities have been extended to also display the additional information being collected. Component-wise, the major improvements have been:

* A Trend page, displaying scatter plots and aggregated information about trends of latency and TPS from PgBench results for each commit;
* Run and benchmark results pages;
* History pages, highlighting changes in system parameters and Postgres configuration. 

In addition, bugs have been fixed and there has been some minor style changes. 









