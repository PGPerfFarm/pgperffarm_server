import React from 'react';
// import './index.css';
import ResultFilter from 'component/result-filter/index.jsx';
import BasicTable    from 'util/basic-table/index.jsx';
import Record      from 'service/record-service.jsx'
import PGUtil        from 'util/util.jsx'

const _util = new PGUtil();
const _record = new Record();
class Portal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: false,
        }

    }

    render() {
        let show = this.state.isLoading ? "none" : "block";
        let style = {
            display: show
        };

        return (
            <div id="page-wrapper">
                <h1>portal page</h1>
                <p>

                </p>

                {/*<BasicTable list={this.state.list} total={this.state.total} current={this.state.currentPage} loadfunc={this.loadRecordList}/>*/}

            </div>
        )
    }
}

export default Portal;