import React from 'react';

// general table
class TableList extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            isFirstLoading: true
        }
    }
    componentWillReceiveProps(){
        // Only when the table is loaded for the first time,isFirstLoading equals true
        this.setState({
            isFirstLoading : false
        });
    }
    render(){
        return (
            <div className="row">
                <div className="col-md-12">
                    <table className="table">
                    {/*todo*/}
                    </table>
                </div>
            </div>
        );
    }
}

export default TableList;