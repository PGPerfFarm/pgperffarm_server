import React from 'react';
import {Card, Icon} from 'semantic-ui-react'
import './index.css';

class TestResultCard extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            selected_items: [
                {'cate': 'Category 2', 'name': '30 days'}
            ],
            restoreNum: 0,
        };


        // this.selectItemClick = this.selectItemClick.bind(this);
    }



    render() {
        let description = [
            'Amy is a violinist with 2 years experience in the wedding industry.',
            'She enjoys the outdoors and currently resides in upstate New York.',
        ].join(' ');
        return (
            <div>
                <Card>
                    <Card.Content header='About Amy'/>
                    <Card.Content description={description}/>
                    <Card.Content extra>
                        <Icon name='user'/>
                        4 Friends
                    </Card.Content>
                </Card>
            </div>
        );
    }
}

export default TestResultCard;