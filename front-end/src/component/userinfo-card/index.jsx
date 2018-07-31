import React from 'react';

import NavTop from 'component/nav-top/index.jsx';
import './index.css';
import {Image, Card, Button, List, Icon} from 'semantic-ui-react'
class UserInfoCard extends React.Component {
    constructor(props){
        super(props);
    }
    render(){
        let userinfo = this.props.userinfo || {}

        return (

            <div className="farmer-card">
                <div className="userinfo-panel panel panel-default panel-blue">

                    <div className="panel-heading userinfo-panel-heading">
                        <div>
                            <h3 className="panel-title">
                                <i className="fa fa-user"></i>&nbsp; Your Info
                            </h3>
                            <span className="panel-report-num">
                                name: Maleic Acid
                            </span>
                        </div>

                        <div>
                            <img className="user-avatar" src="http://s.gravatar.com/avatar/6ccc9d4e8fc9f75d253b5a28e05c11b8" alt=""/>

                        </div>
                    </div>
                    <div className="panel-body userinfo-panel-body">
                        <p><strong>{userinfo.username}</strong></p>
                        <ul className="panel-body-ul">
                            <li><i className="fa fa-desktop fa-fw"></i> {userinfo.machine_num}4 machine(s)</li>
                            <li><i className="fa fa-file fa-fw"></i> {userinfo.reports}5 report(s)</li>
                            <li><i className="fa fa-code-fork fa-fw"></i> {userinfo.branches}2 branch(es) involved</li>
                            <li><i className="fa fa-envelope-o fa-fw"></i> <a href="mailto:mahongyuan1997@gmail.com">mahongyuan@gmail.com</a></li>
                        </ul>
                    </div>
                    <div className="panel-footer clearfix">
                    </div>
                </div>
            </div>
        );
    }
}export default UserInfoCard;

