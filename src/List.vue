<template lang="pug">
.content.is-size-3
  component(:is="payload.numbered ? 'ol' : 'ul'")
    li.placeholder(v-if="!children.length") Add an item to this list
    slot
</template>

<script>
export default {
  props: {
    children: [],
    payload: { type: Object, default: () => {} }
  }
}
</script>

<style scoped>
.placeholder {
  color: #aa7582;
}
</style>
