# Google Summer of Code 2019 - report

The 2019 Google Summer of Code project consists in working on the Develop Performance Farm Database and Website, work in progress from 2018. 

The system consists in an API root at the localhost address (127.0.0.1) which generates JSON performance files, 

The current application has been built on Python and its module Django, but is missing some features:

* Authentication/authorization tied into the community infrastructure;
* Associating test systems with users to upload results to the REST API;
* Checking if a mapping with the same name already exists (`runner.py`);
* Testing account exit appropriately (`collectd.py`);
* Collecting output of configure and making commands (`git.py`);
* API root, the OPTIONS button cannot be unclicked once clicked;
* Graphical interface improvements while viewing JSON results on the local server (i.e. adding back navigation); 
* Adding test cases of different scale sets (scale=10,20…);
* Allowing custom tests to be added;
* Website and interface fixes:
  * Improving responsivity when rescaling the window;
  * Bug fixes (popups when clicking Status/Machine without being logged in);
  * Improving design of the homepage and login form;
  * PG PERF FARM and Home redirect to the same page;
  * Contact, License and Privacy Policy pages missing;
  * There might be an issue with URLs not redirecting properly;
  * 

In the meanwhile, testing is being made with manually created accounts, 

The system is being developed using Debian 9 and OSX Mojave.



## Community bonding

#### Migrating from Python2.7 to Python3

Since Python2.7 is no longer going to be maintained in 2020, the community agrees that migrating is necessary. The latest stable version of Python is Python3.6, and Python3.7 has had some issues with older versions of Django, hence I am going to use the first if I find bugs.

The major changes encountered are:

* `import` syntax;
* `print` syntax;
* Manually compiled requirements with pip3;
* Upgraded the Django version (see below);
* Error while installing psycopg2:
  * `env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2` on Mac, with Xcode developer tools and openssl;

Changes have been added to `requirements.txt`. 

Everything works so far: migrations have no issues, yet there are a couple warnings when accessing the server from browser - I will look into that.



#### Django version

Using Django1.11 is recommended because the authentication module is on a Django application, so there might be incompatibilies. The version has nonetheless being updated from 1.11.10 to 1.11.17, since the older one has bugs concerning Python3.



#### Code specifics

*client*: contains packages with functions used to generate test results and files, with exception handling. Results are collected with Python modules which analyse hardware, system and database performance. 

*front-end*: contains HTML, CSS and JS code the website is built on.

*web*: contains testing functions, role definitions in the authentication system and parsing of the JSON file, along with conversion of existent results in a downloadable format.





