import { useParticipantStore } from "@/stores/participant";


let webSocket = null;
let messageCallback = null;

export function getWebsocketUrl(roomId) {
    return `${import.meta.env.VITE_WS_URL}/${roomId}/`;
}


export function connectWebsocket(roomId, callback) {
    if (webSocket) return; // Avoid creating multiple connections

    const wsUrl = getWebsocketUrl(roomId);
    webSocket = new WebSocket(wsUrl);
    messageCallback = callback;

    webSocket.onopen = () => {
        console.log('WebSocket connected');
        // Send the participant ID to the server. The participant ID is stored in the Pinia store.
        // The server will use this ID to identify the participant.
        const participantStore = useParticipantStore();
        const participantId = participantStore.participant_id;
        
        webSocket.send(JSON.stringify({
            code: 100,
            participant_id: participantId
        }));
    }

    webSocket.onmessage = (event) => {
        try {
            const message = JSON.parse(event.data);
            if (messageCallback) {
                messageCallback(message);
            }
        }
        catch (error) {
            console.error('Failed to parse WebSocket message:', error);
        }
    }

    webSocket.onclose = () => {
        console.log('WebSocket closed');
        webSocket = null;
    }
}

