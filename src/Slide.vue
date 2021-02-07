<template lang="pug">
.slide
  slide-title(v-model="payload.title" :config="config")
  whiteboard.whiteboard(:name="position" v-if="!config.edit")
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
}
</style>
