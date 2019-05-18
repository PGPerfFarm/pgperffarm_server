# Google Summer of Code 2019 - report

Introduction - todo





## Community bonding

#### Migrating from Python2.7 to Python3

Since Python2.7 is no longer going to be maintained in 2020, the community agrees that migrating is necessary. The latest stable version of Python is Python3.6, and Python3.7 has had some issues with older versions of Django, hence I am going to use the first.

The major changes encountered are:

* `import` syntax;
* Manually compiled requirements with pip3;
* Upgraded the Django version (see below);
* General syntax changes (WIP);
* Error while installing psycopg2:
  * `env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2` on Mac, with Xcode developer tools and openssl;

Changes have been added to `requirements.txt`. 

TODO: continue making migrations using Python3.6, debugging and fixing the code.



#### Django version

Using Django1.11 is recommended because the authentication module is on a Django application, so there might be incompatibilies. The version has nonetheless being updated from 1.11.10 to 1.11.17, because the older one has bugs concerning Python3.



## 

