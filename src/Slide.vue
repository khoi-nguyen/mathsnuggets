<template lang="pug">
div
  slide-title(:title="payload.title" @update:title="updatePayload('title', $event)")
  div(:style="`column-count: ${payload.cols}`")
    slot
  .buttons.toolbar
    b-field
      p.control
        b-button
          b-icon(pack="fas" icon="columns")
      b-numberinput.number-input(:value="payload.cols || 1" @input="updatePayload('cols', $event)" controls-position="compact" icon-pack="fas" max="3")
    b-button(@click="addChild('list')")
      b-icon(pack="fas" icon="list")
    b-button(@click="addChild('environment')")
      b-icon(pack="fas" icon="cube")
    widget-select(@select:widget="addChild('widget', $event)")
</template>

<script>
import { clone } from 'lodash'

import SlideTitle from './SlideTitle'
import WidgetSelect from './WidgetSelect'

export default {
  components: {
    SlideTitle,
    WidgetSelect
  },
  props: {
    payload: { type: Object, default: () => {} }
  },
  methods: {
    addChild (component, type = '') {
      this.$emit('add:child', {
        children: component !== 'widget' ? [] : undefined,
        component: component,
        payload: {},
        type: component === 'widget' ? type : undefined
      })
    },
    updatePayload (fieldName, value) {
      const payload = clone(this.payload)
      payload[fieldName] = value
      this.$emit('update:payload', payload)
    }
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
