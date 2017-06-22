import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import logo from './logo.png';
import './App.css';

import StartGameForm from './components/forms/start-game';

class App extends Component {
  constructor (props) {
    super(props);

    this.state = {
      fireRedirect: false
    };

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit (data) {
    this.setState({fireRedirect: true});
  }

  render() {
    const { fireRedirect } = this.state;

    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to Zerogame</h2>
        </div>
        <div>
          <StartGameForm onSubmit={this.handleSubmit} />
        </div>

        {fireRedirect &&
          <Redirect to="/game" />}
      </div>
    );
  }
}

export default App;
