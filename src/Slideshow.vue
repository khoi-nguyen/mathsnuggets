<template lang="pug">
.reveal
  .slides
    section(v-for="(slide, index) in children")
      node(component="slide" v-bind="slide" :position="`children.${index}`")
  clipboard.clipboard
</template>

<script>
import Reveal from 'reveal.js'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

import Clipboard from './Clipboard'
import Node from './Node'

export default {
  computed: {
    ...mapGetters('resource', ['url']),
    ...mapState(['auth', 'config']),
    ...mapState('resource', ['children'])
  },
  methods: {
    ...mapMutations('config', ['changeSlide']),
    ...mapActions('resource', ['loadSlideshow', 'save'])
  },
  sockets: {
    forceSlideChange (data) {
      Reveal.slide(data.slide, 0, 0)
    }
  },
  async mounted () {
    await this.loadSlideshow()
    this.$socket.emit('join', this.url)
    Reveal.initialize({
      center: false,
      hash: true,
      help: false,
      height: 1080,
      margin: 0,
      navigationMode: 'grid',
      pause: false,
      slideNumber: 'c/t',
      touch: false,
      transition: 'none',
      width: 1920
    })
    Reveal.on('slidechanged', event => this.changeSlide(event.indexh))
  },
  components: {
    Clipboard,
    Node
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
.clipboard {
  position: absolute;
  opacity: 1;
  z-index: 10000;
  bottom: 0;
  right: 0;
}
</style>
