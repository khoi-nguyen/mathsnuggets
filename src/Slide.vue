<template lang="pug">
.slide
  slide-title(v-model="payload.title" :config="config")
  slot
</template>

<script>
import SlideTitle from './SlideTitle'

export default {
  components: {
    SlideTitle
  },
  props: {
    config: { type: Object, default: () => {} },
    payload: { type: Object, default: () => {} }
  }
}
</script>
