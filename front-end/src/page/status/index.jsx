import React from 'react';
// import './index.css';
import ResultFilter from 'component/result-filter/index.jsx';
import RecordTable    from 'util/record-table/index.jsx';
import Record      from 'service/record-service.jsx'
import PGUtil        from 'util/util.jsx'

const _util = new PGUtil();
const _record = new Record();
class Status extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: false,
            currentPage: 1,
            total: 3,
            filter: {},
            branch_list: [],
            selected_branches:[],
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
        this.loadRecordList = this.loadRecordList.bind(this);
    }

    componentWillMount() {
        this.loadBranchList();
    }

    handleApplyBtnClick(params) {
        console.log('handle apply!')

        let _this = this
        let selected_branches = []
        this.setState({
            selected_branches: selected_branches,
        });
    }

    loadBranchList() {
        _record.getBranchList().then(res => {
            this.setState({
                branch_list: res.results,
                selected_branches: res.results,
            });
            console.log('now console the branch_list')
            console.dir(res.results)
        }, errMsg => {
            _util.errorTips('get branch list error');
        });
    }


    // load record list
    loadRecordList(page = 1) {
        let _this = this;
        let listParam = {};
        listParam = this.state.filter;
        listParam.page = page;

        _record.getRecordList(listParam).then(res => {
            console.log('res is:' + res)
            this.setState({
                list: res.results,
                total: res.count,
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
            isLoading: flag,
        });
        console.log('status isLoading:' + this.state.isLoading)
    }

    render() {
        // console.log('hi')
        // console.dir(this.state.selected_branches)
        // console.log('done')
        let table_list = this.state.selected_branches.map((value, index) => (
            <RecordTable branch={value.branch_name}/>
        ))

        return (
            <div id="page-wrapper">
                <h1>status page</h1>
                <p>
                    Shown here is the latest status of each farm member for each branch it has reported on in the last
                    30 days.
                    Use the farm member link for history of that member on the relevant branch.
                </p>


                <ResultFilter branches={this.state.branch_list} isLoading={this.state.isLoading} onIsLoadingChange={this.onIsLoadingChange}
                              onApplyBtnClick={this.handleApplyBtnClick}/>
                {table_list}
                {/*<RecordTable list={this.state.list} total={this.state.total} current={this.state.currentPage} loadfunc={this.loadRecordList}/>*/}

            </div>
        )
    }
}

export default Status;