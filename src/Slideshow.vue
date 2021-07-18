<template lang="pug">
.reveal
  .slides
    section(v-for="(slide, index) in children")
      node(
        component="slide"
        v-bind="slide"
        :position="`children.${index}`"
        @insert-slide="insertSlide(index)"
        @delete-slide="deleteSlide(index)"
        @save="save"
      )
  tool-bar(
    :slide-payload="children[config.currentSlide].payload"
    @refresh-slideshow="loadSlideshow"
  )
</template>

<script>
import Reveal from 'reveal.js'
import { mapActions, mapMutations, mapState } from 'vuex'

import Node from './Node'
import ToolBar from './ToolBar'

export default {
  computed: {
    ...mapState(['auth', 'config']),
    ...mapState('resource', ['children'])
  },
  methods: {
    ...mapMutations('config', ['changeSlide']),
    ...mapActions('resource', ['insertSlide', 'deleteSlide', 'loadSlideshow', 'save'])
  },
  async mounted () {
    await this.loadSlideshow()
    Reveal.initialize({
      center: false,
      hash: true,
      help: false,
      height: 1080,
      margin: 0,
      navigationMode: 'grid',
      pause: false,
      slideNumber: 'h.v',
      touch: false,
      transition: 'none',
      width: 1920
    })
    Reveal.on('slidechanged', event => this.changeSlide(event.indexh))
  },
  components: {
    Node,
    ToolBar
  }
}
</script>

<style scoped>
.reveal .slides {
  margin-right: auto;
  margin-left: 0;
}
.reveal .slides section {
  height: 100%;
  padding: 0;
  text-align: left;
}
</style>
