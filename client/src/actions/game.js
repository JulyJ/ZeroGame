export const START_GAME = 'START_GAME';

export const startGame = (name, email, characterName) => {
    return {
        type: START_GAME,
        name,
        email,
        characterName 
    }
}