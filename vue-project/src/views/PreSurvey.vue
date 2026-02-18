<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useParticipantStore } from '@/stores/participant';
import Swal from 'sweetalert2';
import axios from 'axios';

const router = useRouter();
const participantStore = useParticipantStore();
const isSubmitting = ref(false);

// Define the questions and their options
const questions = {
  ai_knowledge: {
    label: 'How much knowledge do you have in artificial intelligence?',
    options: [
      'No competence - no experience in artificial intelligence',
      'Low competence - little experience in artificial intelligence',
      'Average level of competence - some experience in artificial intelligence',
      'Moderately high level of competence - good amount of experience in artificial intelligence',
      'High level of competence - extensive experience in artificial intelligence'
    ]
  },
  gender: {
    label: 'What gender do you identify as?',
    options: ['Female', 'Male', 'Prefer not to answer.']
  },
  age: {
    label: 'What is your age?',
    options: ['Under 18', '18 - 24 years old', '25 - 34 years old', '35 - 45 years old', '45 - 55 years old', 'Over 55']
  },
  ethnicity: {
    label: 'What is your ethnicity?',
    options: ['African-American', 'Asian', 'Caucasian', 'Latino or Hispanic', 'Native American', 'Native Hawaiian or Pacific Islander', 'Two or More', 'Other', 'Prefer not to say']
  },
  education: {
    label: 'What is the highest degree or level of education you have completed?',
    options: ['Some High School', 'High School', 'Bachelor\'s Degree', 'Master\'s Degree', 'Ph.D. or higher', 'Prefer not to say']
  }
};

// Create a reactive object to store all survey responses
const surveyData = reactive({
  ai_knowledge: '',
  gender: '',
  age: '',
  ethnicity: '',
  education: ''
});

const submitSurvey = () => {
  // Check if all questions are answered
  for (const key in surveyData) {
    if (surveyData[key] === '') {
      Swal.fire('Incomplete', 'Please answer all questions to continue.', 'warning');
      return;
    }
  }

  isSubmitting.value = true;
  let body = new FormData();
  body.append('participant_id', participantStore.participant_id);

  // Append all survey data to the form body
  for (const key in surveyData) {
    body.append(key, surveyData[key]);
  }

  axios.post('/record_pre_survey/', body)
    .then((response) => {
      if (response.status !== 200) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Failed to record your survey. Please contact the researchers.',
        });
        isSubmitting.value = false;
        return;
      }
      router.push({ name: 'exit' });
    })
    .catch(error => {
      isSubmitting.value = false;
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'An error occurred while submitting your survey.',
      });
      console.error("Pre survey submission error:", error);
    });
};
</script>

<template>
  <div class="container mt-5">
    <div class="card">
      <div class="card-header">
        <h2>Pre-Experiment Survey</h2>
      </div>
      <div class="card-body">
        <form @submit.prevent="submitSurvey" class="mt-4">
          <div v-for="(question, key) in questions" :key="key" class="mb-4">
            <label class="form-label"><strong>{{ question.label }}</strong></label>
            <div v-for="(option, index) in question.options" :key="index" class="form-check">
              <input
                class="form-check-input"
                type="radio"
                :name="key"
                :id="`${key}-${index}`"
                :value="option"
                v-model="surveyData[key]"
                required
              >
              <label class="form-check-label" :for="`${key}-${index}`">
                {{ option }}
              </label>
            </div>
          </div>
          <button type="submit" class="btn btn-primary w-100" :disabled="isSubmitting">
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            <span v-else>Submit</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  max-width: 800px;
  margin: auto;
}
.form-label {
  font-size: 1.1em;
}
.form-check {
  margin-left: 10px;
}
</style>