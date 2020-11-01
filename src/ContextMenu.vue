<template lang="pug">
div.dropdown-content
  li.dropdown-item(@click="$set(state, 'showGenerator', true)" v-if="component === 'widget'")
    b-icon(pack="fas" icon="cogs")
    span Generator
  li.dropdown-item(v-if="component === 'list'")
    b-checkbox(v-model="payload.numbered") Numbered list
  li.dropdown-item(v-if="component === 'environment'" custom)
    b-checkbox(v-model="payload.collapsed") Collapse when loading
    b-select(placeholder="Style" v-model="payload.style")
      option(value="primary") Dark blue
      option(value="link") Blue
      option(value="info") Light blue
      option(value="success") Green
      option(value="warning") Yellow
      option(value="danger") Red
  hr.dropdown-divider(v-if="component === 'list' || component === 'environment'")
  li.dropdown-item(@click="addChild('widget', 'Pandoc')")
    b-icon(pack="fas" icon="font")
    span Add text
  li.dropdown-item
    widget-select(@select:widget="addChild('widget', $event)" size="is-small")
  hr.dropdown-divider
  li.dropdown-item(v-if="component !== 'widget'")
    b-field(label="Columns")
      b-slider(:min="1" :max="4" :value="payload.cols || 1" @change="$set(payload, 'cols', $event)")
  li.dropdown-item(@click="addChild('list')")
    b-icon(pack="fas" icon="list")
    span Add a list
  li.dropdown-item(@click="addChild('environment')")
    b-icon(pack="fas" icon="cube")
    span Add a block
  hr.dropdown-divider
  li.dropdown-item(@click="$emit('delete')" v-if="component !== 'slide'")
    b-icon(pack="fas" icon="trash")
    span Delete
  hr.dropdown-divider
  li.dropdown-item(@click="$emit('insert-slide')")
    span Insert slide before
</template>

<script>
import WidgetSelect from './WidgetSelect'

export default {
  props: {
    component: String,
    payload: Object,
    state: Object
  },
  components: {
    WidgetSelect
  },
  methods: {
    addChild (component, type = undefined) {
      this.$emit('add-child', { component, type })
    }
  }
}
</script>
