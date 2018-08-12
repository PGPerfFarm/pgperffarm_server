import React from 'react';
// import './index.css';
import {Tab, Divider, Segment, Icon} from 'semantic-ui-react'
import FarmerDetailCard      from 'component/farmer-detail-card/index.jsx'
import Record      from 'service/record-service.jsx'
import PGUtil        from 'util/util.jsx'
import HistoryRecordsPane1 from 'component/history-records-pane1/index.jsx'

const _util = new PGUtil();
const _record = new Record();
class MachineInfo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            machineNo: this.props.match.params.machine_sn,
            branches: [
                {'branch':0,'value':0}
            ],
            machineInfo: {},
            isLoading: false,
            currentPage: 1,
            total:3,
            filter: {},
            list: [
            ]
        },
        // console.dir(this.props.match.params)
        // this.onPageChange = this.onPageChange.bind(this);
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
            console.log('res is:')
            console.dir(res)
            this.setState({
                branches: res.branches || [],
                machineInfo: res.machine_info || {},
                list: res.reports || [],
                // total: res.count,
                isLoading: false
            }, ()=> {
                console.log(this.state.branches);
                // 123
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

    render() {
        // let branches = this.state.branches;
        let panes = [
            { menuItem: 'Review By Branches', render: () => <Tab.Pane attached={true}><HistoryRecordsPane1 machine_sn={this.state.machineInfo.machine_sn} branches={this.state.branches}/></Tab.Pane> },
        ]

        return (
            <div className="container-fluid detail-container">
                <div className="record-title">
                    <div className="record-title-right title-flex">
                        <div className="record-title-top">
                            <span>NO: {this.state.machineNo}</span>
                            {/*<span>Commit: <a target="_blank" href={ PGConstant.PG_GITHUB_MIRROR + commit}>{commit.substring(0, 7)}</a></span>*/}
                        </div>
                        <div className="record-title-bottom">
                            <h2 >Farmer: {this.state.machineInfo.alias}</h2>
                        </div>
                    </div>
                    {/*<div className="record-title-left title-flex">*/}
                        {/*<span>Date joined: {this.state.machineInfo.add_time}</span>*/}
                    {/*</div>*/}
                </div>

                <div className="machine-info-divier-div">
                    <div className="blank"></div>
                    <Divider className="machine-info-divier"></Divider>
                </div>
                <div className="col-md-3">
                    {/*<Segment vertical>Farmer Info</Segment>*/}
                    <FarmerDetailCard machine={this.state.machineInfo} branch_num={this.state.branches.length}></FarmerDetailCard>
                </div>

                <div className="col-md-9">
                    {/*<div className="card-container row">*/}

                    {/*<div className="info-container col-md-12 col-md-offset-1">*/}
                        {/*<MachineRecordTable list={this.state.list} total={this.state.total} current={this.state.currentPage} loadfunc={this.loadRecordList}/>*/}


                        <Tab menu={{pointing: true }} panes={panes} />
                    {/*</div>*/}

                </div>
            </div>
        )
    }
}

export default MachineInfo;