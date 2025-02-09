<script setup>
import { ref, onBeforeUnmount, computed } from 'vue';

const props = defineProps({
  remain_time: {
    type: Number,
    default: 300
  }
});


const timer = ref(null);
const counter = ref(props.remain_time);

function countdown() {
  counter.value--;
  if (counter.value === 0) {
    clearInterval(timer.value);
  }
}

const get_hours = computed(() => {
  return parseInt(counter.value / 3600);
});

const get_minutes = computed(() => {
  return parseInt((counter.value % 3600) / 60);
});

const get_seconds = computed(() => {
  return (counter.value % 60).toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false });
});


// When mounted start the timer
timer.value = setInterval(countdown, 1000);

// Destroy the timer when the component is destroyed
onBeforeUnmount(() => {
  clearInterval(timer.value);
});

</script>
<template>
    <div class="text-center">
      {{get_minutes}} : {{get_seconds}}
    </div>
</template>
<script>

</script>