import React from 'react';
// import styled from 'styled-components';

class StartGameForm extends React.Component {
    constructor (props) {
        super(props);

        this.state = {
            email: '',
            password: '',
            name: '',
            characterName: ''
        };

        this.handleFieldChange = this.handleFieldChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleFieldChange (e) {
        const fieldName = e.target.name;
        const fieldValue = e.target.value;

        this.setState({
            [fieldName]: fieldValue
        });
    }

    handleSubmit (e) {
        // const { handleStartGame } = this.props;
        
        e.preventDefault();

        this.props.onSubmit({
            ...this.state
        });
    }

    render () {
        const { email, password, name, characterName } = this.state;

        return (
            <form onSubmit={this.handleSubmit}>
                <div style={{display: "none"}}>
                <ul>
                    <a href="/oauth/bitbucket">Login with Bitbucket</a><br />
                    <a href="/oauth/facebook">Login with Facebook</a><br />
                    <a href="/oauth/github">Login with Github</a><br />
                    <a href="/oauth/google">Login with Google</a><br />
                    <a href="/oauth/twitter">Login with Twitter</a><br />
                </ul>
                </div>

                <h4>Create character or login with existing:</h4>
                E-mail (unique):
                <div>
                    <input type="text"
                        name="email"
                        placeholder="E-mail"
                        id="email"
                        value={email}
                        required
                        autoFocus
                        onChange={this.handleFieldChange} />
                </div>
                <br />
                Password:
                <div>
                    <input type="text"
                        name="password"
                        placeholder="Password"
                        id="password"
                        value={password}
                        required
                        onChange={this.handleFieldChange} />
                </div>
                <br />
                Your name:
                <div>
                    <input type="text"
                        name="name"
                        placeholder="Name"
                        id="name"
                        value={name}
                        required
                        onChange={this.handleFieldChange} />
                </div>
                <br />
                Your character name:
                <div>
                    <input type="text"
                        name="characterName"
                        placeholder="Character name"
                        id="character_name"
                        value={characterName}
                        required
                        onChange={this.handleFieldChange} />
                </div>
                <br />
                <input type="submit" value="Start game!"/>
            </form>
        );
    }
};

export default StartGameForm;