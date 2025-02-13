import { defineStore } from 'pinia';

export const useTurnStore = defineStore('turn', {
    state: () => ({
        turn_number: 0,
        candidate_roles: null,
    }),
    actions: {
        addTurnNumber() {
            this.turn_number += 1;
        },
        setCandidateRoles(candidate_roles) {
            this.candidate_roles = candidate_roles;
        },
        clearCandidateRoles() {
            this.candidate_roles = null;
        }
    },
});