import React        from 'react';
import {Link}     from 'react-router-dom';

import './index.css';
import slonik from 'image/slonik.png'


class NavTop extends React.Component {
    constructor(props) {
        super(props);
    }

    // log out
    onLogout() {
        //todo
    }

    render() {
        return (
            <div className="navbar navbar-default top-navbar" role="navigation">
                <div className="navbar-header">
                    {/*<button type="button" className="navbar-toggle" data-toggle="collapse" data-target=".sidebar-collapse">*/}
                    {/*<span className="sr-only">Toggle navigation</span>*/}
                    {/*<span className="icon-bar"></span>*/}
                    {/*<span className="icon-bar"></span>*/}
                    {/*<span className="icon-bar"></span>*/}
                    {/*</button>*/}
                    <a className="navbar-brand" href="index.html"><img src={require('image/slonik.png')}/><b>PG Perf
                        Farm</b></a>
                </div>
                <ul className="nav navbar-top-links navbar-left">
                    <li><a href="/home"> <span className="glyphicon glyphicon-home" aria-hidden="true"></span> Home</a>
                    </li>
                    <li><a href="/status"> <span className="glyphicon glyphicon-tasks" aria-hidden="true"></span> Status</a>
                    </li>
                    <li><a href="#"> <span className="glyphicon glyphicon-blackboard" aria-hidden="true"></span>Machine</a>
                    </li>

                    <li className="dropdown">
                        <a className="dropdown-toggle" data-toggle="dropdown" href="#" aria-expanded="false">
                            <span className="glyphicon glyphicon-th-large" aria-hidden="true"></span> Help
                            <span className="glyphicon glyphicon-menu-down" aria-hidden="true"></span>
                        </a>
                        <ul className="dropdown-menu dropdown-alerts">
                            <li className="divider"></li>
                            <li>
                                <a href="#">
                                    <div>
                                        <i className="fa fa-envelope fa-fw"></i> Contact
                                        {/*<span className="pull-right text-muted small">4 min</span>*/}
                                    </div>
                                </a>
                            </li>
                            <li className="divider"></li>
                            <li>
                                <a href="#">
                                    <div>
                                        <i className="fa fa-tasks fa-fw"></i>  Licence
                                        {/*<span className="pull-right text-muted small">4 min</span>*/}
                                    </div>
                                </a>
                            </li>
                            <li className="divider"></li>
                            <li>
                                <a href="#">
                                    <div>
                                        <i className="fa fa-upload fa-fw"></i>  Privacy Policy
                                        {/*<span className="pull-right text-muted small">4 min</span>*/}
                                    </div>
                                </a>
                            </li>
                            <li className="divider"></li>
                            {/*<li>*/}
                                {/*<a className="text-center" href="#">*/}
                                    {/*<strong>See All Alerts</strong>*/}
                                    {/*<i className="fa fa-angle-right"></i>*/}
                                {/*</a>*/}
                            {/*</li>*/}
                        </ul>

                    </li>

                </ul>


                <ul className="nav navbar-top-links navbar-right">

                    <li className="dropdown sign-in">
                        <a className="dropdown-toggle" data-toggle="dropdown" href="#" aria-expanded="false">
                            Sign in
                        </a>

                    </li>

                </ul>
            </div>
        );
    }
}


export default NavTop;