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
    <h2>Faculty Search Task Instruction</h2>
    <div class="content-area">

      <div>
          <!-- Overview Section -->
          <div >
              <h3>What You'll Do</h3>
              <p>Your committee is reviewing three finalists for a faculty position. Each candidate needs to be evaluated using several attributes, for example: Research publications, Teaching Evaluation or mentoring experience.</p>


              <p> Each candidate is required to provide some of this information in their application materials; such information becomes available to <i>all</i> committee members. However, when meeting with candidates one-on-one, each committee member also collects additional information about the candidates; this information is <i>only available to the committee member who collected the information</i> before the committee discussion. In other words:</p>
                  <ul>
                    <li>As one of the committee members, you <strong>will not see</strong> the full set of information  for each candidate. Your teammates (other committee members) will bring important insights on some aspects that you may have not evaluated on.</li>

                  </ul>
              <p>Since you do not get the full candidate information, in this task, your job is to:</p>
                  <ul>
                    <li><b>Review</b> the candidate information provided to you.</li>
                    <li><b>Discuss</b> with other committee members to share your perspective and hear theirs.</li>
                    <li><b>Help your team reach a group decision</b> on the most qualified candidate overall.</li>
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
