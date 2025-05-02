

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

function goExample() {
    router.push({ name: 'CandidateExample' });
}
</script>
<template>
    <div class="container mt-5">
      <div class="card shadow">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">Faculty Search Committee Decision-Making Task</h2>
          
          <p class="text-muted text-center">
            As a member of the search committee, your goal is to evaluate three faculty candidates and select the most qualified one.
          </p>
  
          <div class="accordion" id="taskInstructions">
            <!-- Overview Section -->
            <div class="accordion-item">
              <h2 class="accordion-header" id="headingOverview">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOverview" aria-expanded="true" aria-controls="collapseOverview">
                  1. Overview of Your Role
                </button>
              </h2>
              <div id="collapseOverview" class="accordion-collapse collapse show" aria-labelledby="headingOverview" data-bs-parent="#taskInstructions">
                <div class="accordion-body">
                  You are a member of a university faculty search committee. Your task is to review candidate information, discuss with other committee members, and make a hiring decision.
                </div>
              </div>
            </div>
  
            <!-- Decision Criteria Section -->
            <div class="accordion-item">
              <h2 class="accordion-header" id="headingCriteria">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseCriteria" aria-expanded="false" aria-controls="collapseCriteria">
                  2. Decision Criteria
                </button>
              </h2>
              <div id="collapseCriteria" class="accordion-collapse collapse" aria-labelledby="headingCriteria" data-bs-parent="#taskInstructions">
                <div class="accordion-body">
                  Each candidate has been evaluated based on multiple factors relevant to the faculty position. As a committee member, you will review the three main aspects about each candidate, including:
                  <ul>
                    <li><strong>Teaching Experience</strong> - Publications, research impact, and alignment with the department's needs.</li>
                    <li><strong>Research Contributions</strong> - Courses taught, student engagement, and innovation in pedagogy.</li>
                    <li><strong>Service & Leadership</strong> - Contributions to mentorship, departmental service, and broader academic community involvement.</li>
                  </ul>
                  <p>The best candidate is the one who performs <strong>the strongest across the most attributes</strong>. Each attribute is equally important in the decision-making process, so no single factor should be prioritized over the others.</p>
                  <p>As you review the candidates, consider their strengths and weaknesses holistically rather than focusing on any single attribute. Each committee member has access to important information about the candidates, and discussing different perspectives will help ensure a well-informed decision.</p>
                  <p>During the discussion, aim to integrate insights from all available information to make the best possible selection.</p>
                </div>
              </div>
            </div>
  
            <!-- Process Section -->
            <div class="accordion-item">
              <h2 class="accordion-header" id="headingProcess">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseProcess" aria-expanded="false" aria-controls="collapseProcess">
                  3. Decision Process
                </button>
              </h2>
              <div id="collapseProcess" class="accordion-collapse collapse" aria-labelledby="headingProcess" data-bs-parent="#taskInstructions">
                <div class="accordion-body">
                  <ol>
                    <li><strong>Review candidate profiles</strong> – Examine the qualifications of each candidate. You <strong>cannot</strong> access the profiles during the discussion. But, you are allowed to take notes when reviewing the profiles. </li>
                    <li><strong>Discuss with the committee</strong> – Share insights and deliberate on strengths and weaknesses.</li>
                    <li><strong>Make a final decision</strong> – Work towards a consensus on the best candidate.</li>
                  </ol>
                </div>
              </div>
            </div>
  
            <!-- Discussion Guidelines Section -->
            <div class="accordion-item">
              <h2 class="accordion-header" id="headingGuidelines">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseGuidelines" aria-expanded="false" aria-controls="collapseGuidelines">
                  4. Discussion Guidelines
                </button>
              </h2>
              <div id="collapseGuidelines" class="accordion-collapse collapse" aria-labelledby="headingGuidelines" data-bs-parent="#taskInstructions">
                <div class="accordion-body">
                  <ul>
                    <li>Be open to different perspectives from other committee members.</li>
                    <li>Justify your reasoning with specific candidate details.</li>
                    <li>Aim for a well-reasoned decision that balances research, teaching, and service.</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
  
          <div class="text-center mt-4">
            <button class="btn btn-primary btn-lg" @click="goExample">Next</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
  }
  </style>
  