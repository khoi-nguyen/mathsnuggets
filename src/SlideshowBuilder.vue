<template lang="pug">
.eg-slideshow
  slide(
    :mouseNavigation="false"
    v-for="slideData in data"
  )
    SlideEditor(
      :title.sync="slideData.title"
      :components.sync="slideData.components"
    )
</template>

<script>
import { Slideshow } from 'eagle.js'
import 'animate.css'
import SlideEditor from './SlideEditor'

export default {
  data () {
    return {
      emptySlide: [
        { title: '', components: [{ type: '', fields: [] }] }
      ],
      data: [
        { title: 'Your first slide', components: [{ type: '', fields: [] }] },
        { title: 'Your second slide', components: [{ type: '', fields: [] }] },
        { title: '', components: [{ type: '', fields: [] }] },
        { title: '', components: [{ type: '', fields: [] }] },
        { title: '', components: [{ type: '', fields: [] }] },
        { title: '', components: [{ type: '', fields: [] }] },
        { title: '', components: [{ type: '', fields: [] }] },
        { title: '', components: [{ type: '', fields: [] }] },
        { title: '', components: [{ type: '', fields: [] }] },
        { title: '', components: [{ type: '', fields: [] }] }
      ]
    }
  },
  components: {
    SlideEditor
  },
  mixins: [Slideshow]
}
</script>
