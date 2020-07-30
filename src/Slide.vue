<template lang="pug">
.slide
  slide-title(v-model="payload.title")
  slot
</template>

<script>
import SlideTitle from './SlideTitle'

export default {
  components: {
    SlideTitle
  },
  props: {
    payload: { type: Object, default: () => {} }
  }
}
</script>
