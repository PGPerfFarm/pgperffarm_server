import React from 'react';

import NavTop from 'component/nav-top/index.jsx';
// import './index.css';
import {Image, Card, Button, List, Icon} from 'semantic-ui-react'
class FarmerCard extends React.Component {
    constructor(props){
        super(props);
    }
    render(){
        let machine = this.props.machine
        let system = machine.os_name + ' ' + machine.os_version;
        let camp = machine.comp_name + ' ' + machine.comp_version;
        return (

            <div className="farmer-card">
                <Card>
                    <Card.Content>
                        <Image floated='right' size='mini'
                               src='http://www.semantic-ui.cn/images/avatar2/small/lena.png'/>
                        <Card.Header>Farmer: {machine.alias}</Card.Header>
                        <Card.Meta>report num: {machine.reports}</Card.Meta>
                        <Card.Description>
                            <List>
                                <List.Item icon='computer' content={system} />
                                <List.Item icon='microchip' content={camp} />
                                <List.Item
                                    icon='mail'
                                    content={<a href={machine.owner}>{machine.owner}</a>}
                                />
                            </List>
                        </Card.Description>
                    </Card.Content>
                    <Card.Content extra>
                        <div className='ui buttons'>
                            {/*todo link to machine page*/}
                            <Button basic color='blue'>
                                Other records
                            </Button>
                        </div>
                    </Card.Content>
                </Card>
            </div>
        );
    }
}export default FarmerCard;

