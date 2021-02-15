<template lang="pug">
.container.avoid-column
  b-collapse.message.is-medium(:class="`is-${payload.style || 'primary'}`" :open="!payload.collapsed")
    h3.message-header(:contenteditable="config.edit" @blur="blur" @keydown.enter.prevent="blur" v-text="payload.title" slot="trigger")
    article
      .message-body
        slot
</template>

<script>
export default {
  props: { config: Object, payload: { type: Object, default: () => {} } },
  methods: {
    blur (event) {
      this.updateTitle(event.target.innerText)
    },
    updateTitle (value) {
      this.$set(this.payload, 'title', value)
    }
  }
}
</script>
