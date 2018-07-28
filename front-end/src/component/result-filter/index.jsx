import React from 'react';
import Pagination from 'util/pagination/index.jsx';
import PGUtil        from 'util/util.jsx'
const _util = new PGUtil();
import './index.css';

class ResultFilter extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            selected_items: [
                {'cate': 'Category 2', 'name': '30 days'}
            ],
            restoreNum: 0,
            branch_list:this.props.branch_list,
            selected: [{
                'cate': 'Category 1',
                'index': 0,
                'key': 'date',
                'data': [
                    {'name':'All', 'value':''},
                    {'name':'7 days', 'value':'7'},
                    {'name':'30 days', 'value':'30'}
                ],
            }],
            // selected: [{
            //     'cate': 'Category 1',
            //     'index': 2,
            //     'data': [
            //         'All',
            //         'Improving',
            //         'Regressive'
            //     ],
            // }, {
            //     'cate': 'Category 2',
            //     'index': 1,
            //     'data': [
            //         'All',
            //         '7 days',
            //         '30 days'
            //     ],
            // }, {
            //     'cate': 'Category 3',
            //     'index': 1,
            //     'data': [
            //         'All',
            //         'item3-1',
            //         'item3-2'
            //     ],
            // }],
            isClear: true
        };


        this.selectItemClick = this.selectItemClick.bind(this);
    }

    selectItemClick(e) {
        console.log('selectItemClick!!', this);
        let item_name = e.currentTarget.getAttribute("data-item-name")
        let item_index = e.currentTarget.getAttribute("data-item-index")

        let cate_name = e.currentTarget.getAttribute("data-cate-name")
        let cate_index = e.currentTarget.getAttribute("data-cate-index")

        let newSelected = this.state.selected;
        console.log('prev index is:' + newSelected[cate_index]["index"])
        console.log('cur index is:' + item_index)
        if (newSelected[cate_index]["index"] != item_index) {
            newSelected[cate_index]["index"] = item_index;
            this.setState({
                selected: newSelected,
                isClear: true
            });
        }
    }


    handleClick() {
        console.log('handleClick!!', this);
        let self = this;
    }
    getFilterParams() {
        let params_list = this.state.selected;
        let result = {};
        for (let i = 0; i < params_list.length; i++) {
            let params_item = params_list[i];
            console.log('cur filter index is:' + params_item.index)
            let value = params_item.data[params_item.index]['value']
            let key = params_item.key;
            if (value){
                console.log('key is:' + key)
                if(key == 'date'){
                    result[key] = _util.getDateStr(value * -1)
                }else{
                    result[key] =value
                }

            }

        }
        return result
    }
    applyButtonClick() {
        this.setState({
            // selected: newArr,
            isClear: false
        });
        this.props.onIsLoadingChange(true);
        let params = this.getFilterParams()
        console.dir(params)
        this.props.onApplyBtnClick(params);
        console.log('isLoading:' + this.props.isLoading)
    }

    resetButtonClick() {
        let newArr = this.state.selected;
        newArr.forEach((_item, _index) => {
            console.log(_item);
            _item.index = this.state.restoreNum;
        })
        this.setState({
            selected: newArr,
            isClear: false
        });
    }


    render() {
        let _this = this;

        let filter = this.state.selected.map((item, i) => {

            let filter_item = item["data"].map((s, index) => {
                let is_high_light = index == item["index"] ? "select-all selected" : "select-all"
                return (
                    <dd onClick={(e) => this.selectItemClick(e)} key={index} data-cate-name={item["cate"]}
                        data-cate-index={i} data-item-index={index} data-item-name={s}
                        className={is_high_light}><a
                        href="javascript:void(0);">{s['name']}</a></dd>
                )
            });

            return (
                <li className="select-list" item={item} key={i} data-cate-name={item["cate"]} data-cate-index={i}>
                    <dl data-cate-name={item["cate"]} data-cate-index={i}>
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

        let apply_btn;
        if (this.props.isLoading == true) {
            apply_btn = (
                <a className="btn btn-primary btn-sm title-selected-btn" href="javascript:void(0)"
                   disabled={"disabled"}>
                    <i className="fa fa-spinner fa-pulse"></i> wait...</a>
            )
        } else {
            apply_btn = (
                <a className="btn btn-primary btn-sm title-selected-btn" href="javascript:void(0)"
                   onClick={() => this.applyButtonClick()}>
                    <i className="fa fa-hand-paper-o"></i> Apply</a>
            )
        }
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
                                    {/*<button data-toggle="button" className="btn btn-primary-warn title-selected-btn"*/}
                                    {/*disabled={ this.state.isClear ? "" : "disabled" } onClick={() => this.clearButtonClick()}>*/}
                                    {/*clear*/}
                                    {/*</button>*/}
                                    <a className="btn btn-default btn-sm title-selected-btn" href="javascript:void(0)"
                                       onClick={() => this.resetButtonClick()}
                                       disabled={ this.state.isClear ? "" : "disabled" }>
                                        <i className="fa fa-cog"></i> Reset</a>

                                    {apply_btn}
                                    {/*<button data-toggle="button" className="btn btn-primary title-selected-btn">apply*/}
                                    {/*</button>*/}
                                </div>
                            </div>
                        </div>
                        <div id="panel1" className="panel-collapse collapse in">

                            <div className="panel-body">
                                <ul className="selected_item">
                                    {/*{selected_item}*/}
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
            </div>
        );
    }
}

export default ResultFilter;