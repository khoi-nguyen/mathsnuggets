<template lang="pug">
div.reveal
  div.slides
    section(
      v-for="slide in slideshow"
    )
      SlideEditor(
        :id="id"
        :title.sync="slide.title"
        :components.sync="slide.widgets"
      )
</template>

<script>
import Reveal from 'reveal.js'
import '@fortawesome/fontawesome-free/js/all.js'
import _ from 'lodash'

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
    Reveal.initialize({
      center: false,
      embedded: this.embedded,
      height: this.height ? this.height : '100%',
      margin: 0,
      transition: 'none',
      width: this.width ? this.width : '100%'
    })
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
