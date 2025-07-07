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
      <h2> Faculty Search Example </h2>
      <div class="content-area">
        <p>At some point during your committee discussion, your team has collectively revealed the candidates’ performance on six aspects, as shown in the table below: </p>
        <CandidateTable :candidates="example_candidates"/>
        <strong>Suppose the team wants to make a decision based on the information revealed thus far. How can you  determine who is the best candidate?</strong>
        <p>The team should consider all the six aspects revealed thus far  and evaluate each candidate’s qualification based on their performance on these aspects. <strong>Remember that each attribute is equally important in the decision-making process</strong> .</p>
        <CandidateTable :candidates="example_candidates" :highlightedCells="highlightedCells"/>
        <p>In this example, the highlighted cells indicate the aspects where each candidate excels. Candidate C excels in more aspects compared to the other two candidates. Since all aspects are equally important, Candidate C should be considered as the best candidate at this point.</p>

        <p>However, note that Candidate C may still not be the most qualified candidate overall! This is because we do not know at this point if the discussion within the team is thorough enough to cover all aspects of evaluation; if not, it is possible that another candidate is a better choice once more information gets revealed! So, it is very important to have a comprehensive discussion before making any decisions!
        </p>

        <button class="btn btn-primary btn-lg" @click="next">Try it by yourself</button>
      </div>
    </div>
  </div>
</template>