import React from 'react';

import NavTop from 'component/nav-top/index.jsx';
// import SideNav from 'component/side-nav/index.jsx';
// import './index.scss';
import './theme.css';

class Layout extends React.Component {
    constructor(props){
        super(props);
    }
    render(){
        return (
            <div id="wrapper">
                <NavTop/>
                {this.props.children}
            </div>
        );
    }
}export default Layout;

