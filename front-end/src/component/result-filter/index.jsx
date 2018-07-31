import React from 'react';
import Pagination from 'util/pagination/index.jsx';
import PGUtil        from 'util/util.jsx'
const _util = new PGUtil();
import './index.css';

class ResultFilter extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            // selected_items: [
            //     {'cate': 'Category 2', 'name': '30 days'}
            // ],
            restoreNum: 0,
            branches: this.props.branches,
            isFirstMount:true,
            selected: [
                //     {
                //     'cate': 'Category 1',
                //     'index': 0,
                //     'isMultiple':false,
                //     'key': 'date',
                //     'metaData':{
                //         'name': 'All',
                //         'value': ''
                //     },
                //     'data': [
                //         {'name':'7 days', 'value':'7'},
                //         {'name':'30 days', 'value':'30'}
                //     ],
                // }
            ],

            isClear: true
        };

        this.selectItemClick = this.selectItemClick.bind(this);
        this.metaItemClick = this.metaItemClick.bind(this);
    }

    addBranchTags() {
        let obj = {
            'cate': 'Branches',
            // 'index': 0,
            'isMultiple': true,
            'key': 'branch',
            'metaData': {
                'name': 'All',
                'value': '',
                'isSelected': true
            },
            'totalSelected': 0,
            'data': [],
        }

        let branches = this.state.branches

        for (let i = 0; i < branches.length; i++) {
            let newItem = {}
            newItem['name'] = branches[i].branch_name
            newItem['value'] = branches[i].branch_name
            newItem['isSelected'] = false
            obj['data'].push(newItem)
        }

        let _list = []
        _list.push(obj)
        console.log('lets see the new selected')
        console.log(branches.length)
        console.dir(_list)
        this.setState({
            selected: _list
        });


    }

    componentWillReceiveProps(nextProps) {
        let _this = this
        this.setState({
            branches: nextProps.branches,
        }, () => {
            if(_this.state.isFirstMount){
                _this.addBranchTags();
                _this.setState({
                    isFirstMount: false,
                })
            }
        });
    }

    componentWillMount() {
        // this.addBranchTags();
    }


    metaItemClick(e) {
        console.log('metaItemClick!!', this);
        let item_name = e.currentTarget.getAttribute("data-item-name")
        let item_index = e.currentTarget.getAttribute("data-item-index")

        let cate_name = e.currentTarget.getAttribute("data-cate-name")
        let cate_index = e.currentTarget.getAttribute("data-cate-index")

        let newSelected = this.state.selected;
        newSelected[cate_index].totalSelected = 0;
        newSelected[cate_index].metaData.isSelected = true;
        for (let i = 0; i < newSelected[cate_index].data.length; i++) {
            newSelected[cate_index].data[i].isSelected = false;
        }

        this.setState({
            selected: newSelected,
            isClear: true
        });

    }

    selectItemClick(e) {
        console.log('selectItemClick!!', this);
        let item_name = e.currentTarget.getAttribute("data-item-name")
        let item_index = e.currentTarget.getAttribute("data-item-index")

        let cate_name = e.currentTarget.getAttribute("data-cate-name")
        let cate_index = e.currentTarget.getAttribute("data-cate-index")

        let newSelected = this.state.selected;
        let totalSelected = newSelected[cate_index].totalSelected
        console.log('totalSelected now is:' + totalSelected)
        newSelected[cate_index].metaData['isSelected'] = false;
        newSelected[cate_index].data[item_index]['isSelected'] = !newSelected[cate_index].data[item_index]['isSelected']

        if(newSelected[cate_index].data[item_index]['isSelected'] == true){
            //add totalSelected
            totalSelected += 1
        }else{
            if(totalSelected -1 <= 0){
                newSelected[cate_index].data[item_index]['isSelected'] = true
            }else{
                totalSelected -= 1
            }
        }
        newSelected[cate_index].totalSelected = totalSelected
        console.log('cate name is:' + cate_name)
        console.log('cate index is:' + cate_index)
        console.log('totalSelected is:' + totalSelected)
        console.log('cur index is:' + item_index)


        this.setState({
            selected: newSelected,
            isClear: true
        });

    }


    handleClick() {
        console.log('handleClick!!', this);
        let self = this;
    }

    getSelectedBranches(){
        let metaData = this.state.selected[0].metaData
        if(metaData.isSelected == true && this.state.selected[0].totalSelected == 0){
            return []
        }
        return this.state.selected[0].data
    }
    // getFilterParams() {
    //     let params_list = this.state.selected;
    //     let result = {};
    //     for (let i = 0; i < params_list.length; i++) {
    //         let params_item = params_list[i];
    //         console.log('cur filter index is:' + params_item.index)
    //         let value = params_item.data[params_item.index]['value']
    //         let key = params_item.key;
    //         if (value) {
    //             console.log('key is:' + key)
    //             if (key == 'date') {
    //                 result[key] = _util.getDateStr(value * -1)
    //             } else {
    //                 result[key] = value
    //             }
    //
    //         }
    //
    //     }
    //     return result
    // }

    applyButtonClick() {
        this.setState({
            // selected: newArr,
            isClear: false
        });
        this.props.onIsLoadingChange(true);
        let branches = this.getSelectedBranches()

        console.dir(branches)
        this.props.onApplyBtnClick(branches);
        // console.log('isLoading:' + this.props.isLoading)

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
        console.log('look')
        console.dir(this.state.selected)
        console.log('look done')
        let filter = this.state.selected.map((item, i) => {
            let meta_item
            let filter_items
            let is_high_light = item["metaData"].isSelected == true ? "select-all selected" : "select-all"
            meta_item = (
                <dd onClick={(e) => this.metaItemClick(e)} data-cate-name={item["cate"]}
                    data-cate-index={i} data-item-name='meta' className={is_high_light}><a
                    href="javascript:void(0);">{item["metaData"]['name']}</a></dd>
            )


            if (item.isMultiple) {
                filter_items = item["data"].map((s, index) => {
                    let is_high_light = s['isSelected'] == true ? "select-all selected" : "select-all"
                    let filter_tag = (
                        <dd onClick={(e) => this.selectItemClick(e)} key={index} data-cate-name={item["cate"]}
                            data-cate-index={i} data-item-index={index} data-item-name={s}
                            className={is_high_light}><a
                            href="javascript:void(0);">{s['name']}</a></dd>
                    )


                    return filter_tag
                });
            } else {
                //todo
            }


            return (
                <li className="select-list" item={item} key={i} data-cate-name={item["cate"]} data-cate-index={i}>
                    <dl data-is-multiple={item.isMultiple} data-cate-name={item["cate"]} data-cate-index={i}>
                        <dt data-cate-name={item["cate"]}>{item["cate"]}:</dt>
                        {meta_item}
                        {filter_items}
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

                                    {/*<a className="btn btn-default btn-sm title-selected-btn" href="javascript:void(0)"*/}
                                       {/*onClick={() => this.resetButtonClick()}*/}
                                       {/*disabled={ this.state.isClear ? "" : "disabled" }>*/}
                                        {/*<i className="fa fa-cog"></i> Reset</a>*/}

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