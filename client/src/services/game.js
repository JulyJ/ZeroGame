export const connectToGameServer = (name, email, characterName) => {
    return fetch('http://localhost:8080/start', {
        method: 'post',
        data: {
            email,
            name,
            character_name: characterName
        }
    }).then((res) => res.json());
}