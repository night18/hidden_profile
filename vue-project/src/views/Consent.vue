<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const agreeToConsent = () => {
  router.push({ name: 'PreSurvey' }); // Navigate to the next step
};

const disagreeToConsent = () => {
  window.close(); // Close the browser tab or window
};
</script>

<template>
  <div class="container mt-5">
    <div class="card">
      <div class="card-header">
        <h2>Consent Form</h2>
      </div>
      <div class="card-body">
        <h3>Title of Research Study:</h3>
        <p><strong>The Impact of LLM-Based Individual and Group Assistants on Group Decision Making</strong></p>
        <p><strong>IRB number:</strong> STU00223965 Northwestern University</p>
        <p><strong>IRB Number:</strong> IRB-2025-771 Purdue University</p>
        <p><strong>Team:</strong></p>
        <ul>
          <li>Principal Investigator: PhD. Agnes Horvat</li>
          <li>Principal Investigator: PhD. Ming Yin</li>
          <li>Student Member: Jose Cordova (josecordova2027@u.northwestern.edu)</li>
          <li>Student Member: Chun-wei Chiang</li>
        </ul>
        <p><strong>Supported By:</strong> This research is supported by the National Science Foundation.</p>
        <p><strong>Collaborating Institutions:</strong> Purdue University and Northwestern University</p>
        
        <h3>Key Information about this research study:</h3>
        <p>The following is a short summary of this study to help you decide whether to be a part of this study. Information that is more detailed is explained later on in this form.</p>
        <p>The purpose of this study is to understand how different types of AI support affect how people share information and make decisions together.</p>
        <p>Each participant will be asked to read information about a set of candidates, make a group decision with two other participants using an online chat interface (with or without support from an AI assistant), and complete a short survey about their experience.</p>
        <p>We expect that each participant will be in this research study for approximately 15 minutes, in a single online session.</p>
        <p>The primary potential risk of participation is minor discomfort or frustration during the group discussion. There is also a minimal risk of loss of confidentiality (Prolific ID), which we reduce by using secure platforms and anonymized data.</p>
        <p>The main benefit of being in this study is the opportunity to contribute to research that may improve future AI tools for collaborative decision-making.</p>

        <h3>How many people will be in this study?</h3>
        <p>We expect about 360 people will be in this research study.  </p>


        <h3>What should I know about participating in a research study?        </h3>
        <ul>
            <li>Whether or not you take part is up to you.</li>
            <li>You can choose not to take part.</li>
            <li>You can agree to take part and later change your mind.</li>
            <li>Your decision will not be held against you.</li>
            <li>You do not have to answer any question you do not want to answer.</li>
        </ul>


        <h3>Why am I being asked to take part in this research study?</h3>
        <p>We are asking you to take part in this research study because you are an adult residing in the United States who is eligible to participate in online research and capable of engaging in a group decision-making task.</p>




        <h3>What happens if I say, “Yes, I want to be in this research”?</h3>
        <p>If you choose to take part in this research study, here’s what you can expect:</p>
        <ul>
          <li>You will be reminded of your allotted time slot for the experiment using your Prolific ID. The task will be published on Prolific and you will be reminded one day and 30 minutes before the experiment.</li>
          <li>All parts of the study will take place online, and you can complete them from your own computer or device in one session. The entire study will take at most about 15 minutes.</li>
          <li>You will first be asked to read a short description of the study and give your consent to participate.</li>
          <li>Next, you will be asked to review information about three fictional candidates for a job or award. Each participant will see some information that is shared and some that only they can see.</li>
          <li>Then, you will be randomly placed into a group with two other participants, and you’ll be asked to discuss the candidates in a group chat. Your goal is to work together to choose the best candidate based on the available information.</li>
          <li>Depending on your group’s assignment, you may also receive support from an AI assistant (a chatbot). The AI may either provide messages directly to you (private) or send messages visible to the whole group (shared).</li>
          <li>After the discussion and group decision, you will be asked to complete a short survey about your experience, including your thoughts on the group discussion and the AI support (if applicable).</li>
          <li>No video or audio recordings will be made. However, your typed responses and group chat messages will be saved and analyzed. These will be kept anonymous and stored securely.</li>
        </ul>

        <h3>Will being in this study help me in any way?</h3>
        <p>We cannot promise any benefits to you or others from your taking part in this research. However, possible benefits include gaining insight into how group decision-making works, experiencing how AI tools can assist collaborative tasks, and contributing to research that may improve the design of future technologies to support teamwork, communication, and fairer decision-making processes.</p>


        <h3>Is there any way being in this study could be bad for me?</h3>
        <p>You will need to discuss with other people what candidate is better. If you are uncomfortable with any of the discussion content, you can leave the discussion and/or leave the study at any time. Our system would auto block the swear words during the discussion. We wish everyone could respect others’ opinions and keep polite to other members.</p>
        <p>We will collect your crowdsourcing platform ID to pay you the bonus. Breach of confidentiality is always a risk with data, but we will take precautions to minimize this risk, as described in the confidentiality section.</p>


        <h3>What happens if I do not want to be in this research, or I change my mind later?</h3>
        <p>Participation in research is voluntary. You can decide to participate or not to participate. If you do not want to be in this study or withdraw from the study at any point, you can leave the research at any time by exiting the experiment’s website, and it will not be held against you.</p>

        <h3>How will the researchers protect my information?</h3>
        <p>The project's research records may be reviewed by departments at Northwestern and Purdue Universities responsible for regulatory and research oversight. This information sheet is intended to give you informed consent regarding your participation in this research and also to protect your personally identifiable information by not asking for specific details, such as your name. By clicking “I agree” at the end of this form, you agree that you’ve had time to read and consider this consent information sheet and are comfortable with what is being asked of you as a participant. All data collected from participants will be stored on a password-protected online cloud storage account that will only be accessible to the research team. In the experiment, you may need to discuss the prediction tasks with other participants of the study. In this case, you will be assigned an animal nickname/avatar as your anonymous identity. Please do not share any personally identifiable information when you discuss the task with others. Aside from your Mechanical Turk ID or Prolific ID (depending on where you accept the task, no identifiable information will be collected during this study. Your Mechanical Turk ID and Prolific ID will not be shared outside of our research team without your permission, and they will be promptly deleted after compensation has been successfully provided. Names will not be recorded, and participants in the research records will be referred to by an ID number that does not correspond to any personally identifiable information. De-identified data may be used for future research or given to another investigator for future use without additional consent. </p>

        <h3>Who will have access to the information collected during this research study?</h3>
        <p>Efforts will be made to limit the use and disclosure of your personal information, including research study records, to people who have a need to review this information. We cannot promise complete secrecy.</p>
        <p>There are reasons why information about you may be used or seen by other people beyond the research team during or after this study. Examples include:</p>
        <ul>
            <li>University officials, government officials, study funders, auditors, and the Institutional Review Board may need access to the study information to make sure the study is done in a safe and appropriate manner.</li>
            <li>Collaborating researchers at other institutions who are involved with this study.</li>
        </ul>


        <h3>How might the information collected in this study be shared in the future?</h3>
        <p>De-identified data from this study may be shared with the research community, with journals in which study results are published, and with databases and data repositories used for research. We will remove or code any personal information that could directly identify you before the study data are shared. Despite these measures, we cannot guarantee the anonymity of your personal data.</p>

        <h3>Will I be paid or given anything for taking part in this study?</h3>
        <p>You will receive an electronic payment through the Amazon Mechanical Turk (MTurk) platform, for a maximum total of $4.00 for completing this study.</p>
        <ul>
            <li>Base payment (guaranteed): $2.50 for submitting the main survey/task.</li>
            <li>Performance-based bonus: Up to an additional $1.50, awarded according to the accuracy of your answers on the prediction tasks.</li>
        </ul>
        <p><strong>Prorating / early withdrawal:</strong> Participation is entirely voluntary. If you withdraw before finishing all study activities, you will not receive any payment.</p>


        <h3>Who can I talk to?</h3>
        <p>If you have questions, comments, or concerns about this research project, you can talk to one of the researchers. Please contact us, Jose Cordova at josecordova2027@u.northwestern.edu.</p>

        <p> 
          This research has been reviewed and approved by an Institutional Review Board (“IRB”) – an IRB is a committee that protects the rights of people who participate in research studies. You may contact the IRB by phone at (312) 503-1376 or by email at irbcompliance@northwestern.edu if:
          Your questions, concerns, or complaints are not being answered by the research team.
          You cannot reach the research team.
          You want to talk to someone besides the research team.
          You have questions about your rights as a research participant.
          You want to get information or provide input about this research.

          If you want a copy of this consent for your records, you can print it from the screen. 
          If you cannot print the consent and would like a copy for your records, contact the Principal Investigator with the contact information above.
          If you wish to participate, please click the “I Agree” button and you will be taken to the survey.
          If you do not wish to participate in this study, please select X in the corner of your browser. 
          </p>

        <div class="button-area mt-4">
          <button class="btn btn-primary w-100 mb-2" @click="agreeToConsent">I Agree</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  max-width: 800px;
  margin: auto;
}
.card-header {
  text-align: center;
}
.card-body p, .card-body ul {
  font-size: 1rem;
  line-height: 1.6;
}
.button-area button {
  font-size: 1.1rem;
}
</style>