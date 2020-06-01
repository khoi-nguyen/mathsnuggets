import Vue from 'vue'
import VueRouter from 'vue-router'

import App from './App'
import HomePage from './HomePage'
import SlideshowBuilder from './SlideshowBuilder'

Vue.use(VueRouter)

const routes = [
  { path: '/', component: HomePage },
  { path: '/slideshow_builder', component: SlideshowBuilder }
]

const router = new VueRouter({
  routes
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
