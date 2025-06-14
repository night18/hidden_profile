<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const dialogue_management = ref(null);
const information_pooling = ref(null);
const reaching_consensus = ref(null);
const task_division = ref(null);
const time_management = ref(null);
const technical_coordination = ref(null);
const reciprocal_interaction = ref(null);
const individual_task_orientation = ref(null);
const llm_collaboration = ref(null);
const llm_satisfaction = ref(null);
const llm_quality = ref(null);
const llm_recommendation = ref(null);
const llm_future_use = ref(null);

const submitSurvey = async () => {

    
    const surveyData = {
        dialogue_management: dialogue_management.value,
        information_pooling: information_pooling.value,
        reaching_consensus: reaching_consensus.value,
        task_division: task_division.value,
        time_management: time_management.value,
        technical_coordination: technical_coordination.value,
        reciprocal_interaction: reciprocal_interaction.value,
        individual_task_orientation: individual_task_orientation.value,
        llm_collaboration: llm_collaboration.value,
        llm_satisfaction: llm_satisfaction.value,
        llm_quality: llm_quality.value,
        llm_recommendation: llm_recommendation.value,
        llm_future_use: llm_future_use.value,
    };

    try {
        await axios.post('/api/survey', surveyData);
        // router.push('/thank-you');
    } catch (error) {
        console.error('Error submitting survey:', error);
    }
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
    dialogue_management: { label: "Our discussion flowed smoothly without interruptions.", model: dialogue_management },
    information_pooling: { label: "I actively asked for other team members' knowledge or expertise.", model: information_pooling },
    reaching_consensus: { label: "We carefully evaluated different options before agreeing.", model: reaching_consensus },
    task_division: { label: "We clearly divided the task according to our strengths.", model: task_division },
    time_management: { label: "We kept track of time and adjusted our pace accordingly.", model: time_management },
    technical_coordination: { label: "We effectively coordinated our use of the shared workspace.", model: technical_coordination },
    reciprocal_interaction: { label: "We treated each other with respect and as equals.", model: reciprocal_interaction },
    individual_task_orientation: { label: "I stayed focused and motivated throughout the task.", model: individual_task_orientation },
    llm_collaboration: { label: "I feel like I was collaborating with the LLM facilitator during the task.", model: llm_collaboration },
    llm_satisfaction: { label: "I'm satisfied with the assistance provided by the LLM facilitator in completing the tasks.", model: llm_satisfaction },
    llm_quality: { label: "I'm pleased with the quality of the LLM facilitator in completing the tasks.", model: llm_quality },
    llm_recommendation: { label: "I will recommend the LLM facilitator to my friends if they need to complete similar tasks.", model: llm_recommendation },
    llm_future_use: { label: "If given the option, I would use the LLM facilitator to assist me with completing similar decision-making tasks in the future.", model: llm_future_use },
};
</script>

<template>
<div class="container">
    <div class="jumbotron container">
        <h2>Post-Survey</h2>
        <form @submit.prevent="submitSurvey">
            <div v-for="(question, key) in questions" :key="key" class="mb-4">
                <label><b>{{ question.label }}</b></label>
                <div>
                    <div v-for="(label, index) in likertLabels" :key="index" class="mb-1">
                        <input type="radio" :id="`${key}-${index}`" :name="key" :value="label" v-model="question.model" />
                        <label :for="`${key}-${index}`">{{ label }}</label>
                    </div>
                </div>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
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
