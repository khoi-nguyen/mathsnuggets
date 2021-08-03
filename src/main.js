import 'regenerator-runtime/runtime'
import AsyncComputed from 'vue-async-computed'
import VueRouter from 'vue-router'
import Buefy from 'buefy'
import VueSocketIO from 'vue-socket.io'
import Vuex from 'vuex'
import { sync } from 'vuex-router-sync'

import titleMixin from './titleMixin'

import auth from './store/auth'
import config from './store/config'
import resource from './store/resource'

const Vue = require('vue/dist/vue.min.js')
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
  connection: window.location.origin
}))
Vue.mixin(titleMixin)
Vue.use(Vuex)

const routes = [
  { path: '/', component: HomePage },
  { path: '/about', component: About },
  { path: '/login', component: LoginPage },
  { path: '/resources', component: Resources },
  { path: '/resources/', component: Resources },
  { path: '/resources/:url(.*)', component: Slideshow }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

const store = new Vuex.Store({
  modules: { auth, config, resource }
})

sync(store, router)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
