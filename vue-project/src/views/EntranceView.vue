
<script setup>
import { ref, getCurrentInstance } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const TEST_MODE = getCurrentInstance().appContext.config.globalProperties.$TEST_MODE;
const testId = ref('');
const condition = ref('');


function startTask() {
    router.push({ name: 'TaskInstruction' });
}
</script>
<template>
  <div class="container">
    <div class="jumbotron container">
      <h1> Faculty Search Committee Decision-Making Task </h1>
      <br />
      <div class="content-area">
          <p>You are serving on a university search committee tasked with selecting the most qualified candidate for a faculty position. You will review three candidate profiles and work with other committee members to evaluate their qualifications and make a hiring decision.</p>
          <p>Your role is to carefully assess each candidate based on the provided information and contribute to a thoughtful discussion with your fellow committee members. Please approach this task as you would in a real faculty hiring process.</p>
          <p>You can take this HIT only once. Also, please DO NOT refresh the page.</p>
          <p>Sound interesting? Push the button below to start the HIT.</p>
          <div class="button-area">
              <template v-if="$TEST_MODE">
                  <div class="test-mode">
                      <p>This area with red boundary should only shows in the test mode. If you see the area, please return the tasks and contact the requesters.</p>
                      <div class="form-group">
                          <label for="test_id">Test ID:</label>
                          <input type="text" id="test_id" v-model="testId" class="form-control" />
                      </div>
                      <br>Condition:
                      <div class="btn-group" role="group" >
                          <input type="radio" id="no_llms" value="none" v-model="condition" class="btn-check" autocomplete="off"/>
                          <label for="no_llms" class="btn btn-outline-primary">No LLMs</label>
                      
                          <input type="radio" id="individual_llms" value="individual" v-model="condition" class="btn-check" autocomplete="off"/>
                          <label for="individual_llms" class="btn btn-outline-primary">Individual-level LLMs</label>
                      
                          <input type="radio" id="group_llms" value="group" v-model="condition" class="btn-check" autocomplete="off"/>
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
<script>

export default {
  name: 'EntranceView',
  data() {
    return {
      
    }
  },
  components: {
    
  },
  computed: {
    
  },
  watch: {
    
  },
  created() {
  },
  mounted() {
    
  },
}
</script>
<style scoped>
    .test-mode{
        border: 1px solid red;
        padding: 10px;
        margin: 10px 0;
    }
</style>
