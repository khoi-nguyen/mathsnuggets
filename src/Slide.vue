<template lang="pug">
.slide
  slide-title(v-model="payload.title" :editable="editable")
  slot
</template>

<script>
import SlideTitle from './SlideTitle'

export default {
  components: {
    SlideTitle
  },
  props: {
    editable: Boolean,
    payload: { type: Object, default: () => {} }
  }
}
</script>
