<template lang="pug">
.reveal
  .slides
    section(v-for="(slide, index) in children")
      node(
        component="slide"
        v-bind="slide"
        :position="`children.${index}`"
        @insert-slide="insertSlide(index)"
        @save="save"
      )
      .clipboard
        draggable(v-model="clipboard" group="widgets")
          node(v-bind="image" v-for="(image, i) in clipboard" component="widget")
</template>

<script>
import Reveal from 'reveal.js'
import { cloneDeep, isEqual } from 'lodash'
import draggable from 'vuedraggable'

import { auth } from './auth.js'
import api from './ajax'
import Node from './Node'

export default {
  title: 'Slideshow builder',
  data () {
    const emptySlide = { payload: {}, children: [] }
    return {
      authState: auth.state,
      children: [cloneDeep(emptySlide), cloneDeep(emptySlide)],
      clipboard: [],
      emptySlide: emptySlide,
      saveStack: []
    }
  },
  computed: {
    apiUrl () {
      const slug = this.$route.params.slug
      return slug ? `slideshows/${slug}` : false
    }
  },
  created () {
    window.addEventListener('paste', this.onPaste.bind(this))
  },
  destroyed () {
    window.removeEventListener('paste', this.onPaste.bind(this))
  },
  methods: {
    insertSlide (index) {
      this.save({ action: 'insert', [`children.${index}`]: cloneDeep(this.emptySlide) })
      this.children.splice(index, 0, cloneDeep(this.emptySlide))
    },
    onPaste (event) {
      const items = (event.clipboardData || event.originalEvent.clipboardData).items

      for (const index in items) {
        const item = items[index]
        if (item.kind === 'file') {
          const blob = item.getAsFile()
          const reader = new FileReader()
          reader.onload = function (e) {
            this.clipboard.push({
              component: 'widget',
              type: 'Image',
              payload: {
                src: e.target.result
              }
            })
          }.bind(this)
          reader.readAsDataURL(blob)
        }
      }
    },
    save (payload) {
      if (!isEqual(this.children[this.children.length - 1], this.emptySlide)) {
        this.children.push(cloneDeep(this.emptySlide))
      }
      if (this.apiUrl && this.authState.loggedIn) {
        this.saveStack.push(payload)
        setTimeout(this.sendSaveStack, 200)
      }
    },
    sendSaveStack () {
      if (this.saveStack.length && this.apiUrl && this.authState.loggedIn) {
        api(this.apiUrl, 'POST', this.saveStack)
        this.saveStack = []
      }
    }
  },
  async mounted () {
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
    if (this.apiUrl) {
      const data = await api(this.apiUrl)
      if (data.length) {
        this.children = data
      }
    }
  },
  components: {
    draggable,
    Node
  }
}
</script>

<style scoped>
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
