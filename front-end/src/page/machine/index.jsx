import React from 'react';
// import './index.css';
import ResultFilter from 'component/result-filter/index.jsx';
import RecordTable    from 'util/record-table/index.jsx';
import MachineService      from 'service/machine-service.jsx'
import MachineTable    from 'util/machine-table/index.jsx';
import PGUtil        from 'util/util.jsx'

const _util = new PGUtil();
const _machine = new MachineService();
class Machine extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: false,
            currentPage: 1,
            total: 3,
            machines: [],
        },

        // this.onPageChange = this.onPageChange.bind(this);

        this.loadMachineList = this.loadMachineList.bind(this);
    }

    componentDidMount(){
        this.loadMachineList();
    }

    loadMachineList(page=1){
        _machine.getMachineList().then(res => {
            this.setState({
                machines: res.results,
                total: res.count,
                isLoading: false
            });
        }, errMsg => {
            _util.errorTips(errMsg);
        });
    }


    render() {
        return (
            <div id="page-wrapper">
                <h1>machine page</h1>
                <p>
                    Shown here is the latest status of each farm member for each branch it has reported on in the last
                    30 days.
                    Use the farm member link for history of that member on the relevant branch.
                </p>

                <MachineTable list={this.state.machines} total={this.state.total} current={this.state.currentPage} loadfunc={this.loadRecordList}/>

            </div>
        )
    }
}

export default Machine;