import { defineStore } from 'pinia';

export const useGroupStore = defineStore('group', {
    state: () => ({
        participants: [],
    }),
    actions: {
        initialParticipants(participants) {
            this.participants = participants;
        },
        addParticipant(participant) {
            this.participants.push(participant);
        },
        removeParticipant(participant) {
            this.participants = this.participants.filter(p => p.id !== participant.id);
        },
    },
});