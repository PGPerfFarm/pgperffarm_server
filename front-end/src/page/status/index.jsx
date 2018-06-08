import React from 'react';
// import './index.css';
import ResultFilter from 'component/result-filter/index.jsx';
import ClientBox from 'component/client-box/index.jsx';
import Pagination from 'util/pagination/index.jsx';
import RateBar from 'util/rate-bar/index.jsx';
import TableList    from 'util/table-list/index.jsx';
import BasicTable    from 'util/basic-table/index.jsx';
import Record      from 'service/record-service.jsx'
import PGUtil        from 'util/util.jsx'

const _util = new PGUtil();
const _record = new Record();
class Status extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: false,
            currentPage: 3,
            filter: {},
            list: [
                // {
                //     'alias': 'a_name',
                //     'email': 'a_name@mail.com',
                //     'clients': [2,3,4],
                //     'mark': [140000,1,1],
                // }, {
                //     'alias': 'b_name',
                //     'email': 'b_name@mail.com',
                //     'clients': '4',
                //     'mark': 150000
                // }
            ]

        },
            this.onPageChange = this.onPageChange.bind(this);
        this.onIsLoadingChange = this.onIsLoadingChange.bind(this);
        this.handleApplyBtnClick = this.handleApplyBtnClick.bind(this);
    }

    componentDidMount() {
        this.loadRecordList();
    }

    handleApplyBtnClick() {
        console.log('apply btn clicked!')
        this.loadRecordList()
    }

    // load record list
    loadRecordList() {
        let _this = this;
        let listParam = {};
        listParam.filter = this.state.filter;
        // listParam.pageNum = this.state.pageNum;

        _record.getRecordList(listParam).then(res => {
            console.log('res is:' + res)
            this.setState({
                list: res.results,
                isLoading: false
            });
            _this.changeIsLoading(false);
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

    onPageChange(page) {
        console.log(page);
        console.log(this);
        this.setState({
            current: page,
        });
    }

    changeIsLoading(flag) {
        this.setState({
            isLoading: flag
        });
    }

    onIsLoadingChange(flag) {
        console.log('flag:' + flag)
        this.setState({
            isLoading: flag
        });
        console.log('status isLoading:' + this.state.isLoading)
    }

    render() {
        let show = this.state.isLoading ? "none" : "block";
        let style = {
            display: show
        };

        let listBody = this.state.list.map((machine, index) => {
            let info = machine.machine_info[0];
            let info_str = info.os_name + ' ' + info.os_version + ' ' + info.comp_name + ' ' + info.comp_version;
            let client_max = machine.client_max_num
            return (

                <tr key={index}>

                    <td><a href={'#'}>{info.alias}</a></td>

                    <td><a href={'#'}>{info_str}</a></td>

                    <td>
                        <div>
                            <ClientBox clientNum="1" std="100" median="200">1</ClientBox>
                            <ClientBox clientNum="2" std="100" median="200">2</ClientBox>
                            <ClientBox clientNum="4" std={100} median={2}>4</ClientBox>
                        </div>

                    </td>
                    <td>
                        1111
                        {/*<th rowspan="3"></th>*/}
                        {/*<th rowspan="3">1-2</th>*/}
                        {/*<th rowspan="2">1-3</th>*/}
                        {/*<th rowspan="1">1-4</th>*/}
                        {/*<th rowspan="3">1-5</th>*/}
                    </td>

                    <td rowSpan="2">
                        {machine.clients}
                        {/*<th rowspan="3"></th>*/}
                        {/*<th rowspan="3">1-2</th>*/}
                        {/*<th rowspan="2">1-3</th>*/}
                        {/*<th rowspan="1">1-4</th>*/}
                        {/*<th rowspan="3">1-5</th>*/}
                    </td>
                    <td>

                        {/*<div style={{float: 'left'}}> <p>{machine.mark}</p></div>*/}
                    </td>
                    <td>{new Date().toDateString()}</td>
                </tr>
            );
        });

        return (
            <div id="page-wrapper">
                <h1>status page</h1>
                <p>
                    Shown here is the latest status of each farm member for each branch it has reported on in the last
                    30 days.
                    Use the farm member link for history of that member on the relevant branch.
                </p>


                <ResultFilter isLoading={this.state.isLoading} onIsLoadingChange={this.onIsLoadingChange}
                              onApplyBtnClick={this.handleApplyBtnClick}/>

                <TableList tableHeads={['alias', 'System', 'ro', 'rw', 'date']}>
                    {listBody}
                </TableList>
                {/*<BasicTable></BasicTable>*/}
                <Pagination style={style} onChange={this.onPageChange} current={this.state.currentPage} total={25}/>
                {/*<RateBar std={this.state.std} curMark={this.state.curMark1}/>*/}

            </div>
        )
    }
}

export default Status;