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
          <p> Each candidate has been evaluated on 18 total attributes, drawn from three key areas:</p>
            <ul>
              <li>Research (e.g., publications, research impact, grant record)</li>
              <li>Teaching (e.g., course development, student feedback, teaching awards)</li>
              <li>Service & Leadership (e.g., mentoring, academic service, community involvement)</li>
            </ul>
          
          <p>
            As a committee member, you will only see <b>10 of these 18 attributes</b>, focused on your assigned evaluation area. Other members will see different sets of information.
          </p>
          <p>
            The strongest candidate is the one who <b>performs best across the most attributes</b> compared to others. Your team's goal is to combine your different perspectives to figure out which candidate stands out overall.
          </p>
          <p>
            No single attribute or area should dominate the decision. We look for well-rounded excellence.
          </p>
          <h3>Tips for Discussion</h3>          <ul>
            <li><b>Share what you know</b>. You're the expert in your area—your teammates are counting on you.</li>
            <li><b>Be open-minded</b>. Listen to perspectives from other areas before deciding.</li>
            <li><b>Think holistically</b>. Balance strengths and weaknesses across research, teaching, and service.</li>
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
