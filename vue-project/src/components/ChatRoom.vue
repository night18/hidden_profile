<script setup>
import { ref } from 'vue';

</script>
<template>
  <div class="chat-room">
    <div class="member-area">
      <!-- <span v-for="member in members" :key="member.id" class="member-card">
        <v-animal size="20px" :name="member.avatar_name" :color="avatarColorHex(member.avatar_color)" class="avatar-icon"/>
        {{member_name(member)}}
        <font-awesome-icon :icon="icon_style(member)" :class="{'green_icon': current_state(member)=== 3, 'yellow_icon': current_state(member) === 2, 'gray_icon': current_state(member) === 1 }"/>
      </span> -->
      <div class="card">
        <div class="collapse" id="collapseRule">
          <div class="card card-body">
            <p><strong>Voting Status</strong> <br>
              <font-awesome-icon icon="fa-solid fa-circle" class="gray_icon"/> Waiting for vote<br>
              <font-awesome-icon icon="fa-solid fa-circle" class="green_icon"/> Made final vote!<br>
            </p>
          </div>
        </div>

        <button class="card-footer" data-bs-toggle="collapse" href="#collapseRule" role="button" aria-expanded="false" aria-controls="collapseRule">Icon Explanation</button>
      </div>
    </div>
    <div class="room-area" ref="roomarea">
      <div class="chat-info">
        Feel free to share your thoughts and ideas here. Let's keep the conversation respectful and constructive!
      </div>
      <div v-for="message in messages" :key="message.id" class="message-card">
        <div class="row" v-if="message.sender.subject_id === -1">
          <div class="col-1 vertical-align">
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
      </div>
    </div>
  </div>
</template>
<style scoped>
  .chat-room {
    height: calc(100vh - 70px);
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
    font-size: 0.8em;
  }

  .message-content {
    background-color: #E4E6EB;
    padding: 3px 15px;
    border-radius: 10px;
    display: inline-block;
  }

  .own_message {
    text-align: right;
    margin-left: -10px;
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
    border-radius: 10px;
  }

  .message-input-area {
    background-color: #F0F2F5;
    border-radius: 10px;
  }

  .message-send-button {
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