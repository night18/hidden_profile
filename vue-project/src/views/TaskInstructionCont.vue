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
    <h2>Faculty Search Committee Task Instruction II</h2>
    <div class="content-area">
      
      <!-- Overview Section -->
      <div >
          <h3>What Makes a Strong Candidate?</h3>

          <p>
            As the discussion proceeds, your team will reveal each candidate's performance on different aspects. The strongest candidate is the one who performs best across the <strong>most</strong> aspects compared to others. Your team's goal is to combine your different perspectives to reveal candidates' performance on as many aspects as possible, and then figure out which candidate stands out overall.
          </p>
          <p>
            Note that no single attribute should dominate the decision. We look for well-rounded excellence.
          </p>
          <h3>Tips for Discussion</h3>          <ul>
            <li><b>Share what you know</b>. You have important information—your teammates are counting on you.</li>
            <li><b>Be open-minded</b>. Listen to perspectives from others before deciding.</li>
            <li><b>Think holistically</b>. Balance strengths across all attributes.</li>
          </ul>
      </div>
    </div>
    <div class="mt-4">
        <button class="btn btn-primary btn-lg" @click="goExample">Let's see an example</button>
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
