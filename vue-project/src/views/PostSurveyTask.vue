<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useParticipantStore } from '@/stores/participant';
import { useGroupStore } from '@/stores/group'; // Import the group store
import Swal from 'sweetalert2';
import axios from 'axios';

const router = useRouter();
const participantStore = useParticipantStore();
const groupStore = useGroupStore(); // Instantiate the group store

const submitSurvey = () => {
    let body = new FormData();
    body.append('participant_id', participantStore.participant_id);

    // Loop through responses and check for completion
    for (const key in surveyResponses.value) {
        if (surveyResponses.value[key] === null) {
            Swal.fire('Incomplete', 'Please answer all questions to submit.', 'warning');
            return;
        }
        body.append(key, surveyResponses.value[key]);
    }

    // Post to the new endpoint for the general survey part
    axios.post('/record_post_survey_task/', body)
      .then(() => {
        // Get the condition from the groupStore, as shown in ChatRoom.vue
        

        router.push({ name: 'exit' });
        
      })
      .catch(error => {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to record your survey. Please contact the researchers.',
          });
          console.error("General Survey Error:", error);
      });
};
const likertLabels = [
    "Strongly Disagree",
    "Disagree",
    "Neutral",
    "Agree",
    "Strongly Agree"
];

// Only includes the general discussion questions
const questions = {
    dialogue_management: { label: "Our discussion flowed smoothly without interruptions." },
    information_pooling: { label: "I actively asked for other team members' knowledge or expertise." },
    reaching_consensus: { label: "We carefully evaluated different options before agreeing." },
    time_management: { label: "We kept track of time and adjusted our pace accordingly." },

    reciprocal_interaction: { label: "We treated each other with respect and as equals." },
    individual_task_orientation: { label: "I stayed focused and motivated throughout the task." },
};

// Only includes the responses for the general questions
const surveyResponses = ref({
    dialogue_management: null,
    information_pooling: null,
    reaching_consensus: null,
    time_management: null,
    reciprocal_interaction: null,
    individual_task_orientation: null,
});
</script>

<template>
<div class="container">
    <div class="jumbotron container">
        <h2>Survey </h2>
        <p>
            Please rate your experience on the following scales.
        </p>
        <div class="survey-container">
            <!-- Header Row -->
            <div class="header-spacer"></div> <!-- Empty top-left cell -->
            <div v-for="label in likertLabels" :key="label" class="likert-header">{{ label }}</div>

            <!-- Question Rows -->
            <template v-for="(question, key) in questions" :key="key">
                <label class="question-label"><b>{{ question.label }}</b></label>
                <div v-for="(label, index) in likertLabels" :key="index" class="likert-cell">
                    <input type="radio" :id="`${key}-${index}`" :name="key" :value="index+1" v-model="surveyResponses[key]" />
                </div>
            </template>
        </div>
        <button class="btn btn-primary mt-4" @click="submitSurvey">Submit</button>
    </div>
</div>
</template>

<style scoped>
.survey-container {
  display: grid;
  /* 1 column for questions, 5 for likert scale options */
  grid-template-columns: 3fr repeat(5, 1fr);
  gap: 1rem 0.5rem;
  align-items: center;
  margin-top: 2rem;
}

.likert-header {
  text-align: center;
  font-weight: bold;
  font-size: 0.9em;
}

.question-label {
  text-align: left;
  padding-right: 1rem;
}

.likert-cell {
  text-align: center;
}

.btn-primary {
    margin-top: 2rem;
}
</style>