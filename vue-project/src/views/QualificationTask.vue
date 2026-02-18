<script setup>
  import { ref, watch, computed } from 'vue';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  // --- Phase Logic ---
  const step = ref(1); // 1 = Individual, 2 = Committee, 3 = Full Reveal
  const initialCandidate = ref(''); 
  
  function revealCommitteeInfo() {
    if (initialCandidate.value) {
      step.value = 2;
      window.scrollTo(0,0);
    }
  }
  
  function revealFullProfile() {
    step.value = 3;
    window.scrollTo(0,0);
  }
  
  // --- Final Task Logic ---
  const selectedCandidate = ref('');
  const is_submit = ref(false);
  
  // Sample data (Full Data)
  const candidates = [
    {
      "name": "Candidate A",
      "Teaching": "Good",
      "Mentorship": "Exceptional",
      "Publications": "Good",
      "Citations": "Exceptional",
      "Service": "Good",
      "Leadership": "Good",
    },
    {
      "name": "Candidate B",
      "Teaching": "Exceptional",
      "Mentorship": "Good",
      "Publications": "Average",
      "Citations": "Good",
      "Service": "Exceptional",
      "Leadership": "Exceptional",
    },
    {
      "name": "Candidate C",
      "Teaching": "Good",
      "Mentorship": "Average",
      "Publications": "Exceptional",
      "Citations": "Good",
      "Service": "Good",
      "Leadership": "Average",
    }
  ];
  
  // --- 1. DEFINING ATTRIBUTES ---
  const sharedAttributes = ["Teaching", "Mentorship", "Publications"];
  const privateAttributes = {
    teammate1: "Citations",
    teammate2: "Service",
    teammate3: "Leadership"
  };
  
  // All attributes in the desired order for the final table
  const allAttributesOrder = [
    "Teaching", 
    "Mentorship", 
    "Publications", 
    "Citations", 
    "Service", 
    "Leadership"
  ];
  
  // --- 2. DATA FILTERING FOR STEPS 1 & 2 ---
  const t1_Attributes = [...sharedAttributes, privateAttributes.teammate1];
  const t2_Attributes = [...sharedAttributes, privateAttributes.teammate2];
  const t3_Attributes = [...sharedAttributes, privateAttributes.teammate3];
  
  const createFilteredData = (allowedAttributes) => {
    return candidates.map(c => {
      const row = { name: c.name };
      allowedAttributes.forEach(attr => {
        row[attr] = c[attr];
      });
      return row;
    });
  };
  
  const teammate1Candidates = createFilteredData(t1_Attributes);
  const teammate2Candidates = createFilteredData(t2_Attributes);
  const teammate3Candidates = createFilteredData(t3_Attributes);
  
  // --- 3. HELPER FUNCTIONS ---
  const formatAttributeName = (attribute) => attribute; 
  
  // --- 4. STEP 3: COLOR LOGIC ---
  const getAttributeClass = (attribute) => {
    if (sharedAttributes.includes(attribute)) return 'bg-shared';
    if (attribute === privateAttributes.teammate1) return 'bg-t1';
    if (attribute === privateAttributes.teammate2) return 'bg-t2';
    if (attribute === privateAttributes.teammate3) return 'bg-t3';
    return '';
  };
  
  // --- HIGHLIGHTING LOGIC (For Step 2 Voting) ---
  const highlightedCells = ref([]);
  
  const isHighlighted = (candidateName, attribute) => {
    return highlightedCells.value.some(
      cell => cell.name === candidateName && cell.attribute === attribute
    );
  };
  
  watch(selectedCandidate, () => {
    is_submit.value = false;
    highlightedCells.value = [];
  });
  
  function submit() {
    is_submit.value = true;
    if (selectedCandidate.value === 'Candidate B') {
      highlightedCells.value = [
        { name: "Candidate A", attribute: "Mentorship" },
        { name: "Candidate A", attribute: "Citations" },
        { name: "Candidate B", attribute: "Leadership" },
        { name: "Candidate B", attribute: "Teaching" },
        { name: "Candidate B", attribute: "Service" },
        { name: "Candidate C", attribute: "Publications" }
      ]; 
    } else {
      highlightedCells.value = [];
    }
  }
  
  function validationMessage() {
    if (selectedCandidate.value === 'Candidate B') return 'Congratulations! You have selected the best candidate.';
    if (selectedCandidate.value === 'Candidate A') return 'Candidate A is strong in "Mentorship" and "Citations", but lower in other attributes.';
    if (selectedCandidate.value === 'Candidate C') return 'Candidate C is strong in "Publications" and less experience in other attributes.';
    return 'Your selection is not the best candidate. Please review the candidates and select the most qualified one.';
  }
  
  function next() {
    router.push({ name: 'FormalInstruction' });
  }
  </script>
  
  <template>
    <div class="container">
      <div class="jumbotron container">
        <h2>Qualification Task</h2>
        <div class="content-area">
          
          <div>
            
            <div v-if="step === 1">
              <p>Please review <strong>Your Information</strong> below. Based solely on this information, which candidate do you prefer?</p>
              
              <div class="table-wrapper mb-4" style="max-width: 800px;">
                <h3>Your Information (Teammate 1)</h3>
                <div class="table-responsive">
                  <table class="table table-bordered table-hover">
                    <thead class="table-primary">
                      <tr>
                        <th class="text-center fw-bold"> </th>
                        <th v-for="c in teammate1Candidates" :key="c.name" class="text-center fw-bold">
                          {{ c.name }}
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="attr in t1_Attributes" :key="attr">
                        <td class="fw-bold">{{ formatAttributeName(attr) }}</td>
                        <td v-for="c in teammate1Candidates" :key="c.name" class="text-center">
                          {{ c[attr] || '-' }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
  
              <div class="mb-3">
                <strong>Select your initial preference:</strong>
                <div v-for="(candidate, index) in candidates" :key="'init-'+index" class="form-check">
                  <input type="radio" :id="'init-candidate' + index" :value="candidate.name" class="form-check-input" v-model="initialCandidate" />
                  <label :for="'init-candidate' + index">{{ candidate.name }}</label>
                </div>
              </div>
  
              <button class="btn btn-primary" @click="revealCommitteeInfo" :disabled="!initialCandidate">
                Confirm Selection
              </button>
            </div>
  
            <div v-if="step === 2">
              <p>After some discussion, your committee has reviewed the information <strong>available to each member.</strong></p>
              
              <div class="tables-vertical-container">
                  <div class="table-wrapper">
                    <h3>Teammate 1 (You)</h3>
                    <div class="table-responsive">
                      <table class="table table-bordered table-hover">
                        <thead class="table-primary">
                          <tr><th class="text-center fw-bold"> </th><th v-for="c in teammate1Candidates" :key="c.name" class="text-center fw-bold">{{ c.name }}</th></tr>
                        </thead>
                        <tbody>
                          <tr v-for="attr in t1_Attributes" :key="attr">
                            <td class="fw-bold">{{ formatAttributeName(attr) }}</td>
                            <td v-for="c in teammate1Candidates" :key="c.name" class="text-center" :class="{ 'table-success': isHighlighted(c.name, attr) }">{{ c[attr] || '-' }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
  
                  <div class="table-wrapper">
                    <h3>Teammate 2</h3>
                    <div class="table-responsive">
                      <table class="table table-bordered table-hover">
                        <thead class="table-primary">
                          <tr><th class="text-center fw-bold"> </th><th v-for="c in teammate2Candidates" :key="c.name" class="text-center fw-bold">{{ c.name }}</th></tr>
                        </thead>
                        <tbody>
                          <tr v-for="attr in t2_Attributes" :key="attr">
                            <td class="fw-bold">{{ formatAttributeName(attr) }}</td>
                            <td v-for="c in teammate2Candidates" :key="c.name" class="text-center" :class="{ 'table-success': isHighlighted(c.name, attr) }">{{ c[attr] || '-' }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
  
                  <div class="table-wrapper">
                    <h3>Teammate 3</h3>
                    <div class="table-responsive">
                      <table class="table table-bordered table-hover">
                        <thead class="table-primary">
                          <tr><th class="text-center fw-bold"> </th><th v-for="c in teammate3Candidates" :key="c.name" class="text-center fw-bold">{{ c.name }}</th></tr>
                        </thead>
                        <tbody>
                          <tr v-for="attr in t3_Attributes" :key="attr">
                            <td class="fw-bold">{{ formatAttributeName(attr) }}</td>
                            <td v-for="c in teammate3Candidates" :key="c.name" class="text-center" :class="{ 'table-success': isHighlighted(c.name, attr) }">{{ c[attr] || '-' }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
              </div>
  
              <div class="mt-4">
                <strong>Select the final best candidate:</strong>
                <div v-for="(candidate, index) in candidates" :key="index" class="form-check">
                    <input type="radio" :id="'candidate' + index" :value="candidate.name" class="form-check-input" :disabled="is_submit && selectedCandidate === 'Candidate B'" v-model="selectedCandidate" />
                    <label :for="'candidate' + index">{{ candidate.name }}</label>
                </div>
                <button class="btn btn-primary" @click="submit" :disabled="is_submit && selectedCandidate === 'Candidate B'">
                  Vote for the best candidate
                </button>
                <div v-if="is_submit">
                  <div class="alert mt-3" :class="{ 'alert-success': selectedCandidate === 'Candidate B', 'alert-danger': selectedCandidate !== 'Candidate B' }" role="alert">
                    {{ validationMessage() }}
                  </div>
                </div>
                <div v-if="is_submit && selectedCandidate === 'Candidate B'">
                  <button class="btn btn-info btn-lg text-white" @click="revealFullProfile">Reveal Full Profile</button>
                </div>
              </div>
            </div>
  
            <div v-if="step === 3">
              <h3 class="mb-3">Full Information Distribution</h3>
              <p>Below is the complete profile of all candidates. The rows are highlighted to show which teammate originally held that information.</p>
              
              <div class="legend-container mb-4">
                <span class="badge bg-shared-legend text-dark border">Shared Info</span>
                <span class="badge bg-t1-legend text-dark border">Teammate 1 Only</span>
                <span class="badge bg-t2-legend text-dark border">Teammate 2 Only</span>
                <span class="badge bg-t3-legend text-dark border">Teammate 3 Only</span>
              </div>
  
              <div class="table-responsive">
                <table class="table table-bordered">
                  <thead class="table-primary">
                    <tr>
                      <th class="text-center fw-bold">Attribute</th>
                      <th v-for="c in candidates" :key="c.name" class="text-center fw-bold">{{ c.name }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="attr in allAttributesOrder" :key="attr" :class="getAttributeClass(attr)">
                      <td class="fw-bold">{{ formatAttributeName(attr) }}</td>
                      <td v-for="c in candidates" :key="c.name" class="text-center">
                        {{ c[attr] }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
  
              <div class="mt-4">
                <button class="btn btn-primary btn-lg" @click="next">Start Formal Task</button>
              </div>
            </div>
            
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
  .tables-vertical-container {
    display: flex;
    flex-direction: column;
    gap: 30px;
    margin-bottom: 20px;
  }
  
  .table-wrapper {
    width: 100%;
  }
  
  /* This is the class that styles the header row in all tables */
  .table-primary {
      background-color: #cfe2ff;
  }
  
  .table-success {
      background-color: #d1e7dd;
  }
  
  /* Legend Styling */
  .legend-container {
    display: flex;
    gap: 10px;
  }
  .badge {
    font-size: 0.9rem;
    padding: 8px 12px;
  }
  
  .bg-shared-legend { background-color: #e2e3e5; }
  .bg-t1-legend { background-color: #cff4fc; }
  .bg-t2-legend { background-color: #d1e7dd; }
  .bg-t3-legend { background-color: #f8d7da; }
  
  
  /* TABLE ROW COLORS */
  .bg-shared td, .bg-shared th { 
    background-color: #e2e3e5 !important;
  }
  
  .bg-t1 td, .bg-t1 th { 
    background-color: #cff4fc !important;
  }
  
  .bg-t2 td, .bg-t2 th { 
    background-color: #d1e7dd !important;
  }
  
  .bg-t3 td, .bg-t3 th { 
    background-color: #f8d7da !important;
  }
  </style>