import React from 'react';
import './index.css';
import ResultFilter from 'component/result-filter/index.jsx';
import BasicTable    from 'util/basic-table/index.jsx';
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
            isLoading: false,
        }

    }
    componentDidMount(){
        this.loadUserMachineManageList();
    }
    loadUserMachineManageList(){
        _user.getUserMachineManageList().then(res => {
            this.setState(res);
        }, errMsg => {
            _mm.errorTips(errMsg);
        });
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
                            <a href="\logout" className="list-group-item">
                                <i className="fa fa-arrow-left fa-fw"></i>&nbsp; Logout
                            </a>
                        </div>
                    </div>
                </div>

                <div className="col-md-9">
                    <div className="record-title">
                        <h2 >Welcome Back, {this.state.username}</h2>
                    </div>


                </div>
            </div>


        )
    }
}

export default Portal;