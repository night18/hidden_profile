<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import CountdownTimer from '@/components/CountdownTimer.vue';

const router = useRouter();
const remainTime = ref(300);

onMounted(() => {
  const interval = setInterval(() => {
    if (remainTime.value > 0) {
      remainTime.value--;
    } else {
      clearInterval(interval);
      router.push('/pageA');
    }
  }, 1000);
});


</script>
<template>
  <div class="container">
    <div class="jumbotron container">
      <h2> Waiting Room </h2>
      <div class="content-area">
        <p>
          We are currently waiting for other participants to join the task. Please wait until the task begins.
        </p>
        <CountdownTimer :remain_time="300" />
      </div>
    </div>
  </div>
</template>