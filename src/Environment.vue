<template lang="pug">
.container
  article.message.is-primary.is-medium
    h3.message-header(contenteditable @blur="blur" @keydown.enter.prevent="blur") {{ payload.title }}
    .message-body
      slot
</template>

<script>
import { clone } from 'lodash'

export default {
  props: { payload: { type: Object, default: () => {} } },
  methods: {
    blur (event) {
      this.updatePayload('title', event.target.innerText)
    },
    updatePayload (fieldName, value) {
      const payload = clone(this.payload)
      payload[fieldName] = value
      this.$emit('update:payload', payload)
    }
  }
}
</script>
