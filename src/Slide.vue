<template lang="pug">
.slide
  slide-title(:title="payload.title" @input="updateTitle")
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
  },
  methods: {
    updateTitle (value) {
      this.$set(this.payload, 'title', value)
      this.$emit('update:payload')
    }
  }
}
</script>
