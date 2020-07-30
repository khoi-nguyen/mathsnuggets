<template lang="pug">
div(:class="{ slide: component === 'slide' }")
  div(@contextmenu.prevent.stop="$refs.menu.open" :class="{ slide: component === 'slide' }")
    component(
      :is="component"
      @save="$emit('save', $event)"
      v-bind="attrs"
    )
      div(:style="`column-count: ${payload.cols || 1}`")
        draggable(
          :delay="200"
          :fallback-on-body="true"
          :invert-swap="true"
          :list="children"
          @change="dragAndDrop"
          ghost-class="has-background-white-ter"
          group="widgets"
        )
          component(:is="childComponent" v-for="(child, index) in children")
            node.mb-2(
              :position="`${position}.children.${index}`"
              @add-child="children.splice(index + 1, 0, $event)"
              @delete="deleteChild(index)"
              @save="$emit('save', $event)"
              v-bind="child"
            )
  vue-context(ref="menu" :close-on-click="false")
    context-menu(
      :component="component"
      @add-child="addChild"
      @delete="$emit('delete')"
      v-bind="attrs"
    )
</template>

<script>
import draggable from 'vuedraggable'
import { clone } from 'lodash'
import { VueContext } from 'vue-context'

import ContextMenu from './ContextMenu'
import Environment from './Environment'
import List from './List'
import Slide from './Slide'
import Widget from './Widget'

export default {
  name: 'node',
  props: {
    children: { type: Array, default: () => [] },
    component: { type: String, default: 'slide' },
    payload: { type: Object, default: () => {} },
    position: { type: String, default: '' },
    type: { type: String, default: '' }
  },
  data () {
    return {
      showToolbar: this.component === 'slide'
    }
  },
  watch: {
    payload: {
      handler () {
        this.$emit('save', { action: 'update', [`${this.position}.payload`]: this.payload })
      },
      deep: true
    }
  },
  computed: {
    attrs () {
      const attrs = clone(this.$props)
      if (!attrs.children) {
        attrs.children = []
      }
      if (!attrs.payload) {
        attrs.payload = {}
      }
      return attrs
    },
    childComponent () {
      return this.component === 'list' ? 'li' : 'div'
    }
  },
  methods: {
    addChild (event) {
      const child = {
        children: event.component !== 'widget' ? [] : undefined,
        component: event.component,
        payload: {},
        type: event.component === 'widget' ? event.type : undefined
      }
      this.$emit('save', {
        action: 'update',
        [`${this.position}.children.${this.children.length}`]: child
      })
      if (this.component !== 'widget') {
        this.children.push(child)
      } else {
        this.$emit('add-child', child)
      }
      this.refs.$menu.close()
    },
    deleteChild (index) {
      this.$emit('save', { action: 'delete', [`${this.position}.children.${index}`]: '' })
      this.children.splice(index, 1)
    },
    dragAndDrop (event) {
      const data = event[Object.keys(event)[0]]
      if ('removed' in event) {
        this.$emit('save', { action: 'delete', [`${this.position}.children.${data.oldIndex}`]: '' })
      } else if ('added' in event) {
        const pos = `${this.position}.children.${data.newIndex}`
        this.$emit('save', { action: 'insert', [pos]: data.element })
      } else if ('moved' in event) {
        this.$emit('save', { action: 'swap', [`${this.position}.children.${data.oldIndex}`]: `${this.position}.children.${data.newIndex}` })
      }
    },
    updatePayload (key = false, value = false) {
      if (key !== false) {
        this.$set(this.payload, key, value)
      }
    }
  },
  components: {
    ContextMenu,
    Environment,
    List,
    Slide,
    VueContext,
    Widget,
    draggable
  }
}
</script>

<style scoped>
.avoid-column {
  break-inside: avoid-column !important;
  page-break-inside: avoid;
}
.slide {
  height: 100%;
}
</style>
