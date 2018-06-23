import React from 'react';
import './index.css';
import {Table, Divider, Segment, Image, Label, Card, Button} from 'semantic-ui-react'
import TestResultCard from 'component/test-result-card/index.jsx';
import PGUtil        from 'util/util.jsx'
import Record      from 'service/record-service.jsx'
const _util = new PGUtil();
const _record = new Record();
class DetailInfo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            recordNo: 1,
            detailInfo: {},

        }

        // this.onPageChange = this.onPageChange.bind(this);
        // this.handleIsLoading = this.handleIsLoading.bind(this);
    }

    componentDidMount() {
        this.loadDetailInfo();
    }

    // load record detail
    loadDetailInfo() {
        let listParam = {};
        listParam.recordNo = this.state.recordNo;

        _record.getRecordInfo(listParam).then(res => {
            this.setState(res);
        }, errMsg => {
            this.setState({
                list: []
            });
            _util.errorTips(errMsg);
        });
    }

    render() {
        return (
            <div className="container-fluid detail-container">
                <div className="col-md-3">
                    <Segment vertical>Farmer Info</Segment>
                    <Card>
                        <Card.Content>
                            <Image floated='right' size='mini' src='http://www.semantic-ui.cn/images/avatar2/small/lena.png' />
                            <Card.Header>Steve Sanders</Card.Header>
                            <Card.Meta>Friends of Elliot</Card.Meta>
                            <Card.Description>
                                Steve wants to add you to the group <strong>best friends</strong>
                            </Card.Description>
                        </Card.Content>
                        <Card.Content extra>
                            <div className='ui two buttons'>
                                <Button basic color='green'>
                                    Approve
                                </Button>
                                <Button basic color='red'>
                                    Decline
                                </Button>
                            </div>
                        </Card.Content>
                    </Card>
                </div>

                <div className="col-md-9">
                    {/*<div className="card-container row">*/}
                    <div className="card-container col-md-12 col-md-offset-1">
                        <div className="col-md-6 card-div">
                            <Segment vertical>RO</Segment>
                            <Table celled striped key='1'>
                                <Table.Header>
                                    <Table.Row>
                                        <Table.HeaderCell colSpan="4">Clients:4 scale:10 <a href=""> >>prev</a>
                                            <div>

                                                mertic:200 <span>Improved (+12.4%)</span>
                                            </div>
                                        </Table.HeaderCell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.HeaderCell>Start</Table.HeaderCell>
                                        <Table.HeaderCell>Tps</Table.HeaderCell>
                                        <Table.HeaderCell>mode</Table.HeaderCell>
                                        <Table.HeaderCell>latency</Table.HeaderCell>
                                    </Table.Row>
                                </Table.Header>

                                <Table.Body>
                                    <Table.Row>
                                        <Table.Cell>2018-09-11 15:32</Table.Cell>
                                        <Table.Cell>200.221</Table.Cell>
                                        <Table.Cell>simple</Table.Cell>
                                        <Table.Cell>-1</Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>2018-09-11 15:32</Table.Cell>
                                        <Table.Cell>200.221</Table.Cell>
                                        <Table.Cell>simple</Table.Cell>
                                        <Table.Cell>-1</Table.Cell>
                                    </Table.Row>
                                </Table.Body>
                            </Table>
                        </div>

                        <div className="col-md-6 card-div">

                            <Segment vertical>RW</Segment>
                            <Table celled striped color='red' key='1'>
                                <Table.Header>
                                    <Table.Row>
                                        <Table.HeaderCell colSpan="3">Clients:4</Table.HeaderCell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.HeaderCell>Food</Table.HeaderCell>
                                        <Table.HeaderCell>Calories</Table.HeaderCell>
                                        <Table.HeaderCell>Protein</Table.HeaderCell>
                                    </Table.Row>
                                </Table.Header>

                                <Table.Body>
                                    <Table.Row>
                                        <Table.Cell>Apples</Table.Cell>
                                        <Table.Cell>200</Table.Cell>
                                        <Table.Cell>0g</Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>Orange</Table.Cell>
                                        <Table.Cell>310</Table.Cell>
                                        <Table.Cell>0g</Table.Cell>
                                    </Table.Row>
                                </Table.Body>
                            </Table>

                        </div>
                    </div>

                    <div className="info-container col-md-12 col-md-offset-1">
                        {/*<Segment>*/}
                        <Divider/>
                        <Divider horizontal>Horizontal</Divider>
                        {/*</Segment>*/}

                        <div>
                            <h2><a href="#linuxInfo">Linux Info</a></h2>
                            <div className="" data-example-id="">
                                <dl>
                                    <dt><a href="#">Description lists</a></dt>
                                    <dd>A description list is perfect for defining terms.</dd>
                                    <dt>Euismod</dt>
                                    <dd>
                                    </dd>
                                    <dd></dd>
                                    <dt>Malesuada porta</dt>
                                    <dd>Etiam porta sem malesuada magna mollis euismod.</dd>
                                </dl>
                            </div>
                        </div>

                    </div>

                </div>
            </div>

        )
    }
}

export default DetailInfo;