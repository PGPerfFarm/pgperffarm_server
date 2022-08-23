# Google Summer of Code 2021 Report

PostgreSQL is a big and active open-source DBMS. This means that the code changes frequently and there are a lot of branches and commits. When big changes are made, performance has to be tested.

Performance Farm is a program that can be used to collect and visualize the benchmark results while the source code changes. Developers can analyze the performance of different versions of the source code or the efficacy on different operating systems.

Performance Farm consists of 3 parts.

- Client: A Python script that clones the PostgreSQL source code from a specific branch and creates a temporary PostgreSQL cluster. Then runs pgbench and collect the results and finally uploads the results to the API server.
- REST API: Receives benchmark results from the Client and provides data for the Website.
- Website: The Website shows lists of machines, runs, and benchmark results and also visualizes benchmark result trends.

Performance Farm has been developed as a Google Summer of Code project for a few years and the core structure was almost made. This year was mostly about adding a few more features and removing dependencies.



## Client

The main goal for the Client was to add more system metadata.

`pg_stat_statements` is a module that tracks planning and execution statistics of all SQL statements which is embeded inside PostgreSQL. This had to be built and enabled before the actual benchmark began.

`collectd` collects system and application performance metrics periodically. This daemon has to collect data during each benchmark iteration.

New collectors were added for these and the metadata were added to the final result that will be uploaded to the REST API.

Also, the code was cleaned up to match the PEP8 convention.

Furthermore, some errors occurred on the newest version (14) of PostgreSQL. Fixtures were made to support new versions.



## REST API

As the Client collects more system metadata, the REST API and the database had to be updated to receive these data. The parser, model, and the view has been updated for `pg_stat_statements` and `collectd`.

The API endpoints are updated to have a consistent name and an API document is created.

Also, the Python packages were updated and there were slight fixes to make the script compatible with the newest versions.



## Website

The Website was the biggest change this year. This year, most of the dependencies such as Vue.js were removed.

It was reconstructed using only vanilla Javascript.

Existing pages (home, machines, run, result, postgres, benchmarks, trend, profile) were implemented.

The trend chart was drawn using D3.js. Also, new user interactions such as showing tooltips, highlighting rows, filtering commits, and commit search features were added to the trend chart.



## Weekly Completed Tasks

### June 7 ~ June 14

- Added pg_stat_statements and collectd to Client.
- Tested community auth using a local instance of pgweb.
- Refactored python code using PEP8 convention.

### June 14 ~ June 21

- Implement machine add request for community users and machine approve for staff.
- Updated collectd collector.
- Implemented API's parser for pg_stat_statements and collectd.

### June 21 ~ June 28

- Updated API model and view for pg_stat_statements and collectd.
- Updated API routes using namespace and created API document.
- Created overview, machines, and benchmarks page in frontend.

### June 28 ~ July 5

- Created machine detail, run, result page in frontend.

### July 5 ~ July 12

- Created postgres history, trend page in frontend.

### July 12 ~ July 19

- Created trend chart using D3.
- Added pg_stat_statements and collectd to benchmark result page.
- Fixed parser bugs in the API.

### July 19 ~ July 26

- Added login, profile page in frontend.
- Linked login with pgweb community login.
- Added horizontal scroll for large tables.
- Installed frontend to PostgreSQL's Debian server.

### July 26 ~ August 2

- Show 3 latest runs.
- Updated basic css.
- Fixed bugs.
- Installed REST API to PostgreSQL's Debian server.
- Ran Client runs automatically using crontab.

### August 2 ~ August 9

- Fixed Client's tps parser according to the Postgres version.
- Limited trend chart tick to maximum 10 ticks.
- Added modal to trend page that show runs of each commit.
- Highlight trend table when chart is clicked.
- Implemented commit select filter to trend chart.

### August 9 ~ August 16

- Added commit search feature.
- Added trend table pagination.
- Fixed dependency and security issues.
