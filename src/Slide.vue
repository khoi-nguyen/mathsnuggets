<template lang="pug">
.slide
  slide-title(v-model="payload.title" :config="config")
  .slide-contents
    whiteboard.whiteboard(:name="position" v-if="config.authState.loggedIn && !config.edit")
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
.slide-contents {
  position: relative;
}
.whiteboard {
  position: absolute;
  top: 0;
  z-index: 200;
}
</style>

<style>
.slide-contents button, .slide-contents iframe, .slide-contents .base {
  z-index: 300;
}
</style>
