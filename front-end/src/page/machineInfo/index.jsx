import React from 'react';
// import './index.css';
import ResultFilter from 'component/result-filter/index.jsx';
import BasicTable    from 'util/basic-table/index.jsx';
import Record      from 'service/record-service.jsx'
import PGUtil        from 'util/util.jsx'

const _util = new PGUtil();
const _record = new Record();
class MachineInfo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: false,
            currentPage: 1,
            total:3,
            filter: {},
            list: [
            ]

        },

        this.onPageChange = this.onPageChange.bind(this);
        this.onIsLoadingChange = this.onIsLoadingChange.bind(this);
        this.handleApplyBtnClick = this.handleApplyBtnClick.bind(this);
        this.loadRecordList = this.loadRecordList.bind(this);
    }

    componentDidMount() {
        this.loadHistoryRecordList();
    }

    handleApplyBtnClick(params) {
        console.log('handle apply!')

        let self = this
        this.setState({filter: params}, ()=> {
            self.loadRecordList()
        });
    }

    // load history record list
    loadHistoryRecordList(page=1) {
        let _this = this;
        let listParam = {};
        listParam= this.state.filter;
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

    render() {
        let show = this.state.isLoading ? "none" : "block";
        let style = {
            display: show
        };

        return (
            <div id="page-wrapper">
                <BasicTable list={this.state.list} total={this.state.total} current={this.state.currentPage} loadfunc={this.loadRecordList}/>
            </div>
        )
    }
}

export default MachineInfo;