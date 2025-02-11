import { defineStore } from 'pinia';

export const useProgressStore = defineStore('progress', {
    state: () => ({
        progress: 0,
    }),
    actions: {
        addProgress(progress) {
            this.progress += progress;
        }
    },
});