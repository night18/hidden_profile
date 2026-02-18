<script setup>
import { ref, onMounted } from 'vue';
import { useParticipantStore } from '@/stores/participant';
import axios from 'axios';
import Swal from 'sweetalert2';

const participantStore = useParticipantStore();
const bonus = ref(null);
const taskDetails = ref([]);
const errorMessage = ref('');
const completionCode = ref(''); // Define completionCode as a ref

onMounted(() => {
  let body = new FormData();
  body.append('participant_id', participantStore.participant_id);
  axios.post('/get_bonus/', body)
    .then(response => {
      if (response.status !== 200) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Failed to retrieve bonus.',
        });
        return;
      }
      bonus.value = response.data.bonus;
      taskDetails.value = response.data.list; // Updated to handle the 'list' field

      // Assign the completion code based on the bonus
      if (bonus.value > 0) {
        completionCode.value = "CWYK3VZJ"; // Replace with the actual code for bonus
      } else {
        completionCode.value = "C1K9A104"; // Replace with the actual code for no bonus
      }
    })
    .catch(() => {
      errorMessage.value = 'An error occurred while retrieving your bonus.';
    });
});
</script>

<template>
  <div class="container">
    <div class="jumbotron container">
      <h2>Exit Page</h2>
      <div class="content-area">
        <p>Thank you for your participation. We appreciate your time and effort.</p>
        <p>If you have any questions or feedback, please feel free to contact us.</p>
        <div v-if="bonus !== null">
          <p>Your bonus: <strong>{{ bonus }}</strong></p>
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Turn</th>
                <th>Vote Result</th>
                <th>Best Candidate</th>
                <th>Bonus</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="task in taskDetails" :key="task.task">
                <td>{{ task.task }}</td>
                <td>{{ task.final_vote }}</td>
                <td>{{ task.ground_truth }}</td>
                <td>{{ task.bonus }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else-if="errorMessage">
          <p class="error">{{ errorMessage }}</p>
        </div>
        <div v-else>
          <p>Loading your bonus...</p>
        </div>
      </div>
      <div class="completion-code">
        <h3>Your Prolific Completion Code:</h3>
        <p><strong>{{ completionCode }}</strong></p>
        <p>Please copy this code and submit it on Prolific to confirm your participation.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.completion-code {
  background-color: #f8f9fa;
  border: 2px solid #007bff;
  padding: 20px;
  text-align: center;
  font-size: 1.5em;
  font-weight: bold;
  margin: 20px 0;
  border-radius: 8px;
  color: #007bff;
}
</style>