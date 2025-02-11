<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useParticipantStore } from '@/stores/participant';
import { useChatStore } from '@/stores/useChatStore';
import CountdownTimer from '@/components/CountdownTimer.vue';
import axios from 'axios';
import Swal from 'sweetalert2';

const router = useRouter();
const remainTime = ref(300);
const message = ref('');
const chatStore = useChatStore();

onMounted(() => {
  const interval = setInterval(() => {
    if (remainTime.value > 0) {
      remainTime.value--;
    } else {
      clearInterval(interval);
      router.push('/FailPairing');
    }
  }, 1000);

  let body = new FormData();
  body.append('participant_id', useParticipantStore().participant_id);
  axios.post('/pairing/', body)
    .then((response) => {
      /**
       * json['group_id'] = group_id
       * return JsonResponse(json, status=status.HTTP_200_OK)
       */
      if (response.status !== 200) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Failed to join the group',
        });
        return;
      }

      let group_id = response.data.group_id;
      useParticipantStore().setGroupId(group_id);
      
      chatStore.initializeWebSocket(group_id);

      chatStore.on('room_ready', () => {
        clearInterval(interval);
        console.log('room_ready');
        router.push('/FormalCandidate');
      });
      
      chatStore.on('waiting', (data) => {
        message.value = `Waiting for ${data.remaining} more participants...`;
      });

    })
    .catch((error) => {
      console.error(error);
    });
});


</script>
<template>
  <div class="container">
    <div class="jumbotron container">
      <h2> Waiting Room </h2>
      <div class="content-area">
        <p>We are currently waiting for other participants to join the task. Please wait until the task begins.</p>
        <p>If you wait for more than 5 minutes, you will be redirected to the end page. We will pay you for your time.</p>
        <CountdownTimer :remain_time="300" />
        <p>{{ message }}</p>
      </div>
    </div>
  </div>
</template>