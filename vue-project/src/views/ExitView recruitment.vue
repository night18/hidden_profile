<script setup>
import { ref } from 'vue';

// A single completion code for everyone who completes the recruitment phase.
const completionCode = ref('CNBTWNUO'); // Replace with your actual recruitment completion code
</script>

<template>
  <div class="container">
    <div class="jumbotron container">
      <h2>Thank You for Registering!</h2>
      <div class="content-area">
        <p>Thank you for your interest and for completing the initial consent and survey steps. You have successfully registered for the upcoming study.</p>
        <p>
          Please remember that the experiment will take place on <strong>TODAY Feb 3 at 5pm E.T.</strong>. You will receive reminders from Prolific before the session begins.
        </p>
        <p>If you have any questions, please feel free to contact the research team.</p>
      </div>
      <div class="completion-code">
        <h3>Your Prolific Completion Code:</h3>
        <p><strong>{{ completionCode }}</strong></p>
        <p>Please copy this code and submit it on Prolific to confirm your registration for the study.</p>
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
.content-area p {
  font-size: 1.1rem;
}
</style>