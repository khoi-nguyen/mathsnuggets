<template lang="pug">
.container.avoid-column
  article.message.is-medium(:class="`is-${payload.style || 'primary'}`")
    h3.message-header(contenteditable @blur="blur" @keydown.enter.prevent="blur") {{ payload.title }}
    .message-body
      slot
</template>

<script>
export default {
  props: { payload: { type: Object, default: () => {} } },
  methods: {
    blur (event) {
      this.updateTitle(event.target.innerText)
    },
    updateTitle (value) {
      this.$set(this.payload, 'title', value)
      this.$emit('update:payload')
    }
  }
}
</script>
