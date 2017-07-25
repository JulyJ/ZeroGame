import React from 'react';
import {
    Route,
    BrowserRouter as Router,
    Switch
} from 'react-router-dom';

import Header from './layout/header';
import { PageContainer } from './layout/common';
import IndexPage from '../pages/index';
import GamePage from '../pages/start';

import '../App.css';

const FourOFour = (props) => {
    return (<div>404</div>);
};

const Root = (props) => {
    return (
        <Router>
            <div className="App">
                <Header />

                <PageContainer>
                    <Switch>
                        <Route exact path="/" component={IndexPage} />
                        <Route path="/game" component={GamePage} />
                        <Route path="*" component={FourOFour} />
                    </Switch>
                </PageContainer>
            </div>
        </Router>
    );
}

export default Root;