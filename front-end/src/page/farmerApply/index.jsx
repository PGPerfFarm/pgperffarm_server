import React from 'react';
import {hashHistory} from 'React-router'
import './index.css';
import {Link}     from 'react-router-dom';
import UserInfoCard from 'component/userinfo-card/index.jsx'
import Record      from 'service/record-service.jsx'
import PGUtil        from 'util/util.jsx'
import User         from 'service/user-service.jsx'
import PGConstant from 'util/constant.jsx'

const _user = new User();

const _util = new PGUtil();
const _record = new Record();
class FarmerApply extends React.Component {
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
        let _this = this
        this.setState({
            username: user.username,
        },()=>{
            _this.loadUserPortalInfo()
            _this.loadUserMachineManageList();
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
            _util.errorTips('Please make sure no fields are empty.');
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

    onInputChange(e) {
        let inputValue = e.target.value,
            inputName = e.target.name;
        this.setState({
            [inputName]: inputValue
        });
    }

    onInputKeyUp(e) {
        if (e.keyCode === 13) {
            this.onSubmit();
        }
    }

    onSubmit() {
        // alert(1)
        let machineInfo = {
            os_name: this.state.os_name,
            os_version: this.state.os_version,
            comp_name: this.state.comp_name,
            comp_version: this.state.comp_version,
            machine_owner:this.state.username
        }
        let checkResult = true
        // check success
        if (checkResult) {
            _user.farmerApply(machineInfo).then((res) => {
                // console.dir(res)
                alert('add machine success!')
                hashHistory.push('/portal')
                // window.location.href = this.state.redirect;
            }, (err) => {
                // console.log(err)
                if (PGConstant.AuthorizedErrorCode === err) {
                    _util.errorTips('username or password is mistake!');
                }else{
                    _util.errorTips('login fail');
                }
            });
        }
        // check failure
        else {

            _util.errorTips(checkResult.msg);
        }

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

                    <div className="panel panel-default">
                        <div className="panel-heading">
                            Apply New Machines
                        </div>
                        <div className="panel-body">
                            <div className="row">
                                {/*<!-- /.col-lg-6 (nested) -->*/}
                                <div className="col-lg-12">
                                    {/*<h4>Login Form</h4>*/}
                                    <form role="form">
                                        <div className="form-group input-group">
                                            {/*<label className="control-label" for="inputLogin"> login input</label>*/}
                                            <span class="input-group-addon">system name</span>
                                            <input type="text" className="form-control" id="inputOSName"
                                                   placeholder="etc.Debian,Ubuntu"
                                                   name="os_name"
                                                   onKeyUp={e => this.onInputKeyUp(e)}
                                                   onChange={e => this.onInputChange(e)}/>
                                        </div>
                                        <div className="form-group input-group">
                                            <span class="input-group-addon">system version</span>
                                            <input type="text" className="form-control" id="inputOSVersion"
                                                   name="os_version"
                                                   placeholder="etc.9,14.4" onKeyUp={e => this.onInputKeyUp(e)}
                                                   onChange={e => this.onInputChange(e)}/>
                                        </div>
                                        <div className="form-group input-group">
                                            <span class="input-group-addon">arch name</span>
                                            <input type="text" className="form-control" id="inputCampName"
                                                   name="comp_name"
                                                   placeholder="etc.x86" onKeyUp={e => this.onInputKeyUp(e)}
                                                   onChange={e => this.onInputChange(e)}/>
                                        </div>
                                        <div className="form-group input-group">
                                            <span class="input-group-addon">arch version</span>
                                            <input type="text" className="form-control" id="inputCampVersion"
                                                   name="comp_version"
                                                   placeholder="etc.64" onKeyUp={e => this.onInputKeyUp(e)}
                                                   onChange={e => this.onInputChange(e)}/>
                                        </div>
                                        <button type="button" className="btn btn-primary"  onClick={e => {this.onSubmit(e)}}>Submit</button>
                                    </form>
                                </div>
                                {/*<!-- /.col-lg-6 (nested) -->*/}
                            </div>
                            {/*<!-- /.row (nested) -->*/}
                        </div>
                        {/*<!-- /.panel-body -->*/}
                    </div>
                </div>
            </div>


        )
    }
}

export default FarmerApply;