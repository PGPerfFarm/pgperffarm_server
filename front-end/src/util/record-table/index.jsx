import React from 'react';
import {Link}     from 'react-router-dom';
import {Icon, Table, Label, Message, Button} from 'semantic-ui-react'
import Pagination from 'util/pagination/index.jsx'
import Record      from 'service/record-service.jsx'
import './index.css';
const _record = new Record();
function Bubble(props) {

    if (props.num <= 0) {
        return null;
    }
    let className = props.name + 'IconClassName';
    return (
        <Label circular size="mini" className={"mini-label " + className}>
            {props.num}
        </Label>
    );
}

//todo
// function TrendCell(trend) {
//     const isNull = !list;
//     const isEmpty = !isNull && !list.length;
//     let improvedIconClassName = trend.improved > 0 ? 'improved' : 'anonymous'
//     let quoIconClassName = trend.quo > 0 ? 'quo' : 'anonymous'
//     let regressiveIconClassName = trend.regressive > 0 ? 'regressive' : 'anonymous'
//     if (!trend.is_first) {
//         return (
//             <Table.Cell  textAlign='center'>
//                 first report
//             </Table.Cell>
//         );
//     } else {
//         return (
//             <div>
//                 <Table.Cell textAlign='center'>
//                     <Icon className={"bgc-clear " + improvedIconClassName} name='smile outline' size='large'/>
//                     <Bubble num={trend.improved} name="improved"/>
//                 </Table.Cell>
//                 <Table.Cell textAlign='center'>
//                     <Icon className={"bgc-clear " + quoIconClassName} name='meh outline' size='large'/>
//                     <Bubble num={trend.quo} name="quo"/>
//                 </Table.Cell>
//                 <Table.Cell textAlign='center'>
//                     <Icon className={"bgc-clear " + regressiveIconClassName} name='frown outline'
//                           size='large'/>
//                     <Bubble num={trend.regressive} name="regressive"/>
//                 </Table.Cell>
//             </div>
//         );
//     }
//
// }

// general basic table
class RecordTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            branch: this.props.branch,
            isFirstLoading: true,
            total: this.props.total,
            currentPage: 1,
            list: []
        }
    }

    componentWillMount() {
        this.loadRecordListByBranch(this.state.branch);
    }
    loadRecordListByBranch(branch,page=1) {
        let _this = this;
        let listParam = {};
        listParam.page = page;
        listParam.branch = branch;

        _record.getRecordListByBranch(listParam).then(res => {
            console.log('branch res is:' + res)
            this.setState({
                list: res.results,
                total: res.count,
                isLoading: false
            });
        }, errMsg => {
            this.setState({
                list: []
            });
            _util.errorTips(errMsg);
            console.log(errMsg)
        });

        console.log(this.state.list)
    }
    onPageNumChange(current) {
        let _this = this
        this.setState({
            currentPage: current
        }, () => {
            this.loadRecordListByBranch(_this.state.branch,current);
        });
        console.log('current:' + this.state.currentPage)
    }

    render() {
        // let branch = record.pg_info.pg_branch;
        let _list = this.state.list || []
        let style = {
            display: 'show'
        };
        let listBody = _list.map((record, index) => {
            let machine = record.machine_info[0];
            let system = machine.os_name + ' ' + machine.os_version + ' ' + machine.comp_name + ' ' + machine.comp_version;
            let alias = machine.alias;


            let trend = record.trend
            let improvedIconClassName = trend.improved > 0 ? 'improved' : 'anonymous'
            let quoIconClassName = trend.quo > 0 ? 'quo' : 'anonymous'
            let regressiveIconClassName = trend.regressive > 0 ? 'regressive' : 'anonymous'
            return (

                <Table.Row key={index}>
                    {/*alias*/}
                    <Table.Cell><a href="#">{alias}</a></Table.Cell>

                    {/*system*/}
                    <Table.Cell><a href="#">{system}</a></Table.Cell>

                    {/*branch*/}
                    {/*<Table.Cell>{branch}</Table.Cell>*/}

                    {/*trending-data*/}

                    <Table.Cell textAlign='center'>
                        <Icon className={"bgc-clear " + improvedIconClassName} name='smile outline' size='large'/>
                        <Bubble num={trend.improved} name="improved"/>
                    </Table.Cell>
                    <Table.Cell textAlign='center'>
                        <Icon className={"bgc-clear " + quoIconClassName} name='meh outline' size='large'/>
                        <Bubble num={trend.quo} name="quo"/>
                    </Table.Cell>
                    <Table.Cell textAlign='center'>
                        <Icon className={"bgc-clear " + regressiveIconClassName} name='frown outline'
                              size='large'/>
                        <Bubble num={trend.regressive} name="regressive"/>
                    </Table.Cell>


                    <Table.Cell textAlign='center'>
                        <Link color='linkedin' to={'detailInfo/' + record.uuid}>
                            <Icon name='linkify'/> Link
                        </Link>
                    </Table.Cell>


                    {/*date*/}
                    <Table.Cell>{record.add_time}</Table.Cell>
                </Table.Row>
            );
        });

        return (
            <Table celled structured compact textAlign='center'>
                <Table.Header>
                    {/*<Table.Row>*/}
                        {/*<Table.HeaderCell rowSpan='9'>Branch: {this.state.branch}</Table.HeaderCell>*/}
                    {/*</Table.Row>*/}
                    <Table.Row>
                        <Table.HeaderCell rowSpan='2'>Alias</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>System</Table.HeaderCell>
                        {/*<Table.HeaderCell rowSpan='2'>Branch</Table.HeaderCell>*/}
                        <Table.HeaderCell colSpan='3'>Trending</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>Detail</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>Date</Table.HeaderCell>
                    </Table.Row>
                    <Table.Row>
                        <Table.HeaderCell>improvement</Table.HeaderCell>
                        <Table.HeaderCell>status quo</Table.HeaderCell>
                        <Table.HeaderCell>regression</Table.HeaderCell>
                    </Table.Row>

                </Table.Header>

                <Table.Body>
                    {listBody}
                </Table.Body>
                <Table.Footer>
                    <Table.Row>
                        <Table.HeaderCell colSpan='10'>
                            <Pagination style={style} onChange={(current) => this.onPageNumChange(current)} pageSize={2}
                                        current={this.state.currentPage} total={this.state.total}/>

                        </Table.HeaderCell>

                    </Table.Row>
                </Table.Footer>
            </Table>
        );

    }


}

export default RecordTable;