import 'regenerator-runtime/runtime'
import AsyncComputed from 'vue-async-computed'
import Vue from 'vue'
import VueRouter from 'vue-router'
import Buefy from 'buefy'

import titleMixin from './titleMixin'

const App = () => import('./App')
const About = () => import('./About')
const HomePage = () => import('./HomePage')
const LoginPage = () => import('./LoginPage')
const Resources = () => import('./Resources')
const Slideshow = () => import('./Slideshow')

Vue.use(AsyncComputed)
Vue.use(Buefy)
Vue.use(VueRouter)
Vue.mixin(titleMixin)

const routes = [
  { path: '/', component: HomePage },
  { path: '/about', component: About },
  { path: '/login', component: LoginPage },
  { path: '/resources', component: Resources },
  { path: '/resources/:slug', component: Slideshow },
  { path: '/slideshow_builder', component: Slideshow }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
