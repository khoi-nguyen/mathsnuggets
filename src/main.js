import 'regenerator-runtime/runtime'
import Vue from 'vue'
import VueRouter from 'vue-router'
import Buefy from 'buefy'

import App from './App'
import About from './About'
import HomePage from './HomePage'
import LoginPage from './LoginPage'
import Resources from './Resources'
import SlideshowBuilder from './SlideshowBuilder'

Vue.use(Buefy)
Vue.use(VueRouter)

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
