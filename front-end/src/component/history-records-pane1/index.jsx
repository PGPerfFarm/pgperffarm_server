import React from 'react';
import Pagination from 'util/pagination/index.jsx';
import {Tab, Divider, Icon, Label} from 'semantic-ui-react'

import MachineRecordTable from 'util/machine-record-table/index.jsx'
import Record      from 'service/record-service.jsx'
import PGUtil        from 'util/util.jsx'

const _util = new PGUtil();
const _record = new Record();
import './index.css';

class HistoryRecordPane1 extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            currentList: [],
            currentTotal: 0,
            currentPage:1,
            machine_sn: props.machine_sn || '',
            branches: props.branches,
            selected_branch: props.branches[0].value,
        }
        // console.dir(this.state.branches)
        this.loadMachineRecordListByBranch = this.loadMachineRecordListByBranch.bind(this);
        // this.loadMachineRecordListByBranch
    }

    componentDidMount() {
        // console.log(this.state.branches[0].value)
        this.loadMachineRecordListByBranch()
    }
    componentWillReceiveProps(nextProps) {
        let _this = this
        this.setState({
            branches: nextProps.branches,
            machine_sn: nextProps.machine_sn,
        },() => {
            if(this.state.branches.length > 0) {
                _this.handleBranchTagClick(_this.state.branches[0].value)
            }

        });
    }
    handleBranchTagClick(branch_id){
        console.log('new reload branch is: ' + branch_id)

        this.setState({
            selected_branch: branch_id,
        },() => {
            this.loadMachineRecordListByBranch()
        });

    }

    // load record list
    loadMachineRecordListByBranch(page=1) {
        let _this = this;
        let listParam = {};

        listParam.page = page;
        listParam.test_machine__machine_sn = this.state.machine_sn;
        listParam.branch__id = this.state.selected_branch;
        if(listParam.branch__id <= 0) {
            return;
        }
        _record.getMachineRecordListByBranch(listParam).then(res => {
            _this.setState({
                currentList: res.results,
                currentTotal: res.count,
                isLoading: false
            });
        }, errMsg => {
            _this.setState({
                curentList: []
            });
            _util.errorTips(errMsg);

            console.log(errMsg)
        });

        console.log(this.state.list)
    }

    render(){
        let _list = this.state.branches || [];
        console.log('list is')
        console.dir(_list)
        let branch_tags = _list.map((branchItem, index) => {
            let className = branchItem.value == this.state.selected_branch ? 'active_branch' : '';
            return (
                <Label className={className} onClick={() => this.handleBranchTagClick(branchItem.value)}>
                    <Icon name='usb' />{branchItem.branch}
                </Label>
            );
        });



        return (
            <div>
                <div className="branch-tags-container">
                    {branch_tags}
                    {/*<div>*/}
                        {/*current num: {this.state.currentTotal}*/}
                    {/*</div>*/}
                </div>

                    <MachineRecordTable list={this.state.currentList} total={this.state.currentTotal} current={this.state.currentPage} loadfunc={this.loadMachineRecordListByBranch}/>

            </div>
        );
    }
}

export default HistoryRecordPane1;