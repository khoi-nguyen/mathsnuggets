<template lang="pug">
div(:class="{reveal: !form, container: form, form: form}")
  .slides
    section(v-for="(slide, index) in children")
      section(v-for="vpos in range")
        node(
          :additionalAttrs="{ vpos }"
          component="slide"
          :config="config"
          v-bind="slide"
          :position="`children.${index}`"
          @insert-slide="insertSlide(index)"
          @delete-slide="deleteSlide(index)"
          @save="save"
        )
    .container(v-if="form")
      marked-form(:config="config" :url="apiUrl" :form="children")
  tool-bar(:config="config" :slide-payload="slidePayload" v-if="config.authState.loggedIn || !form" @refresh-slideshow="loadSlideshow")
</template>

<script>
import _ from 'lodash'
import Reveal from 'reveal.js'

import { auth } from './auth.js'
import api from './ajax'
import MarkedForm from './MarkedForm'
import Node from './Node'
import ToolBar from './ToolBar'

export default {
  title: 'Slideshow builder',
  props: {
    form: Boolean
  },
  data () {
    const emptySlide = { payload: {}, children: [] }
    return {
      children: [_.cloneDeep(emptySlide), _.cloneDeep(emptySlide)],
      config: {
        authState: auth.state,
        currentSlide: 0,
        edit: false,
        feedback: !this.form,
        form: this.form,
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
    },
    range () {
      if (this.form) {
        return [0]
      }
      return [0, 1]
    },
    slidePayload () {
      return this.children[this.config.currentSlide].payload
    }
  },
  methods: {
    insertSlide (index) {
      this.save({ action: 'insert', [`children.${index}`]: _.cloneDeep(this.emptySlide) })
      this.children.splice(index, 0, _.cloneDeep(this.emptySlide))
    },
    deleteSlide (index) {
      this.save({ action: 'delete', [`children.${index}`]: '' })
      this.children.splice(index, 1)
    },
    async loadSlideshow () {
      if (this.apiUrl) {
        const data = await api(this.apiUrl)
        if (data.length) {
          this.children = data
        }
      }
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
    Reveal.on('slidechanged', event => {
      this.$set(this.config, 'currentSlide', event.indexh)
    })
  },
  components: {
    MarkedForm,
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
.form {
  margin-bottom: 100px;
}
</style>
