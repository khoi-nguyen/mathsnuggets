<template lang="pug">
.slide
  slide-title(v-model="payload.title" :config="config")
  .slide-contents
    whiteboard.whiteboard(
      :name="position + config.currentCanvas"
      v-if="config.whiteboard && showWhiteboard"
      v-model="payload.canvasses[config.currentCanvas]"
      :read-only="!loggedIn"
      :active="true"
      :key="position + config.currentCanvas"
    )
    div(:class="{split: payload.split && config.whiteboard}")
      slot
  tool-bar(:payload="payload")
</template>

<script>
import _ from 'lodash'
import { mapState } from 'vuex'

import SlideTitle from './SlideTitle'
import ToolBar from './ToolBar'
import Whiteboard from './Whiteboard'

export default {
  components: {
    SlideTitle,
    ToolBar,
    Whiteboard
  },
  props: {
    payload: { type: Object, default: () => {} },
    position: String
  },
  computed: {
    active () {
      return this.config.currentSlide === parseInt(this.position.split('.')[1])
    },
    ...mapState('auth', ['loggedIn']),
    ...mapState(['config'])
  },
  watch: {
    'config.currentSlide': {
      immediate: true,
      handler (currentSlide, previousSlide) {
        const position = parseInt(this.position.split('.')[1])
        if (!this.showWhiteboard) {
          if (currentSlide === position) {
            this.debounced()
          } else if (previousSlide === position && this.debounced) {
            this.debounced.cancel()
          }
        }
      }
    }
  },
  data () {
    return {
      showWhiteboard: false,
      debounced: _.debounce(() => { this.showWhiteboard = true }, 2000)
    }
  }
}
</script>

<style scoped>
.whiteboard {
  position: absolute;
  top: 0;
  z-index: 1;
}
.split {
  width: 960px;
}
</style>

<style>
.slide-contents a,
.slide-contents button,
.slide-contents textarea.field,
.slide-contents select.field,
.reveal .slide-contents iframe,
.slide-contents h3.message-header,
.slide-contents .computed-field .base {
  z-index: 2;
}
.slide-contents select.field,
.slide-contents textarea.field,
.slide-contents iframe {
  position: relative;
}
</style>
