<template lang="pug">
div.slide
  SlideTitle(
    :value="title"
    @update:value="$emit('update:title', $event)"
    @validate:title="$emit('validate:title', $event)"
  )
  .columns
    div.column(v-for="i in [0, 1]" v-if="i < colsCount")
      draggable(v-model="localComponents[i]")
        ResourceComponent(
          v-for="(component, index) in localComponents[i]"
          :type.sync="component.type"
          :fields.sync="component.fields"
          @add-component="addComponent(component, i, index)"
          @delete="deleteWidget(i, index)"
          @validate:widget="$emit('validate:widget', {col: i, pos: index})"
        )
  .add-col.is-size-2.has-text-grey(
    v-if="colsCount != 2"
    tabindex="-1"
    @click="localComponents.push([{type: '', fields: []}])"
  )
    i.fas.fa-columns
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
    ResourceComponent,
    SlideTitle
  }
}
</script>

<style scoped>
.add-col {
  bottom: 25px;
  cursor: pointer;
  left: 10px;
  position: absolute;
}
.slide {
  height: 100%;
}
</style>
