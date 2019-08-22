# PostgreSQL Performance Farm

This repository contains the code for the PostgreSQL Performance Farm, aiming to collect Postgres performance data through a Python script, outputting results on a JSON file. Results are then being sent to a Django-REST application and browsed with a Vue.js website on top of it.

----

### Structure

- *pgperffarm-front-end*: directory containing Javascript (Vue) source code.
- *client*: directory containing Python script to collect performance results.
- *rest_api*: directory containing the Django-REST API that forms the basis of the website.

This application is being developed as part of the Google Summer of Code project, started in 2018: the previous version can be found in the dev/ branch of GitHub.



### Requirements

The Performance Farm requires:

- osX or any Linux based distribution;
- Python 3.5 or later (and pip3);
- Node 8.12 or later;
- Django 1.11.17;
- Postgres 11 or later (while it should work with 9-10);
- Collectd 5.9 or later.

The Django version cannot be upgraded since it requires compatibility with the PostgreSQL website infrastructure.



### Installation

#### API

```bash
$ cd rest_api
```

In order to run the site, you will need to setup a Python `virtualenv`, e.g:

```bash
$ sudo pip3 install virtualenvwrapper
$ source /usr/local/bin/virtualenvwrapper.sh
$ mkvirtualenv pgperffarm
```

For ease of future use, configure virtualenvs from your `.bash_profile`:

```bash
$ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bash_profile
```

To activate the environment in future sessions, run:

```bash
$ workon pgperffarm
```

Then, install the required modules. Note that we use Django 1.8 as that's what is currently supported on the postgresql.org infrastructure:

```bash
$ pip3 install -r web/requirements.txt
```

Next, create a `settings_local.py` file:

```bash
$ cp rest_api/settings_local.py.in rest_api/pgperffarm/settings_local.py
```

Edit the file and change the database configuration and other settings to suit your environment. Make sure you create the required database and user account on your PostgreSQL server.

- If you're on osX, usually the host is '/tmp';
- If you're on Linux, usually the host is '/var/run/postgresql'.

Finally, synchronise the database:

```bash
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

Note that at the moment the only authentication methods are admin authentication and JWT. To create an admin local account, run:

```bash
$ python3 manage.py createsuperuser
```

That should be all. To test, run the following command and point a browser at the URL shown:

```bash
$ python3 manage.py runserver
```

You should see the index page of the application. To log in, use 127.0.0.1/admin.



##### Troubleshooting

Common issues encountered:

- Not found *auth_user* relation: delete migrations and remake everything.
- Error while installing psycopg2:
  - Type `env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip3 install psycopg2` on Mac, with Xcode developer tools and openssl.
- Problem starting Postgres:
  - Verify that Postgres is up and running, restart it and check the settings file for the correct path.



#### Website

The website can work without virtual environment. To install required node modules, run:

```
yarn install
```

To compile and run for local testing, run:

```
yarn run serve
```

To compile and create the folder for production, run:

```
yarn run build
```



#### Client code

The client code can work without virtual environment, yet requires the installation of a few additional packages. Run:

```bash
$ cd client
$ pip3 install -r requirements.txt
```

Next, edit the settings_local.py file to fit your needs. Remember that it is tied to the machine secret, therefore each test result will belong to the machine with the secret specified in the settings file.

After that, the client code is ready to execute. 

```bash
$ python3 client-code.py
```

Note that there may be issues with directories, since each system has its own defaults and permissions. If you encounter any problem, feel free to open an issue.

