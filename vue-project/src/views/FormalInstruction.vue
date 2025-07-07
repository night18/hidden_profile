<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useParticipantStore } from '@/stores/participant';
import axios from 'axios';
/** Animal Anonymous */
import Animal from '@/components/Animal.vue';
import { colors, animals } from '@/components/constants.js';
/** Alert Message */
import Swal from 'sweetalert2'


const router = useRouter();
const avatar_color = ref('');
const avatar_animal = ref('');
const agreement = ref(false);

function generateAvatar() {
    avatar_color.value = Object.keys(colors)[Math.floor(Math.random() * Object.keys(colors).length)];
    avatar_animal.value = animals[Math.floor(Math.random() * animals.length)];
}

function refresh() {
    generateAvatar();
}

function submit() {
    let body = new FormData();
    body.append('participant_id', useParticipantStore().participant_id);
    body.append('avatar_color', avatar_color.value);
    body.append('avatar_name', avatar_animal.value);

    axios.post('/record_avatar/', body)
        .then((response) => {
            if (response.status !== 200) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Failed to record the avatar. Please Return the study and contact the researcher.',
                });
                return;
            }
            router.push({ name: 'WaitingRoom' });
        });
}

generateAvatar();
</script>
<template>
<div class="container">
    <div class="jumbotron container">
        <h2>Group Phase Instruction</h2>
        <div class="content-area">
            <p>Now, we are about to move on to the group phase. You will be assigned to a group of three people to form a search committee. As a member of a search committee, you will be working with other committee members to evaluate the qualifications of three candidates and make a hiring decision. For each of these tasks, you need to follow the following steps:</p>
            <ol>
                <li>Review the candidate profiles and make your initial decision on your own.</li>
                <li>Discuss with other members in your group and vote for the best candidate.</li>
            </ol>
            <p><b>Discussion rules:</b> 
            </p>
            <ul>
                <li>Be respectful. Share your views calmly, and avoid insults, attacks, or threats</li>
                <li>Do NOT give out any of your personal information during the discussion.</li>
            </ul>

            <p><b>Bonus opportunity:</b> for each group task, you can earn <b>$1.5 </b>as an additional bonus  if the candidate that your group selects in the end is indeed the candidate who excels on more aspects than other candidates when considering all aspects of evaluation. 
            </p>
            <p>To protect your identity, we would assign you an avatar to represent you in your group throughout the rest of this study. If you are not satisfied with the assigned avatar, please click the <b>Refresh</b> button to get a new one.</p>
            <div class="avatar-area">
                Your anonymous avatar is: <b>{{ avatar_color }} {{ avatar_animal }}</b> <br>
                <Animal :color="avatar_color" :name="avatar_animal" />
                <button class="btn btn-secondary" @click="refresh">Refresh</button>
                

            </div>

        </div>
        <b>Agreement:</b>

        <div class="form-check">
            <input type="checkbox" class="form-check-input" id="agreement" v-model="agreement" />
            <label class="form-check-label" for="agreement">I have read and agree to follow the discussion rules and instructions.</label>
        </div>

        <button class="btn btn-primary btn-lg" @click="submit" :disabled="!agreement">Next</button>
    </div>
</div>
</template>
<style scoped>
.avatar-area {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-top: 20px;
}

.avatar-area button {
    margin-top: 10px;
}
</style>