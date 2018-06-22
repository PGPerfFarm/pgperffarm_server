import React from 'react';
import {Icon, Table, Menu, Message, Button} from 'semantic-ui-react'
import Pagination from 'util/pagination/index.jsx'
import './index.css';

// general basic table
class BasicTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isFirstLoading: true,
            total: this.props.total,
            currentPage: 1,
        }
    }

    onPageNumChange(current){
        this.setState({
            currentPage : current
        }, () => {
            this.props.loadfunc(current);
        });
        console.log('current:' + this.state.currentPage)
    }

    render() {

        let _list = this.props.list
        let style = {
            display: 'show'
        };
        let listBody = _list.map((record, index) => {
            let machine = record.machine_info[0];
            let system = machine.os_name + ' ' + machine.os_version + ' ' + machine.comp_name + ' ' + machine.comp_version;
            let alias = machine.alias;
            let branch = record.pg_info.pg_branch;

            let trend = record.trend
            return (

                <Table.Row key={index}>
                    {/*alias*/}
                    <Table.Cell><a href="#">{alias}</a></Table.Cell>

                    {/*system*/}
                    <Table.Cell><a href="#">{system}</a></Table.Cell>

                    {/*branch*/}
                    <Table.Cell>{branch}</Table.Cell>

                    {/*trending-data*/}
                    <Table.Cell textAlign='center'>
                        <Icon color='green' name='checkmark' size='large'/>{trend.improved}
                    </Table.Cell>
                    <Table.Cell textAlign='center'>
                        <Icon color='green' name='meh' size='large'/>{trend.quo}
                    </Table.Cell>
                    <Table.Cell textAlign='center'>
                        <i className="fa fa-meh-o"></i>{trend.regressive}
                    </Table.Cell>
                    <Table.Cell textAlign='center'>
                        <a href={'detail/' + record.uuid}>
                            <Button size='mini' color='linkedin'>
                                <Icon name='linkify' /> Link
                            </Button>
                        </a>
                    </Table.Cell>
                    {/*date*/}
                    <Table.Cell>{new Date().toDateString()}</Table.Cell>
                </Table.Row>
            );
        });

        return (
            <Table celled structured compact textAlign='center'>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell rowSpan='2'>Alias</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>System</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>Branch</Table.HeaderCell>
                        <Table.HeaderCell colSpan='3'>Trending</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>Detail</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>Date</Table.HeaderCell>
                    </Table.Row>
                    <Table.Row>
                        <Table.HeaderCell>improved</Table.HeaderCell>
                        <Table.HeaderCell>quo</Table.HeaderCell>
                        <Table.HeaderCell>regressive</Table.HeaderCell>
                    </Table.Row>

                </Table.Header>

                <Table.Body>
                    {listBody}
                </Table.Body>
                <Table.Footer>
                    <Table.Row>
                        <Table.HeaderCell colSpan='10'>
                            {/*<Menu size='small' floated='right' pagination>*/}
                                {/*<Menu.Item as='a' icon>*/}
                                    {/*<Icon name='chevron left'/>*/}
                                {/*</Menu.Item>*/}
                                {/*<Menu.Item as='a'>1</Menu.Item>*/}
                                {/*<Menu.Item as='a'>2</Menu.Item>*/}
                                {/*<Menu.Item as='a'>3</Menu.Item>*/}
                                {/*<Menu.Item as='a'>4</Menu.Item>*/}
                                {/*<Menu.Item as='a' icon>*/}
                                    {/*<Icon name='chevron right'/>*/}
                                {/*</Menu.Item>*/}
                            {/*</Menu>*/}
                            <Pagination style={style} onChange={(current) => this.onPageNumChange(current)} pageSize={2} current={this.state.currentPage} total={this.props.total}/>

                        </Table.HeaderCell>

                    </Table.Row>
                </Table.Footer>
            </Table>
        );

    }
}

export default BasicTable;