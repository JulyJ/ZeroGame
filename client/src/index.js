import React from 'react';
import ReactDOM from 'react-dom';
import {
    Route,
    BrowserRouter as Router,
    Switch,
    Redirect
} from 'react-router-dom';
import registerServiceWorker from './registerServiceWorker';
import './App.css';

import RootComponent from './components/root';
import Header from './components/layout/header';
import { PageContainer } from './components/layout/common';
import IndexPage from './pages/index';
import GamePage from './pages/start';

const FourOFour = (props) => {
    return (<div>404</div>);
};

ReactDOM.render(
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
    </Router>, document.getElementById('root'));
registerServiceWorker();
