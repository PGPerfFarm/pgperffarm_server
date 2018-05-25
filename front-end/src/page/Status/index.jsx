import React from 'react';
// import './index.scss';
import ResultFilter from 'component/result-filter/index.jsx';
import RateBar from 'util/rate-bar/index.jsx';

class Status extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            std: 150000,
            curMark1: 243732,
            curMark2: 143733,
            curMark3: 43732,
            curMark4: 3732,
            curMark5: 32,

        }
    }
    render(){
        return (
            <div id="page-wrapper" >
                <h1>status page</h1>
                <p>
                    Shown here is the latest status of each farm member for each branch it has reported on in the last 30 days.
                    Use the farm member link for history of that member on the relevant branch.
                </p>
                <ResultFilter/>
                <RateBar std={this.state.std} curMark={this.state.curMark1}/>

            </div>
        )
    }
}

export default Status;