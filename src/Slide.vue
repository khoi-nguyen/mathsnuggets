<template lang="pug">
div
  slide-title(:title="payload.title" @update:title="updatePayload('title', $event)")
  slot
</template>

<script>
import { clone } from 'lodash'

import SlideTitle from './SlideTitle'

export default {
  components: {
    SlideTitle
  },
  props: {
    payload: { type: Object, default: () => {} }
  },
  methods: {
    updatePayload (fieldName, value) {
      const payload = clone(this.payload)
      payload[fieldName] = value
      this.$emit('update:payload', payload)
    }
  }
}
</script>
