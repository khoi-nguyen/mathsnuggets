<template lang="pug">
div.reveal
  div.slides
    section(
      v-for="(slide, index) in slideshow"
    )
      SlideEditor(
        :id="id"
        :title.sync="slide.title"
        :components.sync="slide.widgets"
        @validate:title="saveTitle(index, $event)"
        @validate:widget="saveWidget(index, $event[0], $event[1])"
      )
</template>

<script>
import Reveal from 'reveal.js'
import '@fortawesome/fontawesome-free/js/all.js'
import _ from 'lodash'
import { getSlideshow, saveSlideshow } from './ajax'

import SlideEditor from './SlideEditor'

export default {
  props: {
    embedded: Boolean,
    height: String,
    width: String
  },
  data () {
    const emptySlide = { title: '', widgets: [[{ type: '', fields: [] }]] }
    return {
      id: {},
      slideshow: [_.cloneDeep(emptySlide), _.cloneDeep(emptySlide)]
    }
  },
  computed: {
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
  mounted () {
    getSlideshow(function (data) {
      this.slideshow = data
    }.bind(this))
    Reveal.initialize({
      center: false,
      embedded: this.embedded,
      height: this.height ? this.height : '100%',
      margin: 0,
      transition: 'none',
      width: this.width ? this.width : '100%'
    })
  },
  methods: {
    saveWidget (slide, col, position) {
      const payload = {
        key: `slides.${slide}.widgets.${col}.${position}`,
        patch: this.data[slide].widgets[col][position]
      }
      saveSlideshow(payload)
    },
    saveTitle (slide, title) {
      const payload = {
        key: `slides.${slide}.title`,
        patch: title
      }
      saveSlideshow(payload)
    }
  },
  components: {
    SlideEditor
  }
}
</script>

<style lang="scss" scoped>
.reveal .slides section {
  padding: 0;
  text-align: left;
}
</style>
