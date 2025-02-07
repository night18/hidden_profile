import { createRouter, createWebHistory } from 'vue-router';
/* Participant related */
import EntranceView from '@/views/EntranceView.vue';
import TaskInstruction from '@/views/TaskInstruction.vue';
import CandidateExample from '@/views/CandidateExample.vue';
import QualificationTask from '@/views/QualificationTask.vue';

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
    }
  ]
});

export default router