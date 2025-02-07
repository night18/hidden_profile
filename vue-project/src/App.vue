
<script setup>
import { RouterView } from 'vue-router';
</script>

<template>
  <RouterView />
</template>
<script>
export default {
  name: 'App',
  components: {
    RouterView
  },
  beforeCreate() {
    // check the intial state of the token
    
  },
  setup() {
    return {
      // token: ref(localStorage.getItem('token'))
    }
  }
}
</script>

<style scoped>
</style>
