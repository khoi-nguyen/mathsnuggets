import Vue from 'vue'
import VueRouter from 'vue-router'
import VTooltip from 'v-tooltip'
import Buefy from 'buefy'

import App from './App'
import About from './About'
import HomePage from './HomePage'
import LoginPage from './LoginPage'
import Resources from './Resources'
import SlideshowBuilder from './SlideshowBuilder'

Vue.use(Buefy)
Vue.use(VueRouter)
Vue.use(VTooltip)

const routes = [
  { path: '/', component: HomePage },
  { path: '/about', component: About },
  { path: '/login', component: LoginPage },
  { path: '/resources', component: Resources },
  { path: '/resources/:id', component: SlideshowBuilder, props: { slides: true } },
  { path: '/slideshow_builder', component: SlideshowBuilder, props: { slides: true } }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
