import React from 'react';
import {Link}     from 'react-router-dom';
import {Icon, Table, Label, Message, Button} from 'semantic-ui-react'
import Pagination from 'util/pagination/index.jsx'
import './index.css';

function LastestLink(props) {
    let _list = props.list
    if (_list <= 0) {
        return null;
    }

    let ret = _list.map((item, index) => {
        return (
            <Link color='linkedin' to={'detailInfo/' + item.uuid}>
                 {item.branch}
            </Link>
        );
    });
    return ret;
}

// general basic table
class MachineTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isFirstLoading: true,
            total: this.props.total,
            currentPage: 1,
        }
    }


    onPageNumChange(current) {
        this.setState({
            currentPage: current
        }, () => {
            this.props.loadfunc(current);
        });
        console.log('current:' + this.state.currentPage)
    }

    render() {
        // let branch = record.pg_info.pg_branch;
        let _list = this.props.list || []
        let style = {
            display: 'show'
        };
        let listBody = _list.map((machineItem, index) => {
            let machine = machineItem
            let system = machine.os_name + ' ' + machine.os_version + ' ' + machine.comp_name + ' ' + machine.comp_version;

            // let improvedIconClassName = trend.improved > 0 ? 'improved' : 'anonymous'
            // let quoIconClassName = trend.quo > 0 ? 'quo' : 'anonymous'
            // let regressiveIconClassName = trend.regressive > 0 ? 'regressive' : 'anonymous'
            let color = 'positive';
            if(machine.state == 'pending'){
                color = 'warning';
            }else if(machine.state == 'prohibited'){
                color = 'negative';
            }
            return (
                <Table.Row key={index} className={color}>
                    {/*alias*/}
                    <Table.Cell><a href="#">{machine.alias}</a></Table.Cell>

                    {/*system*/}
                    <Table.Cell><a href="#">{system}</a></Table.Cell>

                    {/*State*/}
                    <Table.Cell>
                        {machine.state}
                    </Table.Cell>

                    {/*lastest-records*/}
                    <Table.Cell textAlign='center'>
                        {/*<Icon className={"bgc-clear " + improvedIconClassName} name='smile outline' size='large'/>*/}
                        {/*<Bubble num={trend.improved} name="improved"/>*/}
                        <div className="link-div">
                            <LastestLink list={machine.lastest}/>
                        </div>
                    </Table.Cell>

                    {/*machine history*/}
                    <Table.Cell textAlign='center'>
                        <Link color='linkedin' to={'machineInfo/' + machine.machine_sn}>
                            <Icon name='linkify'/> Link
                        </Link>
                    </Table.Cell>

                    {/*date*/}
                    <Table.Cell>{machine.add_time}</Table.Cell>
                </Table.Row>
            );
        });

        return (
            <Table celled structured compact textAlign='center'>
                <Table.Header>
                    {/*<Table.Row>*/}
                        {/*<Table.HeaderCell rowSpan='9'>Branch: 10_STABLE</Table.HeaderCell>*/}
                    {/*</Table.Row>*/}
                    <Table.Row>
                        <Table.HeaderCell rowSpan='2'>Alias</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>System</Table.HeaderCell>
                        {/*<Table.HeaderCell rowSpan='2'>Branch</Table.HeaderCell>*/}
                        <Table.HeaderCell rowSpan='2'>State</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='3'>Lastest</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>History</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>Add Date</Table.HeaderCell>
                    </Table.Row>
                    {/*<Table.Row>*/}
                        {/*<Table.HeaderCell>improvement</Table.HeaderCell>*/}
                        {/*<Table.HeaderCell>status quo</Table.HeaderCell>*/}
                        {/*<Table.HeaderCell>regression</Table.HeaderCell>*/}
                    {/*</Table.Row>*/}

                </Table.Header>

                <Table.Body>
                    {listBody}
                </Table.Body>
                <Table.Footer>
                    <Table.Row>
                        <Table.HeaderCell colSpan='10'>

                            <Pagination style={style} onChange={(current) => this.onPageNumChange(current)} pageSize={15}
                                        current={this.state.currentPage} total={this.props.total}/>
                        </Table.HeaderCell>

                    </Table.Row>
                </Table.Footer>
            </Table>
        );

    }


}

export default MachineTable;