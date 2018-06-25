import React from 'react';

import './index.css';
import {List, Item} from 'semantic-ui-react'
class InfoList extends React.Component {
    constructor(props) {
        super(props);
    }

    scrollToAnchor(anchorName)  {
        if (anchorName) {
            let anchorElement = document.getElementById(anchorName);
            if(anchorElement) { anchorElement.scrollIntoView(); }
        }
    }

    render() {
        let info = this.props.info
        let name = this.props.name
        let _list = Object.keys(info).map(key => {
            let _list2 = 0
            return (
                <List.Item as='li'>
                    <a href='javascript:void(0)' id={'name'+key} onClick={()=>this.scrollToAnchor('name' + key)}><h3>{'name' + key}</h3></a>
                    {/*<h3>{key}</h3>*/}
                    <List.List as='ul'>
                        <List.Item className="clear-list-style" >{info[key]}</List.Item>
                    </List.List>
                </List.Item>
            );
        });
        return (
            <List className='info-list' as='ul'>

                <List.Item as='li'>

                    <a href='javascript:void(0)' id={name + 'Info'} onClick={()=>this.scrollToAnchor(name + 'Info')}><h2>{name} Info</h2></a>
                    <List.List as='ul'>

                        {_list}
                        {/*<List.Item as='li'>*/}
                        {/*<a href='#'>Link to somewhere</a>*/}
                        {/*</List.Item>*/}
                        {/*<List.Item as='li'>Rebates</List.Item>*/}


                    </List.List>

                </List.Item>

                <List.Item as='li'>Warranty</List.Item>
            </List>
        );
    }
}
export default InfoList;

