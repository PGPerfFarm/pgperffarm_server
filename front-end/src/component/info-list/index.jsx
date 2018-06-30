import React from 'react';

import './index.css';
import {List, Item, Accordion} from 'semantic-ui-react'
class InfoList extends React.Component {
    constructor(props) {
        super(props);
    }

    scrollToAnchor(anchorName) {
        if (anchorName) {
            let anchorElement = document.getElementById(anchorName);
            if (anchorElement) {
                anchorElement.scrollIntoView();
            }
        }
    }

    render() {
        let info = this.props.info
        let name = this.props.name
        let _list = []
        React.Children.forEach(Object.keys(info), (child, i) => {
            // console.log('child: ' + i)
            let Item
            if(info[child].length >= 300) {
                console.log(child+' is too long')

                let panel =[{
                    title: child,
                    content: info[child],
                }]

                 Item = (
                    <List.Item className='clear-list-style' key={i} value='-'>
                        <Accordion className='pre' defaultActiveIndex={[0, 0]} panels={panel} exclusive={false} fluid />

                        {/*<a href='javascript:void(0)' id={'' + child} onClick={() => this.scrollToAnchor('' + child)}>*/}
                            {/*<h3>{'' + child}301</h3></a>*/}
                        {/*/!*<h3>{key}</h3>*!/*/}
                        {/*<List.List as='ul'>*/}
                            {/*<List.Item className="clear-list-style pre">{info[child]}</List.Item>*/}
                        {/*</List.List>*/}

                    </List.Item>
                )
            }else{
                 Item = (
                    <List.Item as='li' key={i}>
                        <a href='javascript:void(0)' id={'' + child} onClick={() => this.scrollToAnchor('' + child)}>
                            <h3>{'' + child}</h3></a>
                        {/*<h3>{key}</h3>*/}
                        <List.List as='ul'>
                            <List.Item className="clear-list-style pre">{info[child]}</List.Item>
                        </List.List>
                    </List.Item>
                )
            }


            _list.push({
                key: `label${i}`,
                value: Item
            })
        })

        const itemComponents = _list.map(item => {
            return <div key={item.key}>{item.value}</div>
        })

        return (
            <List className='info-list' as='ul'>

                <List.Item as='li'>

                    <a href='javascript:void(0)' id={name + 'Info'} onClick={() => this.scrollToAnchor(name + 'Info')}>
                        <h2>{name} Info</h2></a>
                    <List.List as='ul'>

                        {itemComponents}
                        {/*<List.Item as='li'>*/}
                        {/*<a href='#'>Link to somewhere</a>*/}
                        {/*</List.Item>*/}
                        {/*<List.Item as='li'>Rebates</List.Item>*/}


                    </List.List>

                </List.Item>
            </List>
        );
    }
}
export default InfoList;

