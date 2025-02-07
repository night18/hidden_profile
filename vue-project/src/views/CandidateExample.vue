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

// Define highlighted cells
const highlightedCells = [
  { name: "Candidate B", attribute: "Number of Courses Taught" },
  { name: "Candidate B", attribute: "Student Teaching Evaluations" },
  { name: "Candidate C", attribute: "Number of Peer-Reviewed Publications" },
  { name: "Candidate C", attribute: "Citation Impact" },
  { name: "Candidate A", attribute: "Service on Editorial Boards" },
  { name: "Candidate C", attribute: "Service on Editorial Boards" },
  { name: "Candidate A", attribute: "Conference Organization Roles" },
];

function next() {
  // Redirect to the next page
  router.push({ name: 'QualificationTask' });
}

</script>
<template>
  <div class="container">
    <div class="jumbotron container">
      <h2> Candidate Example </h2>
      <div class="content-area">
        <p>You are serving on a university search committee tasked with selecting the most qualified candidate for a faculty position. You will review three candidate profiles and work with other committee members to evaluate their qualifications and make a hiring decision. Here is an example of how the candidate profiles will be presented to you.</p>
        <CandidateTable :candidates="example_candidates"/>
        <strong>In this example, how can we determine who is the best candidate?</strong>
        <p>Consider the attributes provided for each candidate and evaluate their qualifications based on the information presented. Remember that each attribute is equally important in the decision-making process.</p>
        <CandidateTable :candidates="example_candidates" :highlightedCells="highlightedCells"/>
        <p>In this example, the highlighted cells indicate the attributes where each candidate excels. Use this information to compare the candidates and make an informed decision. Remember to consider all attributes and evaluate the candidates holistically to make the best decision.</p>
        <p><strong>Candidate C</strong> excels in more attributes compared to the other candidates. Based on this information, Candidate C may be considered the best candidate in this scenario.</p>
        <button class="btn btn-primary btn-lg" @click="next">Next</button>
      </div>
    </div>
  </div>
</template>