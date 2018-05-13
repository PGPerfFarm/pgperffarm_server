import React from 'react';

import './index.css';

class ResultFilter extends React.Component {
    constructor(props) {
        super(props);
    }

    handleClick() {
        console.log('clicked!!', this);
        var self = this;
        $(self).nextAll().eq(0).collapse("collapse");
    }

    render() {
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
                                    <button data-toggle="button" className="btn btn-primary-warn title-selected-btn">
                                        clear
                                    </button>
                                    <button data-toggle="button" className="btn btn-primary title-selected-btn">apply
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div id="panel1" className="panel-collapse collapse in">
                            <div className="panel-body">
                                <ul className="select">
                                    <li className="select-list">
                                        <dl id="select1">
                                            <dt>Category 1:</dt>
                                            <dd className="select-all selected"><a href="#">All</a></dd>
                                            <dd><a href="#">Improving</a></dd>
                                            <dd><a href="#">Regressive</a></dd>
                                        </dl>
                                    </li>
                                    <li className="select-list">
                                        <dl id="select2">
                                            <dt>Category 2:</dt>
                                            <dd className="select-all selected"><a href="#">All</a></dd>
                                            <dd><a href="#">today</a></dd>
                                            <dd><a href="#">7 days</a></dd>
                                            <dd><a href="#">30 days</a></dd>
                                        </dl>
                                    </li>
                                    <li className="select-list">
                                        <dl id="select3">
                                            <dt>Category 3:</dt>
                                            <dd className="select-all selected"><a href="#">All</a></dd>
                                            <dd><a href="#">item1</a></dd>
                                            <dd><a href="#">item2</a></dd>
                                        </dl>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>

                </div>
                <div class="panel panel-default">
                    <div class="panel-heading">
                        Advanced Tables
                    </div>
                    <div class="panel-body">
                        <div class="table-responsive">
                            <div id="dataTables-example_wrapper" class="dataTables_wrapper form-inline" role="grid">
                                <div class="row">
                                    <div class="col-sm-6">
                                        <div class="dataTables_length" id="dataTables-example_length"><label><select
                                            name="dataTables-example_length" aria-controls="dataTables-example"
                                            class="form-control input-sm">
                                            <option value="10">10</option>
                                            <option value="25">25</option>
                                            <option value="50">50</option>
                                            <option value="100">100</option>
                                        </select> records per page</label></div>
                                    </div>
                                    <div class="col-sm-6">
                                        <div id="dataTables-example_filter" class="dataTables_filter">
                                            <label>Search:<input type="search" class="form-control input-sm"
                                                                 aria-controls="dataTables-example"/></label></div>
                                    </div>
                                </div>
                                <table class="table table-striped table-bordered table-hover dataTable no-footer"
                                       id="dataTables-example" aria-describedby="dataTables-example_info">
                                    <thead>
                                    <tr role="row">
                                        <th class="sorting_asc" tabindex="0" aria-controls="dataTables-example"
                                            rowspan="1" colspan="1" aria-sort="ascending"
                                            aria-label="Rendering engine: activate to sort column ascending"
                                            style={{width: '225px'}}>Rendering engine
                                        </th>
                                        <th class="sorting" tabindex="0" aria-controls="dataTables-example" rowspan="1"
                                            colspan="1" aria-label="Browser: activate to sort column ascending"
                                            style={{width: '299px'}}>Browser
                                        </th>
                                        <th class="sorting" tabindex="0" aria-controls="dataTables-example" rowspan="1"
                                            colspan="1" aria-label="Platform(s): activate to sort column ascending"
                                            style={{width: '275px'}}>Platform(s)
                                        </th>
                                        <th class="sorting" tabindex="0" aria-controls="dataTables-example" rowspan="1"
                                            colspan="1" aria-label="Engine version: activate to sort column ascending"
                                            style={{width: '189px'}}>Engine version
                                        </th>
                                        <th class="sorting" tabindex="0" aria-controls="dataTables-example" rowspan="1"
                                            colspan="1" aria-label="CSS grade: activate to sort column ascending"
                                            style={{width: '132px'}}>CSS grade
                                        </th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr class="gradeA odd">
                                        <td class="sorting_1">Gecko</td>
                                        <td class=" ">Firefox 1.0</td>
                                        <td class=" ">Win 98+ / OSX.2+</td>
                                        <td class="center ">1.7</td>
                                        <td class="center ">A</td>
                                    </tr>
                                    <tr class="gradeA even">
                                        <td class="sorting_1">Gecko</td>
                                        <td class=" ">Firefox 1.5</td>
                                        <td class=" ">Win 98+ / OSX.2+</td>
                                        <td class="center ">1.8</td>
                                        <td class="center ">A</td>
                                    </tr>
                                    <tr class="gradeA odd">
                                        <td class="sorting_1">Gecko</td>
                                        <td class=" ">Firefox 2.0</td>
                                        <td class=" ">Win 98+ / OSX.2+</td>
                                        <td class="center ">1.8</td>
                                        <td class="center ">A</td>
                                    </tr>
                                    <tr class="gradeA even">
                                        <td class="sorting_1">Gecko</td>
                                        <td class=" ">Firefox 3.0</td>
                                        <td class=" ">Win 2k+ / OSX.3+</td>
                                        <td class="center ">1.9</td>
                                        <td class="center ">A</td>
                                    </tr>
                                    <tr class="gradeA odd">
                                        <td class="sorting_1">Gecko</td>
                                        <td class=" ">Camino 1.0</td>
                                        <td class=" ">OSX.2+</td>
                                        <td class="center ">1.8</td>
                                        <td class="center ">A</td>
                                    </tr>
                                    <tr class="gradeA even">
                                        <td class="sorting_1">Gecko</td>
                                        <td class=" ">Camino 1.5</td>
                                        <td class=" ">OSX.3+</td>
                                        <td class="center ">1.8</td>
                                        <td class="center ">A</td>
                                    </tr>
                                    <tr class="gradeA odd">
                                        <td class="sorting_1">Gecko</td>
                                        <td class=" ">Netscape 7.2</td>
                                        <td class=" ">Win 95+ / Mac OS 8.6-9.2</td>
                                        <td class="center ">1.7</td>
                                        <td class="center ">A</td>
                                    </tr>
                                    <tr class="gradeA even">
                                        <td class="sorting_1">Gecko</td>
                                        <td class=" ">Netscape Browser 8</td>
                                        <td class=" ">Win 98SE+</td>
                                        <td class="center ">1.7</td>
                                        <td class="center ">A</td>
                                    </tr>
                                    <tr class="gradeA odd">
                                        <td class="sorting_1">Gecko</td>
                                        <td class=" ">Netscape Navigator 9</td>
                                        <td class=" ">Win 98+ / OSX.2+</td>
                                        <td class="center ">1.8</td>
                                        <td class="center ">A</td>
                                    </tr>
                                    <tr class="gradeA even">
                                        <td class="sorting_1">Gecko</td>
                                        <td class=" ">Mozilla 1.0</td>
                                        <td class=" ">Win 95+ / OSX.1+</td>
                                        <td class="center ">1</td>
                                        <td class="center ">A</td>
                                    </tr>
                                    </tbody>
                                </table>
                                <div class="row">
                                    <div class="col-sm-6">
                                        <div class="dataTables_info" id="dataTables-example_info" role="alert"
                                             aria-live="polite" aria-relevant="all">Showing 1 to 10 of 57 entries
                                        </div>
                                    </div>
                                    <div class="col-sm-6">
                                        <div class="dataTables_paginate paging_simple_numbers"
                                             id="dataTables-example_paginate">
                                            <ul class="pagination">
                                                <li class="paginate_button previous disabled"
                                                    aria-controls="dataTables-example" tabindex="0"
                                                    id="dataTables-example_previous"><a href="#123">Previous</a></li>
                                                <li class="paginate_button active" aria-controls="dataTables-example"
                                                    tabindex="0"><a href="#">1</a></li>
                                                <li class="paginate_button " aria-controls="dataTables-example"
                                                    tabindex="0"><a href="#">2</a></li>
                                                <li class="paginate_button " aria-controls="dataTables-example"
                                                    tabindex="0"><a href="#">3</a></li>
                                                <li class="paginate_button " aria-controls="dataTables-example"
                                                    tabindex="0"><a href="#">4</a></li>
                                                <li class="paginate_button " aria-controls="dataTables-example"
                                                    tabindex="0"><a href="#">5</a></li>
                                                <li class="paginate_button " aria-controls="dataTables-example"
                                                    tabindex="0"><a href="#">6</a></li>
                                                <li class="paginate_button next" aria-controls="dataTables-example"
                                                    tabindex="0" id="dataTables-example_next"><a href="#">Next</a></li>
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