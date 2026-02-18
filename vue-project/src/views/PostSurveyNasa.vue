<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useParticipantStore } from '@/stores/participant';
import Swal from 'sweetalert2';
import axios from 'axios';

const router = useRouter();
const participantStore = useParticipantStore();

const likertLabels = ["Very Low", "Low", "Neutral", "High", "Very High"];

const questions = {
    mental_demand: { label: "Mental Demand", description: "How mentally demanding was the task?" },
    temporal_demand: { label: "Temporal Demand", description: "How hurried or rushed was the pace of the task?" },
    performance: { label: "Performance", description: "How successful were you in accomplishing what you were asked to do?" },
    effort: { label: "Effort", description: "How hard did you have to work to accomplish your level of performance?" },
    frustration: { label: "Frustration", description: "How insecure, discouraged, irritated, stressed, and annoyed were you?" },
};

const surveyResponses = ref({
    mental_demand: null,
    temporal_demand: null,
    performance: null,
    effort: null,
    frustration: null,
});

const submitNasaSurvey = () => {
    let body = new FormData();
    body.append('participant_id', participantStore.participant_id);

    // Loop through responses to check for completion and append data
    for (const key in surveyResponses.value) {
        if (surveyResponses.value[key] === null) {
            Swal.fire('Incomplete', 'Please answer all questions to submit.', 'warning');
            return; // Stop the submission if any question is unanswered
        }
        body.append(key, surveyResponses.value[key]);
    }
    axios.post('/record_post_survey_nasa/', body)
      .then(() => {
        router.push({ name: 'PostSurveyTask' });
      })
      .catch(error => {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to record your survey. Please contact the researchers.',
          });
          console.error("NASA-TLX Survey Error:", error);
      });
};

</script>

<template>
    <div class="container">
        <div class="survey-page-container">
            <h2>Survey</h2>
            <p>Please rate your experience on the following scales.</p>
            
            <div class="survey-container">
            <!-- Header Row -->
            <div class="header-spacer"></div> <!-- Empty top-left cell -->
            <div v-for="label in likertLabels" :key="label" class="likert-header">{{ label }}</div>

            <!-- Question Rows -->
            <template v-for="(question, key) in questions" :key="key">
                <label class="question-label">
                    <b>{{ question.label }}</b>
                    <p class="text-muted small m-0">{{ question.description }}</p>
                </label>
                <div v-for="(label, index) in likertLabels" :key="index" class="likert-cell">
                    <input type="radio" :id="`${key}-${index}`" :name="key" :value="index+1" v-model="surveyResponses[key]" />
                </div>
            </template>
        </div>
        <button class="btn btn-primary mt-4" @click="submitNasaSurvey">Submit</button>
    </div>
</div>
</template>

<style scoped>
.jumbotron {
    background-color: #f8f9fa;
    padding: 2rem;
    border-radius: 0.3rem;
    margin-top: 2rem;
}
.survey-container {
  display: grid;
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