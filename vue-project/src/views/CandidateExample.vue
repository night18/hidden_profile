<script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import CandidateTable from '@/components/CandidateTable.vue';
  
  const router = useRouter();
  
  // Sample data
  const example_candidates = [
    {
      "name": "Candidate A",
      "Teaching": "Good",
      "Mentorship": "Good",
      "Publications": "Average",
      "Citations": "Average",
      "Service": "Exceptional",
      "Press Coverage": "Exceptional",
    },
    {
      "name": "Candidate B",
      "Teaching": "Exceptional",
      "Mentorship": "Exceptional",
      "Publications": "Average",
      "Citations": "Good",
      "Service": "Average",
      "Press Coverage": "Good",
    },
    {
      "name": "Candidate C",
      "Teaching": "Average",
      "Mentorship": "Good",
      "Publications": "Exceptional",
      "Citations": "Exceptional",
      "Service": "Exceptional",
      "Press Coverage": "Good",
    }
  ];
  
  // Define highlighted cells
  const highlightedCells = [
    { name: "Candidate B", attribute: "Teaching" },
    { name: "Candidate B", attribute: "Mentorship" },
    { name: "Candidate C", attribute: "Publications" },
    { name: "Candidate C", attribute: "Citations" },
    { name: "Candidate A", attribute: "Service" },
    { name: "Candidate C", attribute: "Service" },
    { name: "Candidate A", attribute: "Press Coverage" },
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
          <p>At some point during your committee discussion, your team has collectively revealed the candidates’ performance on six aspects.</p>
          
          <strong>Suppose the team wants to make a decision based on the information revealed thus far. How can you  determine who is the best candidate?</strong>
          <p>The team should consider all the six aspects revealed thus far and evaluate each candidate’s qualification based on their performance on these aspects. <strong>Remember that each attribute is equally important in the decision-making process</strong>.</p>
          
          <!-- Only the highlighted table remains -->
          <CandidateTable :candidates="example_candidates" :highlightedCells="highlightedCells"/>
          
          <p>In this example, the highlighted cells indicate the aspects where each candidate excels. Candidate C excels in more aspects compared to the other two candidates. Since all aspects are equally important, Candidate C should be considered as the best candidate at this point.</p>
  
          <p><strong>However, note that Candidate C may still not be the most qualified candidate overall! </strong> This is because we do not know at this point if the discussion within the team is thorough enough to cover all aspects of evaluation; if not, it is possible that another candidate is a better choice once more information gets revealed! So, it is very important to have a comprehensive discussion before making any decisions!
          </p>
  
          <button class="btn btn-primary btn-lg" @click="next">Try it by yourself</button>
        </div>
      </div>
    </div>
  </template>