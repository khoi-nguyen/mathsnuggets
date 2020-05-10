<template lang="pug">
div
  SlideTitle(:value="title" @update:value="$emit('update:title', $event)")
  draggable(
    v-model="localComponents"
  )
    ResourceComponent(
      v-for="(component, index) in localComponents"
      :type.sync="component.type"
      :fields.sync="component.fields"
      @add-component="addComponent(component, index)"
      @delete="localComponents.splice(index, 1)"
    )
</template>

<script>
import draggable from 'vuedraggable'
import ResourceComponent from './ResourceComponent'
import SlideTitle from './SlideTitle'

export default {
  props: {
    title: String,
    components: Array
  },
  data () {
    return {
      localComponents: this.components || []
    }
  },
  methods: {
    addComponent (component, position) {
      this.localComponents.splice(position + 1, 0, JSON.parse(JSON.stringify(component)))
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
    ResourceComponent,
    SlideTitle
  }
}
</script>
