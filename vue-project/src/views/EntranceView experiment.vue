
<script setup>
import { ref, getCurrentInstance } from 'vue';
import { useRouter } from 'vue-router';
import { useParticipantStore } from '@/stores/participant';
import Swal from 'sweetalert2'
import axios from 'axios';

const router = useRouter();

const TEST_MODE = getCurrentInstance().appContext.config.globalProperties.$TEST_MODE;
const testId = ref('');
const condition = ref('');
const url = window.location.href; 
const prolific_test = false;
function startTask() {
  let body = new FormData();
  
  if (TEST_MODE) {
    if (testId.value === '') {
      Swal.fire({
        icon: 'error',
        title: 'Test ID is required',
        text: 'Please enter the test ID',
      });
      return;
    }
    if (condition.value === '') {
      Swal.fire({
        icon: 'error',
        title: 'Condition is required',
        text: 'Please select the condition',
      });
      return;
    }

    body.append('worker_id', testId.value);
    body.append('condition', condition.value);
    body.append('study_id', 'test');
    body.append('session_id', 'test');
  } else {
    /** 
     * Prolicfic Crowd Worker ID
     * https://dev.d1uau7ss3lp78y.amplifyapp.com/qualificationentrance/?PROLIFIC_PID={{%PROLIFIC_PID%}}&STUDY_ID={{%STUDY_ID%}}&SESSION_ID={{%SESSION_ID%}}
     */
    if (url.indexOf('?') === -1) {
      Swal.fire({
        icon: 'error',
        title: 'Invalid URL',
        text: 'Please return the task',
      });
      return;
    }

    let prolificArray = url.split('?')[1].split('&'); // ['PROLIFIC_PID=123', 'STUDY_ID=123', 'SESSION_ID=123']
    let worker_id = prolificArray[0].split('=')[1];
    worker_id += '_' + Math.floor(1000 + Math.random() * 9000); // Append a random 4-digit number
    let study_id = prolificArray[1].split('=')[1];
    let session_id = prolificArray[2].split('=')[1];




    if (
      typeof worker_id === 'undefined' || 
      worker_id === null || 
      worker_id === '') 
    {
      Swal.fire({
        icon: 'error',
        title: 'Could not get the worker ID',
        text: 'Please return the task',
      });
      return;
    }

    body.append('worker_id', worker_id)
    body.append('study_id', study_id)
    body.append('session_id', session_id)
  }

  axios.post('/create_participant/', body)
    .then((response) => {
      if (response.status === 201) {
        useParticipantStore().setParticipantId(response.data.participant_id);
        router.push({ name: 'TaskInstruction' });
      } else {
        Swal.fire({
          icon: 'error',
          title: 'Could not store the participant id to browser',
          text: 'Please return the task',
        });
        return;
      }
    })
    .catch((error) => {
      console.error("Error creating participant:", error.response ? error.response.data : error);

      Swal.fire({
        icon: 'error',
        title: 'Could not create the participant',
        text: 'Please return the task',
      });
      return;
    });
}
</script>
<template>
  <div class="container">
    <div class="jumbotron container">
      <h1> Faculty Search Committee Decision-Making Task </h1>
      <br />
      <div class="content-area">
          <p>You are serving on a university search committee tasked with selecting the most qualified candidate for a faculty position. You will review three candidate profiles and work with other committee members to evaluate their qualifications and make a hiring decision.</p>
          <p>Your role is to carefully assess each candidate based on the provided information and contribute to a thoughtful discussion with your fellow committee members. </p>
          
          <p><b>Bonus opportunity:</b> for each group task, you can earn <b>$1.5 </b>as an additional personal bonus  if the candidate that your group selects in the end is indeed the candidate who excels on more aspects than other candidates when considering all aspects of evaluation. 
            </p>
          <p>You can take this task only once. Also, please <strong>DO NOT</strong> refresh the page.</p>
          <p>Sounds interesting? Push the button below to start the task.</p>
          <div class="button-area">
              <template v-if="TEST_MODE">
                  <div class="test-mode">
                      <p>This area with red boundary should only shows in the test mode. If you see the area, please return the tasks and contact the requesters.</p>
                      <div class="form-group">
                          <label for="test_id">Test ID:</label>
                          <input type="text" id="test_id" v-model="testId" class="form-control" />
                      </div>
                      <br>Condition:
                      <div class="btn-group" role="group" >
                          <input type="radio" id="no_llms" value="0" v-model="condition" class="btn-check" autocomplete="off"/>
                          <label for="no_llms" class="btn btn-outline-primary">No LLMs</label>
                      
                          <input type="radio" id="individual_llms" value="1" v-model="condition" class="btn-check" autocomplete="off"/>
                          <label for="individual_llms" class="btn btn-outline-primary">Individual-level LLMs</label>
                      
                          <input type="radio" id="group_llms" value="2" v-model="condition" class="btn-check" autocomplete="off"/>
                          <label for="group_llms" class="btn btn-outline-primary">Group-level LLMs</label>
                      </div>
                  </div>
              </template>
              <button class="btn btn-primary btn-lg" @click="startTask">Start Task</button>
          </div>
      </div>
    </div>
  </div>
  </template>
<style scoped>
    .test-mode{
        border: 1px solid red;
        padding: 10px;
        margin: 10px 0;
    }
</style>
