<script setup>
import { ref, computed } from 'vue';
import { useParticipantStore } from '@/stores/participant';
import { useGroupStore } from '@/stores/group';
import { useTurnStore } from '@/stores/turn';
import { useChatStore } from '@/stores/chat';

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

</script>
<template>
  <div class="chat-room">
    <!-- <div class="member-area"> -->
      <!-- <span v-for="member in members" :key="member.id" class="member-card">
        <v-animal size="20px" :name="member.avatar_name" :color="avatarColorHex(member.avatar_color)" class="avatar-icon"/>
        {{member_name(member)}}
        <font-awesome-icon :icon="icon_style(member)" :class="{'green_icon': current_state(member)=== 3, 'yellow_icon': current_state(member) === 2, 'gray_icon': current_state(member) === 1 }"/>
      </span> -->
      <!-- <div class="card">
        <div class="collapse" id="collapseRule">
          <div class="card card-body">
            <p><strong>Voting Status</strong> <br>
              <font-awesome-icon icon="fa-solid fa-circle" class="gray_icon"/> Waiting for vote<br>
              <font-awesome-icon icon="fa-solid fa-circle" class="green_icon"/> Made final vote!<br>
            </p>
          </div>
        </div>

        <button class="card-footer" data-bs-toggle="collapse" href="#collapseRule" role="button" aria-expanded="false" aria-controls="collapseRule">Icon Explanation</button>
      </div> -->
    <!-- </div> -->
    <div class="room-area" ref="roomarea">
      <div class="chat-info">
        Feel free to share your thoughts and ideas here. Let's keep the conversation respectful and constructive!
      </div>
      <div v-for="message in messages" :key="message.id" class="message-card">
        <!-- message from LLM asssitant -->
        <div class="row" v-if="message.sender.participant_id === -1">
          <div class="col-1 icon-div">
            <div class="message-avatar-icon">
              <font-awesome-icon icon="fa-solid fa-globe" class="circle-icon"/>
            </div>
          </div>
          <div class="col-9">
            <div class="row">
              <div class="message-avatar-name">LLM Assistant</div>
            </div>
            <div class="row">
              <div class="message-content">
                <span>{{message.content}}</span>
              </div>
            </div>
          </div>
        </div>
        <!-- message from other participants, where the sender's participant id does not match the partcipants in the useParticipantStore -->
        <div class="row" v-else-if=" message.sender.participant_id !== participantStore.participant_id">
          <div class="col-1 icon-div">
            <div class="message-avatar-icon">
              <font-awesome-icon icon="fa-solid fa-user" class="circle-icon"/>
            </div>
          </div>
          <div class="col-9">
            <div class="row">
              <div class="message-avatar-name"> {{get_participant_name(message.sender.participant_id)}} </div>
            </div>
            <div class="row">
              <div class="message-content">
                <span>{{message.content}}</span>
              </div>
            </div>
          </div>
        </div>
        <!-- message from the participant himself or herself -->
        <div class="row" v-else>
          <div class="col-2"></div>
          <div class="col-9">
            <div class="row">
              <div class="message-avatar-name">{{get_participant_name(message.sender.participant_id)}}</div>
            </div>
            <div class="row">
              <div class="message-content own_message">
                <span>{{message.content}}</span>
              </div>
            </div>
          </div>
          <div class="col-1 icon-div-own">
            <div class="message-avatar-icon">
              <font-awesome-icon icon="fa-solid fa-user" class="circle-icon"/>
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
    margin-bottom: 2px;
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
    vertical-align: center;
    margin: auto 0;
    padding-right: 40px;
  }

  .icon-div-own {
    vertical-align: center;
    margin: auto 0;
  }

  .message-avatar-icon {
    display: inline-block;
    text-align: center;
    line-height: 30px;
    margin: auto 0;
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
    background-color: #E4E6EB;
    padding: 3px 15px;
    border-radius: 10px;
    display: inline-block;
  }

  .own_message {
    margin-left: 0px;
  }

  .own_message .message-content {
    background-color: #0184ff;
    color:  #ffffff;
    margin-right: 0;
    margin-left: auto;
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