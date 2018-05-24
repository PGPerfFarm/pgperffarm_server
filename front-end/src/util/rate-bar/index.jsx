import React        from 'react';

import echarts from 'echarts/lib/echarts';
// import  'echarts/lib/chart/line';
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/grid'
import 'echarts/lib/chart/bar'

import 'echarts/lib/component/title';
import lineChart from './lineChart';

// import { pieOption, barOption, lineOption, scatterOption, mapOption, radarOption, candlestickOption } from './optionConfig/options'
// const BarReact = asyncComponent(() => import(/* webpackChunkName: "BarReact" */'./EchartsDemo/BarReact')) // bar component


// General rate bar
class RateBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {

        }
    }

    componentDidMount() {
        // init echarts
        let myChart = echarts.init(document.getElementById('main'));
        let option = {
            tooltip : {
                trigger: 'axis',
                axisPointer : {
                    type : 'shadow'
                }
            },
            legend: {
                data: ['std', 'current']
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis:  {
                type: 'value'
            },
            yAxis: {
                type: 'category',
                data: ['2 clients','4 clients']
            },
            series: [
                {
                    name: 'std',
                    type: 'bar',
                    stack: 'current',
                    label: {
                        normal: {
                            show: true,
                            position: 'insideRight'
                        }
                    },
                    data: [320, 302]
                },
                {
                    name: 'std',
                    type: 'bar',
                    stack: 'current',
                    label: {
                        normal: {
                            show: true,
                            position: 'insideRight'
                        }
                    },
                    data: [120, 132]
                },
            ]
        };

        myChart.setOption(option);


    }
    render() {
        return (
            <div id="main" style={{ width: 400, height: 400 }}></div>
        );
    }
}

export default RateBar;