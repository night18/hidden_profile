import { createRouter, createWebHistory } from 'vue-router';
/* Participant related */
import EntranceView from '@/views/EntranceView.vue';
import TaskInstruction from '@/views/TaskInstruction.vue';
import TaskInstructionCont from '@/views/TaskInstructionCont.vue';
import TaskInstructionContinued from '@/views/TaskInstructionContinued.vue';
import CandidateExample from '@/views/CandidateExample.vue';
import QualificationTask from '@/views/QualificationTask.vue';
import WaitingRoom from '@/views/WaitingRoom.vue';
import FormalCandidate from '@/views/formal/FormalCandidate.vue';
import GroupDiscussion from '@/views/formal/GroupDiscussion.vue';
import FailPairing from '@/views/errors/FailPairing.vue';
import NetiquetteRule from '@/views/NetiquetteRule.vue';
import FormalInstruction from '@/views/FormalInstruction.vue';
import ExitView from '@/views/ExitView.vue';
import TeammateLeft from '@/views/errors/TeammateLeft.vue';
import PostSurvey from '@/views/PostSurvey.vue';

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
      path: '/TaskInstructionCont',
      name: 'TaskInstructionCont',
      component: TaskInstructionCont,
    },
    {
      path: '/TaskInstructionContinued',
      name: 'TaskInstructionContinued',
      component: TaskInstructionContinued
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
      path: '/FormalInstruction',
      name: 'FormalInstruction',
      component: FormalInstruction,
    },
    {
      path: '/NetiquetteRule',
      name: 'NetiquetteRule',
      component: NetiquetteRule,
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
      path: '/PostSurvey',
      name: 'PostSurvey',
      component: PostSurvey,
    },
    {
      path: '/FailPairing',
      name: 'FailPairing',
      component: FailPairing,
    },
    {
      path: '/exit',
      name: 'exit',
      component: ExitView,
    },
    {
      path: '/TeammateLeft',
      name: 'TeammateLeft',
      component: TeammateLeft,
    },
  ]
});

export default router