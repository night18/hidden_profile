<script setup>
import { ref, watch, computed } from 'vue';
import { useRouter } from 'vue-router';
import CandidateTable from '@/components/CandidateTable.vue';

const router = useRouter();

const knowledgeCheckAnswer = ref('');
const knowledgeCheckPassed = computed(() => {
  return knowledgeCheckAnswer.value.toLowerCase().trim().includes('true');
});

const selectedCandidate = ref('');
const is_submit = ref(false);

// Sample data with one-word attributes
const candidates = [
  {
    "name": "Candidate A",
    "Teaching": "Good",
    "Evaluations": "Good",
    "Publications": "Good",
    "Citations": "Average",
    "Service": "Exceptional",
    "Leadership": "Exceptional",
  },
  {
    "name": "Candidate B",
    "Teaching": "Exceptional",
    "Evaluations": "Exceptional",
    "Publications": "Average",
    "Citations": "Good",
    "Service": "Exceptional",
    "Leadership": "Exceptional",
  },
  {
    "name": "Candidate C",
    "Teaching": "Good",
    "Evaluations": "Average",
    "Publications": "Exceptional",
    "Citations": "Exceptional",
    "Service": "Exceptional",
    "Leadership": "Average",
  }
];

const allAttributes = [
  "Teaching",
  "Evaluations",
  "Publications",
  "Citations",
  "Service",
  "Leadership"
];

// Define shared attributes
const sharedAttributes = [
  "Teaching",
  "Evaluations",
  "Publications"
];

// Define private attributes for each teammate
const privateAttributes = {
  teammate1: "Citations",
  teammate2: "Service",
  teammate3: "Leadership"
};

// Helper function to generate data for a table with placeholders
const createTableData = (visiblePrivateAttr) => {
  const visibleAttrs = [...sharedAttributes, visiblePrivateAttr];
  return candidates.map(candidate => {
    const tableRow = { name: candidate.name };
    allAttributes.forEach(attr => {
      // If the attribute is visible for this teammate, show the data. Otherwise, show 'N/A'
      tableRow[attr] = visibleAttrs.includes(attr) ? candidate[attr] : 'N/A';
    });
    return tableRow;
  });
};

// Generate data for each table
const teammate1Candidates = createTableData(privateAttributes.teammate1);
const teammate2Candidates = createTableData(privateAttributes.teammate2);
const teammate3Candidates = createTableData(privateAttributes.teammate3);


// Define master list of highlighted cells
const highlightedCells = ref([]);

// Create filtered highlight lists for each teammate
const teammate1Highlights = computed(() => {
  const visibleAttrs = [...sharedAttributes, privateAttributes.teammate1];
  return highlightedCells.value.filter(cell => visibleAttrs.includes(cell.attribute));
});

const teammate2Highlights = computed(() => {
  const visibleAttrs = [...sharedAttributes, privateAttributes.teammate2];
  return highlightedCells.value.filter(cell => visibleAttrs.includes(cell.attribute));
});

const teammate3Highlights = computed(() => {
  const visibleAttrs = [...sharedAttributes, privateAttributes.teammate3];
  return highlightedCells.value.filter(cell => visibleAttrs.includes(cell.attribute));
});


watch(selectedCandidate, (newValue, oldValue) => {
  is_submit.value = false;
  highlightedCells.value = []; // Clear highlights when selection changes
});

function submit() {
  is_submit.value = true;
  if (selectedCandidate.value === 'Candidate B') {
    highlightedCells.value = [
      { name: "Candidate A", attribute: "Leadership" },
      { name: "Candidate B", attribute: "Leadership" },
      { name: "Candidate A", attribute: "Service" },
      { name: "Candidate B", attribute: "Service" },
      { name: "Candidate C", attribute: "Service" },
      { name: "Candidate C", attribute: "Citations" },
      { name: "Candidate C", attribute: "Publications" },
      { name: "Candidate B", attribute: "Evaluations" },
      { name: "Candidate B", attribute: "Teaching" }
    ]; 
  } else {
    highlightedCells.value = []; // Clear highlights if wrong candidate is selected
  }
}

function validationMessage() {
  if (selectedCandidate.value === 'Candidate B') {
    return 'Congratulations! You have selected the best candidate.';
  }
  if (selectedCandidate.value === 'Candidate A') {
    return 'Candidate A is strong in "Leadership" and "Service", but lower in other four evaluations. Please review all qualifications carefully.';
  }
  if (selectedCandidate.value === 'Candidate C') {
    return 'Candidate C is strong in "Service", "Citations", and "Publications" and less experience in other attributes. Please review all qualifications carefully.';
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

        <!-- New Qualification Question -->
        <div class="mb-4 p-3 border rounded">
          <label for="knowledgeCheck" class="form-label fw-bold">Participants can have information regarding different attributes, please type true or false in the box.</label>
          <input type="text" id="knowledgeCheck" class="form-control" v-model="knowledgeCheckAnswer" placeholder="Type your answer here">
        </div>

        <!-- The rest of the task appears only after the above question is answered correctly -->
        <div v-if="knowledgeCheckPassed">
          <p>After some discussion, your committee has reviewed the information <strong>available to each member.</strong> If you had to make a hiring decision right now, which candidate would be the best to select?</p>
          
          <div class="tables-container">
            <div class="top-row">
              <div class="table-wrapper">
                <h3>Teammate 1</h3>
                <CandidateTable :candidates="teammate1Candidates" :highlightedCells="teammate1Highlights"/>
              </div>

              <div class="table-wrapper">
                <h3>Teammate 2</h3>
                <CandidateTable :candidates="teammate2Candidates" :highlightedCells="teammate2Highlights"/>
              </div>
            </div>
            <div class="bottom-row">
              <div class="table-wrapper">
                <h3>Teammate 3</h3>
                <CandidateTable :candidates="teammate3Candidates" :highlightedCells="teammate3Highlights"/>
              </div>
            </div>
          </div>

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
  </div>

</template>

<style scoped>
.tables-container {
  display: flex;
  flex-direction: column; /* Stack the rows vertically */
  gap: 15px; /* Adds space between the rows */
  margin-bottom: 20px;
}

.top-row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 15px; /* Adds space between the top two tables */
}

.bottom-row {
  display: flex;
  justify-content: flex-start; /* Aligns the single table to the left */
}

.bottom-row .table-wrapper {
  flex-basis: calc(50% - 7.5px); /* Makes the bottom table the same width as the top ones */
  max-width: calc(50% - 7.5px);
}

.table-wrapper {
  flex: 1; /* Each table wrapper will take up equal space in its row */
  min-width: 0; /* Prevents flex items from overflowing */
}

/* Use :deep to style the child component (CandidateTable) */
.table-wrapper :deep(table) {
  font-size: 0.75rem; /* Makes the font smaller */
  width: 100%;
  table-layout: fixed; /* Helps with column width consistency */
}

.table-wrapper :deep(th),
.table-wrapper :deep(td) {
  padding: 4px 6px; /* Reduces padding in cells */
  word-wrap: break-word; /* Wraps long text */
}
</style>