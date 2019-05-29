import React        from 'react';
import {Link}     from 'react-router-dom';

import './index.css';
import slonik from 'image/slonik.png'
import PGUtil    from 'util/util.jsx'
const _util = new PGUtil();
import User         from 'service/user-service.jsx'
const _user = new User();

class NavTop extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            // username: _util.getStorage('userInfo').username || '',
            userinfo: _util.getStorage('userInfo')|| {},
            isLoggedIn: true
        }
    }

    // logout
    onLogout() {
        _util.removeStorage('userInfo');
        window.location.href = '/login';
    }

    componentWillMount(){
        this.setState({
            isLoggedIn: this.isLoggedIn(),
        });
    }

    isLoggedIn() {
        if(this.state.userinfo.token){
            return true;
        }
        return false;
    }

    render() {
        let isLoggedIn = this.state.isLoggedIn;

        let button = null;
        if (isLoggedIn) {
            button = <li className="dropdown loggedin">
                <a className="dropdown-toggle" data-toggle="dropdown" href="#" aria-expanded="false">
                    <img className="img-circle img-thumbnail user-head-pic" src={require('image/slonik.png')}
                         alt="headPic"/>
                </a>
                <ul className="dropdown-menu dropdown-alerts loggedin-ul">
                    <li>
                        <Link to="/portal">
                            <div>
                                <i className="fa fa-tasks fa-fw"></i> My machines
                            </div>
                        </Link>
                    </li>
                    <li className="divider"></li>
                    <li>
                        <a onClick={() => {this.onLogout()}}>
                            <div>
                                <i className="fa fa-upload fa-fw"></i> Log out
                            </div>
                        </a>
                    </li>
                    <li className="divider"></li>
                </ul>
            </li>;
        } else {
            button = <li className="dropdown sign-in">
                <Link to="/login" aria-expanded="false">
                    Log in
                </Link>
            </li>;
        }

        return (
            <div className="navbar navbar-default top-navbar" role="navigation">
                <div className="navbar-header">

                    <a className="navbar-brand" href="index.html"><img src={require('image/slonik.png')}/><b>PG Perf
                        Farm</b></a>
                </div>
                <ul className="nav navbar-top-links navbar-left">
                    <li><Link to="/home"> <span className="glyphicon glyphicon-home" aria-hidden="true"></span>
                        Home</Link>
                    </li>
                    <li><Link to="/status"><span className="glyphicon glyphicon-tasks" aria-hidden="true"></span>Status</Link>
                    </li>

                    <li><Link to="/machine"> <span className="glyphicon glyphicon-blackboard" aria-hidden="true"></span>Machine</Link>
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
                                        <i className="fa fa-tasks fa-fw"></i> License
                                        {/*<span className="pull-right text-muted small">4 min</span>*/}
                                    </div>
                                </a>
                            </li>
                            <li className="divider"></li>
                            <li>
                                <a href="/ppolicy">
                                    <div>
                                        <i className="fa fa-upload fa-fw"></i> Privacy Policy
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
                    {button}
                </ul>
            </div>
        );
    }
}


export default NavTop;