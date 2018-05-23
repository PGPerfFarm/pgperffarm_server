import React from 'react';
import Pagination from 'util/pagination/index.jsx';
import './index.css';

class ResultFilter extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            current: 3,
            selected_items: [
                {'cate':'Category 2','name':'30 days'}
            ],
            selected: [{
                'cate': 'Category 1',
                'data': [
                    'All',
                    'Improving',
                    'Regressive'
                ],
            }, {
                'cate': 'Category 2',
                'data': [
                    'All',
                    '7 days',
                    '30 days'
                ],
            }, {
                'cate': 'Category 3',
                'data': [
                    'All',
                    'item3-1',
                    'item3-2'
                ],
            }],
            isClear: false
        };

        this.onChange = this.onChange.bind(this);
        this.selectItemClick = this.selectItemClick.bind(this);
    }

    selectItemClick(e) {
        console.log('selectItemClick!!', this);
        let item_name = e.currentTarget.getAttribute("data-item-name")
        console.log(item_name);
        let cate_name = e.target.getAttribute("data-cate-name")
        console.log(cate_name);
        this.setState({
            //todo
            'selected_items': [...this.state.selected_items, item_name],
        });

    }

    deleteSelectItemClick(e) {
        console.log('deleteSelectItemClick!!', this);
        let item_name = e.currentTarget.getAttribute("data-item-name")
        console.log(item_name);
        let cate_name = e.target.getAttribute("data-cate-name")
        console.log(cate_name);
        this.setState({
            //todo
        });
    }
    handleClick() {
        console.log('handleClick!!', this);
        var self = this;
    }

    applyButtonClick() {
        //todo
    }

    clearButtonClick() {
        //todo
    }

    onChange(page) {
        console.log(page);
        console.log(this);
        this.setState({
            current: page,
        });
    }

    render() {
        let _this = this;

        let selected_item = _this.state.selected_items.map((s, index) => {
            // let is_high_light = index == 0 ? "select-all selected" :"select-all"
            return (
                <li key={index} data-item-name={s.name} data-cate-name={s.cate}>{s.cate + ': ' + s.name} <a href="javascript:void(0)" onClick={(e) => this.deleteSelectItemClick(e)}>x</a></li>
            )
        });

        let filter = this.state.selected.map((item, i) => {

            let filter_item = item["data"].map((s, index) => {
                let is_high_light = index == 0 ? "select-all selected" : "select-all"
                return (
                    <dd onClick={(e) => this.selectItemClick(e)} key={index} data-item-name={s} className={is_high_light}><a
                        href="#">{s}</a></dd>
                )
            });

            return (
                <li className="select-list" item={item} key={i}>
                    <dl id={'select'}>
                        <dt data-cate-name={item["cate"]}>{item["cate"]}:</dt>
                        {filter_item}
                        {/*<dd className="select-all selected"><a href="#">All</a></dd>*/}
                        {/*<dd><a href="#">today</a></dd>*/}
                        {/*<dd><a href="#">7 days</a></dd>*/}
                        {/*<dd><a href="#">30 days</a></dd>*/}
                    </dl>
                </li>
            )
        });

        return (
            <div id="wrapper">
                <div className="panel-group" id="accordion">
                    <div className="panel panel-default">
                        <div className="panel-heading" onClick={() => this.handleClick()}>
                            <div className="panel-title">
                                <a href="#panel1" className="panel-toggle" data-toggle="collapse"
                                   data-parent="#accordion">
                                    <span className="glyphicon glyphicon-search" aria-hidden="true"></span>Filter
                                </a>
                                <div className="title-selected-result">
                                    <span>--</span>
                                    <button data-toggle="button" className="btn btn-primary-warn title-selected-btn"
                                            disabled={ this.state.isClear ? "disabled" : "" }>
                                        clear
                                    </button>
                                    <button data-toggle="button" className="btn btn-primary title-selected-btn">apply
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div id="panel1" className="panel-collapse collapse in">

                            <div className="panel-body">
                                <ul className="selected_item">
                                    {selected_item}
                                </ul>


                                <ul className="select">

                                    {filter}

                                    {/*<li className="select-list">*/}
                                    {/*<dl id="select1">*/}
                                    {/*<dt>Category 1:</dt>*/}
                                    {/*<dd className="select-all selected"><a href="#">All</a></dd>*/}
                                    {/*<dd><a href="#">Improving</a></dd>*/}
                                    {/*<dd><a href="#">Regressive</a></dd>*/}
                                    {/*</dl>*/}
                                    {/*</li>*/}
                                    {/*<li className="select-list">*/}
                                    {/*<dl id="select2">*/}
                                    {/*<dt>Category 2:</dt>*/}
                                    {/*<dd className="select-all selected"><a href="#">All</a></dd>*/}
                                    {/*<dd><a href="#">today</a></dd>*/}
                                    {/*<dd><a href="#">7 days</a></dd>*/}
                                    {/*<dd><a href="#">30 days</a></dd>*/}
                                    {/*</dl>*/}
                                    {/*</li>*/}
                                    {/*<li className="select-list">*/}
                                    {/*<dl id="select3">*/}
                                    {/*<dt>Category 3:</dt>*/}
                                    {/*<dd className="select-all selected"><a href="#">All</a></dd>*/}
                                    {/*<dd><a href="#">item1</a></dd>*/}
                                    {/*<dd><a href="#">item2</a></dd>*/}
                                    {/*</dl>*/}
                                    {/*</li>*/}
                                </ul>
                            </div>
                        </div>
                    </div>

                </div>
                <p>...</p>
                <Pagination onChange={this.onChange} current={this.state.current} total={25}></Pagination>
                <div className="panel panel-default">
                    <div className="panel-heading">
                        Advanced Tables
                    </div>
                    <div className="panel-body">
                        <div className="table-responsive">
                            <div id="dataTables-example_wrapper" className="dataTables_wrapper form-inline" role="grid">
                                <div className="row">
                                    <div className="col-sm-6">
                                        <div className="dataTables_length" id="dataTables-example_length"><label><select
                                            name="dataTables-example_length" aria-controls="dataTables-example"
                                            className="form-control input-sm">
                                            <option value="10">10</option>
                                            <option value="25">25</option>
                                            <option value="50">50</option>
                                            <option value="100">100</option>
                                        </select> records per page</label></div>
                                    </div>
                                    <div className="col-sm-6">
                                        <div id="dataTables-example_filter" className="dataTables_filter">
                                            <label>Search:<input type="search" className="form-control input-sm"
                                                                 aria-controls="dataTables-example"/></label></div>
                                    </div>
                                </div>
                                <table className="table table-striped table-bordered table-hover dataTable no-footer"
                                       id="dataTables-example" aria-describedby="dataTables-example_info">
                                    <thead>
                                    <tr role="row">
                                        <th className="sorting_asc" colSpan="0" aria-controls="dataTables-example"
                                            rowSpan="1" colSpan="1" aria-sort="ascending"
                                            aria-label="Rendering engine: activate to sort column ascending"
                                            style={{width: '225px'}}>Rendering engine
                                        </th>
                                        <th className="sorting" colSpan="0" aria-controls="dataTables-example"
                                            rowSpan="1"
                                            colSpan="1" aria-label="Browser: activate to sort column ascending"
                                            style={{width: '299px'}}>Browser
                                        </th>
                                        <th className="sorting" colSpan="0" aria-controls="dataTables-example"
                                            rowSpan="1"
                                            colSpan="1" aria-label="Platform(s): activate to sort column ascending"
                                            style={{width: '275px'}}>Platform(s)
                                        </th>
                                        <th className="sorting" colSpan="0" aria-controls="dataTables-example"
                                            rowSpan="1"
                                            colSpan="1" aria-label="Engine version: activate to sort column ascending"
                                            style={{width: '189px'}}>Engine version
                                        </th>
                                        <th className="sorting" colSpan="0" aria-controls="dataTables-example"
                                            rowSpan="1"
                                            colSpan="1" aria-label="CSS grade: activate to sort column ascending"
                                            style={{width: '132px'}}>CSS grade
                                        </th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr className="gradeA odd">
                                        <td className="sorting_1">Gecko</td>
                                        <td className=" ">Firefox 1.0</td>
                                        <td className=" ">Win 98+ / OSX.2+</td>
                                        <td className="center ">1.7</td>
                                        <td className="center ">A</td>
                                    </tr>
                                    <tr className="gradeA even">
                                        <td className="sorting_1">Gecko</td>
                                        <td className=" ">Firefox 1.5</td>
                                        <td className=" ">Win 98+ / OSX.2+</td>
                                        <td className="center ">1.8</td>
                                        <td className="center ">A</td>
                                    </tr>
                                    <tr className="gradeA odd">
                                        <td className="sorting_1">Gecko</td>
                                        <td className=" ">Firefox 2.0</td>
                                        <td className=" ">Win 98+ / OSX.2+</td>
                                        <td className="center ">1.8</td>
                                        <td className="center ">A</td>
                                    </tr>
                                    <tr className="gradeA even">
                                        <td className="sorting_1">Gecko</td>
                                        <td className=" ">Firefox 3.0</td>
                                        <td className=" ">Win 2k+ / OSX.3+</td>
                                        <td className="center ">1.9</td>
                                        <td className="center ">A</td>
                                    </tr>
                                    <tr className="gradeA odd">
                                        <td className="sorting_1">Gecko</td>
                                        <td className=" ">Camino 1.0</td>
                                        <td className=" ">OSX.2+</td>
                                        <td className="center ">1.8</td>
                                        <td className="center ">A</td>
                                    </tr>
                                    <tr className="gradeA even">
                                        <td className="sorting_1">Gecko</td>
                                        <td className=" ">Camino 1.5</td>
                                        <td className=" ">OSX.3+</td>
                                        <td className="center ">1.8</td>
                                        <td className="center ">A</td>
                                    </tr>
                                    <tr className="gradeA odd">
                                        <td className="sorting_1">Gecko</td>
                                        <td className=" ">Netscape 7.2</td>
                                        <td className=" ">Win 95+ / Mac OS 8.6-9.2</td>
                                        <td className="center ">1.7</td>
                                        <td className="center ">A</td>
                                    </tr>
                                    <tr className="gradeA even">
                                        <td className="sorting_1">Gecko</td>
                                        <td className=" ">Netscape Browser 8</td>
                                        <td className=" ">Win 98SE+</td>
                                        <td className="center ">1.7</td>
                                        <td className="center ">A</td>
                                    </tr>
                                    <tr className="gradeA odd">
                                        <td className="sorting_1">Gecko</td>
                                        <td className=" ">Netscape Navigator 9</td>
                                        <td className=" ">Win 98+ / OSX.2+</td>
                                        <td className="center ">1.8</td>
                                        <td className="center ">A</td>
                                    </tr>
                                    <tr className="gradeA even">
                                        <td className="sorting_1">Gecko</td>
                                        <td className=" ">Mozilla 1.0</td>
                                        <td className=" ">Win 95+ / OSX.1+</td>
                                        <td className="center ">1</td>
                                        <td className="center ">A</td>
                                    </tr>
                                    </tbody>
                                </table>
                                <div className="row">
                                    <div className="col-sm-6">
                                        <div className="dataTables_info" id="dataTables-example_info" role="alert"
                                             aria-live="polite" aria-relevant="all">Showing 1 to 10 of 57 entries
                                        </div>
                                    </div>
                                    <div className="col-sm-6">
                                        <div className="dataTables_paginate paging_simple_numbers"
                                             id="dataTables-example_paginate">
                                            <ul className="pagination">
                                                <li className="paginate_button previous disabled"
                                                    aria-controls="dataTables-example" colSpan="0"
                                                    id="dataTables-example_previous"><a href="#123">Previous</a></li>
                                                <li className="paginate_button active"
                                                    aria-controls="dataTables-example"
                                                    colSpan="0"><a href="#">1</a></li>
                                                <li className="paginate_button " aria-controls="dataTables-example"
                                                    colSpan="0"><a href="#">2</a></li>
                                                <li className="paginate_button " aria-controls="dataTables-example"
                                                    colSpan="0"><a href="#">3</a></li>
                                                <li className="paginate_button " aria-controls="dataTables-example"
                                                    colSpan="0"><a href="#">4</a></li>
                                                <li className="paginate_button " aria-controls="dataTables-example"
                                                    colSpan="0"><a href="#">5</a></li>
                                                <li className="paginate_button " aria-controls="dataTables-example"
                                                    colSpan="0"><a href="#">6</a></li>
                                                <li className="paginate_button next" aria-controls="dataTables-example"
                                                    colSpan="0" id="dataTables-example_next"><a href="#">Next</a></li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default ResultFilter;