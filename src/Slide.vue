<template lang="pug">
.slide
  slide-title(v-model="payload.title" :config="config")
  .slide-contents
    whiteboard.whiteboard(:name="position" v-if="!config.edit" v-model="payload.canvas" :read-only="!config.authState.loggedIn")
    slot
</template>

<script>
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
    position: String
  }
}
</script>

<style scoped>
.whiteboard {
  position: absolute;
  top: 0;
  z-index: 200;
}
</style>

<style>
.slide-contents a,
.slide-contents button,
.slide-contents textarea.field,
.slide-contents select.field,
.reveal .slide-contents iframe,
.slide-contents h3.message-header,
.slide-contents .base {
  z-index: 300;
}
.slide-contents select.field,
.slide-contents textarea.field,
.slide-contents iframe {
  position: relative;
}
</style>
