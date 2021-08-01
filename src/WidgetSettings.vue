<template lang="pug">
.field.is-grouped.is-grouped-right.is-grouped-multiline.widget-settings(v-if="config.edit")
  slot
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: mapState(['config'])
}
</script>

<style scoped>
.widget-settings {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 99;
}
</style>
