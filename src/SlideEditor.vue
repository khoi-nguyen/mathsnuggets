<template lang="pug">
.columns
  div.column(v-for="col in [0, 1]" v-if="col < components.length")
    draggable(v-model="localComponents[col]")
      resource-component(
        v-for="(component, index) in localComponents[col]"
        :type.sync="component.type"
        :fields.sync="component.fields"
        @add-component="addComponent(component, col, index)"
        @delete="deleteWidget(col, index)"
        @validate:widget="$emit('validate:widget', {key: `${position}.widgets.${col}.${index}`, value: $event})"
      )
</template>

<script>
import draggable from 'vuedraggable'
import ResourceComponent from './ResourceComponent'

export default {
  props: {
    components: { type: Array, default: () => [] },
    position: { type: String, default: '' }
  },
  components: {
    draggable,
    ResourceComponent
  },
  data () {
    return {
      localComponents: this.components
    }
  },
  watch: {
    components (value) {
      this.localComponents = value
    },
    localComponents (value) {
      this.$emit('update:components', value)
    }
  },
  methods: {
    addComponent (component, col, position) {
      this.localComponents[col].splice(position + 1, 0, JSON.parse(JSON.stringify(component)))
    },
    deleteWidget (col, pos) {
      this.localComponents[col].splice(pos, 1)
      this.$emit('delete:widget', { col: col, pos: pos })
    }
  }
}
</script>
