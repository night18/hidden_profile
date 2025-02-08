<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import CandidateTable from '@/components/CandidateTable.vue';

const router = useRouter();
// Sample data
const example_candidates = [
  {
    "name": "Candidate A",
    "Number of Courses Taught": "4",
    "Student Teaching Evaluations": "3.0/5.0",
    "Number of Peer-Reviewed Publications": "2",
    "Citation Impact": "5",
    "Service on Editorial Boards": "Yes",
    "Conference Organization Roles": "Yes",
  },
  {
    "name": "Candidate B",
    "Number of Courses Taught": "6",
    "Student Teaching Evaluations": "4.5/5.0",
    "Number of Peer-Reviewed Publications": "5",
    "Citation Impact": "10",
    "Service on Editorial Boards": "No",
    "Conference Organization Roles": "No",
  },
  {
    "name": "Candidate C",
    "Number of Courses Taught": "3",
    "Student Teaching Evaluations": "4.0/5.0",
    "Number of Peer-Reviewed Publications": "10",
    "Citation Impact": "20",
    "Service on Editorial Boards": "Yes",
    "Conference Organization Roles": "No",
  }
];

function next() {
  // Redirect to the next page
  router.push({ name: 'GroupDiscussion' });
}

</script>
<template>
  <div class="container">
    <div class="jumbotron container">
      <h2> Formal Task</h2>
      <div class="content-area">
        <p>You are serving on a university search committee tasked with selecting the most qualified candidate for a faculty position. You will review three candidate profiles and work with other committee members to evaluate their qualifications and make a hiring decision.</p>
        <CandidateTable :candidates="example_candidates"/>
        
        <p>Consider the attributes provided for each candidate and evaluate their qualifications based on the information presented. Remember that each attribute is equally important in the decision-making process.</p>
        <p>After you click the next button, you cannot access the candidate profiles again. But, you could tke notes on a separate sheet of paper.</p>
        
        <button class="btn btn-primary btn-lg" @click="next">Next</button>
      </div>
    </div>
  </div>
</template>