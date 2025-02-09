import { createRouter, createWebHistory } from 'vue-router';
/* Participant related */
import EntranceView from '@/views/EntranceView.vue';
import TaskInstruction from '@/views/TaskInstruction.vue';
import CandidateExample from '@/views/CandidateExample.vue';
import QualificationTask from '@/views/QualificationTask.vue';
import WaitingRoom from '@/views/WaitingRoom.vue';
import FormalCandidate from '@/views/formal/FormalCandidate.vue';
import GroupDiscussion from '@/views/formal/GroupDiscussion.vue';
import FailPairing from '@/views/errors/FailPairing.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'entrance',
      component: EntranceView,
    },
    {
      path: '/TaskInstruction',
      name: 'TaskInstruction',
      component: TaskInstruction,
    },
    {
      path: '/CandidateExample',
      name: 'CandidateExample',
      component: CandidateExample,
    },
    {
      path: '/QualificationTask',
      name: 'QualificationTask',
      component: QualificationTask,
    },
    {
      path: '/WaitingRoom',
      name: 'WaitingRoom',
      component: WaitingRoom,
    },
    {
      path: '/FormalCandidate',
      name: 'FormalCandidate',
      component: FormalCandidate,
    },
    {
      path: '/GroupDiscussion',
      name: 'GroupDiscussion',
      component: GroupDiscussion,
    },
    {
      path: '/FailPairing',
      name: 'FailPairing',
      component: FailPairing,
    }
  ]
});

export default router