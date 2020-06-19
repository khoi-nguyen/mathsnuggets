import 'regenerator-runtime/runtime'
import Vue from 'vue'
import VueRouter from 'vue-router'
import Buefy from 'buefy'

import titleMixin from './titleMixin'

const App = () => import('./App')
const About = () => import('./About')
const HomePage = () => import('./HomePage')
const LoginPage = () => import('./LoginPage')
const Resources = () => import('./Resources')
const SlideshowBuilder = () => import('./SlideshowBuilder')

Vue.use(Buefy)
Vue.use(VueRouter)
Vue.mixin(titleMixin)

const routes = [
  { path: '/', component: HomePage },
  { path: '/about', component: About },
  { path: '/login', component: LoginPage },
  { path: '/resources', component: Resources },
  { path: '/resources/:id', component: SlideshowBuilder },
  { path: '/slideshow_builder', component: SlideshowBuilder }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
