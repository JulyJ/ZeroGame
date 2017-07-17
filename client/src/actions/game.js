export const START_GAME = 'START_GAME';
export const USER_DATA_RECEIVED = 'USER_DATA_RECEIVED';
export const MESSAGE_RECEIVED = 'MESSAGE_RECEIVED';
export const STOP_JOURNEY = 'STOP_JOURNEY';
export const PLAYER_LEVEL_UP = 'PLAYER_LEVEL_UP';

export const startGame = (name, email, password, characterName) => {
    return {
        type: START_GAME,
        name,
        email,
        password,
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

export const parseMessage = (data) => {
    if (data.type === 'chat') {
        return messageReceived(data);
    }

    if (data.type === 'level') {
        return {
            type: PLAYER_LEVEL_UP,
            message: data.message
        }
    }
}