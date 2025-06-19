<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useParticipantStore } from '@/stores/participant';
import Swal from 'sweetalert2';
import axios from 'axios';

const router = useRouter();
const participantStore = useParticipantStore();

const submitSurvey = () => {

    let body = new FormData();
    body.append('participant_id', participantStore.participant_id);
    body.append('dialogue_management', surveyResponses.value.dialogue_management);
    body.append('information_pooling', surveyResponses.value.information_pooling);
    body.append('reaching_consensus', surveyResponses.value.reaching_consensus);
    body.append('task_division', surveyResponses.value.task_division);
    body.append('time_management', surveyResponses.value.time_management);
    body.append('technical_coordination', surveyResponses.value.technical_coordination);
    body.append('reciprocal_interaction', surveyResponses.value.reciprocal_interaction);
    body.append('individual_task_orientation', surveyResponses.value.individual_task_orientation);
    body.append('llm_collaboration', surveyResponses.value.llm_collaboration);
    body.append('llm_satisfaction', surveyResponses.value.llm_satisfaction);
    body.append('llm_quality', surveyResponses.value.llm_quality);
    body.append('llm_recommendation', surveyResponses.value.llm_recommendation);
    body.append('llm_future_use', surveyResponses.value.llm_future_use);

    axios.post('/record_post_survey/', body)
      .then((response) => {
        if (response.status != 200) {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to record your survey. Please contact the researchers.',
          });
          return;
        }

        router.push({ name: 'exit' });
      })

};

const likertLabels = [
    "Strongly Disagree",
    "Disagree",
    "Somewhat Disagree",
    "Neutral",
    "Somewhat Agree",
    "Agree",
    "Strongly Agree"
];

const questions = {
    dialogue_management: { label: "Our discussion flowed smoothly without interruptions." },
    information_pooling: { label: "I actively asked for other team members' knowledge or expertise." },
    reaching_consensus: { label: "We carefully evaluated different options before agreeing." },
    task_division: { label: "We clearly divided the task according to our strengths." },
    time_management: { label: "We kept track of time and adjusted our pace accordingly." },
    technical_coordination: { label: "We effectively coordinated our use of the shared workspace." },
    reciprocal_interaction: { label: "We treated each other with respect and as equals." },
    individual_task_orientation: { label: "I stayed focused and motivated throughout the task." },
    llm_collaboration: { label: "I feel like I was collaborating with the LLM facilitator during the task." },
    llm_satisfaction: { label: "I'm satisfied with the assistance provided by the LLM facilitator in completing the tasks." },
    llm_quality: { label: "I'm pleased with the quality of the LLM facilitator in completing the tasks." },
    llm_recommendation: { label: "I will recommend the LLM facilitator to my friends if they need to complete similar tasks." },
    llm_future_use: { label: "If given the option, I would use the LLM facilitator to assist me with completing similar decision-making tasks in the future." },
};

// Create a reactive object to store all survey responses
const surveyResponses = ref({
    dialogue_management: null,
    information_pooling: null,
    reaching_consensus: null,
    task_division: null,
    time_management: null,
    technical_coordination: null,
    reciprocal_interaction: null,
    individual_task_orientation: null,
    llm_collaboration: null,
    llm_satisfaction: null,
    llm_quality: null,
    llm_recommendation: null,
    llm_future_use: null,
});
</script>

<template>
<div class="container">
    <div class="jumbotron container">
        <h2>Survey</h2>
        <p>
          Wonderful! You almost completed all the search committee tasks. One last thing, please complete the survey. We will show how much bonus you could earn in the next page.
        </p>
        <div>
            <div v-for="(question, key) in questions" :key="key" class="mb-4">
                <label><b>{{ question.label }}</b></label>
                <div>
                    <div v-for="(label, index) in likertLabels" :key="index" class="mb-1">
                        <input type="radio" :id="`${key}-${index}`" :name="key" :value="index+1" v-model="surveyResponses[key]" />
                        <label :for="`${key}-${index}`">{{ label }}</label>
                    </div>
                </div>
            </div>
            <button class="btn btn-primary" @click="submitSurvey">Submit</button>
          </div>
    </div>
</div>
</template>

<style scoped>
.mb-4 {
    margin-bottom: 1.5rem;
}
.mb-1 {
    margin-bottom: 0.5rem;
}
</style>
