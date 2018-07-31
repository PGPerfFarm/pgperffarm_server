import React from 'react';

import NavTop from 'component/nav-top/index.jsx';
import './index.css';
import {Image, Card, Button, List, Icon} from 'semantic-ui-react'
class FarmerDetailCard extends React.Component {
    constructor(props){
        super(props);
    }
    render(){
        let machine = this.props.machine || {}
        let branch_num = this.props.branch_num || 0
        let system = machine.os_name + ' ' + machine.os_version;
        let camp = machine.comp_name + ' ' + machine.comp_version;
        let owner = machine.owner || {};
        return (

            <div className="farmer-card">
                <Card>
                    <Card.Content>
                        <Image floated='right' size='mini'
                               src={machine.avatar}/>
                        <Card.Header>Owner: {owner.username}</Card.Header>
                        <Card.Meta>report num: {machine.reports}</Card.Meta>
                        <Card.Description>
                            <List>
                                <List.Item icon='computer' content={system} />
                                <List.Item icon='microchip' content={camp} />
                                <List.Item
                                    icon='mail'
                                    content={<a href={owner.email}>{owner.email}</a>}
                                />
                            </List>
                        </Card.Description>
                    </Card.Content>
                    <Card.Content extra className='flex-box'>

                        <div className='ui buttons'>
                            {/*todo link to machine page*/}
                                <Button basic mini color='grey'>
                                    {branch_num} branches involved
                                </Button>
                        </div>
                    </Card.Content>
                </Card>
            </div>
        );
    }
}export default FarmerDetailCard;

