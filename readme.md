# PostgreSQL Performance Farm

This repository contains the code for the PostgreSQL Performance Farm, aiming to collect Postgres performance data through a Python script, outputting results on a JSON file. Results are then being sent to a Django-REST application and browsed with a Vue.js website on top of it.

----

### Structure

- *pgperffarm-front-end*: directory containing Javascript (Vue.js) source code.
- *client*: directory containing Python script to collect performance results.
- *rest_api*: directory containing the Django-REST API that forms the basis of the website;
- *docs*, directory containing related documentation.

This application is being developed as part of the Google Summer of Code project, started in 2018: the previous version can be found in the dev/ branch of GitHub. The 2019 version has been extended in 2020 and is currently work in progress.

For a full explanation about functioning of the script, check the documentation file in related folder.



### Requirements for running the client script

The Performance Farm **client script** requires:

- osX or any Linux based distribution;
- Python 3.6 or later (and pip3 or any package manager);
- Postgres 11 or later (while it should work with 9-10);
- Collectd 5.9 or later (in progress to either be completely removed or an optional dependency);
- Bison 2.3 or later;
- Flex 2.5 or later;

There might be other dependencies to configure and build Postgres which are not present on minimal installations of Linux, and will cause failure of the process. Such dependencies are (tested with Debian systems):

* zlib1g-dev;
* libreadline-dev.



#### Other requirements

To also run the API and the website (to test locally, compile and maintain, for instance), there are some additional requirements to install. If one does not plain to host or run for development the API and the website, those are not needed.

##### API

The API still relies on Python3, Django and Django-REST, and aside from additional Python packages there is no other requirements. Since it needs a specific Django version compliant with the Postgres infrastructure, it is advised to run the API in a virtual environment.

 The additional packages are:

* Django 2.2.13;
* Django-cors-headers (in the process of being removed);
* Django-rest-framework (in the process of being removed);
* Requests;
* Urllib3;
* Psycopg2;
* Pycryptodomex.

More information about requirements file and installation script can be found in the installation instructions below.

##### Website

The website is made with Vue.js, and all files are saved in .vue format to then be compiled into Javascript code.

The structure has been tested with both Yarn and Webpack, however to help code optimization Webpack is the preferred module bundler. Unfortunately, this implies also having Node and NPM installed on the machine taking care of building for production.

Once the website has been built, its files only consist in HTML, CSS and Javascript, therefore it is possible to compile and serve on different machines. 

Main requirements for **compiling** are:

* Node version 12 or higher;
* NPM version 6 or higher;
* Webpack version 3.6.0 or higher;
* Webpack-dev-server version 2.9.1 or higher.

Other packages are contained in the dedicated JSON file and can be installed following the instructions below. Since the website is still being developed, there are some packages (i. e. linters) which are not needed for production and will be removed in the future.



### Limitations

Since the infrastructure is still being developed, for the time by it is subject to some limitations which are being worked on:

* Results only get displayed on the website if they belong to the official repositories, i. e. https://github.com/postgres/postgres.git or http://git.postgresql.org/git/postgresql.git;
* Collectd is temporarily disabled;
* Logs are only saved locally if an exception occurs;
* Supported branches are only HEAD, 13_STABLE, 12_STABLE, 11_STABLE, 10_STABLE.



### Installation

#### Client code

The client code can work without virtual environment, yet requires the installation of a few additional packages. Remember not to run as root!

Run:

```bash
% cd client
% pip3 install -r requirements.txt
```

Next, edit the `settings_local.py` file to fit your needs. Remember that it is tied to the machine secret, obtained registering the machine in the website, therefore each test result will belong to the machine with the secret specified in the settings file.

Specifically, it is possible can set:

* Whether to test locally or upload results to the API;
* Whether to call `git pull` at every execution;

* Path in which to clone, install and collect output (should have non-superuser access);
* Postgres configuration;
* Database name for PgBench (must exist);
* PgBench configuration or set of configurations (two of the same configurations are allowed, as long as all the parameters are integers and clients are arrays).

After that, the client code is ready to execute. 

```bash
% python3 perffarm-client.py
```

The client script clones and runs tests on each of the branches specified above, and uploads them automatically after each iteration is complete if the appropriate flag is set.

If mistakes occur, the \$PGDATA directory is removed and it should be safe to re-run again. However, if there are still problems, it is advised to just remove the whole ​\$BASE_PATH.

Note that there may be issues with directories, since each system has its own defaults and permissions. If you encounter any problem, feel free to open an issue.

##### Cronjob

To set up automatic execution of the script, it is advised to create a cron job for it. The username is optional, and should be the same as $PGUSER.

```
USER=username
0 */2 * * * /path/to/pgperffarm/client/perffarm-client.py >> /path/to/perffarm.log 2>&1
```

A reasonable interval for the cronjob would be 2-6 hours, roughly as often as the MASTER branch is being updated. 



#### API

The API does not need installation to collect results, but it can be ran locally for development.

```bash
$ cd rest_api
```

In order to run the site, you will need to setup a Python `virtualenv`, e.g:

```bash
$ python3 -m venv /path/to/new/virtual/environment
```

To activate the environment, run:

```bash
$ source /path/to/new/virtual/environment/bin/activate
```

Then, install the required modules. Note that the API uses Django 2.2.13 as that's what is currently supported on the postgresql.org infrastructure:

```bash
$ pip3 install -r requirements.txt
```

Next, create a `settings_local.py` file:

```bash
$ cp rest_api/settings_local.py.in rest_api/settings_local.py
```

Edit the file and change the database configuration and other settings to suit your environment. Make sure you create the required database and user account on your PostgreSQL server.

- On osX, usually the host is `/tmp`;
- On Linux, usually the host is `/var/run/postgresql`.

Finally, synchronise the database and load the data:

```bash
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py loaddata initial_data.json
```

To create an admin local account, run:

```bash
$ python3 manage.py createsuperuser
```

That should be all. To test, run the following command and point a browser at the URL shown:

```bash
$ python3 manage.py runserver
```

You should see the index page of the application. To log in, use `127.0.0.1/admin`.

The API also supports authentication from the Postgres community infrastructure, however it has not been tied to the official website yet; at the moment it is possible to test with pgweb local servers.

##### Troubleshooting

Common issues encountered:

- Not found *auth_user* relation: delete migrations and remake everything.
- Error while installing psycopg2:
  - Try with the binary version or an older one.
- Problem starting Postgres:
  - Verify that Postgres is up and running, restart it and check the settings file for the correct path;
  - Check the sockets to see whether they exist.



#### Website

```bash
% cd pgperffarm-front-end
```

Before testing the website, it is necessary to install dependencies:

```
% npm install
```

To run for local testing, run:

```
% npm run dev
```

To compile and create the folder for production, run:

```
% npm run build
```

Once the website has been built, output files are found in the dist folder, which can be deployed and served with a web server.



