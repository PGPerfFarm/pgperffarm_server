import React from 'react';
import './index.css';
import {Grid, Divider, Segment, Image as ImageComponent, Item} from 'semantic-ui-react'
import TestResultCard from 'component/test-result-card/index.jsx';
import PGUtil        from 'util/util.jsx'
import Record      from 'service/record-service.jsx'
const _util           = new PGUtil();
const _record = new Record();
class DetailInfo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            recordNo: 1,
            detailInfo: {},

        }

        // this.onPageChange = this.onPageChange.bind(this);
        // this.handleIsLoading = this.handleIsLoading.bind(this);
    }

    componentDidMount(){
        this.loadDetailInfo();
    }
    // load record detail
    loadDetailInfo(){
        let listParam = {};
        listParam.recordNo = this.state.recordNo;

        _record.getRecordInfo(listParam).then(res => {
            this.setState(res);
        }, errMsg => {
            this.setState({
                list : []
            });
            _util.errorTips(errMsg);
        });
    }

    render() {
        return (
            <div id="page-wrapper">
                <div className="container row">
                    <div className="col-md-12">
                        <div className="col-md-2">
                            <TestResultCard />
                        </div>

                        <div className="col-md-10">
                            {/*<div className="card-container row">*/}
                            <div className="card-container col-md-11 col-md-offset-1">
                                <div className="col-md-5 card-div">
                                    <TestResultCard />
                                </div>

                                <div className="col-md-5 card-div">
                                    <TestResultCard />
                                </div>
                            </div>

                            <div className="info-container col-md-9 col-md-offset-1">
                                {/*<Segment>*/}
                                <Divider/>
                                <Divider horizontal>Horizontal</Divider>
                                {/*</Segment>*/}

                                <div>
                                    <h2><a href="#linuxInfo">Linux Info</a></h2>
                                    <div className="" data-example-id="">
                                        <dl>
                                            <dt><a href="#">Description lists</a></dt>
                                            <dd>A description list is perfect for defining terms.</dd>
                                            <dt>Euismod</dt>
                                            <dd>
                                            </dd>
                                            <dd></dd>
                                            <dt>Malesuada porta</dt>
                                            <dd>Etiam porta sem malesuada magna mollis euismod.</dd>
                                        </dl>
                                    </div>
                                </div>

                            </div>

                        </div>
                    </div>
                </div>

                {/*<div className="ui card">*/}
                {/*<div class="content">*/}
                {/*<div class="header">Project Timeline</div>*/}
                {/*</div>*/}
                {/*<div class="content">*/}
                {/*<h4 class="ui sub header">活动</h4>*/}
                {/*<div class="ui small feed">*/}
                {/*<div class="event">*/}
                {/*<div class="content">*/}
                {/*<div class="summary"><a>Elliot Fu</a> added <a>Jenny Hess</a> to the project </div>*/}
                {/*</div>*/}
                {/*</div>*/}
                {/*<div class="event">*/}
                {/*<div class="content">*/}
                {/*<div class="summary"><a>Stevie Feliciano</a> was added as an <a>Administrator</a> </div>*/}
                {/*</div>*/}
                {/*</div>*/}
                {/*<div class="event">*/}
                {/*<div class="content">*/}
                {/*<div class="summary"><a>Helen Troy</a> added two pictures </div>*/}
                {/*</div>*/}
                {/*</div>*/}
                {/*</div>*/}
                {/*</div>*/}
                {/*<div class="extra content">*/}
                {/*<button class="ui button">Join Project</button>*/}
                {/*</div>*/}
                {/*</div>*/}

            </div>
        )
    }
}

export default DetailInfo;