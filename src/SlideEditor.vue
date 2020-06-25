<template lang="pug">
.columns
  div.column(v-for="i in [0, 1]" v-if="i < components.length")
    draggable(v-model="localComponents[i]")
      resource-component(
        v-for="(component, index) in localComponents[i]"
        :type.sync="component.type"
        :fields.sync="component.fields"
        @add-component="addComponent(component, i, index)"
        @delete="deleteWidget(i, index)"
        @validate:widget="$emit('validate:widget', {col: i, pos: index})"
      )
</template>

<script>
import draggable from 'vuedraggable'
import ResourceComponent from './ResourceComponent'

export default {
  props: {
    components: { type: Array, default: () => [] }
  },
  data () {
    return {
      localComponents: this.components
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
  },
  watch: {
    components (value) {
      this.localComponents = value
    },
    localComponents (value) {
      this.$emit('update:components', value)
    }
  },
  components: {
    draggable,
    ResourceComponent
  }
}
</script>
