import { defineStore } from 'pinia';

export const useTurnStore = defineStore('turn', {
    state: () => ({
        total_turns: 0,
        turn_number: 0,
        candidate_roles: null,
    }),
    actions: {
        initializeTurn(total_turns) {
            this.total_turns = total_turns;
            this.turn_number = 0;
        },
        addTurnNumber() {
            this.turn_number += 1;
        },
        setCandidateRoles(candidate_roles) {
            this.candidate_roles = candidate_roles;
        },
        clearCandidateRoles() {
            this.candidate_roles = null;
        },
        isTurnFinished() {
            return this.turn_number >= this.total_turns;
        }
    },
});