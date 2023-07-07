# Google Summer of Code 2023 Report

PostgreSQL is an excellent and progressively refined database management system. To test its performance, the Postgres Performance Farm was born as a result of the efforts of GSOC developers in previous years. In order to improve Pgperffarm even more, this year the GSOC project focused on the following aspects:




## Client

The main change to the client is adding a Fair use derivation of TPC-H Benchmark, of which the code is stored in the folder `pgtpch`.

Secondly the structure of the workflow in the `perffarm-client.py` is changed to run different modes of benchmarks instead of only Pgbench.

Thirdly the client supports custom database name and the upload function supports basic auth now. 

## Back-end

In order to add new benchmarks, modifications to the database structure is done. Adding new models and change the existing ones but also not violating 3NF the database design principle.

Secondly to incorporate with frontend changing to Django template, each backend view function needs to be changed to return Django template instead.

The email notification is also implemented on the server so that in case the performance drops, the user will be notified.

## Front-end

The front-end was a website written in vanilla Javascript. And this year the whole website is rewritten with Django template.

Webpages for the TPC-H part are also added. For the TPC-H trend and query result, charts and digrams are added with D3.js.

## Weekly Completed Tasks


### may 29 ~ 4-June 
added explain query to Tpch
saving the explain query and sending to the server

### 5-June ~ 11-June
added expalin query with cost off to Tpch
saving the explain query and sending to the server


### 12-June ~ 18-June
Change the some part of code on client side to save the Tpch Querys, and send them to the server, in Tpch_res.py  added a new Dictionary to save the  querys, and in Upload.py added some code  fto send the  querys to the server.

On server side added a new model to save the Tpch Querys, epxlain Cost on and Cost off results, and  in parsing_function.py added a new function   to parse and  save the Tpch Querys, epxlain Cost on and Cost off results to the database.
We are not saving the expain cost off results to the database, because results may be same for dffferent benchmarks, so i created  a hash function to check if the results are same or not, if they are same we are not saving them to the database.


### 19-June ~ 25-June
In the week worked on frontend part of Tpch, added a new page to show the Tpch Querys, and added a new page to show the Tpch Querys explain results, and added a new page to show the Tpch Querys explain cost on and cost off results.
And added bar graph for excution and planning time of Tpch Querys

### 29-June ~ 6-July

during this week i deployed the project in the server, and fixed some bugs in the project.
configured the project with Ngix ans Uwsgi, for the deployment.

setup the Client script on the server, and configured the client script to run the Tpch benchmark.
add a creotab job to run the client script  3 times a day.
Doing testing

Fixed the Connnection error in client script https://github.com/PGPerfFarm/pgperffarm/commit/158d846dd45dca80b6b8297ab2893a766f7f4468
fixed the tpch projetect_path                 https://github.com/PGPerfFarm/pgperffarm/commit/2516192abb0845be316053ed6d11674580761fe2


###  New Models for Tpch
```TpchQuery    # to save the Tpch Querys
      query_id (Id of the query)
      query_statement (Query statement)
    ``````
```ExplainQueryCostOnResult    # to save the Tpch Querys explain cost on  results
    tpch_query  (Foreign key to TpchQuery)
    tpch_result (foreign key to TpchResult)
    planning_time (planning time of the query)
    execution_time (execution time of the query)
    ``````
```ExplainQueryCostOnResultDetails    # to save the Tpch Querys explain cost on  results details
   explain_query_cost_on_result (Foreign key to ExplainQueryCostOnResult)
   result (Json field to save results)
    ``````  
```ExplainQueryCostOffResult  # TO save the cost on results
     tpch_query (Foreign key to TpchQuery)
     plan_hash (hash of the plan)
     The results of tpch explain cost off are not changing for different benchmarks, so we are not saving them to the database, we are just saving the hash of the plan, and if the hash is already in the database we are not saving the results to the database.
     ```