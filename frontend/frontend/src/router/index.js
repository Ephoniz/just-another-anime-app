import Vue from 'vue';
import VueRouter from 'vue-router';
import TheShark from '../components/TheShark.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/shark',
    name: 'TheShark',
    component: TheShark
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;
