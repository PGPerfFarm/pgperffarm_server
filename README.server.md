# PostgreSQL Performance Farm Server Side

This document is about the Server Side of Performance Farm. It contains descriptions about the REST API and the Website.



## REST API

### Requirements

The API relies on Django. Since it needs a specific Django version compliant with the Postgres infrastructure, it is advised to run the API in a virtual environment.

 The additional packages are:

* Django 3.2
* requests
* urllib3
* psycopg2
* pycryptodomex

More information about requirements file and installation script can be found in the installation instructions below.

### Installation

```bash
$ cd rest_api
```

Set up and activate Python `virtualenv`

```bash
$ python3 -m venv /path/to/venv
$ source /path/to/venv/bin/activate
```

Install the required modules.

```bash
$ pip3 install -r requirements.txt
```

Next, create a `rest_api/settings_local.py` file:

```bash
$ cp rest_api/settings_local.py.in rest_api/settings_local.py
```

Edit the file and change the database configuration and other settings to suit your environment. Make sure you create the required database and user account on your PostgreSQL server.

Finally, synchronise the database and load the data:

```bash
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py loaddata initial_data.json
```

Additionally, to create an admin local account, run:

```bash
$ python3 manage.py createsuperuser
```

To run the server for testing, run the following command and point a browser at the URL shown:

```bash
$ python3 manage.py runserver
```

You should see the index page of the application. To log in, go to `/admin`.

The API also supports authentication from the Postgres community infrastructure, however it has not been tied to the official website yet; at the moment it is possible to test with pgweb local servers.

### Email notification functionality

In settings `settings_local.py` file, you can specify the email configurations (email host, host user and user password)

When the server is running, in the user page, the email notification can be set on or off and the thresholds can be set for PgBench and TPC-H like benchmarks accordingly.

## Website

### Requirements

The Website is built with flask template. No additional package install is required.

Only one external library is being used inside the code. D3.js is being used for drawing the trend charts. It is being loaded from [Google Hosted Libraries](https://developers.google.com/speed/libraries#d3.js).