import Vue from 'vue'
import VueRouter from 'vue-router'

import App from './App'
import About from './About'
import HomePage from './HomePage'
import LoginPage from './LoginPage'
import Plot from './Plot'
import SlideshowBuilder from './SlideshowBuilder'

Vue.use(VueRouter)

const routes = [
  { path: '/', component: HomePage },
  { path: '/about', component: About },
  { path: '/login', component: LoginPage },
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
