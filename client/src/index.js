import React from 'react';
import ReactDOM from 'react-dom';
import {
    Route,
    BrowserRouter as Router,
    Switch,
    Redirect
} from 'react-router-dom';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import './index.css';

import RootComponent from './components/root';
import GamePage from './pages/start';

const FourOFour = (props) => {
    return (<div>404</div>);
};

ReactDOM.render(
    <Router>
        <div>
            <Switch>
                <Route exact path="/" component={App} />
                <Route path="/game" component={GamePage} />
                <Route path="*" component={FourOFour} />
            </Switch>
        </div>
    </Router>, document.getElementById('root'));
registerServiceWorker();
