<template lang="pug">
component(
  :is="component"
  :payload="payload || {}"
  :type="type"
  @add:child="addChild"
  @save="$emit('save', $event)"
  @update:payload="updateProp('payload', $event)"
)
  draggable.drop(
    :emptyInsertThreshold="100"
    :list="children || []"
    @change="dragAndDrop"
    ghost-class="has-background-white-ter"
    group="widgets"
    handle=".handle"
  )
    component(:is="component === 'list' ? 'li' : 'div'" v-for="(child, index) in children").columns
      .column.is-narrow.has-text-grey-lighter
        b-dropdown
          span(slot="trigger")
            b-icon.handle(pack="fas" icon="ellipsis-v")
          b-dropdown-item(@click="deleteChild(index)") Delete
      .column
        node(
          :children="child.children || []"
          :component="child.component"
          :payload="child.payload || {}"
          :position="`${position}.children.${index}`"
          :type="child.type"
          @save="$emit('save', $event)"
          @update:children="updateChildren(index, 'children', $event)"
          @update:payload="updateChildren(index, 'payload', $event)"
        )
</template>

<script>
import draggable from 'vuedraggable'
import { cloneDeep, forEach, isEmpty } from 'lodash'

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
  methods: {
    addChild (event) {
      this.$emit('update:children', this.children.concat([event]))
      this.$emit('save', { action: 'update', [`${this.position}.children.${this.children.length}`]: event })
    },
    deleteChild (index) {
      this.children.splice(index, 1)
      this.$emit('save', { action: 'delete', [`${this.position}.children.${index}`]: '' })
    },
    dragAndDrop (event) {
      const indices = event[Object.keys(event)[0]]
      if ('removed' in event) {
        this.$emit('save', { action: 'delete', [`${this.position}.children.${indices.oldIndex}`]: '' })
      } else if ('added' in event) {
        const pos = `${this.position}.children.${indices.newIndex}`
        this.$emit('save', { action: 'insert', [pos]: this.clean(this.children[indices.newIndex]) })
      } else if ('moved' in event) {
        this.$emit('save', { action: 'swap', [`${this.position}.children.${indices.oldIndex}`]: `${this.position}.children.${indices.newIndex}` })
      }
    },
    clean (node) {
      const obj = {}
      forEach(['children', 'component', 'payload', 'type'], function (key) {
        if (!isEmpty(node[key])) {
          obj[key] = node[key]
        }
      })
      return obj
    },
    updateChildren (index, key, value) {
      let children = cloneDeep(this.children)
      if (index < children.length) {
        children[index][key] = value
      } else {
        children = children.concat({ [key]: value })
      }
      this.$emit('update:children', children)
    },
    updateProp (prop, value) {
      this.$emit(`update:${prop}`, value)
      this.$emit('save', { action: 'update', [`${this.position}.${prop}`]: value })
    }
  },
  components: {
    Environment,
    List,
    Slide,
    Widget,
    draggable
  }
}
</script>

<style>
.drop {
  min-height: 20px;
}
.message {
  break-inside: avoid-column;
}
</style>
