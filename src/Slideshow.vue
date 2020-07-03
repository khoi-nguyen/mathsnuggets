<template lang="pug">
.reveal
  .slides
    section(v-for="(slide, index) in children")
      node(
        :cols.sync="slide.cols"
        :component="slide.component"
        :children.sync="slide.children"
        :position="`children.${index}`"
        :title.sync="slide.title"
        @save="save"
      )
  .trash
    draggable(group="widgets" v-model="trash")
</template>

<script>
import Reveal from 'reveal.js'
import { cloneDeep, isEqual } from 'lodash'
import draggable from 'vuedraggable'

import { auth } from './auth.js'
import { api } from './ajax'
import Node from './Node'

export default {
  title: 'Slideshow builder',
  data () {
    const emptySlide = { title: '', cols: 1, component: 'slide', children: [] }
    return {
      authState: auth.state,
      children: [cloneDeep(emptySlide), cloneDeep(emptySlide)],
      emptySlide: emptySlide,
      saveStack: [],
      trash: []
    }
  },
  computed: {
    apiUrl () {
      const slug = this.$route.params.slug
      return slug ? `slideshows/${slug}` : false
    }
  },
  methods: {
    save (payload) {
      if (!isEqual(this.children[this.children.length - 1], this.emptySlide)) {
        this.children.push(cloneDeep(this.emptySlide))
        this.$nextTick(() => (Reveal.sync()))
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
      height: '100%',
      margin: 0,
      slideNumber: 'c/t',
      transition: 'none',
      width: '100%'
    })
    if (this.apiUrl) {
      const data = await api(this.apiUrl)
      if (data.length) {
        this.children = data
        this.$nextTick(() => (Reveal.sync()))
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
.trash {
  bottom: 0;
  height: 150px;
  position: absolute;
  text-align: center;
  width: 100%;
}
.trash div {
  height: 100%;
}
</style>
