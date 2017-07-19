import React from 'react';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';

import {
    connectToGameServer,
    connectWebsocket,
    disconnectWebsocket,
    sendStartEncounterCommand
} from '../services/game';
import {
    STOP_JOURNEY,
    userDataReceived,
    messageReceived,
    parseMessage
} from '../actions/game';
import GameMessages from '../components/game/game-messages';

class StartPage extends React.Component {
    constructor (props) {
        super(props);

        this.state = {
            isLoading: true,
            fireRedirectToMainPage: false
        };

        this.handleStopJourney = this.handleStopJourney.bind(this);
    }

    redirectToMainPage () {
        this.setState({
            fireRedirectToMainPage: true
        });
    }

    handleStopJourney () {
        const { onJourneyStop } = this.props;

        this.redirectToMainPage();
        onJourneyStop();

        disconnectWebsocket();
    }

    handleStartEncounter () {

        sendStartEncounterCommand();
    }

    async componentDidMount () {
        const {
            name,
            email,
            password,
            characterName,
            onUserDataReceived,
            onMessageReceived
        } = this.props;
 
        try {
            const userDataResult = await connectToGameServer(name, email, password, characterName);
            if (userDataResult.status === 'ok') {
                onUserDataReceived(userDataResult.userData);
                connectWebsocket(userDataResult.userData, onMessageReceived);
            }
            else {
                this.redirectToMainPage();
            }
        } catch (err) {
            console.error(err);
            this.redirectToMainPage();
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
            password,
            characterName,
            playerLevel
        } = this.props;

        const { isLoading } = this.state;
        
        if (isLoading) {
            return this.renderLoading();
        }

        const { fireRedirectToMainPage } = this.state;

        return (
            <div>
                Let the journey begin, {name}!
                <div>
                    HERO LEVEL {playerLevel}
                </div>
                
                <div>
                    <button onClick={this.handleStopJourney}>
                        Stop Journey
                    </button>
                </div>
                <div>
                    <button onClick={this.handleStartEncounter}>
                        Start Encounter
                    </button>
                </div>

                <GameMessages />
                <div>
                {fireRedirectToMainPage &&
                    <Redirect push={true} to="/" />}
                </div>

            </div>
        );
    }
};

export default connect((state) => {
    const { id, name, email, password, characterName, playerLevel } = state.game;

    return {
        id,
        name,
        email,
        password,
        characterName,
        playerLevel
    }
}, (dispatch) => {
    return {
        onUserDataReceived: (userData) => {
            dispatch(userDataReceived(userData));
        },
        onMessageReceived: (message) => {

            dispatch(parseMessage(message));
        },
        onJourneyStop: () => {
            dispatch({
                type: STOP_JOURNEY
            })
        }
    };
})(StartPage);