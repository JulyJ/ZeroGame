export const startGame = (email, name, characterName) => {
    fetch('http://localhost:8080/start', {
        data: {
            email,
            name,
            character_name: characterName
        }
    });
}