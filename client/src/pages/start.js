import React from 'react';
import { connect } from 'react-redux';

import { connectToGameServer } from '../services/game';

class StartPage extends React.Component {
    constructor (props) {
        super(props);
    }

    componentDidMount () {
        const {
            name,
            email,
            characterName
        } = this.props;

        connectToGameServer(name, email, characterName);
    }

    render () {
        const {
            name,
            email,
            characterName
        } = this.props;

        return (
            <div>
                Let the journey begin!

                <div>{name}</div>
                <div>{email}</div>
                <div>{characterName}</div>
            </div>
        );
    }
};

export default connect((state) => {
    const { name, email, characterName } = state.game;

    return {
        name,
        email,
        characterName
    }
}, () => {return {};})(StartPage);