<script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import Swal from 'sweetalert2'; // Assuming SweetAlert2 is installed as seen in other files
  
  const router = useRouter();
  const knowledgeCheckAnswer = ref('');
  
  function goExample() {
      // Basic validation: Check if answer is "true" (case-insensitive)
      const answer = knowledgeCheckAnswer.value.trim().toLowerCase();
      
      if (answer === 'true') {
          router.push({ name: 'TaskInstructionCont' });
      } else if (answer === 'false') {
          // Specific error for the wrong answer
          Swal.fire({
              icon: 'error',
              title: 'Incorrect',
              text: 'That is incorrect. Please make sure you read the instructions correctly.',
          });
      } else {
          // Error for empty or invalid text (not true/false)
          Swal.fire({
              icon: 'warning',
              title: 'Invalid Input',
              text: 'Please type either "true" or "false" in the text box.',
          });
      }
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
                <p>Your committee is reviewing three finalists for a faculty position. Each candidate needs to be evaluated using several attributes, for example: Publications, Teaching or mentoring experience.</p>
  
  
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
  
        <!-- Knowledge Check Section -->
        <div class="mb-4 p-3 border rounded bg-light">
          <label for="knowledgeCheck" class="form-label fw-bold">Participants can have information regarding different attributes, please type true or false in the box.</label>
          <input type="text" id="knowledgeCheck" class="form-control" v-model="knowledgeCheckAnswer" placeholder="Type your answer here">
        </div>
  
        <div class="mt-4">
            <button class="btn btn-primary btn-lg" @click="goExample">Next</button>
        </div>
      </div>
    </div>
  </div>
  </template>
  
  <style scoped>
  .bg-light {
    background-color: #f8f9fa !important;
  }
  </style>