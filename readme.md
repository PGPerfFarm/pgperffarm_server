# PostgreSQL Performance Farm

This repository contains the code for the PostgreSQL Performance Farm.

IMPORTANT: migrating from Python2 to Python3 is in progress, hence why code might not work - for any issues feel free to contact @ila at ilaria.battiston@gmail.com

----

#### Configuration

```bash
refs/remotes/origin/masterweb/
```

The web/ directory contains the Django application that forms the basis of the website. In order to run the site, you will need to setup a Python `virtualenv`, e.g:

```bash
$ sudo pip install virtualenvwrapper
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
$ PATH=$PATH:/usr/local/pgsql/bin pip install -r web/requirements.txt
```

Next, create a `settings_local.py` file::

```bash
$ cp web/pgperffarm/settings_local.py.in web/pgperffarm/settings_local.py
```

Edit the file and change the database configuration and other settings to suit your environment. Make sure you create the required database and user account on your PostgreSQL server.

Finally, synchronise the database:

```bash
$ cd web
$ python manage.py makemigrations
$ python manage.py migrate
```

That should be all. To test, run the following command and point a browser at the URL shown:

```bash
$ python manage.py runserver
```

You should see the index page of the application.