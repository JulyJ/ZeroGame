import * as gameActions from '../actions/game';

const initialState = {
    name: '',
    characterName: '',
    email: ''
};

const gameReducer = (state = initialState, action) => {
    switch (action.type) {
        case gameActions.START_GAME:
            return {
                ...state,
                name: action.name,
                characterName: action.characterName,
                email: action.email
            }
        default:
            return state;
    }
}

export default gameReducer;