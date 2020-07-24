<template lang="pug">
.content.is-size-3
  component(:is="payload.numbered ? 'ol' : 'ul'")
    slot
</template>

<script>
export default {
  props: { payload: { type: Object, default: () => {} } }
}
</script>
