import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const GameMessagesContainer = styled.div`
    margin-top: 50px;
    padding-left: 30px;
    width: 1140px;
    text-align: left;
`;

const GameMessages = (props) => {
    const { messages } = props;

    return (
        <GameMessagesContainer>
            {messages.map((message, i) => (
                <div key={i}>
                    {message}
                </div>
            ))}
        </GameMessagesContainer>
    );
};

export default connect((state) => {
    const { messages } = state.game;

    return {
        messages
    }
})(GameMessages);