import { defineStore } from 'pinia';

export const useParticipantStore = defineStore('participant', {
    state: () => ({
        participant_id: null,
        group_id: null,
    }),
    actions: {
        setParticipantId(id) {
            this.participant_id = id;
        },
        clearParticipantId() {
            this.participant_id = null;
        },
        setGroupId(id) {
            this.group_id = id;
        },
        clearGroupId() {
            this.group_id = null;
        },
    }
});