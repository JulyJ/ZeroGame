import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import thunk from 'redux-thunk';
import { applyMiddleware, createStore, combineReducers, compose } from 'redux';

import RootComponent from './components/root';
import gameReducer from './reducers/game';

const reducers = combineReducers({
    game: gameReducer
});

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const store = createStore(
    reducers,
    composeEnhancers(applyMiddleware(thunk))
);

ReactDOM.render((
    <Provider store={store}>
        <RootComponent />
    </Provider>
), document.getElementById('root'));