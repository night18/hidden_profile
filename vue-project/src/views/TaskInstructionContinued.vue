<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

function goExample() {
    router.push({ name: 'CandidateExample' });
}
</script>
<template>
<div class="container">
  <div class="jumbotron container">
    <h2>Faculty Search Committee Decision-Making Task (Continued)</h2>
    <div class="content-area">
      <p>As a member of the search committee, your goal is to evaluate three faculty candidates and select the most qualified one.</p>
      <div>

          <!-- Process Section -->
          <div >
              <h3>3. Decision Process</h3>
              <ol>
                  <li><strong>Review candidate profiles</strong> - Examine the qualifications of each candidate.</li>
                  <li><strong>Discuss with the committee</strong> - Share insights and deliberate on strengths and weaknesses.</li>
                  <li><strong>Make a final decision</strong> - Work towards a consensus on the best candidate.</li>
              </ol>
          </div>

          <!-- Discussion Guidelines Section -->
          <div >
              <h3>4. Discussion Guidelines</h3>
              <ul>
                  <li>Be open to different perspectives from other committee members.</li>
                  <li>Justify your reasoning with specific candidate details.</li>
                  <li>Aim for a well-reasoned decision that balances research, teaching, and service.</li>
              </ul>
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
