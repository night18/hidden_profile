import { defineStore } from 'pinia';

export const useGroupStore = defineStore('group', {
    state: () => ({
        participants: [],
    }),
    actions: {
        initialParticipants(participants) {
            this.participants = participants;
        },
        addParticipant(participant_id) {
            this.participants.push(participant_id);
        },
        removeParticipant(participant_id) {
            this.participants = this.participants.filter(p => p !== participant_id);
        },
    },
});