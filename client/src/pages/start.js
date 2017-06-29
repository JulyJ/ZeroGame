import React from 'react';
import { connect } from 'react-redux';

import { connectToGameServer, connectWebsocket } from '../services/game';
import { userDataReceived, messageReceived } from '../actions/game';
import GameMessages from '../components/game/game-messages';

class StartPage extends React.Component {
    constructor (props) {
        super(props);

        this.state = {
            isLoading: true
        };
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

        return (
            <div>
                Let the journey begin!

                <div>{id} - {name}</div>
                <div>{email}</div>
                <div>{characterName}</div>

                <GameMessages />
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
        }
    };
})(StartPage);