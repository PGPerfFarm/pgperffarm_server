import React from 'react';
import { Icon, Table, Menu, Message } from 'semantic-ui-react'
import './index.css';

// general basic table
class BasicTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isFirstLoading: true
        }
    }


    render() {
        let list = this.props.list

        return (
            <Table celled structured compact>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell rowSpan='2'>Alias</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>System</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>Branch</Table.HeaderCell>
                        <Table.HeaderCell textAlign='center' colSpan='3'>read only</Table.HeaderCell>
                        <Table.HeaderCell textAlign='center' colSpan='3'>read & write</Table.HeaderCell>
                        <Table.HeaderCell rowSpan='2'>Date</Table.HeaderCell>
                    </Table.Row>
                    <Table.Row>
                        <Table.HeaderCell>1 client</Table.HeaderCell>
                        <Table.HeaderCell>2 clients</Table.HeaderCell>
                        <Table.HeaderCell>4 clients</Table.HeaderCell>

                        <Table.HeaderCell>1 client</Table.HeaderCell>
                        <Table.HeaderCell>2 clients</Table.HeaderCell>
                        <Table.HeaderCell>4 clients</Table.HeaderCell>
                    </Table.Row>
                    {/*<Table.Row>*/}
                        {/*<Table.HeaderCell>1 clients</Table.HeaderCell>*/}
                        {/*<Table.HeaderCell>2 clients</Table.HeaderCell>*/}
                        {/*<Table.HeaderCell>4 clients</Table.HeaderCell>*/}
                    {/*</Table.Row>*/}
                </Table.Header>

                <Table.Body>
                    <Table.Row>
                        {/*alias*/}
                        <Table.Cell><a href="#">Cabbage</a></Table.Cell>

                        {/*system*/}
                        <Table.Cell><a href="#">Ubuntu 16 x86_64</a></Table.Cell>

                        {/*branch*/}
                        <Table.Cell>REL9_6_STABLE</Table.Cell>

                        {/*rw-data*/}
                        <Table.Cell textAlign='center'>
                            <Icon color='green' name='checkmark' size='large' />
                        </Table.Cell>
                        <Table.Cell />
                        <Table.Cell />

                        {/*rw-data*/}
                        <Table.Cell />
                        <Table.Cell textAlign='center'>
                            <Icon color='green' name='checkmark' size='large' />
                        </Table.Cell>
                        <Table.Cell />

                        {/*date*/}
                        <Table.Cell>{new Date().toDateString()}</Table.Cell>
                    </Table.Row>
                </Table.Body>
                <Table.Footer>
                    <Table.Row>
                        <Table.HeaderCell colSpan='10'>
                            <Menu size='small' floated='right' pagination>
                                <Menu.Item as='a' icon>
                                    <Icon name='chevron left' />
                                </Menu.Item>
                                <Menu.Item as='a'>1</Menu.Item>
                                <Menu.Item as='a'>2</Menu.Item>
                                <Menu.Item as='a'>3</Menu.Item>
                                <Menu.Item as='a'>4</Menu.Item>
                                <Menu.Item as='a' icon>
                                    <Icon name='chevron right' />
                                </Menu.Item>
                            </Menu>

                        </Table.HeaderCell>
                    </Table.Row>
                </Table.Footer>
            </Table>
        );

    }
}

export default BasicTable;