import React from 'react';
import './index.css';
import {Table, Divider, Segment, Image, Label, Card, Button, List, Icon} from 'semantic-ui-react'
import PGUtil        from 'util/util.jsx'
import FarmerCard      from 'component/farmer-card/index.jsx'
import InfoList      from 'component/info-list/index.jsx'
import Record      from 'service/record-service.jsx'
const _util = new PGUtil();
const _record = new Record();

class DetailInfo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            recordNo: this.props.match.params.uuid,
            recordInfo: {},
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
            this.setState({
                recordInfo: res
            });
            console.log(this.state.recordInfo)
        }, errMsg => {
            // this.setState({
            //     recordInfo: {}
            // });
            _util.errorTips(errMsg);
        });
    }

    render() {
        let machine = this.state.recordInfo.test_machine || {};
        let dataset = this.state.recordInfo.dataset_info || {};
        let meta_info = this.state.recordInfo.meta_info || {};
        let linux_info = this.state.recordInfo.linux_info || {};
        let ro = dataset.ro || {};
        let rw = dataset.rw || {};
        console.log(machine)
        // Object.keys(obj).map(key => console.log(obj[key]));
        let ro_10 = ro['10'] || {};
        let rw_10 = rw['10'] || {};

        let rw_tables = Object.keys(rw_10).map(key => {
            console.log(rw_10[key])
            let metric = 0;
            let percentage = 0.0;
            let status = -1;
            let tableRow = rw_10[key].map((item, idx) => {
                console.log('item is:')
                console.log(item)
                metric = parseFloat(item['metric']).toFixed(4)
                percentage = (item['percentage'] * 100).toFixed(2).toString() + '%'
                status = item['status']

                let results = item['results'].map((result, idx) => {
                    return (
                        <Table.Row>
                            <Table.Cell>{result.run}</Table.Cell>
                            <Table.Cell>{result.tps}</Table.Cell>
                            <Table.Cell>{result.mode}</Table.Cell>
                            <Table.Cell>{result.latency}</Table.Cell>
                        </Table.Row>
                    );
                });
                return results;

            });
            let trend_span

            if (status == -1) {
                trend_span = <span>{percentage}</span>;
            } else if (status == 1){
                trend_span = <span className="trend-span improved"><Icon name="angle double up"/>+{percentage}</span>;
            } else if (status == 2){
                trend_span = <span className="trend-span quo"><Icon name="bars"/>+{percentage}</span>;
            } else if (status == 3){
                trend_span = <span className="trend-span regressive"><Icon name="angle double down"/>{percentage}</span>;
            }

            return (
                <Table celled striped>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell colSpan="4">
                                <div className="client-title-div">
                                    <div>Client(s) {key}: {metric}  {trend_span}</div>
                                    <div><a href=""> >>prev</a></div>
                                </div>
                                {/*<div>*/}
                                    {/*<span>Improved ()</span>*/}
                                {/*</div>*/}
                            </Table.HeaderCell>
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Run</Table.HeaderCell>
                            <Table.HeaderCell>Tps</Table.HeaderCell>
                            <Table.HeaderCell>mode</Table.HeaderCell>
                            <Table.HeaderCell>latency</Table.HeaderCell>
                        </Table.Row>
                    </Table.Header>

                    <Table.Body>
                        {tableRow}
                        {/*<Table.Row>*/}
                        {/*<Table.Cell>2018-09-11 15:32</Table.Cell>*/}
                        {/*<Table.Cell>200.221</Table.Cell>*/}
                        {/*<Table.Cell>simple</Table.Cell>*/}
                        {/*<Table.Cell>-1</Table.Cell>*/}
                        {/*</Table.Row>*/}
                    </Table.Body>
                </Table>
            );
        });


        let ro_tables = Object.keys(ro_10).map(key => {
            console.log(ro_10[key])
            let metric = 0;
            let percentage = 0.0;
            let status = -1;
            let tableRow = ro_10[key].map((item, idx) => {
                console.log('item is:')
                console.log(item)
                metric = parseFloat(item['metric']).toFixed(4)
                percentage = (item['percentage'] * 100).toFixed(2).toString() + '%'
                status = item['status']

                let results = item['results'].map((result, idx) => {
                    return (
                        <Table.Row>
                            <Table.Cell>{result.run}</Table.Cell>
                            <Table.Cell>{result.tps}</Table.Cell>
                            <Table.Cell>{result.mode}</Table.Cell>
                            <Table.Cell>{result.latency}</Table.Cell>
                        </Table.Row>
                    );
                });
                return results;

            });
            let trend_span

            if (status == -1) {
                trend_span = <span>{percentage}</span>;
            } else if (status == 1){
                trend_span = <span className="trend-span improved"><Icon name="angle double up"/>+{percentage}</span>;
            } else if (status == 2){
                trend_span = <span className="trend-span quo"><Icon name="bars"/>+{percentage}</span>;
            } else if (status == 3){
                trend_span = <span className="trend-span regressive"><Icon name="angle double down"/>{percentage}</span>;
            }

            return (
                <Table celled striped>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell colSpan="4">
                                <div className="client-title-div">
                                    <div>Client(s) {key}: {metric}  {trend_span}</div>
                                    <div><a href=""> >>prev</a></div>
                                </div>
                                {/*<div>*/}
                                {/*<span>Improved ()</span>*/}
                                {/*</div>*/}
                            </Table.HeaderCell>
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Run</Table.HeaderCell>
                            <Table.HeaderCell>Tps</Table.HeaderCell>
                            <Table.HeaderCell>mode</Table.HeaderCell>
                            <Table.HeaderCell>latency</Table.HeaderCell>
                        </Table.Row>
                    </Table.Header>

                    <Table.Body>
                        {tableRow}
                        {/*<Table.Row>*/}
                        {/*<Table.Cell>2018-09-11 15:32</Table.Cell>*/}
                        {/*<Table.Cell>200.221</Table.Cell>*/}
                        {/*<Table.Cell>simple</Table.Cell>*/}
                        {/*<Table.Cell>-1</Table.Cell>*/}
                        {/*</Table.Row>*/}
                    </Table.Body>
                </Table>
            );
        });

        return (
            <div className="container-fluid detail-container">
                <div className="record-title">
                    <h2 >NO: {this.state.recordNo}</h2>
                </div>

                <div className="col-md-3">

                    <Segment vertical>Farmer Info</Segment>
                    <FarmerCard machine={machine}></FarmerCard>
                    //todo add a catalog
                </div>

                <div className="col-md-9">
                    {/*<div className="card-container row">*/}
                    <div className="card-container col-md-12 col-md-offset-1">
                        <div className="col-md-6 card-div">
                            <Segment vertical>RO</Segment>
                            {ro_tables}
                            {/*<Table celled striped key='1'>*/}
                            {/*<Table.Header>*/}
                            {/*<Table.Row>*/}
                            {/*<Table.HeaderCell colSpan="4">Clients:4 scale:10 <a href=""> >>prev</a>*/}
                            {/*<div>*/}

                            {/*mertic:200 <span>Improved (+12.4%)</span>*/}
                            {/*</div>*/}
                            {/*</Table.HeaderCell>*/}
                            {/*</Table.Row>*/}
                            {/*<Table.Row>*/}
                            {/*<Table.HeaderCell>Start</Table.HeaderCell>*/}
                            {/*<Table.HeaderCell>Tps</Table.HeaderCell>*/}
                            {/*<Table.HeaderCell>mode</Table.HeaderCell>*/}
                            {/*<Table.HeaderCell>latency</Table.HeaderCell>*/}
                            {/*</Table.Row>*/}
                            {/*</Table.Header>*/}

                            {/*<Table.Body>*/}
                            {/*<Table.Row>*/}
                            {/*<Table.Cell>2018-09-11 15:32</Table.Cell>*/}
                            {/*<Table.Cell>200.221</Table.Cell>*/}
                            {/*<Table.Cell>simple</Table.Cell>*/}
                            {/*<Table.Cell>-1</Table.Cell>*/}
                            {/*</Table.Row>*/}
                            {/*<Table.Row>*/}
                            {/*<Table.Cell>2018-09-11 15:32</Table.Cell>*/}
                            {/*<Table.Cell>200.221</Table.Cell>*/}
                            {/*<Table.Cell>simple</Table.Cell>*/}
                            {/*<Table.Cell>-1</Table.Cell>*/}
                            {/*</Table.Row>*/}
                            {/*</Table.Body>*/}
                            {/*</Table>*/}

                        </div>

                        <div className="col-md-6 card-div">

                            <Segment vertical>RW</Segment>
                            {rw_tables}

                        </div>
                    </div>

                    <div className="info-container col-md-12 col-md-offset-1">
                        {/*<Segment>*/}
                        <Divider/>
                        <Divider horizontal>Horizontal</Divider>
                        {/*</Segment>*/}

                        <div>
                            {/*<h2><a href="#linuxInfo">Linux Info</a></h2>*/}
                            {/*<div className="" data-example-id="">*/}
                                {/*<dl>*/}
                                    {/*<dt><a href="#">Description lists</a></dt>*/}
                                    {/*<dd>A description list is perfect for defining terms.</dd>*/}
                                    {/*<dt>Euismod</dt>*/}
                                    {/*<dd>*/}
                                    {/*</dd>*/}
                                    {/*<dd></dd>*/}
                                    {/*<dt>Malesuada porta</dt>*/}
                                    {/*<dd>Etiam porta sem malesuada magna mollis euismod.</dd>*/}
                                {/*</dl>*/}
                            {/*</div>*/}


                            <InfoList name="Meta" info={meta_info}> </InfoList>
                            <InfoList name="Linux" info={linux_info}> </InfoList>
                        </div>

                    </div>

                </div>
            </div>

        )
    }
}

export default DetailInfo;