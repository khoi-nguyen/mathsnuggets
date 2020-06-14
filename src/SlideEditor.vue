<template lang="pug">
div.slide
  slide-title(
    :value="title"
    @update:value="$emit('update:title', $event)"
    @validate:title="$emit('validate:title', $event)"
  )
  .columns
    div.column(v-for="i in [0, 1]" v-if="i < colsCount")
      draggable(v-model="localComponents[i]")
        resource-component(
          v-for="(component, index) in localComponents[i]"
          :type.sync="component.type"
          :fields.sync="component.fields"
          @add-component="addComponent(component, i, index)"
          @delete="deleteWidget(i, index)"
          @validate:widget="$emit('validate:widget', {col: i, pos: index})"
        )
  .buttons
    b-tooltip(label="Back to resources list" position="is-right")
      b-button(tag="a" href="/resources")
        b-icon(pack="fas" icon="sign-out-alt")
    b-tooltip(
      v-if="colsCount != 2"
      label="Split in two columns"
      position="is-right"
    )
      b-button(@click="localComponents.push([{type: '', fields: []}])")
        b-icon(pack="fas" icon="columns")
    b-tooltip(
      v-if="authState.loggedIn"
      label="Automatic saving enabled"
      position="is-right"
    )
      b-button
        b-icon(pack="fas" icon="save")
</template>

<script>
import draggable from 'vuedraggable'
import ResourceComponent from './ResourceComponent'
import SlideTitle from './SlideTitle'
import { auth } from './auth.js'

export default {
  props: {
    title: String,
    components: Array
  },
  computed: {
    colsCount () {
      return (this.components || []).length
    }
  },
  data () {
    return {
      localComponents: this.components || [],
      authState: auth.state
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
.buttons {
  bottom: 35px;
  left: 10px;
  position: absolute;
}
.buttons span, .buttons a {
  cursor: pointer;
  color: inherit;
  margin-right: 0.2em;
}
.slide {
  height: 100%;
}
</style>
