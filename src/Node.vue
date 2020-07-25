<template lang="pug">
.node
  b-dropdown.float.has-text-grey-lighter(v-if="component !== 'slide'" hoverable)
    span(slot="trigger")
      b-icon.handle(pack="fas" icon="ellipsis-v")
    b-dropdown-item(v-if="component === 'list'")
      b-checkbox(:value="payload.numbered" @input="updatePayload($event, 'numbered')") Numbered list
    b-dropdown-item(v-if="component === 'environment'" custom)
      b-select(placeholder="Style" :value="payload.style" @input="updatePayload($event, 'style')")
        option(value="primary") Dark blue
        option(value="link") Blue
        option(value="info") Light blue
        option(value="success") Green
        option(value="warning") Yellow
        option(value="danger") Red
    b-dropdown-item(@click="$emit('delete')") Delete
  component(
    :is="component"
    @save="$emit('save', $event)"
    @update:payload="updatePayload($event)"
    v-bind="attrs"
  )
    div(:style="`column-count: ${payload.cols || 1}`")
      draggable(
        :fallback-on-body="true"
        :invert-swap="true"
        :list="children"
        @change="dragAndDrop"
        ghost-class="has-background-white-ter"
        group="widgets"
        handle=".handle"
      )
        component(:is="childComponent" v-for="(child, index) in children")
          node(
            :position="`${position}.children.${index}`"
            @delete="deleteChild(index)"
            @save="$emit('save', $event)"
            @update:payload="$set(child, 'payload', $event)"
            v-bind="child"
          )
        .buttons.are-small(slot="footer")
          b-button(@click="showToolbar = !showToolbar" type="is-text")
            .toolbar-trigger
              b-icon(pack="fas" icon="angle-double-right")
          .buttons(v-if="showToolbar")
            p.control
              b-button
                b-icon(pack="fas" icon="columns")
            b-numberinput.numberinput(
              :editable="false"
              :value="payload.cols || 1"
              @input="updatePayload($event, 'cols')"
              controls-position="compact"
              icon-pack="fas"
              size="is-small"
            )
            b-button(@click="addChild('list')")
              b-icon(pack="fas" icon="list")
            b-button(@click="addChild('environment')")
              b-icon(pack="fas" icon="cube")
            widget-select(@select:widget="addChild('widget', $event)" size="is-small")
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
  data () {
    return {
      showToolbar: false
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
.numberinput {
  width: 90px;
}
.hidden {
  visibility: hidden;
}
.toolbar-trigger {
  color: #cccccc;
}
</style>
