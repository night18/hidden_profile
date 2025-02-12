<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useParticipantStore } from '@/stores/participant';
import { useChatStore } from '@/stores/chat';
import { useTurnStore } from '@/stores/turn';
import { useCandidateProfileStore } from '@/stores/candidate_profile';
import CandidateTable from '@/components/CandidateTable.vue';

const router = useRouter();

const participantStore = useParticipantStore();
const chatStore = useChatStore();
const candidateProfileStore = useCandidateProfileStore();
const turnStore = useTurnStore();


onMounted(() => {
  // 1. Ask for the role of the participant through the channel when onMounted is called
  // 2. Based on the role provide the candidate profiles. The candidate profiles is a list. This step might combine with the first step.

  chatStore.sendMessage({
    type: 'candidate_profiles_by_turn',
    participant_id: participantStore.participant_id,
    turn: turnStore.turn,
  });

  chatStore.on('candidate_profiles', (data) => {
    console.log(data);
    turnStore.setRole(data.role);
    candidateProfileStore.initial_candidate_profiles(data.candidate_profiles);
  });
});





</script>
<template>
  <div class="container">
    <div class="jumbotron container">
      <h2> Formal Task</h2>
      <div class="content-area">
        <p>You are serving on a university search committee tasked with selecting the most qualified candidate for a faculty position. You will review three candidate profiles and work with other committee members to evaluate their qualifications and make a hiring decision.</p>
        <!-- creeate a CandidateTable that fetch candidate profile from  candidateProfileStore -->
        <CandidateTable :candidateProfiles="candidateProfileStore.candidate_profiles" />
        
        <p>Consider the attributes provided for each candidate and evaluate their qualifications based on the information presented. Remember that each attribute is equally important in the decision-making process.</p>
        <p>After you click the next button, you cannot access the candidate profiles again. But, you could tke notes on a separate sheet of paper.</p>
        
        <button class="btn btn-primary btn-lg" @click="">Next</button>
      </div>
    </div>
  </div>
</template>