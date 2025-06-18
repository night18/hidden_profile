<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

function goExample() {
    router.push({ name: 'TaskInstructionCont' });
}
</script>
<template>
<div class="container">
  <div class="jumbotron container">
    <h2>Faculty Search Committee Task Instruction</h2>
    <div class="content-area">
      <p>In this task, you'll take on the role of a <b>university search committee member</b> responsible for hiring a new professor. Your goal is to evaluate three candidates and <b>collaboratively</b> select the most qualified individual for a faculty position.</p>
      <div>
          <!-- Overview Section -->
          <div >
              <h3>What You'll Do</h3>
              <p>
                  Your committee is reviewing <b>three finalists</b> for a faculty position. Each candidate brings a unique set of strengths in three important areas:
                  <ul>
                    <li><strong>Research Contributions</strong> - Courses taught, student engagement, and innovation in pedagogy.</li>
                    <li><strong>Teaching Experience</strong> - Publications, research impact, and alignment with the department's needs.</li>
                    <li><strong>Service & Leadership</strong> - Contributions to mentorship, departmental service, and broader academic community involvement.</li>
                  </ul>
                  As a committee member in a specific area, you will focus on just one of these areas in the beginning.That means:
                  <ul>
                    <li>You'll review detailed information about candidates in <b>your assigned focus area</b>.</li>
                    <li>You <b>won't see</b> the full profile. Your teammates (other committee members) will bring insights from other areas.</li>
                  </ul>
                  Your job is to:
                  <ul>
                    <li><b>Review</b> the candidate information provided to you.</li>
                    <li><b>Discuss</b> with other committee members to share your perspective and hear theirs.</li>
                    <li><b>Help your team reach a group decision</b> on the most qualified candidate overall.</li>
                  </ul>
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
