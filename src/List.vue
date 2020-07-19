<template lang="pug">
.content.is-size-3
  b-dropdown.float.has-text-grey-lighter(hoverable)
    span(slot="trigger")
      b-icon(pack="fas" icon="tools")
      span &nbsp;
    b-dropdown-item(custom)
      b-field
        p.control
          b-button(type="is-small")
            b-icon(pack="fas" icon="columns")
        b-numberinput(:value="payload.cols || 1" @input="updatePayload('cols', $event)" icon-pack="fas" max="3" controls-position="compact" size="is-small")
  component(:is="payload.numbered ? 'ol' : 'ul'" :style="`column-count: ${payload.cols || 1}`")
    slot
</template>

<script>
import { clone } from 'lodash'

export default {
  props: { payload: { type: Object, default: {} } },
  methods: {
    updatePayload (fieldName, value) {
      const payload = clone(this.payload)
      payload[fieldName] = value
      this.$emit('update:payload', payload)
    }
  }
}
</script>

<style scoped>
.float {
  float: left;
}
</style>
