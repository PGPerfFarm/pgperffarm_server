import React from 'react';
import './index.css';
import ResultFilter from 'component/result-filter/index.jsx';
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
            isLoading: false,
            machines:[],
            userinfo: {}
        }

    }
    componentDidMount(){
        let user = _util.getStorage('userInfo')
        this.setState({
            username: user.username,
        });
        console.log(user.token)
        this.loadUserMachineManageList();
    }

    loadUserInfo(){
        _user.getUserInfo().then(res => {
            this.setState({
                userinfo: res.userinfo,
            });
        }, errMsg => {
            _util.errorTips(errMsg);
        });
    }

    loadUserMachineManageList(page=1){
        _user.getUserMachineManageList().then(res => {
            this.setState({
                machines: res.results,
                total: res.count,
                isLoading: false
            });
        }, errMsg => {
            _util.errorTips(errMsg);
        });
    }
    onLogout(){
        _util.removeStorage('userInfo');
        window.location.href = '/login';
        // _user.logout().then(res => {
        //     _util.removeStorage('userInfo');
        //     window.location.href = '/login';
        // }, errMsg => {
        //     _util.errorTips(errMsg);
        // });
    }

    render() {
        let show = this.state.isLoading ? "none" : "block";
        let style = {
            display: show
        };

        return (
            <div className="container-fluid detail-container">

                <div className="col-md-3">

                    {/*<Segment vertical>Farmer Info</Segment>*/}
                    <UserInfoCard info={this.state.userinfo}></UserInfoCard>

                    <div className="panel panel-default panel-blue">
                        <div className="panel-heading">
                            <h3 className="panel-title">
                                <i className="fa fa-bookmark"></i>&nbsp; Shortcuts
                            </h3>
                        </div>
                        <div className="list-group">
                            <a href="\add-machine" className="list-group-item">
                                <i className="fa fa-globe fa-fw"></i>&nbsp; Add a New Mchine
                            </a>
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

                    <MachineTable list={this.state.machines} total={this.state.total} current={this.state.currentPage} loadfunc={this.loadRecordList}/>
                </div>
            </div>


        )
    }
}

export default Portal;