<script setup>
import { ref, computed } from 'vue';
import { useParticipantStore } from '@/stores/participant';
import { useGroupStore } from '@/stores/group';
import { useTurnStore } from '@/stores/turn';
import { useChatStore } from '@/stores/chat';
import Animal from '@/components/Animal.vue';

const send_out_message = ref('');
const participantStore = useParticipantStore();
const turnStore = useTurnStore();
const groupStore = useGroupStore();
const chatStore = useChatStore();

const get_participant_name = (participant_id) => {
  // Check the role description of the participant from turn.
  let participant = turnStore.candidate_roles.find(candidate_role => candidate_role.participant === participant_id);
  if (participant) {
    return participant.role_desc + " Committee";
  }
  return "";
};

const messages = chatStore.messages;


function sendMessage() {
  chatStore.sendMessage({
    "type": "message",
    "sender": participantStore.participant_id,
    "turn_number": turnStore.turn_number,
    "content": send_out_message.value
  });
  send_out_message.value = '';
}

// Avoid to directly access the groupStore
function avatarColorById(participant_id) {
  return groupStore.getParticipantAvatarColorById(participant_id);
}
function avatarAnimalById(participant_id) {
  return groupStore.getParticipantAvatarAnimalById(participant_id);
}

function avatarNameById(participant_id) {
  return avatarColorById(participant_id) + " " + avatarAnimalById(participant_id) + " (" + get_participant_name(participant_id) + ")";
}

function current_state(member) {
  // 1: not ready, 2: ready to vote, 3: voted
  // Search the member in the groupStore
  let participant = groupStore.participants.find(participant => participant._id === member._id);
  if (participant) {
    if (participant.complete_final !== null && participant.complete_final === true) {
      // If complete_final is not null and is true, return 3
      return 3;
    }
    // If ready_to_vote is not null and is true, return 2
    if (participant.ready_to_vote !== null && participant.ready_to_vote === true) {
      return 2;
    }
    if (participant.complete_initial !== null && participant.complete_initial === true) {
      // If complete_initial is not null and is true, return 1
      return 1;
    }
    
  }
  return 0; // Default to not ready
}

// Given a message, format the message content. Replace the \n with <br>.
function formatMessageContent(content) {
  return content.replace(/\n/g, '<br>');
}

function get_group_condition() {
  // Get the group condition from the groupStore
  return groupStore.getCondition() !== 0;
}

function get_group_condition_private() {
  // Get the group condition from the groupStore
  return groupStore.getCondition() == 1;
}


</script>
<template>
  <div class="chat-room">
    <div class="member-area">
      <span v-for="member in groupStore.participants" :key="member._id" class="member-card">
        <Animal
          :color="avatarColorById(member._id)"
          :name="avatarAnimalById(member._id)"
          size="22px"
          class="avatar-icon"
        />
        {{ avatarColorById(member._id) + " " + avatarAnimalById(member._id) }}
        <font-awesome-icon icon="fa-solid fa-circle" :class="{'green_icon': current_state(member)=== 3, 'yellow_icon': current_state(member) === 2, 'gray_icon': current_state(member) === 1, 'red_icon': current_state(member) === 0 }"/>
      </span>
      <div class="card">
        <div class="collapse" id="collapseRule">
          <div class="card-body">
            <p><strong>Voting Status</strong> <br>
              <font-awesome-icon icon="fa-solid fa-circle" class="red_icon"/> Errors! <br>
              <font-awesome-icon icon="fa-solid fa-circle" class="gray_icon"/> Not Ready <br>
              <font-awesome-icon icon="fa-solid fa-circle" class="yellow_icon"/> Ready to vote <br>
              <font-awesome-icon icon="fa-solid fa-circle" class="green_icon"/> Made final vote!<br>
            </p>
          </div>
        </div>

        <button class="card-footer" data-bs-toggle="collapse" href="#collapseRule" role="button" aria-expanded="false" aria-controls="collapseRule">Icon Explanation</button>
      </div>
    </div>
    <div class="room-area" ref="roomarea">
      <div v-if="get_group_condition()" class="chat-info">
        You can call the LLM assistant to summarize the conversation by typing "<b>@Quori</b>" in the message box. <br>
      </div>
      <div v-for="message in messages" :key="message.id" class="message-card">
        
        <!-- message from LLM asssitant -->
        <div class="row" v-if="message.sender.participant_id === -1">
          <div class="col-1 icon-div">
            <div class="message-avatar-icon">
              <font-awesome-icon icon="fa-solid fa-robot" class="circle-icon"/>
            </div>
          </div>
          <div class="col-9">
            <div class="row">
              <div class="message-avatar-name">Quori<span v-if="get_group_condition_private()"> (PRIVATE MESSAGE)</span></div>
            </div>
            <div class="row">
              <div :class="get_group_condition_private() ? 'llm-message-private' : 'llm-message'">
                <span v-html="formatMessageContent(message.content)"></span>
              </div>
            </div>
          </div>
        </div>
        <!-- message from other participants, where the sender's participant id does not match the partcipants in the useParticipantStore -->
        <div class="row" v-else-if=" message.sender.participant_id !== participantStore.participant_id">
          <div class="col-1 icon-div">
            <div class="message-avatar-icon">
              <Animal
                :color="avatarColorById(message.sender.participant_id)"
                :name="avatarAnimalById(message.sender.participant_id)"
                size="35px"
              />
            </div>
          </div>
          <div class="col-9">
            <div class="row">
                <div class="message-avatar-name">
                  {{ avatarNameById(message.sender.participant_id) }}
                </div>
            </div>
            <div class="row">
              <div class="message-content">
                <div class="message-border">
                  <span v-html="formatMessageContent(message.content)"></span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- message from the participant himself or herself -->
        <div class="row own_message" v-else>
          <div class="col-2"></div>
          <div class="col-9">
            <div class="row">
              <div class="message-avatar-name">
                {{ avatarNameById(message.sender.participant_id) }}
              </div>
            </div>
            <div class="row">
              <div class="message-content">
                <div class="message-border">
                  <span v-html="formatMessageContent(message.content)"></span>
                </div>
              </div>
            </div>
          </div>
          <div class="col-1 icon-div-own">
            <div class="message-avatar-icon">
              <Animal
                :color="avatarColorById(message.sender.participant_id)"
                :name="avatarAnimalById(message.sender.participant_id)"
                size="35px"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="message-area">
      <div class="input-group message-input-area">
        <input type="text" class="form-control" placeholder="Type your message here..." v-model="send_out_message" @keyup.enter="sendMessage">
        <button class="btn btn-primary message-send-button" @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
</template>
<style scoped>
  .chat-room {
    /* height: calc(100vh - 70px); */
    height: calc(100vh - 140px); /* TODO: add it back */
    min-height: 391px;
    width: 100%;
    border: solid 1px #1d3557;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
  }

  @media (max-height: 600px) {
    .chat-room {
      height: calc(100vh - 150px);
    }
  }

  .member-area {
    padding: 10px 15px;
    border-bottom: solid 1px #E5E5E5;
    line-height: 20px;
  }

  .member-card {
    display: inline-block;
    padding: 4px 5px;
    background-color: #e5e5e5;
    line-height: 20px;
    border-radius: 5px;
    text-align: center;
    margin-right: 2px;
    margin-bottom: 10px;
  }

  .card {
    border: solid 1px black;
  }

  .card-footer {
    background-color: #5C636A;
    color: white;
    border: none;
    text-align: center;
    cursor: pointer;
  }

  .room-area {
    padding: 10px 0 10px 10px;
    /* min-height: 300px; */
    max-height: 800px;
    background-color: white;
    height: 100vh;
    border-radius: 10px;
    overflow-x: none;
    flex: 1;
    overflow-y: auto;
  }

  .message-card {
    padding-bottom: 10px;
  }

  .message-card .row{
    width: 100%;
  }

  .icon-div {
    vertical-align: bottom;
    margin: auto 0 0 0;
    padding-right: 40px;
  }

  .icon-div-own {
    vertical-align: bottom;
    margin: auto 0 0 0;
  }

  .avatar-icon {
    /* border-radius: 50%; */
    display: inline-block;
    margin-right: 5px;
  }

  .message-avatar-icon {
    display: block;
    text-align: center;
    line-height: 40px;
  }

  .circle-icon-judge {
    background: #432818;
    color:  #FFFFFF;
    width: 20px;
    height: 16px;
    border-radius: 50%;
    text-align: center;
    line-height: 30px;
    vertical-align: middle;
    padding: 7px 5px;
  }

  .circle-icon {
    background: #980002;
    color:  #FFFFFF;
    width: 20px;
    height: 16px;
    border-radius: 50%;
    text-align: center;
    line-height: 30px;
    vertical-align: middle;
    padding: 7px 5px;
  }

  .message-avatar-name {
    padding-left: 0px;
    font-size: 0.8em;
  }

  .message-content {
    display: inline-block;
  }

  .message-border {
    width: fit-content;
    background-color: #0184ff;
    color:  #ffffff;
    padding: 3px 15px;
    border-radius: 15px;
    margin-right: auto;
    margin-left: 0;
  }


  .llm-message {
    background:#ffefc1;          /* distinguishable */
    border-left:3px solid #f0b90b;/* accent */
    padding:3px 15px;
    border-radius:15px;
    max-width:90%;
    opacity:0.92;
  }

  .llm-message-private{
    background:#ffefc1;          /* distinguishable */
    border-left:3px solid #f0b90b;/* accent */
    padding:3px 15px;
    border-radius:15px;
    max-width:70%;
    opacity:0.92;
    position: relative;      /* ⬅️ enables absolute child */

  }
  
  .llm-message-private::after {
    content: "PRIVATE LLM MESSAGE  (only visible to you)";
    position: absolute;
    top: 50%;
    left: 150%;
    transform: translate(-50%, -50%);
    font-size: 0.8em;
    font-weight: 600;
    letter-spacing: 0.5px;
    color: #555;
    opacity: 0.25;           /* subtle */
    pointer-events:none;
    z-index:1;  }
    
  .own_message {
    text-align: right;
  }

  .own_message > .col-2{
    margin-right: 0; /* reduce or remove right margin */
    padding-left: 0 !important;
    padding-right: 0 !important;
    /* border-radius: 15px; */
  }

    .own_message > .col-9 {
    margin-right: 0; /* reduce or remove right margin */
    padding-left: 0 !important;
    padding-right: 0px !important;
    /* border-radius: 15px; */
  }

  .own_message .message-content {
    text-align: right;
  }

  .own_message .message-border {
    width: fit-content;
    background-color: #0184ff;
    color:  #ffffff;
    padding: 3px 15px;
    border-radius: 15px;
    margin-left: auto;
    margin-right: 0;
  }

  .own_message .col {
    padding-right: 0;
  }

  .message-area {
    border: solid 1px #1d3557;
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
  }

  .message-input-area {
    background-color: #F0F2F5;
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
  }

  .message-send-button {
    border-top-right-radius: 0px;
    border-bottom-right-radius: 10px;
  }

  .chat-info {
    display: block;
    text-align: left;
    color: #666666;
    border-style: solid;
    border-color: #999999;
    margin-left: -10px;
    margin: 0 20px;
    padding-left: 5px;
    padding-bottom: 10px;
  }

  .red_icon {
    color: #e63946;
  }

  .gray_icon {
    color: #8d99ae;
  }

  .green_icon {
    color: #57cc99;
  }

  .yellow_icon {
    color: #f5cd79;
  }

  .red_icon {
    color: #f42c57;
  }

  .devil_background {
    background-color: #8b0000;
    color: white;
  }

  #accordion-icon, #accordion-rule {
    padding-left: 5px;
    padding-right: 5px;
    background-color: #e5f9f9;
  }
</style>