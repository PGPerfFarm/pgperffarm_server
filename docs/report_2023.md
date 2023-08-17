# Google Summer of Code 2023 Report

PostgreSQL is an excellent and progressively refined database management system. To test its performance, the Postgres Performance Farm was born as a result of the efforts of GSOC developers in previous years. In order to improve Pgperffarm even more, this year the GSOC project focused on the following aspects:




## Client

The Client was a Python script that clones the PostgreSQL source code from a specific branch and creates a temporary PostgreSQL cluster. Then runs pgbench and collect the results and finally uploads the results to the backend.


The client Script is modified to run the custom queries and collect the explain plans and upload them to the backend. Eaplain plans are add in TPC-H benchmark. By generating and collecting EXPLAIN query plans, the performance farm can help users better understand the performance characteristics of their queries. This can be particularly helpful for identifying slow or inefficient queries and helping users optimize their database performance.


## Server

The server is a Django application that provides a REST API to store and retrieve the results of the benchmarks. The server also provides a web interface to visualize the results.


The server is modified to store the explain plans and display them in the UI. The new Models is added to store the explaine plans and the new API is added to upload the explain plans to the server. Also the new Models is add for pgbench custom queries results and the new API is added to upload the custom queries results to the server. From server we can download the explain plans and pgbench custom queries configurations.

##  Completed Tasks



added explain query to Tpch
saving the explain query and sending to the server


added expalin query with cost off to Tpch
saving the explain query and sending to the server



Change the some part of code on client side to save the Tpch Querys, and send them to the server, in Tpch_res.py  added a new Dictionary to save the  querys, and in Upload.py added some code  fto send the  querys to the server.

On server side added a new model to save the Tpch Querys, epxlain Cost on and Cost off results, and  in parsing_function.py added a new function   to parse and  save the Tpch Querys, epxlain Cost on and Cost off results to the database.
We are not saving the expain cost off results to the database, because results may be same for dffferent benchmarks, so i created  a hash function to check if the results are same or not, if they are same we are not saving them to the database.



In the week worked on frontend part of Tpch, added a new page to show the Tpch Querys, and added a new page to show the Tpch Querys explain results, and added a new page to show the Tpch Querys explain cost on and cost off results.
And added bar graph for excution and planning time of Tpch Querys



during this week i deployed the project in the server, and fixed some bugs in the project.
configured the project with Ngix ans Uwsgi, for the deployment.

setup the Client script on the server, and configured the client script to run the Tpch benchmark.
add a creotab job to run the client script  3 times a day.
Doing testing

Fixed the Connnection error in client script https://github.com/PGPerfFarm/pgperffarm/commit/158d846dd45dca80b6b8297ab2893a766f7f4468
fixed the tpch projetect_path                 https://github.com/PGPerfFarm/pgperffarm/commit/2516192abb0845be316053ed6d11674580761fe2


###  New Models for Tpch
    TpchQuery #  to save the Tpch Querys
    query_id (Id of the query)
    query_statement (Query statement)
    
    ExplainQueryCostOnResult    # to save the Tpch Querys explain cost on  results
        tpch_query  (Foreign key to TpchQuery)
        tpch_result (foreign key to TpchResult)
        planning_time (planning time of the query)
        execution_time (execution time of the query)
   
    ExplainQueryCostOnResultDetails    # to save the Tpch Querys explain cost on  results details
        explain_query_cost_on_result (Foreign key to ExplainQueryCostOnResult)
        result (Json field to save results)
    
    ExplainQueryCostOffResult  # TO save the cost on results
        tpch_query (Foreign key to TpchQuery)
        plan_hash (hash of the plan)
    The results of tpch explain cost off are not changing for different benchmarks, so we are not saving them to the database, we are just saving the hash of the plan, and if the hash is already in the database we are not saving the results to the database.
     


### New models for Pgbench custom
    PgbenchCustomDetails   # to save the pgbench custom queries results
       init_sql (Intiazation sql file of pgbench custom)
       pgbench_result_id (Foreign key to PgbenchResult)

    custom_queries  # Table for store the custom queries
       pgbench_result_id (Foreign key to PgbenchResult)
       custom_query   (foreign key to custom_query)

    custom_query  # Table for store the custom queries
       data (custom query)
       weight (weight of the query)
       hash (hash of the query)

    
   