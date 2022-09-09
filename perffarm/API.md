# Performance Farm REST API


## Benchmark

### GET /benchmark/overview

Get the latest benchmark runs.

### GET /benchmark/machines

Get benchmark runs of each machine and benchmark config.

### GET /benchmark/history/[machine_id]

Get benchmark runs of a certain machine.

### GET /benchmark/postgres/[machine_id]

Get postgres settings of a certain machine.

### GET /benchmark/pgbench_trends/[machine_id]/[benchmark_config_id]

Get benchmark trend of a certain machine and benchmark config.

### GET /benchmark/pgbench_results_commit/[git_commit]/[machine_id]/[benchmark_config_id]

Get benchmark runs of a certain machine, benchmark config, and commit.

### GET /benchmark/pgbench_results_complete/[pgbench_result_id]

Get details, logs, run statements, and configs of a certain benchmark result.


## Machine

### GET /machine/list

Get list of machines and latest runs.

### GET /machine/user

* Community user authentication required.

Get list of machines of a user.

### POST /machine/add

* Community user authentication required.

Send a request to add a machine.

### POST /machine/approve

* Staff authentication required.

Approve a machine so that it can upload benchmark results.

### POST /machine/edit/[machine_id]

* Community user authentication required.

Edit details of a machine.


## User

### GET /user/community_login

Login using pgweb community login.

### GET /user/logout

* Community user authentication required.

Logout.

### GET /user/auth_receive

Callback for pgweb authentication.


## Run

### POST /run/upload

Upload benchmark results from a machine.

### GET /run/[run_id]

Get details of a certain benchmark run.


## Tpch

### GET /tpch/machines

Get tpch benchmark runs of each machine and benchmark config.

### GET /tpch/details/[run_id]

Get details of a certain benchmark run.

### GET /tpch/trend/[machine_id]/[scale_factor]

Get the trends of tpch runs for a machine with certain scale factor

### GET /tpch/runs_commit/[machine_id]/[scale_factor]/[commit]

Get the tpch runs for a certain machine with certain scale factor under certain git commit