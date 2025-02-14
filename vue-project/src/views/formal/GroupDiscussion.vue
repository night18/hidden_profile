<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import ChatRoom from '@/components/ChatRoom.vue';
import { useCandidateProfileStore } from '@/stores/candidate_profile';
const router = useRouter();

const selectedCandidate = ref('');
const candidateProfileStore = useCandidateProfileStore();
const candidates = candidateProfileStore.candidate_profiles;

// Sample data

</script>
<template>
  <div class="container">
    <div class="jumbotron container">
      <div class="row">
        <div class="col-md-6">
          <h2> Group Discussion </h2>
          <div class="content-area">
            <p>In this task, you will be paired with another committee member to discuss the best candidate. You will have 15 minutes to discuss the topic.</p>
            <p>Consider the attributes provided for each candidate and evaluate their qualifications based on the information presented. Remember that each attribute is equally important in the decision-making process.</p>
            <p>After you have discussed with your partner, select the candidate you believe is the best fit for the faculty position.</p>
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
        <div class="col-md-6">
          <ChatRoom />
        </div>
      </div>
    </div>
  </div>
</template>