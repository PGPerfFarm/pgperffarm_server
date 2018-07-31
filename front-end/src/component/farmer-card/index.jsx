import React from 'react';
import {Link}     from 'react-router-dom';
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
        let owner = machine.owner || {}
        return (

            <div className="farmer-card">
                <Card>
                    <Card.Content>
                        <Image floated='right' size='mini'
                               src={machine.avatar}/>
                        <Card.Header>Farmer: {machine.alias}</Card.Header>
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

                                <Link color='linkedin' to={'/machineInfo/' + machine.machine_sn}>
                                    <Button basic color='blue'>
                                    Other records
                                    </Button>
                                </Link>

                        </div>
                    </Card.Content>
                </Card>
            </div>
        );
    }
}export default FarmerCard;

