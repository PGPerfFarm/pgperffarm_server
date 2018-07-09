import React from 'react';
// import './index.css';
import {Table, Divider, Segment, Icon} from 'semantic-ui-react'
import FarmerDetailCard      from 'component/farmer-detail-card/index.jsx'
import Record      from 'service/record-service.jsx'
import PGUtil        from 'util/util.jsx'
import MachineRecordTable from 'util/machine-record-table/index.jsx'
const _util = new PGUtil();
const _record = new Record();
class MachineInfo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            machineNo: this.props.match.params.machine_sn,
            machineInfo: {},
            isLoading: false,
            currentPage: 1,
            total:3,
            filter: {},
            list: [
            ]
        },
        console.dir(this.props.match.params)
        this.onPageChange = this.onPageChange.bind(this);
        this.handleApplyBtnClick = this.handleApplyBtnClick.bind(this);
        this.loadHistoryRecordList = this.loadHistoryRecordList.bind(this);
    }

    componentDidMount() {
        this.loadHistoryRecordList();
    }

    handleApplyBtnClick(params) {
        console.log('handle apply!')

        let self = this
        this.setState({filter: params}, ()=> {
            self.loadRecordList()
        });
    }

    // load history record list
    loadHistoryRecordList() {
        let _this = this;
        let listParam = {};
        // listParam= this.state.filter;
        // listParam.page = page;
        listParam.machine_sn = this.state.machineNo;
        _record.getHistoryRecordList(listParam).then(res => {
            console.log('res is:' + res)
            this.setState({
                machineInfo: res.machine_info || {},
                list: res.reports || [],
                // total: res.count,
                isLoading: false
            });
            // _this.changeIsLoading(false);
        }, errMsg => {
            this.setState({
                list: []
            });
            _util.errorTips(errMsg);

            console.log(errMsg)
            _this.changeIsLoading(false);
        });

        console.log(this.state.list)
    }

    onPageChange(page) {
        console.log(page);
        console.log(this);
        this.setState({
            current: page,
        });
    }

    render() {
        let show = this.state.isLoading ? "none" : "block";
        let style = {
            display: show
        };

        return (
            <div className="container-fluid detail-container">
                <div className="record-title">

                    <div className="record-title-top">
                        <span>NO: {this.state.machineNo}</span>
                        {/*<span>Add Date: {this.state.machineInfo.addtime}</span>*/}
                    </div>
                    <h2 >Farmer: {this.state.machineInfo.alias}</h2>
                </div>

                <div className="machine-info-divier-div">
                    <div className="blank"></div>
                    <Divider className="machine-info-divier"></Divider>
                </div>
                <div className="col-md-3">
                    <Segment vertical>Farmer Info</Segment>
                    <FarmerDetailCard machine={this.state.machineInfo}></FarmerDetailCard>
                </div>

                <div className="col-md-9">
                    {/*<div className="card-container row">*/}

                    <div className="info-container col-md-12 col-md-offset-1">
                        <MachineRecordTable list={this.state.list} total={this.state.total} current={this.state.currentPage} loadfunc={this.loadRecordList}/>
                    </div>

                </div>
            </div>
        )
    }
}

export default MachineInfo;