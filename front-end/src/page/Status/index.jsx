import React from 'react';
// import './index.css';
import ResultFilter from 'component/result-filter/index.jsx';
import Pagination from 'util/pagination/index.jsx';
import RateBar from 'util/rate-bar/index.jsx';
import TableList    from 'util/table-list/index.jsx';

class Status extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            currentPage: 3,
            std: 150000,
            curMark1: 243732,
            curMark2: 143733,
            curMark3: 43732,
            curMark4: 3732,
            curMark5: 32,
            isLoading: false,
            list: [
                {
                    'alias': 'a_name',
                    'email': 'a_name@mail.com',
                    'clients': '2',
                    'mark': 140000,
                }, {
                    'alias': 'b_name',
                    'email': 'b_name@mail.com',
                    'clients': '4',
                    'mark': 150000,
                }
            ]

        }
        this.onPageChange = this.onPageChange.bind(this);
        this.handleisLoading = this.handleisLoading.bind(this);
    }

    onPageChange(page) {
        console.log(page);
        console.log(this);
        this.setState({
            current: page,
        });
    }

    handleisLoading(isLoading) {
        this.setState({
            isLoading: isLoading
        })
    }

    render() {
        let show = this.state.isLoading ? "none" : "block";
        let style = {
            display: show
        };

        let listBody = this.state.list.map((machine, index) => {
            return (
                <tr key={index}>
                    <td>{machine.alias}</td>
                    <td>{machine.email}</td>
                    <td>{machine.clients}</td>
                    <td>

                        <p> {machine.mark}</p>
                        <RateBar style={{zIndex: 999}} std={this.state.std} curMark={this.state.curMark1}/>
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


                <ResultFilter isLoading={this.state.isLoading} onIsLoadingChange={this.handleisLoading}/>

                <TableList tableHeads={['alias', 'email', 'clients', 'mark', 'date']}>
                    {listBody}
                </TableList>

                <Pagination style={style} onChange={this.onPageChange} current={this.state.currentPage} total={25}/>
                <RateBar std={this.state.std} curMark={this.state.curMark1}/>

            </div>
        )
    }
}

export default Status;