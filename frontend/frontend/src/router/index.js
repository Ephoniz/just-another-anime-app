import Vue from 'vue';
import VueRouter from 'vue-router';
import AnimeCharacter from '../components/AnimeCharacter.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/anime_characters',
    name: 'Anime characters',
    component: AnimeCharacter
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;
