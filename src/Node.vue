<template lang="pug">
.node
  b-dropdown.float.has-text-grey-lighter(v-if="component !== 'slide'")
    span(slot="trigger")
      b-icon.handle(pack="fas" icon="ellipsis-v")
    b-dropdown-item(@click="$emit('delete')") Delete
  component(
    :is="component"
    @save="$emit('save', $event)"
    @update:payload="updatePayload($event)"
    v-bind="attrs"
  )
    draggable(
      :fallback-on-body="true"
      :invert-swap="true"
      :list="children"
      @change="dragAndDrop"
      ghost-class="has-background-white-ter"
      group="widgets"
      handle=".handle"
    )
      div(:style="`column-count: ${payload.cols || 1}`")
        component(:is="childComponent" v-for="(child, index) in children")
          node(
            :position="`${position}.children.${index}`"
            @delete="deleteChild(index)"
            @save="$emit('save', $event)"
            @update:payload="$set(child, 'payload', $event)"
            v-bind="child"
          )
      .buttons(slot="footer")
        b-field
          p.control
            b-button
              b-icon(pack="fas" icon="columns")
          b-numberinput(
            :value="payload.cols || 1"
            @input="updatePayload($event, 'cols')"
            controls-position="compact"
            icon-pack="fas")
        b-button(@click="addChild('list')")
          b-icon(pack="fas" icon="list")
        b-button(@click="addChild('environment')")
          b-icon(pack="fas" icon="cube")
        widget-select(@select:widget="addChild('widget', $event)")
</template>

<script>
import draggable from 'vuedraggable'
import { clone } from 'lodash'

import Environment from './Environment'
import List from './List'
import Slide from './Slide'
import Widget from './Widget'
import WidgetSelect from './WidgetSelect'

export default {
  name: 'node',
  props: {
    children: { type: Array, default: () => [] },
    component: { type: String, default: 'slide' },
    payload: { type: Object, default: () => {} },
    position: { type: String, default: '' },
    type: { type: String, default: '' }
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
    addChild (component, type) {
      const child = {
        children: component !== 'widget' ? [] : undefined,
        component: component,
        payload: {},
        type: component === 'widget' ? type : undefined
      }
      this.$emit('save', {
        action: 'update',
        [`${this.position}.children.${this.children.length}`]: child
      })
      this.children.push(child)
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
    updatePayload (value, key = false) {
      let payload = value
      if (key !== false) {
        payload = clone(this.payload)
        payload[key] = value
      }
      this.$emit('update:payload', payload)
      this.$emit('save', { action: 'update', [`${this.position}.payload`]: payload })
    }
  },
  components: {
    Environment,
    List,
    Slide,
    Widget,
    WidgetSelect,
    draggable
  }
}
</script>

<style scoped>
.node > .float {
  display: none;
}
.node:hover > .float {
  display: block;
  float: left;
}
.message {
  break-inside: avoid-column;
}
</style>
