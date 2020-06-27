<template lang="pug">
div.reveal
  div.trash
    draggable(group="widgets" v-model="trash")
  div.slides
    section(
      v-for="(slide, index) in slideshow"
    )
      slide-title(
        :value.sync="slide.title"
        @validate:title="save('update', `slides.${index}.title`, $event)"
      )
      slide-editor(
        :position="`slides.${index}`"
        :components.sync="slide.widgets"
        @delete:widget="save('delete', $event)"
        @insert:widget="save('insert', $event.key, $event.value)"
        @swap:widget="save('swap', $event.key, $event.value)"
        @validate:widget="save('update', $event.key, $event.value)"
      )
      .buttons
        b-tooltip(label="Back to resources list" position="is-right")
          b-button(tag="a" href="/resources")
            b-icon(pack="fas" icon="sign-out-alt")
        b-tooltip(
          v-if="slide.widgets.length == 1"
          label="Split in two columns"
          position="is-right"
        )
          b-button(@click="slide.widgets.push([])")
            b-icon(pack="fas" icon="columns")
        b-tooltip(
          v-if="authState.loggedIn"
          label="Automatic saving enabled"
          position="is-right"
        )
          b-button
            b-icon(pack="fas" icon="save")
        component-select(@add:widget="slide.widgets[0].push({type: $event})")
</template>

<script>
import { auth } from './auth.js'
import Reveal from 'reveal.js'
import _ from 'lodash'
import { api } from './ajax'
import draggable from 'vuedraggable'

import ComponentSelect from './ComponentSelect'
import SlideEditor from './SlideEditor'
import SlideTitle from './SlideTitle'

export default {
  title: 'Slideshow builder',
  data () {
    const emptySlide = { title: '', widgets: [[]] }
    return {
      authState: auth.state,
      slideshow: [_.cloneDeep(emptySlide), _.cloneDeep(emptySlide)],
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
  watch: {
    slideshow: {
      handler () {
        if (!_.isEqual(this.slideshow[this.slideshow.length - 1], this.emptySlide)) {
          this.slideshow.push(_.cloneDeep(this.emptySlide))
          this.$nextTick(() => (Reveal.sync()))
        }
      },
      deep: true
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
      this.slideshow = data
      this.$nextTick(() => (Reveal.sync()))
    }
  },
  methods: {
    save (action, key, value = '') {
      const payload = { action: action }
      payload[key] = value
      this.saveStack.push(payload)
      setTimeout(this.sendSaveStack, 200)
    },
    sendSaveStack () {
      if (this.saveStack.length && this.apiUrl && this.authState.loggedIn) {
        api(this.apiUrl, 'POST', this.saveStack)
        this.saveStack = []
      }
    }
  },
  components: {
    ComponentSelect,
    draggable,
    SlideEditor,
    SlideTitle
  }
}
</script>

<style scoped>
.reveal .slides section {
  height: 100%;
  padding: 0;
  text-align: left;
}
.buttons {
  bottom: 35px;
  left: 10px;
  position: absolute;
}
.buttons span, .buttons a {
  cursor: pointer;
  color: inherit;
  margin-right: 0.2em;
}
.trash {
  bottom: 0;
  height: 150px;
  position: absolute;
  text-align: center;
  width: 100%;
}
</style>
