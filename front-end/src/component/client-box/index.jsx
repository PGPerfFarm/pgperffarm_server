import React from 'react';
import './index.css';
import classNames from 'classnames';
class ClientBox extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            isImprove: true,
        };

    }

    render() {
        let imgSrc = require('image/client-icon/' + this.props.clientNum + '.png');
        let std = this.props.std;
        let median = this.props.median;
        let boxClass = classNames({
            'client-box': true,
            'improve': median > std,
            'decline': (median <= std)
        });

        return (
            <div className={boxClass}>
                <img src={imgSrc} alt=""/>
            </div>
        );
    }
}

export default ClientBox;