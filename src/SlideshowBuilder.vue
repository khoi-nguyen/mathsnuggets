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
        @validate:title="save(`slides.${index}.title`, $event)"
      )
      slide-editor(
        :position="`slides.${index}`"
        :components.sync="slide.widgets"
        @dragndrop="saveSlide($event.split('.')[1])"
        @validate:widget="save($event.key, $event.value)"
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
          b-button(@click="slide.widgets.push([{type: '', fields: []}])")
            b-icon(pack="fas" icon="columns")
        b-tooltip(
          v-if="authState.loggedIn"
          label="Automatic saving enabled"
          position="is-right"
        )
          b-button
            b-icon(pack="fas" icon="save")
        component-select(@add:widget="slide.widgets[0].push({type: $event, fields: []})")
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
      trash: []
    }
  },
  computed: {
    apiUrl () {
      const slug = this.$route.params.slug
      return slug ? `slideshows/${slug}` : false
    },
    data () {
      const transform = function (obj) {
        return _.transform(obj, function (result, val, key) {
          if ('type' in obj && obj.type === '') {
            return
          }
          if (key === 'fields') {
            const result = {}
            _.forEach(val, function (field) {
              if (field.value !== field.default && !field.computed) {
                result[field.name] = field.value
              }
            })
            val = result
          }
          if (_.isObject(val) || _.isArray(val)) {
            val = transform(val)
          }
          if (!_.isEmpty(val)) {
            result[key] = val
          }
        })
      }
      return transform(this.slideshow)
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
    save (key, value) {
      const payload = {}
      payload[key] = value
      if (this.apiUrl && this.authState.loggedIn) {
        api(this.apiUrl, 'POST', payload)
      }
    },
    saveSlide (slide) {
      const payload = {}
      payload[`slides.${slide}`] = this.data[slide]
      if (this.apiUrl && this.authState.loggedIn) {
        api(this.apiUrl, 'POST', payload)
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
