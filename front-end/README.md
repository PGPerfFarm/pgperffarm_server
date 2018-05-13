# PostgreSql Performance Farm 

The PostgreSQL Performance Farm project is a community project to collect performance data from tests as code changes are made to PostgreSQL. To support this effort, a database needs to be created for storing results, and a Web site developed to review results. This project will focus on developing the Web site on top of the database.
The database will be using PostgreSQL in the back-end. Test results will come in the form of JSON and flat files. The Web application will be developed using the Django Web framework.

### Installing Yarn

Read the [Installation Guide](https://yarnpkg.com/en/docs/install) on our website for detailed instructions on how to install Yarn.

#### Develop

Webpack auto-watches client assets.

```
yarn install
yarn run dev
```

#### Build

Bundle the assets for production.

```
```