<template lang="pug">
.container.avoid-column
  b-collapse.message.is-medium(:class="`is-${payload.style || 'primary'}`" :open="!payload.collapsed")
    h3.message-header(slot="trigger")
      form-field(:editable="config.edit" v-model="payload.title" type="Markdown")
    article
      .message-body
        slot
</template>

<script>
import FormField from './FormField'

export default {
  props: { config: Object, payload: { type: Object, default: () => {} } },
  methods: {
    blur (event) {
      this.updateTitle(event.target.innerText)
    },
    updateTitle (value) {
      this.$set(this.payload, 'title', value)
    }
  },
  components: {
    FormField
  }
}
</script>
