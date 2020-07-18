<template lang="pug">
div
  slide-title(:title="title" @update:title="$emit('update:title', $event)")
  div(:style="`column-count: ${cols}`")
    slot
  .buttons.toolbar
    b-field
      p.control
        b-button
          b-icon(pack="fas" icon="columns")
      b-numberinput.number-input(:value="cols" @input="$emit('update:cols', $event)" controls-position="compact" icon-pack="fas" max="3")
    b-button(@click="$emit('add:child', {component: 'list', children: []})")
      b-icon(pack="fas" icon="list")
    b-button(@click="$emit('add:child', {component: 'environment', title: 'Hello', children: []})")
      b-icon(pack="fas" icon="cube")
    widget-select(@select:widget="$emit('add:child', {component: 'widget', type: $event})")
</template>

<script>
import SlideTitle from './SlideTitle'
import WidgetSelect from './WidgetSelect'

export default {
  components: {
    SlideTitle,
    WidgetSelect
  },
  props: {
    cols: { type: Number, default: 1 },
    title: String
  }
}
</script>

<style scoped>
.toolbar {
  bottom: 35px;
  position: absolute;
}
.toolbar .number-input {
  width: 120px;
}
</style>
