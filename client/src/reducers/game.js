import * as gameActions from '../actions/game';

const initialState = {
    messages: [],

    id: null,
    name: '',
    characterName: '',
    email: '',
    password: '',
    playerLevel: '...'
};

const gameReducer = (state = initialState, action) => {
    switch (action.type) {
        case gameActions.START_GAME:
            return {
                ...state,
                name: action.name,
                characterName: action.characterName,
                email: action.email,
                password: action.password
            };
        case gameActions.USER_DATA_RECEIVED:
            return {
                ...state,
                id: action.userData.id
            };
        case gameActions.MESSAGE_RECEIVED:
            return {
                ...state,
                messages: [
                    action.message,
                    ...state.messages
                ]
            };
        case gameActions.STOP_JOURNEY:
            return {
                ...initialState
            };

        case gameActions.PLAYER_LEVEL_UP:
            return {
                ...state,
                playerLevel: action.message
            };

        default:
            return state;
    }
}

export default gameReducer;