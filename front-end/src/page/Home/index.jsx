import React from 'react';
import './index.scss';

class Home extends React.Component{
    render(){
        return (
            <div id="page-wrapper" className="jumbotron">
                <h1>Hello, world!</h1>
                <p>
                    The PostgreSQL Performance Farm project is a community project to collect performance data from tests as code changes are made to PostgreSQL. To support this effort, a database needs to be created for storing results, and a Web site developed to review results.
                    This project will focus on developing the Web site on top of the database.
                    The database will be using PostgreSQL in the back-end. Test results will come in the form of JSON and flat files. The Web application will be developed using the Django Web framework.
                </p>
                <p>
                    As an example, the PostgreSQL Build Farm site is a central repository for the results of testing source code changes for PostgreSQL as they occur, on a wide variety of platforms.
                </p>

                {/*<button className="btn btn-warning">test</button>*/}
            </div>
        )
    }
}

export default Home;