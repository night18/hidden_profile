import { defineStore } from 'pinia';

export const useTurnStore = defineStore('turn', {
    state: () => ({
        turn: 0,
        role: null,
    }),
    actions: {
        addProgress() {
            this.turn += 1;
        },
        setRole(role) {
            this.role = role;
        },
        clearRole() {
            this.role = null;
        },
    },
});