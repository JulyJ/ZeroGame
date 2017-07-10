import React from 'react';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';

import { connectToGameServer, connectWebsocket, disconnectWebsocket } from '../services/game';
import { STOP_JOURNEY, userDataReceived, messageReceived } from '../actions/game';
import GameMessages from '../components/game/game-messages';

class StartPage extends React.Component {
    constructor (props) {
        super(props);

        this.state = {
            isLoading: true,
            fireRedirect: false
        };

        this.handleStopJourney = this.handleStopJourney.bind(this);
    }

    handleStopJourney () {
        const { onJourneyStop } = this.props;

        this.setState({
            fireRedirect: true,
        }, () => {
            onJourneyStop();
        });
        disconnectWebsocket();
    }

    async componentDidMount () {
        const {
            name,
            email,
            characterName,
            onUserDataReceived,
            onMessageReceived
        } = this.props;
 
        try {
            const userData = await connectToGameServer(name, email, characterName);
            onUserDataReceived(userData);

            connectWebsocket(userData, onMessageReceived);
        } catch (err) {
            console.error(err);

        }
        
        this.setState({
            isLoading: false
        });
    }

    renderLoading () {
        return (
            <div>
                Loading...
            </div>
        );
    }

    render () {
        const {
            id,
            name,
            email,
            characterName
        } = this.props;

        const { isLoading } = this.state;
        
        if (isLoading) {
            return this.renderLoading();
        }

        const { fireRedirect } = this.state;

        return (
            <div>
                Let the journey begin, {name}!
                <div>
                    <button onClick={this.handleStopJourney}>
                        Stop Journey
                    </button>
                </div>
                <GameMessages />
                <div>
                {fireRedirect &&
                    <Redirect push={true} to="/" />}
                </div>

            </div>
        );
    }
};

export default connect((state) => {
    const { id, name, email, characterName } = state.game;

    return {
        id,
        name,
        email,
        characterName
    }
}, (dispatch) => {
    return {
        onUserDataReceived: (userData) => {
            dispatch(userDataReceived(userData));
        },
        onMessageReceived: (message) => {
            dispatch(messageReceived(message));
        },
        onJourneyStop: () => {
            dispatch({
                type: STOP_JOURNEY
            })
        }
    };
})(StartPage);