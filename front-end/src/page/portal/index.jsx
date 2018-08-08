import React from 'react';
import {Link}     from 'react-router-dom';
import './index.css';
import MachineTable    from 'util/machine-table/index.jsx';
import UserInfoCard from 'component/userinfo-card/index.jsx'
import Record      from 'service/record-service.jsx'
import PGUtil        from 'util/util.jsx'
import User         from 'service/user-service.jsx'
const _user = new User();

const _util = new PGUtil();
const _record = new Record();
class Portal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            machines:[],
            userinfo: {}
        }
        this.loadUserMachineManageList = this.loadUserMachineManageList.bind(this);
    }
    componentDidMount(){

        let user = _util.getStorage('userInfo')
        this.setState({
            username: user.username,
        },()=>{
            this.loadUserPortalInfo()
            this.loadUserMachineManageList();
        });
        console.log(user.token)

    }

    loadUserPortalInfo(){
        let username = this.state.username
        _user.getUserPortalInfo(username).then(res => {
            this.setState({
                userinfo: res,
            });
        }, errMsg => {
            _util.errorTips(errMsg);
        });
    }

    loadUserMachineManageList(page=1){

        let listParam = {};
        listParam.page = page;
        listParam.machine_owner__username = this.state.username;
        _user.getUserMachineManageList(listParam).then(res => {
            this.setState({
                machines: res.results,
                total: res.count,
            });
        }, errMsg => {
            _util.errorTips(errMsg);
        });
    }
    onLogout(){
        _util.removeStorage('userInfo');
        // this.props.history.push('/login')
        // hashHistory.push('/login')
        window.location.href = '/';
    }

    render() {
        return (
            <div className="container-fluid detail-container">

                <div className="col-md-3">

                    {/*<Segment vertical>Farmer Info</Segment>*/}
                    <UserInfoCard userinfo={this.state.userinfo}></UserInfoCard>

                    <div className="panel panel-default panel-blue">
                        <div className="panel-heading">
                            <h3 className="panel-title">
                                <i className="fa fa-bookmark"></i>&nbsp; Shortcuts
                            </h3>
                        </div>
                        <div className="list-group">
                            <Link target='_blank'  to="farmerApply/" className="list-group-item">
                                <i className="fa fa-globe fa-fw"></i>&nbsp; Add a New Mchine
                            </Link>

                            <a onClick={() => {this.onLogout()}} className="list-group-item">
                                <i className="fa fa-arrow-left fa-fw"></i>&nbsp; Logout
                            </a>
                        </div>
                    </div>
                </div>

                <div className="col-md-9">
                    <div className="record-title">
                        <h2 >Welcome Back, {this.state.username}</h2>
                    </div>

                    <MachineTable list={this.state.machines} total={this.state.total} current={this.state.currentPage} loadfunc={this.loadUserMachineManageList}/>
                </div>
            </div>


        )
    }
}

export default Portal;