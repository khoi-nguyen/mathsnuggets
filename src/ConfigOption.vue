<template lang="pug">
div.control
  div.tags.has-addons
    span.tag.is-dark.is-medium {{ name }}
    span.tag.is-medium
      slot
</template>

<script>
export default {
  props: {
    name: String
  }
}
</script>
