<template lang="pug">
div(:class="{ slide: component === 'slide' }" @contextmenu="openMenu")
  component(:is="component" v-bind="attrs" :blacklist.sync="blacklist")
    .columns
      .column(v-for="col in columnIndices")
        draggable(:value="col < children.length ? children[col] : []" @input="updateChildren(col, $event)" v-bind="draggableOptions")
          component(:is="childComponent" v-for="(child, index) in children[col]")
            node.mb-2(
              :position="`${position}.children.${col}.${index}`"
              @add-child="insertChildAfter(col, index, $event)"
              @delete="deleteChild(col, index)"
              v-bind="child"
              v-if="child.component"
            )
  vue-context(ref="menu" :close-on-click="false")
    context-menu(@add-child="addChild" @delete="$emit('delete')" v-bind="attrs")
</template>

<script>
import _ from 'lodash'
import draggable from 'vuedraggable'
import { VueContext } from 'vue-context'
import { mapActions, mapState } from 'vuex'

import ContextMenu from './ContextMenu'
import Environment from './Environment'
import List from './List'
import Slide from './Slide'
import SpeechBubble from './SpeechBubble'
import Widget from './Widget'

export default {
  name: 'node',
  props: {
    children: { type: Array, default: () => [[]] },
    component: { type: String, default: '' },
    payload: { type: Object, default: () => {} },
    position: { type: String, default: '' },
    type: { type: String, default: '' }
  },
  data () {
    return {
      blacklist: [],
      state: {}
    }
  },
  watch: {
    payload: {
      handler () {
        const payload = _.cloneDeep(this.payload)
        for (var i = 0; i < this.blacklist.length; i++) {
          delete payload[this.blacklist[i]]
        }
        while (this.children.length < this.columnCount) {
          this.children.push([])
        }
        if (this.position) {
          this.save({ action: 'update', [`${this.position}.payload`]: payload })
        }
      },
      deep: true
    }
  },
  computed: {
    draggableOptions () {
      return {
        delay: 200,
        emptyInsertThreshold: 100,
        ghostClass: 'has-background-white-ter',
        group: 'widgets-slide-' + this.slide
      }
    },
    attrs () {
      return {
        children: this.children || [[]],
        component: this.component,
        payload: this.payload || {},
        position: this.position,
        state: this.state,
        type: this.type
      }
    },
    childComponent () {
      return this.component === 'list' ? 'li' : 'div'
    },
    columnCount () {
      return this.payload && this.payload.cols ? this.payload.cols : 1
    },
    columnIndices () {
      return _.range(this.columnCount)
    },
    slide () {
      return this.position ? this.position.split('.')[1] : this.config.currentSlide
    },
    ...mapState(['config'])
  },
  methods: {
    addChild (event) {
      const child = {
        children: event.component !== 'widget' ? [[]] : undefined,
        component: event.component,
        payload: event.payload || {},
        type: event.component === 'widget' ? event.type : undefined
      }
      const lastColIndex = this.columnCount - 1
      const colIndex = this.children[lastColIndex].length
      this.save({
        action: 'update',
        [`${this.position}.children.${lastColIndex}.${colIndex}`]: child
      })
      if (this.component !== 'widget') {
        this.children[lastColIndex].push(child)
      } else {
        this.$emit('add-child', child)
      }
      this.$refs.menu.close()
    },
    insertChildAfter (col, position, child) {
      this.save({ action: 'insert', [`${this.position}.children.${col}.${position + 1}`]: child })
      this.children[col].splice(position + 1, 0, child)
    },
    deleteChild (col, index) {
      this.save({ action: 'delete', [`${this.position}.children.${col}.${index}`]: '' })
      this.children[col].splice(index, 1)
    },
    openMenu (event) {
      if (this.config.edit) {
        this.$refs.menu.open(event)
        event.preventDefault()
        event.stopPropagation()
      }
    },
    updateChildren (col, event) {
      this.save({
        action: 'update',
        [`${this.position}.children.${col}`]: event
      })
      for (let i = 0; i < event.length; i++) {
        this.$set(this.children[col], i, event[i])
      }
      if (this.children[col].length > event.length) {
        this.children[col].splice(event.length, this.children[col].length - event.length)
      }
    },
    ...mapActions('resource', ['save'])
  },
  components: {
    ContextMenu,
    Environment,
    List,
    Slide,
    SpeechBubble,
    VueContext,
    Widget,
    draggable
  }
}
</script>

<style scoped>
.slide {
  height: 100%;
}
.invisible {
  visibility: hidden;
}
</style>
