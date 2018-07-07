import React from 'react';
import ReactDom from 'react-dom';
import {HashRouter as Router, Route, Link, Redirect, Switch} from 'react-router-dom';
import createHistory from 'history/createHashHistory'
const history = createHistory()
import {spring, AnimatedRoute, AnimatedSwitch} from 'react-router-transition';
// layout
import Layout from 'component/layout/index.jsx'
// page
import Login from './page/login/index.jsx'
import Home from './page/home/index.jsx'

import Status from './page/status/index.jsx'
import PPolicy from './page/ppolicy/index.jsx'
import DetailInfo from './page/detailInfo/index.jsx'

import Portal from './page/portal/index.jsx'
// we need to map the `scale` prop we define below
// to the transform style property
function mapStyles(styles) {
    return {
        opacity: styles.opacity,
        transform: `scale(${styles.scale})`,
    };
}

// wrap the `spring` helper to use a bouncy config
function bounce(val) {
    return spring(val, {
        stiffness: 330,
        damping: 22,
    });
}

// child matches will...
const bounceTransition = {
    // start in a transparent, upscaled state
    atEnter: {
        opacity: 0,
        scale: 1.2,
    },
    // leave in a transparent, downscaled state
    atLeave: {
        opacity: bounce(0),
        scale: bounce(0.8),
    },
    // and rest at an opaque, normally-scaled state
    atActive: {
        opacity: bounce(1),
        scale: bounce(1),
    },
};

class App extends React.Component {
    constructor(props) {
        super(props);
    }


    render() {
        let LayoutRouter = (
            <Layout>
                    <Route exact path="/login/" component={Login}/>
                    <Route exact path="/" component={Home}/>

                    <Route exact path="/home/" component={Home}/>
                    <Route exact path="/status/" component={Status}/>
                    <Route exact path="/ppolicy/" component={PPolicy}/>

                    <Route exact path="/portal/" component={Portal}/>
                    <Route path="/detailInfo/:uuid" component={DetailInfo}/>
                    {/*<Route path="/detail/:uuid" component={DetailInfo}/>*/}
                    {/*<Redirect exact from="/order" to="/order/index"/>*/}
                    {/*<Redirect exact from="/user" to="/user/index"/>*/}
                    {/*<Route component={ErrorPage}/>*/}
            </Layout>
        );
        return (
            <Router>
                <AnimatedSwitch
                    atEnter={bounceTransition.atEnter}
                    atLeave={bounceTransition.atLeave}
                    atActive={bounceTransition.atActive}
                    mapStyles={mapStyles}
                    className="route-wrapper"
                >
                    {/*<Route path="/login" component={Login}/>*/}
                    <Route path="/" render={ props => LayoutRouter}/>
                </AnimatedSwitch>
            </Router>
        )
    }
}

ReactDom.render(
    <App />,
    document.getElementById("app")
);
