import SockJS from 'sockjs-client';

export async function connectToGameServer (name, email, password, characterName) {
    const res = await fetch('http://localhost:8080/client_start', {
        method: 'post',
        mode: 'cors',
        credentials: true,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email,
            password,
            name,
            character_name: characterName
        })
    });
    
    return res.json();
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
        const data = JSON.parse(e.data);
        
        onMessageReceived(data);
    };

    sock.onclose = function() {
        console.log('close');
    };
};

export const disconnectWebsocket = (e) => {
    if (sock != null) {
        sock.send(JSON.stringify({
            command: 'stop_journey'
        }));
        sock.close()
    }
};

export const sendStartEncounterCommand = (e) => {
    if (sock != null) {
        sock.send(JSON.stringify({
            command: 'start_encounter'
        }));
    }
};

export const sendStopEncounterCommand = (state) => {
    if (sock != null) {
        sock.send(JSON.stringify({
            command: 'stop_encounter'
        }
        ));
    }
};