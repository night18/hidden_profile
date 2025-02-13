import { defineStore } from 'pinia';
import { set } from 'vue-demi';

export const useCandidateProfileStore = defineStore('candidate_profile', {
    state: () => ({
        // This should store the candidates' profile data as a list of objects.
        candidate_profiles: null,
    }),
    actions: {
        initialCandidateProfiles() {
            this.candidate_profiles = null;
        },
        setCandidateProfiles(candidate_profiles) {
            this.candidate_profiles = candidate_profiles;
        },
    },

});