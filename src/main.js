import Eagle from 'eagle.js'
import SlideshowBuilder from './SlideshowBuilder'
import Vue from 'vue'

import 'bulma/css/bulma.css'
import '@fortawesome/fontawesome-free/js/all.js'

Vue.use(Eagle)

new Vue({
  render: h => h(SlideshowBuilder)
}).$mount('#app')
