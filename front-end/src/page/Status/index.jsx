import React from 'react';
// import './index.scss';
import ResultFilter from 'component/result-filter/index.jsx';

class Status extends React.Component{
    render(){
        return (
            <div id="page-wrapper" >
                <h1>status page</h1>
                <p>
                    Shown here is the latest status of each farm member for each branch it has reported on in the last 30 days.
                    Use the farm member link for history of that member on the relevant branch.
                </p>
                <ResultFilter/>
            </div>
        )
    }
}

export default Status;