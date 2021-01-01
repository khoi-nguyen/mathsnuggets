import 'regenerator-runtime/runtime'
import AsyncComputed from 'vue-async-computed'
import VueRouter from 'vue-router'
import Buefy from 'buefy'
import VueSocketIO from 'vue-socket.io'

import titleMixin from './titleMixin'

const Vue = require('vue/dist/vue.js')
const App = () => import('./App')
const About = () => import('./About')
const HomePage = () => import('./HomePage')
const LoginPage = () => import('./LoginPage')
const Resources = () => import('./Resources')
const Slideshow = () => import('./Slideshow')

Vue.use(AsyncComputed)
Vue.use(Buefy)
Vue.use(VueRouter)
Vue.use(new VueSocketIO({
  connection: process.env.APP_URL
}))
Vue.mixin(titleMixin)

const routes = [
  { path: '/', component: HomePage },
  { path: '/about', component: About },
  { path: '/login', component: LoginPage },
  { path: '/resources', component: Resources },
  { path: '/resources/', component: Resources },
  { path: '/resources/:teacher', component: Resources },
  { path: '/resources/:teacher/', component: Resources },
  { path: '/resources/:teacher/:year', component: Resources },
  { path: '/resources/:teacher/:year/', component: Resources },
  { path: '/resources/:teacher/:year/:slug', component: Slideshow },
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
