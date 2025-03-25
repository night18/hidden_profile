<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import CandidateTable from '@/components/CandidateTable.vue';

const router = useRouter();

const selectedCandidate = ref('');
const is_submit = ref(false);

// Sample data
const candidates = [
  {
    "name": "Candidate A",
    "Number of Courses Taught": "4",
    "Student Teaching Evaluations": "4.0/5.0",
    "Number of Peer-Reviewed Publications": "2",
    "Citation Impact": "5",
    "Service on Editorial Boards": "Yes",
    "Conference Organization Roles": "Yes",
  },
  {
    "name": "Candidate B",
    "Number of Courses Taught": "6",
    "Student Teaching Evaluations": "4.5/5.0",
    "Number of Peer-Reviewed Publications": "5",
    "Citation Impact": "10",
    "Service on Editorial Boards": "Yes",
    "Conference Organization Roles": "Yes",
  },
  {
    "name": "Candidate C",
    "Number of Courses Taught": "3",
    "Student Teaching Evaluations": "3.0/5.0",
    "Number of Peer-Reviewed Publications": "10",
    "Citation Impact": "20",
    "Service on Editorial Boards": "Yes",
    "Conference Organization Roles": "No",
  }
];

// Define highlighted cells
const highlightedCells = [
  { name: "Candidate B", attribute: "Number of Courses Taught" },
  { name: "Candidate B", attribute: "Student Teaching Evaluations" },
  { name: "Candidate C", attribute: "Number of Peer-Reviewed Publications" },
  { name: "Candidate C", attribute: "Citation Impact" },
  { name: "Candidate A", attribute: "Service on Editorial Boards" },
  { name: "Candidate C", attribute: "Service on Editorial Boards" },
  { name: "Candidate A", attribute: "Conference Organization Roles" },
];

watch(selectedCandidate, (newValue, oldValue) => {
  is_submit.value = false;
});

function submit() {
  is_submit.value = true;
}

function validationMessage() {
  if (selectedCandidate.value === 'Candidate B') {
    return 'Congratulations! You have selected the best candidate.';
  }
  return 'Your selection is not the best candidate. Please review the candidates and select the most qualified one.';
}

function next() {
  // Redirect to the next page
  router.push({ name: 'FormalInstruction' });
}

</script>
<template>
  <div class="container">
    <div class="jumbotron container">
      <h2>Qualification Task</h2>
      <div class="content-area">
        <p>You are serving on a university search committee tasked with selecting the most qualified candidate for a faculty position. You will review three candidate profiles and work with other committee members to evaluate their qualifications and make a hiring decision.</p>
        <CandidateTable :candidates="candidates" />
        <div>
          <strong>Select the best candidate:</strong>
          <div
            v-for="(candidate, index) in candidates"
            :key="index"
            class="form-check"
            >
              <input
                type="radio"
                :id="'candidate' + index"
                :value="candidate.name"
                class="form-check-input"
                :disabled="is_submit && selectedCandidate === 'Candidate B'"
                v-model="selectedCandidate" />
              <label 
                :for="'candidate' + index"
              >
                {{ candidate.name }}
              </label>
          </div>
          <button class="btn btn-primary" @click="submit" :disabled="is_submit && selectedCandidate === 'Candidate B'">
            Vote for the best candidate
          </button>
          <div v-if="is_submit">
            <div 
              class="alert mt-3" 
              :class="{ 'alert-success': selectedCandidate === 'Candidate B', 'alert-danger': selectedCandidate !== 'Candidate B' }"
              role="alert">
              {{ validationMessage() }}
            </div>
          </div>
          <div v-if="is_submit && selectedCandidate === 'Candidate B'">
            <button class="btn btn-primary btn-lg" @click="next">Start Formal Task</button>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped>
/* Add any necessary styles here */
</style>