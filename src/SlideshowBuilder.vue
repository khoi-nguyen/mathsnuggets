<template lang="pug">
div.reveal
  div.slides
    section(
      v-for="slideData in data"
    )
      SlideEditor(
        :title.sync="slideData.title"
        :components.sync="slideData.components"
      )
</template>

<script>
import Reveal from 'reveal.js/js/reveal'
import 'reveal.js/css/reveal.css'
import 'bulma/css/bulma.css'
import '@fortawesome/fontawesome-free/js/all.js'

import SlideEditor from './SlideEditor'

export default {
  data () {
    return {
      emptySlide: [
        { title: '', components: [[{ type: '', fields: [] }]] }
      ],
      data: [
        { title: 'Your first slide', components: [[{ type: '', fields: [] }]] },
        { title: 'Your second slide', components: [[{ type: '', fields: [] }]] }
      ]
    }
  },
  mounted () {
    Reveal.initialize({
      center: false,
      height: '100%',
      margin: 0,
      transition: 'none',
      width: '100%'
    })
  },
  components: {
    SlideEditor
  }
}
</script>

<style>
body, html {
  overflow: hidden;
}
</style>

<style scoped>
.slides section {
  padding: 0;
  text-align: left;
}
</style>
