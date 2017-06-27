import SockJS from 'sockjs-client';

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
};

let sock = null;

export const connectWebsocket = (userData, onMessageReceived) => {
    sock = new SockJS(`http://${window.location.hostname}:8080/ws`);

    sock.onopen = function(e) {
        sock.send(JSON.stringify({
            command: 'start_journey',
            command_data: userData
        }));
    };

    sock.onmessage = function(e) {
        const data = e.data;
        
        onMessageReceived(data);
    };

    sock.onclose = function() {
        console.log('close');
    };
};