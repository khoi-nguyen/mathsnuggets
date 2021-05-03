<template lang="pug">
.slide
  slide-title(v-model="payload.title" :config="config")
  .slide-contents
    whiteboard.whiteboard(:name="position" v-if="!config.form && vpos && !config.edit && showWhiteboard" v-model="payload.canvas" :read-only="!config.authState.loggedIn" :active="active")
    div(:class="{split: payload.split && vpos}")
      slot
</template>

<script>
import _ from 'lodash'

import SlideTitle from './SlideTitle'
import Whiteboard from './Whiteboard'

export default {
  components: {
    SlideTitle,
    Whiteboard
  },
  props: {
    config: { type: Object, default: () => {} },
    payload: { type: Object, default: () => {} },
    position: String,
    vpos: Number
  },
  computed: {
    active () {
      return this.config.currentSlide === parseInt(this.position.split('.')[1])
    }
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
