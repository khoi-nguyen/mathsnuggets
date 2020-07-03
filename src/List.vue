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
        b-numberinput(:value="cols" @input="$emit('update:cols', $event)" icon-pack="fas" max="3" controls-position="compact" size="is-small")
  component(:is="numbered ? 'ol' : 'ul'" :style="`column-count: ${cols}`")
    slot
</template>

<script>
export default {
  props: {
    cols: { type: Number, default: 1 },
    numbered: { type: Boolean, default: true }
  }
}
</script>

<style scoped>
.float {
  float: left;
}
</style>
