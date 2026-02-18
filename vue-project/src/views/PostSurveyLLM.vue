<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useParticipantStore } from '@/stores/participant';
import Swal from 'sweetalert2';
import axios from 'axios';

const router = useRouter();
const participantStore = useParticipantStore();

const likertLabels = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"];
const openEndedResponse = ref('');

const llmQuestions = {
    llm_summary: { label: "The LLM facilitator did a good job summarizing information when needed to reach a decision." },
    llm_encouragement: { label: "The LLM facilitator did a good job encouraging participants to share information to reach a decision." },
    llm_alternatives: { label: "The LLM facilitator raised alternative perspectives or provided useful counterarguments to reach a decision." },
      llm_collaboration: { label: "I feel like I was collaborating with the LLM facilitator during the task." },
    llm_satisfaction: { label: "I'm satisfied with the assistance provided by the LLM facilitator in completing the tasks." },
    llm_quality: { label: "I'm pleased with the quality of the LLM facilitator in completing the tasks." },
    llm_recommendation: { label: "I would recommend the LLM facilitator to my friends if they need to complete similar tasks." },
    llm_future_use: { label: "If given the option, I would use the LLM facilitator to assist me with completing similar decision-making tasks in the future." },
};

const surveyResponses = ref({
    llm_summary: null,
    llm_encouragement: null,
    llm_alternatives: null,
    llm_collaboration: null,
    llm_satisfaction: null,
    llm_quality: null,
    llm_recommendation: null,
    llm_future_use: null,
});

const submitLlmSurvey = () => {
    let body = new FormData();
    body.append('participant_id', participantStore.participant_id);
    // Append the optional open-ended response. It will be an empty string if not filled.
    body.append('open_ended_response', openEndedResponse.value);

    // Check only the required Likert questions for completion
    for (const key in surveyResponses.value) {
        if (surveyResponses.value[key] === null) {
            Swal.fire('Incomplete', 'Please answer all multiple-choice questions to continue.', 'warning');
            return;
        }
        body.append(key, surveyResponses.value[key]);
    }

    axios.post('/record_post_survey_llm/', body)
      .then(() => {
        // Navigate to the next part of the survey
        router.push({ name: 'PostSurveyNasa' }); 
      })
      .catch(error => {
          Swal.fire('Error', 'Could not save survey. Please try again.', 'error');
          console.error("LLM Survey Error:", error);
      });
};
</script>

<template>
    <div class="container">
        <div class="survey-page-container">
            <h2>Survey</h2>
            <p>Please answer the following questions about the LLM facilitator.</p>
    
            <!-- Optional open-ended question -->
            <div class="my-4">
                <label for="open-ended" class="form-label"><b>How did you feel about the facilitator during the task? What did you (dis)like about the facilitator? (Optional)</b></label>
                <textarea id="open-ended" class="form-control" rows="3" v-model="openEndedResponse"></textarea>
            </div>
            
            <div class="survey-container">
                <!-- Header Row -->
                <div class="header-spacer"></div> <!-- Empty top-left cell -->
                <div v-for="label in likertLabels" :key="label" class="likert-header">{{ label }}</div>
    
                <!-- Question Rows -->
                <template v-for="(question, key) in llmQuestions" :key="key">
                    <label class="question-label"><b>{{ question.label }}</b></label>
                    <div v-for="(label, index) in likertLabels" :key="index" class="likert-cell">
                        <input type="radio" :id="`${key}-${index}`" :name="key" :value="index+1" v-model="surveyResponses[key]" />
                    </div>
                </template>
            </div>
            <button class="btn btn-primary mt-4" @click="submitLlmSurvey">Continue</button>
        </div>
    </div>
    </template>
    
    <style scoped>
    .survey-page-container {
        padding: 2rem 0;
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