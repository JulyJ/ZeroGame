export const connectToGameServer = (name, email, characterName) => {
    return fetch('http://localhost:8080/client_start', {
        method: 'post',
        mode: 'cors',
        credentials: true,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email,
            name,
            character_name: characterName
        })
    }).then((res) => res.json());
}