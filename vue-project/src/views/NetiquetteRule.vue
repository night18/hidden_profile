<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const agreement = ref(false);

function submit() {
  router.push({ name: 'WaitingRoom' });
}
</script>
<template>
<div class="container">
    <div class="jumbotron container">
        <h2>Discussion Netiquette and Rules</h2>
        <div class="content-area">
            In the group phase, you will need to discuss with other members of your group and vote for the best candidate. To encourage a safe and healthy discussion environment, we'd like to remind you of a few rules you should follow during the discussion:
            <ol>
                <li>Respect other people during the discussion. You might have different opinions from other people in your group on some candidates. Please communicate your opinions to others in a rational way. Do not verbally abuse, attack, embarrass, or threaten anyone else in the chat room.</li>
                <li>Do <b>NOT</b> give out any of your personal information during the discussion. This includes your full name, address, email address, or phone number.</li>
            </ol>
            <b>Agreement</b>
            <div class="form-check">
                <input type="checkbox" class="form-check-input" id="agreement" v-model="agreement" />
                <label class="form-check-label" for="agreement">I have read and agree to follow the discussion rules.</label>
            </div>
        </div>
        <button class="btn btn-primary" @click="submit" :disabled="!agreement">Next</button>
      
    </div>
</div>
</template>
<style scoped>
</style>