export const START_GAME = 'START_GAME';
export const USER_DATA_RECEIVED = 'USER_DATA_RECEIVED';
export const MESSAGE_RECEIVED = 'MESSAGE_RECEIVED';

export const startGame = (name, email, characterName) => {
    return {
        type: START_GAME,
        name,
        email,
        characterName 
    }
};

export const userDataReceived = (userData) => {
    return {
        type: USER_DATA_RECEIVED,
        userData
    }
};

export const messageReceived = (message) => {
    return {
        type: MESSAGE_RECEIVED,
        message
    }
};