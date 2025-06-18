<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

function goExample() {
    router.push({ name: 'TaskInstructionContinued' });
}
</script>
<template>
<div class="container">
  <div class="jumbotron container">
    <h2>Faculty Search Committee Decision-Making Task</h2>
    <div class="content-area">
      <p>As a member of the search committee, your goal is to evaluate three faculty candidates and select the most qualified one.</p>
      <div>
          <!-- Overview Section -->
          <div >
              <h3>1. Overview of Your Role</h3>
              <p>
                  You are a member of a university faculty search committee. Your task is to review candidate information, discuss with other committee members, and make a hiring decision.
              </p>
          </div>

          <!-- Decision Criteria Section -->
          <div >
              <h3>2. Decision Criteria</h3>
              <p>
                  Each candidate has been evaluated based on multiple factors relevant to the faculty position. As a committee member, you will review the three main aspects about each candidate, including:
              </p>
              <ul>
                  <li><strong>Teaching Experience</strong> - Publications, research impact, and alignment with the department's needs.</li>
                  <li><strong>Research Contributions</strong> - Courses taught, student engagement, and innovation in pedagogy.</li>
                  <li><strong>Service & Leadership</strong> - Contributions to mentorship, departmental service, and broader academic community involvement.</li>
              </ul>
              <p>
                  The best candidate is the one who performs <strong>the strongest across the most attributes</strong>. Each attribute is equally important in the decision-making process, so no single factor should be prioritized over the others.
              </p>
              <p>
                  As you review the candidates, consider their strengths and weaknesses holistically rather than focusing on any single attribute. Each committee member has access to important information about the candidates, and discussing different perspectives will help ensure a well-informed decision.
              </p>
              <p>
                  During the discussion, aim to integrate insights from all available information to make the best possible selection.
              </p>
          </div>


      </div>

      <div class="mt-4">
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
</style>
