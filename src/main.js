import Vue from 'vue'
import VueRouter from 'vue-router'
import VTooltip from 'v-tooltip'

import App from './App'
import About from './About'
import HomePage from './HomePage'
import Plot from './Plot'
import SlideshowBuilder from './SlideshowBuilder'

Vue.use(VueRouter)
Vue.use(VTooltip)

const routes = [
  { path: '/', component: HomePage },
  { path: '/about', component: About },
  { path: '/plot', component: Plot },
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
