<template lang="pug">
.columns
  div.column(v-for="col in [0, 1]" v-if="col < components.length")
    draggable(v-model="localComponents[col]" group="widgets" @change="dragAndDrop(col, $event)")
      resource-component(
        v-for="(component, index) in localComponents[col]"
        :type.sync="component.type"
        :fields.sync="component.fields"
        @validate:widget="$emit('validate:widget', {key: `${position}.widgets.${col}.${index}`, value: $event})"
      )
</template>

<script>
import _ from 'lodash'
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
    dragAndDrop (col, event) {
      const indices = event[Object.keys(event)[0]]
      if ('removed' in event) {
        this.$emit('delete:widget', `${this.position}.widgets.${col}.${indices.oldIndex}`)
      } else if ('added' in event) {
        const element = _.cloneDeep(indices.element)
        const payload = {}
        _.forEach(element.fields, function (field) {
          if (field.value && !field.computed) {
            payload[field.name] = field.value
          }
        })
        element.fields = payload
        this.$emit('insert:widget', { key: `${this.position}.widgets.${col}.${indices.newIndex}`, value: element })
      } else if ('moved' in event) {
        this.$emit('swap:widget', { key: `${this.position}.widgets.${col}.${indices.oldIndex}`, value: indices.newIndex })
      }
    }
  }
}
</script>
