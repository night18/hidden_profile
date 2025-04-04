<script setup>
import { ref, onMounted } from 'vue';
import { useParticipantStore } from '@/stores/participant';
import axios from 'axios';
import Swal from 'sweetalert2';

const participantStore = useParticipantStore();
const bonus = ref(null);
const errorMessage = ref('');


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
    })
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
        </div>
        <div v-else-if="errorMessage">
          <p class="error">{{ errorMessage }}</p>
        </div>
        <div v-else>
          <p>Loading your bonus...</p>
        </div>
      </div>
      <button class="btn btn-lg btn-primary">Submit Study</button>
    </div>
  </div>
</template>