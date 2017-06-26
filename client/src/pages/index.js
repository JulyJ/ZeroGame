import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';

import StartGameForm from '../components/forms/start-game';

class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            fireRedirect: false
        };

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(data) {
        this.setState({ fireRedirect: true });
    }

    render() {
        const { fireRedirect } = this.state;

        return (
            <div>
                <StartGameForm onSubmit={this.handleSubmit} />

                {fireRedirect &&
                    <Redirect to="/game" />}
            </div>
        );
    }
}

export default App;
