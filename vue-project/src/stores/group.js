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
            // Remove the participant from the participants array
            this.participants = this.participants.filter(p => p._id !== participant_id);
        },
        setParticipantCompleteInitial(participant_id) {
            // Find the participant and set complete_initial to true
            const participant = this.participants.find(p => p._id === participant_id);
            if (participant) {
                participant.complete_initial = true;
            }
        },
        SetParticipantReadyToVote(participant_id) {
            const participant = this.participants.find(p => p._id === participant_id);
            if (participant) {
                participant.ready_to_vote = true;
            }
        },
        clearParticipantStatus() {
            this.participants.forEach(participant => {
                participant.ready_to_vote = false;
                participant.complete_initial = false;
            });
        },
    },
});