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
        @validate:title="saveSlide(index)"
        @validate:widget="saveSlide(index)"
        @delete:widget="saveSlide(index)"
      )
</template>

<script>
import { auth } from './auth.js'
import Reveal from 'reveal.js'
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
      authState: auth.state,
      id: {},
      slideshow: [_.cloneDeep(emptySlide), _.cloneDeep(emptySlide)],
      emptySlide: emptySlide
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
  mounted () {
    Reveal.initialize({
      center: false,
      embedded: this.embedded,
      height: this.height ? this.height : '100%',
      margin: 0,
      slideNumber: 'c/t',
      transition: 'none',
      width: this.width ? this.width : '100%'
    })
    if (this.$route.params.id) {
      getSlideshow(this.$route.params.id, function (data) {
        this.slideshow = data
        this.$nextTick(() => (Reveal.sync()))
      }.bind(this))
    }
  },
  methods: {
    saveSlide (slide, col, position) {
      const payload = {
        key: `slides.${slide}`,
        patch: this.data[slide]
      }
      if (this.$route.params.id && this.authState.loggedIn) {
        saveSlideshow(this.$route.params.id, payload)
      }
    }
  },
  components: {
    SlideEditor
  }
}
</script>

<style lang="scss" scoped>
.reveal .slides section {
  height: 100%;
  padding: 0;
  text-align: left;
}
</style>
