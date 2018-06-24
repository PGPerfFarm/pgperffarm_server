import React from 'react';

import './index.css';
import {List, Item} from 'semantic-ui-react'
class InfoList extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let info = this.props.info
        let name = this.props.name
        let _list = Object.keys(info).map(key => {
            let _list2 = 0
            return (
                <List.Item as='li'>
                    <h3>{key}</h3>
                    <List.List as='ul'>
                        <List.Item className="clear-list-style" >{info[key]}</List.Item>
                    </List.List>
                </List.Item>
            );
        });
        return (
            <List className='info-list' as='ul'>

                <List.Item as='li'>
                    <h2>{name} Info</h2>
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

