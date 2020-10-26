<template lang="pug">
div(:class="{ slide: component === 'slide' }" @contextmenu.prevent.stop="$refs.menu.open")
  component(:is="component" @save="$emit('save', $event)" v-bind="attrs")
    draggable(:value="children" @input="updateChildren" v-bind="draggableOptions")
      component(:is="childComponent" v-for="(child, index) in children")
        node.mb-2(
          :config="config"
          :position="`${position}.children.${index}`"
          @add-child="insertChildAfter(index, $event)"
          @delete="deleteChild(index)"
          @insert-slide="$emit('insert-slide')"
          @save="$emit('save', $event)"
          v-bind="child"
          :class="{invisible: config.whiteboardMode}"
        )
  vue-context(ref="menu" :close-on-click="false" v-if="config.authState.loggedIn")
    context-menu(@add-child="addChild" @delete="$emit('delete')" @insert-slide="$emit('insert-slide')" v-bind="attrs")
</template>

<script>
import draggable from 'vuedraggable'
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
    config: { type: Object, default: () => {} },
    payload: { type: Object, default: () => {} },
    position: { type: String, default: '' },
    type: { type: String, default: '' }
  },
  data () {
    return {
      state: {}
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
    draggableOptions () {
      return {
        delay: 200,
        fallBackOnBody: true,
        ghostClass: 'has-background-white-ter',
        group: 'widgets',
        invertSwap: true,
        style: { columnCount: (this.payload || {}).cols || 1 }
      }
    },
    attrs () {
      return {
        children: this.children || [],
        component: this.component,
        config: this.config || {},
        payload: this.payload || {},
        position: this.position,
        state: this.state,
        type: this.type
      }
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
      this.$refs.menu.close()
    },
    insertChildAfter (position, child) {
      this.$emit('save', { action: 'insert', [`${this.position}.children.${position + 1}`]: child })
      this.children.splice(position + 1, 0, child)
    },
    deleteChild (index) {
      this.$emit('save', { action: 'delete', [`${this.position}.children.${index}`]: '' })
      this.children.splice(index, 1)
    },
    updateChildren (event) {
      this.$emit('save', {
        action: 'update',
        [`${this.position}.children`]: event
      })
      for (let i = 0; i < event.length; i++) {
        this.$set(this.children, i, event[i])
      }
      if (this.children.length > event.length) {
        this.children.splice(event.length, this.children.length - event.length)
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
  page-break-inside: avoid !important;
}
.slide {
  height: 100%;
}
.invisible {
  visibility: hidden;
}
</style>
