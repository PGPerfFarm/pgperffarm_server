# Google Summer of Code 2022 Report

PostgreSQL is an excellent and progressively refined database management system. To test its performance, the Postgres Performance Farm was born as a result of the efforts of GSOC developers in previous years.In order to improve Pgperffarm even more, this year the GSOC project focused on the following aspects.

In order to improve Pgperffarm even more, this year the GSOC project focused on the following aspects.

* Add new benchmarking types to the client. (like fair use derivation based on the TPC-H benchmark)
* Refactor the front-end with Django template.
* Add new features to the backend. (e.g. Adding email notification feature)


## Client

The main change to the client is adding a Fair use derivation of TPC-H Benchmark, of which the code is stored in the folder `pgtpch`.

Secondly the structure of the workflow in the `perffarm-client.py` is changed to run different modes of benchmarks instead of only Pgbench.

Thirdly the client supports custom database name and the upload function supports basic auth now. 

## Back-end

In order to add new benchmarks, modifications to the database structure is done. Adding new models and change the existing ones but also not violating 3NF the database design principle.

Secondly to incorporate with frontend changing to Django template, each backend view function needs to be changed to return Django template instead.

The email notification is also implemented on the server so that in case the performance drops, the user will be notified.

## Front-end

The front-end is a website written in vanilla Javascript. And this year the whole website is rewritten with Django template.

Webpages for the TPC-H part are also added. For the TPC-H trend and query result, charts and digrams are added with D3.js.

## Weekly Completed Tasks


### June 13 ~ June 27

- Added basic authentication to the back-end and front-end.
- Deployed the project on the server.


### June 27 -  July 11 

- Rewrote the front-end with Django template

### July 11 - 25 

- Added TPC-H benchmark to the back-end and front-end.

### July 29 - Aug 12 

- Added email notification feature to the back-end.
- Unified chart packages to d3.js.

### Aug 19 - 26 

- Redesigned the database schema and applied changed to the back-end.
- Updated client workflow.

### Aug 26 - Sep 9
- Integration test & debugging.
- Added support for custom database name.
- Finalized documentation.
