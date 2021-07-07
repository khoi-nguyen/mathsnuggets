<template lang="pug">
.field.is-grouped.is-grouped-right.is-grouped-multiline.widget-settings
  slot
</template>

<script>
export default {
}
</script>

<style scoped>
.widget-settings {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 1
}
</style>
