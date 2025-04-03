<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useParticipantStore } from '@/stores/participant';
import { useChatStore } from '@/stores/chat';
import { useTurnStore } from '@/stores/turn';
import { useGroupStore } from '@/stores/group';
import { useCandidateProfileStore } from '@/stores/candidate_profile';
import CountdownTimer from '@/components/CountdownTimer.vue';
import CandidateTable from '@/components/CandidateTable.vue';
import Swal from 'sweetalert2';
import axios from 'axios';

const router = useRouter();
const chatStore = useChatStore();
const participantStore = useParticipantStore();
const candidateProfileStore = useCandidateProfileStore();
const turnStore = useTurnStore();
const groupStore = useGroupStore();
const selectedCandidate = ref('');
const isSubmitting = ref(false); // Track submission state

onMounted(() => {
  console.log('FormalCandidate mounted');
    
    // Only the first participant in the participant list will send a request to the server
  if (participantStore.participant_id === groupStore.participants[0]._id) {
    if (turnStore.candidate_roles !== null) {
      return;
    }
    chatStore.sendMessage({
      type: 'role_by_turn',
      participant_id: participantStore.participant_id,
      turn_number: turnStore.turn_number,
    });
  }

  chatStore.on('role_assignment', (data) => {
    console.log('role_assignment');
    console.log(data);
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

  // Deep watch whether all participants have completed the initial decision
  watch(() => groupStore.participants, (newVal) => {
    if (newVal.length === 0) {
      return;
    }
    const allComplete = newVal.every((participant) => participant.complete_initial);
    if (allComplete) {
      router.push('/GroupDiscussion');
    }
  }, { deep: true });

  // Record the partcipant who complete the initial decision
  chatStore.on('complete_initial', (data) => {
    console.log('complete_initial');
    if (data.turn_number !== turnStore.turn_number) {
      return;
    }    
    
    groupStore.setParticipantCompleteInitial(data.sender);
  });
});

function next() {
  isSubmitting.value = true; // Show spinner
  let body = new FormData();
  body.append('participant_id', participantStore.participant_id);
  body.append('turn_number', turnStore.turn_number);
  body.append('selected_candidate', selectedCandidate.value);
  axios.post('/initial_decision/', body)
    .then((response) => {
      if (response.status !== 200) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Failed to record the selected candidate',
        });
        isSubmitting.value = false; // Hide spinner on error
        return;
      }
      chatStore.sendMessage({
        type: 'complete_initial',
        sender: participantStore.participant_id,
        turn_number: turnStore.turn_number,
      });
    })
    .catch(() => {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'An error occurred while submitting your decision',
      });
      isSubmitting.value = false; // Hide spinner on error
    });
}
</script>
<template>
  <div class="container">
    <div class="timer">
      <b>Time Remaining</b>
      <CountdownTimer :remain_time="120" />
    </div>
    <div class="jumbotron container">
      <h2> Formal Task</h2>
      <div class="content-area">
        <p>You are serving on a university search committee tasked with selecting the most qualified candidate for a faculty position. You will review three candidate profiles and work with other committee members to evaluate their qualifications and make a hiring decision.</p>
        <CandidateTable v-if="candidateProfileStore.candidate_profiles !== null" :candidates="candidateProfileStore.candidate_profiles" />
        
        <p>Consider the attributes provided for each candidate and evaluate their qualifications based on the information presented. Remember that each attribute is equally important in the decision-making process.</p>
        <div
          v-if="candidateProfileStore.candidate_profiles !== null"
          v-for="(candidate, index) in candidateProfileStore.candidate_profiles"
          :key="index"
          class="form-check"
          >
            <input
              type="radio"
              :id="candidate._id"
              :value="candidate.name"
              class="form-check-input"
              v-model="selectedCandidate" />
            <label 
              :for="candidate._id"
            >
              {{ candidate.name }}
            </label>
          </div>        
        <button 
          class="btn btn-primary btn-lg" 
          @click="next" 
          :disabled="isSubmitting"
        >
          <span v-if="isSubmitting">Waiting other committees
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          </span>
          <span v-if="!isSubmitting">Submit</span>
        </button>
        <p v-if="isSubmitting" class="mt-3">Your teammates are still working on their decisions. Please wait...</p>
      </div>
    </div>
  </div>
</template>
<style scoped>
.timer {
  position: fixed;
  top: 10px;
  right: 10px;
  background-color: white;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  z-index: 1000;
}
</style>