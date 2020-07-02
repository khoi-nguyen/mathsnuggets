<template lang="pug">
.container
  article.message.is-primary.is-medium
    h3.message-header(contenteditable @blur="blur" @keydown.enter.prevent="blur") {{ title }}
    .message-body
      slot
</template>

<script>
export default {
  props: {
    title: String
  },
  methods: {
    blur (event) {
      this.$emit('update:title', event.target.innerText)
    }
  }
}
</script>
