<template lang="pug">
.reveal(:class="{graphPaper: config.graphPaper}")
  .slides
    section(v-for="(slide, index) in children")
      node(
        component="slide"
        :config="config"
        v-bind="slide"
        :position="`children.${index}`"
        @insert-slide="insertSlide(index)"
        @save="save"
      )
  tool-bar(:config="config")
</template>

<script>
import _ from 'lodash'
import Reveal from 'reveal.js'

import { auth } from './auth.js'
import api from './ajax'
import Node from './Node'
import ToolBar from './ToolBar'

export default {
  title: 'Slideshow builder',
  data () {
    const emptySlide = { payload: {}, children: [] }
    return {
      children: [_.cloneDeep(emptySlide), _.cloneDeep(emptySlide)],
      config: {
        authState: auth.state,
        currentSlide: 0,
        edit: false,
        columns: false,
        graphPaper: false,
        whiteboardMode: false
      },
      emptySlide: emptySlide,
      saveStack: []
    }
  },
  computed: {
    apiUrl () {
      const params = this.$route.params
      return params.slug ? `slideshows/${params.teacher}/${params.year}/${params.slug}` : false
    }
  },
  watch: {
    'config.columns' (newValue) {
      Reveal.configure({ width: newValue ? '50%' : '100%' })
    }
  },
  methods: {
    insertSlide (index) {
      this.save({ action: 'insert', [`children.${index}`]: _.cloneDeep(this.emptySlide) })
      this.children.splice(index, 0, _.cloneDeep(this.emptySlide))
    },
    save (payload) {
      if (!_.isEqual(this.children[this.children.length - 1], this.emptySlide)) {
        this.children.push(_.cloneDeep(this.emptySlide))
      }
      if (this.apiUrl && this.config.authState.loggedIn) {
        this.saveStack.push(payload)
        setTimeout(this.sendSaveStack, 200)
      }
    },
    sendSaveStack () {
      if (this.saveStack.length && this.apiUrl && this.config.authState.loggedIn) {
        api(this.apiUrl, 'POST', this.saveStack)
        this.saveStack = []
      }
    }
  },
  async mounted () {
    if (this.apiUrl) {
      const data = await api(this.apiUrl)
      if (data.length) {
        this.children = data
      }
    }
    Reveal.initialize({
      center: false,
      hash: true,
      help: false,
      height: '100%',
      margin: 0,
      pause: false,
      slideNumber: 'c/t',
      touch: false,
      transition: 'none',
      width: '100%'
    })
    Reveal.on('slidechanged', event => {
      this.$set(this.config, 'currentSlide', event.indexh)
    })
  },
  components: {
    Node,
    ToolBar
  }
}
</script>

<style scoped>
.graphPaper {
  background: url('https://upload.wikimedia.org/wikipedia/commons/9/9f/Graph-paper.svg');
}
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
