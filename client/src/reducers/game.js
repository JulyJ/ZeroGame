import * as gameActions from '../actions/game';

const initialState = {
    id: null,
    name: '',
    characterName: '',
    email: '',
    messages: []
};

const gameReducer = (state = initialState, action) => {
    switch (action.type) {
        case gameActions.START_GAME:
            return {
                ...state,
                name: action.name,
                characterName: action.characterName,
                email: action.email
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
        default:
            return state;
    }
}

export default gameReducer;