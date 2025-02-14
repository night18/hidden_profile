import { defineStore } from 'pinia';
import { useParticipantStore } from './participant';

export const useChatStore = defineStore('chat', {
  state: () => ({
    roomId: null,
    socket: null,
    eventCallbacks: {},
    messages: [],
  }),

  actions: {
    initializeWebSocket(roomId) {
      if (this.socket && this.roomId === roomId) {
        return;
      }

      this.roomId = roomId;
      const wsUrl = `${import.meta.env.VITE_WS_URL}${roomId}/`;
      
      this.socket = new WebSocket(wsUrl);

      this.socket.onopen = () => {
        console.log("WebSocket connected.");
        
        this.sendMessage({ type: "join", participant_id: useParticipantStore().participant_id });
      };

      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "message") {
          this.messages.push(data.content);
        }

        if (data.type in this.eventCallbacks) {
          this.eventCallbacks[data.type].forEach((callback) => callback(data));
        }
      };

      this.socket.onclose = () => {
        console.log("WebSocket closed.");
      }

      this.socket.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
    },
    sendMessage(data) {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(JSON.stringify(data));
      } else {
        console.error("WebSocket not connected.");
      }
    },
    on(eventType, callback) {
      if (!(eventType in this.eventCallbacks)) {
        this.eventCallbacks[eventType] = [];
      }
      this.eventCallbacks[eventType].push(callback);
    }
  }
});