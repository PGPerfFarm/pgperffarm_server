import React from 'react';
import {Link}     from 'react-router-dom';
import {Icon, Table, Label, Message, Button} from 'semantic-ui-react'
import Pagination from 'util/pagination/index.jsx'
import './index.css';

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

                    {/*State*/}
                    <Table.Cell>acitve</Table.Cell>

                    {/*lastest-records*/}

                    <Table.Cell textAlign='center'>
                        <Icon className={"bgc-clear " + improvedIconClassName} name='smile outline' size='large'/>
                        <Bubble num={trend.improved} name="improved"/>
                    </Table.Cell>

                    {/*machine history*/}
                    <Table.Cell textAlign='center'>
                        <Link color='linkedin' to={'machineInfo/' + record.uuid}>
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
                        {/*<Table.HeaderCell rowSpan='9'>Branch: 10_STABLE</Table.HeaderCell>*/}
                    {/*</Table.Row>*/}
                    <Table.Row>
                        <Table.HeaderCell rowSpan='2'>Alias</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>System</Table.HeaderCell>
                        {/*<Table.HeaderCell rowSpan='2'>Branch</Table.HeaderCell>*/}
                        <Table.HeaderCell rowSpan='2'>State</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='3'>Lastest</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>History</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>Date</Table.HeaderCell>
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

                            <Pagination style={style} onChange={(current) => this.onPageNumChange(current)} pageSize={2}
                                        current={this.state.currentPage} total={this.props.total}/>
                        </Table.HeaderCell>

                    </Table.Row>
                </Table.Footer>
            </Table>
        );

    }


}

export default MachineTable;