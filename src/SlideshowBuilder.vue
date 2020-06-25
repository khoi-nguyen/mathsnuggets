<template lang="pug">
div.reveal
  div.slides
    section(
      v-for="(slide, index) in slideshow"
    )
      SlideEditor(
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
import { api } from './ajax'

import SlideEditor from './SlideEditor'

export default {
  title: 'Slideshow builder',
  data () {
    const emptySlide = { title: '', widgets: [[{ type: '', fields: [] }]] }
    return {
      authState: auth.state,
      slideshow: [_.cloneDeep(emptySlide), _.cloneDeep(emptySlide)],
      emptySlide: emptySlide
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
    saveSlide (slide) {
      const payload = {}
      payload[`slides.${slide}`] = this.data[slide]
      if (this.apiUrl && this.authState.loggedIn) {
        api(this.apiUrl, 'POST', payload)
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
