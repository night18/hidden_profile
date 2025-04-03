<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import ChatRoom from '@/components/ChatRoom.vue';
import { useCandidateProfileStore } from '@/stores/candidate_profile';
import CountdownTimer from '@/components/CountdownTimer.vue';
import CandidateTable from '@/components/CandidateTable.vue';

const router = useRouter();

const selectedCandidate = ref('');
const candidateProfileStore = useCandidateProfileStore();
const candidates = candidateProfileStore.candidate_profiles;

const showCandidateTable = ref(false);

const toggleCandidateTable = () => {
  showCandidateTable.value = !showCandidateTable.value;
};

const closeCandidateTable = () => {
  showCandidateTable.value = false;
};

const showCandidateSelection = ref(false);

const ready = () => {
  showCandidateSelection.value = true;
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

onMounted(() => {
  const cleanup = disableCopyPaste();
  onUnmounted(cleanup);
});
</script>
<template>
  <div class="container">
    <div class="timer">
      <b>Time Remaining</b>
      <CountdownTimer :remain_time="900" />
    </div>
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
              <button class="close-button" @click="closeCandidateTable">x</button>
              <CandidateTable v-if="candidateProfileStore.candidate_profiles !== null" :candidates="candidateProfileStore.candidate_profiles" />
            </div>
            <div v-if="!showCandidateSelection" class="ready-area">
              <p>If you have fully discussed with other search committee members, please click the ready to vote button.</p>
              <button class="btn btn-primary btn-lg" @click="ready">Ready to Vote</button>
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
                  class="form-check-input"
                  v-model="selectedCandidate" />
                <label :for="'candidate' + index">
                  {{ candidate.name }}
                </label>
              </div>
              <button class="btn btn-primary btn-lg" style="margin-top: 10px;" @click="submit">Vote for the Best Candidate</button>
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

.close-button {
  position: absolute;
  top: 5px;
  right: 5px;
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
}
</style>