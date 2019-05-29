import React from 'react';
import './index.scss';

class Home extends React.Component{
    render(){
        return (
            <div id="page-wrapper" className="jumbotron">
                <h1>PostgreSQL Performance Farm</h1>
                <p>
                    The PostgreSQL Performance Farm project is a community project to collect performance data from tests, as code changes are made to PostgreSQL. Test results come as JSON or flat files, and the server-side interface is deployed using the Django framework.
                </p>
                <p>
                    This website enables registered users to upload, browse and download test results for all machines.
                </p>

                {/*<button className="btn btn-warning">test</button>*/}
            </div>
        )
    }
}

export default Home;
