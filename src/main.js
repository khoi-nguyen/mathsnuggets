import Vue from 'vue'
import VueRouter from 'vue-router'
import VTooltip from 'v-tooltip'
import Buefy from 'buefy'

import App from './App'
import About from './About'
import HomePage from './HomePage'
import LoginPage from './LoginPage'
import Plot from './Plot'
import Resources from './Resources'
import SlideshowBuilder from './SlideshowBuilder'

Vue.use(Buefy)
Vue.use(VueRouter)
Vue.use(VTooltip)

const routes = [
  { path: '/', component: HomePage, props: { navbar: true } },
  { path: '/about', component: About, props: { navbar: true } },
  { path: '/login', component: LoginPage, props: { navbar: true } },
  { path: '/plot', component: Plot, props: { navbar: true } },
  { path: '/resources', component: Resources, props: { navbar: true } },
  { path: '/resources/:id', component: SlideshowBuilder, props: { navbar: false } },
  { path: '/slideshow_builder', component: SlideshowBuilder, props: { navbar: false } }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
