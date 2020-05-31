<template lang="pug">
div
  SlideTitle(:value="title" @update:value="$emit('update:title', $event)")
  .columns
    div.column(v-for="i in [0, 1]" v-if="i < colsCount")
      draggable(v-model="localComponents[i]")
        ResourceComponent(
          v-for="(component, index) in localComponents[i]"
          :type.sync="component.type"
          :fields.sync="component.fields"
          @add-component="addComponent(component, i, index)"
          @delete="localComponents[i].splice(index, 1)"
        )
  button.button.is-success.is-outlined(
    v-if="colsCount != 2"
    tabindex="-1"
    @click="localComponents.push([{type: '', fields: []}])"
  )
    span.icon
      i.fas.fa-plus-circle
    span Add column
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
  computed: {
    colsCount () {
      return (this.localComponents || []).length
    }
  },
  data () {
    return {
      localComponents: this.components || []
    }
  },
  methods: {
    addComponent (component, col, position) {
      this.localComponents[col].splice(position + 1, 0, JSON.parse(JSON.stringify(component)))
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
