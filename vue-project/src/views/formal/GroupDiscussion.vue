<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import ChatRoom from '@/components/ChatRoom.vue';
import { useCandidateProfileStore } from '@/stores/candidate_profile';
import { useParticipantStore } from '@/stores/participant';
import { useTurnStore } from '@/stores/turn';
import { useChatStore } from '@/stores/chat';
import { useGroupStore } from '@/stores/group';
import CountdownTimer from '@/components/CountdownTimer.vue';
import CandidateTable from '@/components/CandidateTable.vue';
import Swal from 'sweetalert2';
import axios from 'axios';

const router = useRouter();

const participantStore = useParticipantStore();
const candidateProfileStore = useCandidateProfileStore();
const turnStore = useTurnStore();
const chatStore = useChatStore();
const groupStore = useGroupStore();

// Candidate Related Variables
const candidates = candidateProfileStore.candidate_profiles;
const selectedCandidate = ref('');

// Display Related Variables
const showCandidateTable = ref(false); // Display  the floadting window
const showCandidateSelection = ref(false); // Display the candidate selection
const isReady = ref(false); // Track if the participant is ready to vote
const isSubmitting = ref(false); // Track submission state
const countdownFinished = ref(false); // Track if the countdown is finished
const countdownTime = ref(120); // Countdown time in seconds

const toggleCandidateTable = () => {
  showCandidateTable.value = !showCandidateTable.value;
};

const closeCandidateTable = () => {
  showCandidateTable.value = false;
};

const ready = () => {
  isReady.value = true;
  chatStore.sendMessage({
    type: 'ready_to_vote',
    sender: participantStore.participant_id,
    turn_number: turnStore.turn_number,
  });
};

const submit = () => {
  if (selectedCandidate.value === '') {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Please select a candidate before submitting.',
    });
    return;
  }

  isSubmitting.value = true;
  let body = new FormData();
  body.append('participant_id', participantStore.participant_id);
  body.append('turn_number', turnStore.turn_number);
  body.append('selected_candidate', selectedCandidate.value);
  axios.post('/final_decision/', body)
    .then((response) => {
      if (response.status !== 200) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Failed to submit your vote.',
        });
        isSubmitting.value = false;
        return;
      }
      // Send a message to the chat room to let other participants know the candidate has selected
      chatStore.sendMessage({
        type: 'complete_final',
        sender: participantStore.participant_id,
        turn_number: turnStore.turn_number,
      });
    })
    .catch(() => {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'An error occurred while submitting your vote.',
      });
      isSubmitting.value = false;
    });
};

// Disable copy-paste functionality
const disableCopyPaste = () => {
  const preventAction = (event) => event.preventDefault();
  document.addEventListener('copy', preventAction);
  document.addEventListener('cut', preventAction);
  document.addEventListener('paste', preventAction);

  return () => {
    document.removeEventListener('copy', preventAction);
    document.removeEventListener('cut', preventAction);
    document.removeEventListener('paste', preventAction);
  };
};

const startCountdown = () => {
  setTimeout(() => {
    countdownFinished.value = true;
  }, countdownTime.value * 1000); // Convert seconds to milliseconds
};

onMounted(() => {
  startCountdown();
  const cleanup = disableCopyPaste();
  onUnmounted(cleanup);

  watch(() => groupStore.participants, (newVal) => {
    if (newVal.length === 0) {
      return;
    }
    const allReady = newVal.every((participant) => participant.ready_to_vote);
    if (allReady) {
      showCandidateSelection.value = true;
    }

    const allComplete = newVal.every((participant) => participant.complete_final);
    if (allComplete) {
      turnStore.addTurnNumber();
      groupStore.clearParticipantStatus()
      if (turnStore.isTurnFinished()) {
        // Close the chat room
        chatStore.closeWebSocket();
        router.push( {name: 'PostSurvey'} );
      } else {
        router.push( {name: 'FormalCandidate' } );
      }
    }
  }, { deep: true });

  // Listen for messages from the chat room
  chatStore.on('ready_to_vote', (data) => {
    if (data.turn_number !== turnStore.turn_number) {
      return;
    }
    // Set the participant is ready
    groupStore.setParticipantReadyToVote(data.sender);
  });

  chatStore.on('complete_final', (data) => {
    if (data.turn_number !== turnStore.turn_number) {
      return;
    }
    // Set the participant is ready
    groupStore.setParticipantCompleteFinal(data.sender);
  });

});
</script>
<template>
  <div class="container">
    <div class="jumbotron container">
      <div class="row">
        <div class="col-md-6">
          <h2> Group Discussion </h2>
          <div class="content-area">
            <p>In this task, you will be paired with committee members to discuss the best candidate. You will have 15 minutes to discuss the topic.</p>
            <p>Consider the attributes provided for each candidate and evaluate their qualifications based on the information presented. Remember that each attribute is equally important in the decision-making process.</p>
            
            <p>
              <button
                class="btn btn-secondary"
                @click="toggleCandidateTable"
              >
                Check candidate profile
            </button>
            </p>
            <div
              v-if="showCandidateTable"
              class="floating-table"
            >
              <div class="floating-table-header">
                <div class="row">
                  <div class="col-11">
                    Candidate Profiles
                  </div>
                  <div class="col-1 text-end">
                    <button class="close-button" @click="closeCandidateTable">X</button>
                  </div>
                </div>
              </div>
              <div class="floating-table-content">
                <CandidateTable v-if="candidateProfileStore.candidate_profiles !== null" :candidates="candidateProfileStore.candidate_profiles" />
              </div>
            </div>
            <div v-if="!showCandidateSelection" class="ready-area">
              <p>You must discuss with the other search committee members for at least 2 minutes. Once you have fully discussed, please click the 'Ready to Vote' button.</p>
              <button class="btn btn-primary btn-lg" @click="ready" :disabled="!countdownFinished || isReady">
                <span v-if="!countdownFinished">
                  <CountdownTimer :remain_time="countdownTime" />
                </span>
                <span v-else-if="isReady">
                  Waiting other committees 
                  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                </span>
                <span v-else>
                  Ready to Vote
                </span>
              </button>
            </div>
            <div v-if="showCandidateSelection">
              <p>Please elect the candidate you believe is the best fit for the faculty position.</p>
              <div
                v-for="(candidate, index) in candidates"
                :key="index"
                class="form-check"
              >
                <input
                  type="radio"
                  :id="'candidate' + index"
                  :value="candidate._id"
                  :name="candidate.name"
                  class="form-check-input"
                  v-model="selectedCandidate" />
                <label :for="'candidate' + index">
                  {{ candidate.name }}
                </label>
              </div>
              <button
                class="btn btn-primary btn-lg"
                style="margin-top: 10px;"
                @click="submit"
                :disabled="isSubmitting"
              >
                <span v-if="isSubmitting">Waiting other committees
                  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                </span>
                <span v-if="!isSubmitting">Vote</span>
              </button>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <ChatRoom />
        </div>
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

.floating-table {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  padding: 10px;
}

.floating-table-header {
  display: block;
  border-bottom: 1px solid #ccc;
}

.close-button {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
}

.floating-table-content {
  padding: 10px;
  max-height: 70vh;
  overflow-y: auto;
}


</style>