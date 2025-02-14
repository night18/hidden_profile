<script setup>
import { ref, onMounted, watchEffect, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useParticipantStore } from '@/stores/participant';
import { useChatStore } from '@/stores/chat';
import { useTurnStore } from '@/stores/turn';
import { useGroupStore } from '@/stores/group';
import { useCandidateProfileStore } from '@/stores/candidate_profile';
import CandidateTable from '@/components/CandidateTable.vue';
import Swal from 'sweetalert2';
import axios from 'axios';

const router = useRouter();
const chatStore = useChatStore();
const participantStore = useParticipantStore();
const candidateProfileStore = useCandidateProfileStore();
const turnStore = useTurnStore();

onMounted(() => {
  console.log('FormalCandidate mounted');
    
  chatStore.on('role_assignment', (data) => {
    console.log(data);
    // Set the role of the participant
    turnStore.setCandidateRoles(data.pairs);

    // Request the candidate profiles based on the role of the participant
    let body = new FormData();
    body.append('participant_id', participantStore.participant_id);
    body.append('turn_number', turnStore.turn_number);
    axios.post('/candidate_profile_by_turn/', body)
      .then((response) => {
        if (response.status !== 200) {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to get candidate profiles',
          });
          return;
        }

        candidateProfileStore.setCandidateProfiles(response.data.candidate_profiles);
      });

  });

  chatStore.on('user_left_after_pairing', (data) => {
    // Remove the participant from the group
    useGroupStore().removeParticipant(data.participant_id);
    // Alert the user that a participant has left, say sorry to finish the task. When users click OK, they will be redirected to the Ending page.
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Sorry, a participant has left the task. Please click OK to finish the task.',
    }).then(() => {
      // router.push('/Ending');
    });
  });
  
  // Only the first participant in the participant list will send a request to the server
  if (participantStore.participant_id === useGroupStore().participants[0]) {
    if (turnStore.candidate_roles !== null) {
      return;
    }
    chatStore.sendMessage({
      type: 'role_by_turn',
      participant_id: participantStore.participant_id,
      turn_number: turnStore.turn_number,
    });
  }
});

function next() {
  router.push('/GroupDiscussion');
}



</script>
<template>
  <div class="container">
    <div class="jumbotron container">
      <h2> Formal Task</h2>
      <div class="content-area">
        <p>You are serving on a university search committee tasked with selecting the most qualified candidate for a faculty position. You will review three candidate profiles and work with other committee members to evaluate their qualifications and make a hiring decision.</p>
        <CandidateTable v-if="candidateProfileStore.candidate_profiles !== null" :candidates="candidateProfileStore.candidate_profiles" />
        
        <p>Consider the attributes provided for each candidate and evaluate their qualifications based on the information presented. Remember that each attribute is equally important in the decision-making process.</p>
        <p>After you click the next button, you <strong>cannot</strong> access the candidate profiles again. But, you could tke notes on a separate sheet of paper.</p>
        
        <button class="btn btn-primary btn-lg" @click="next">Next</button>
      </div>
    </div>
  </div>
</template>