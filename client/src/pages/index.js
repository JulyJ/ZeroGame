import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';

import StartGameForm from '../components/forms/start-game';
import { startGame } from '../actions/game';

class IndexPage extends Component {
    constructor(props) {
        super(props);

        this.state = {
            fireRedirect: false
        };

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(data) {
        const { handleStartGame } = this.props;

        this.setState({ fireRedirect: true }, () => {
            handleStartGame(data.name, data.email, data.characterName);
        });
    }

    render() {
        const { fireRedirect } = this.state;

        return (
            <div>
                <StartGameForm onSubmit={this.handleSubmit} />

                {fireRedirect &&
                    <Redirect push={true} to="/game" />}
            </div>
        );
    }
};

const mapStateToProps = () => {
    return {};
};
const mapDispatchToProps = (dispatch) => {
    return {
        handleStartGame: (name, email, characterName) => {
            dispatch(startGame(name, email, characterName));
        }
    };
};

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(IndexPage);
