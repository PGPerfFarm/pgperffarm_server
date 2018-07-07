import React from 'react';

import NavTop from 'component/nav-top/index.jsx';
// import './index.css';
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

                    <div className="panel-heading">
                        <h3 className="panel-title">
                            <i className="fa fa-user"></i>&nbsp; Your Info
                        </h3>
                    </div>
                    <div className="panel-body">
                        <p><strong>{userinfo.username}</strong></p>
                        <ul className="panel-body-ul">
                            <li><i className="fa fa-desktop fa-fw"></i> {userinfo.machine_num} machine(s)</li>
                            <li><i className="fa fa-file fa-fw"></i> {userinfo.reports} report(s)</li>
                            <li><i className="fa fa-code-fork fa-fw"></i> {userinfo.branches} branch(es) involved</li>
                            <li><i className="fa fa-envelope-o fa-fw"></i> <a href={'mailto' + userinfo.email}></a>{userinfo.email}</li>
                        </ul>
                    </div>
                    {/*<div className="panel-footer clearfix">*/}
                    {/*</div>*/}
                </div>
            </div>
        );
    }
}export default UserInfoCard;

