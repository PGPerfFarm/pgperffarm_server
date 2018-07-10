import React from 'react';
import Pagination from 'util/pagination/index.jsx';
import {Tab, Divider, Icon, Label} from 'semantic-ui-react'

import MachineRecordTable from 'util/machine-record-table/index.jsx'
import PGUtil        from 'util/util.jsx'
const _util = new PGUtil();
import './index.css';

class HistoryRecordPane1 extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            list: [],
            branches: props.branches || [],
            selected_branch: '',
            restoreNum: 0,
            selected: [{
                'cate': 'Category 1',
                'index': 0,
                'key': 'date',
                'data': [
                    {'name': 'All', 'value': ''},
                    {'name': '7 days', 'value': '7'},
                    {'name': '30 days', 'value': '30'}
                ],
            }],
        }
        console.log('br')
        console.dir(this.state.branches)
    }

    componentDidMount() {
        // this.loadHistoryRecordList();
    }
    componentWillReceiveProps(nextProps) {
        this.setState({branches: nextProps.branches});
    }
    reloadRecordTable(branch_id){
        console.log('new reload branch is: ' + branch_id)
    }


    render(){
        let _list = this.state.branches || [];
        console.log('list is')
        console.dir(_list)
        let branch_tags = _list.map((branchItem, index) => {
            return (
                <Label onClick={() => this.reloadRecordTable(branchItem.value)}>
                    <Icon name='usb' />{branchItem.branch}
                </Label>
            );
        });



        return (
            <div>
                <div className="branch-tags-container">
                    {branch_tags}
                </div>

                    <MachineRecordTable list={this.state.list} total={this.state.total} current={this.state.currentPage} loadfunc={this.loadRecordList}/>

            </div>
        );
    }
}

export default HistoryRecordPane1;