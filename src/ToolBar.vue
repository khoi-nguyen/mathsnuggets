<template lang="pug">
div
  .tray.buttons.are-medium
    b-button(@click="config.edit = !config.edit" v-if="config.authState.loggedIn" type="is-danger" :inverted="!config.edit")
      b-icon(pack="fas" icon="edit")
    b-button(type="is-link" @click="$set(slidePayload, 'split', !slidePayload.split)" :inverted="!slidePayload.split")
      b-icon(pack="fas" icon="columns")
    b-button(@click="config.whiteboardMode = !config.whiteboardMode" type="is-success" :inverted="!config.whiteboardMode")
      b-icon(pack="fas" icon="chalkboard")
    b-button(@click="$emit('refresh-slideshow')" type="is-warning" :inverted="true")
      b-icon(pack="fas" icon="sync")
    b-button(@click="solverModal = true" type="is-link" :inverted="true")
      b-icon(pack="fab" icon="python")
    b-dropdown(position="is-top-right")
      b-button(slot="trigger" :inverted="true" type="is-primary")
        b-icon(pack="fas" icon="tools")
      b-dropdown-item
        b-button(@click="graphing = true" type="is-link" :inverted="true")
          b-icon(pack="fas" icon="chart-line")
          span Grapher
      b-dropdown-item
        b-button(@click="geometry = true" type="is-info" :inverted="true")
          b-icon(pack="fas" icon="drafting-compass")
          span Geometry
    b-dropdown(position="is-top-right" :mobile-modal="false")
      b-button(slot="trigger" type="is-info" :inverted="true")
        b-icon(pack="fas" icon="calculator")
      iframe(src="https://www.desmos.com/testing/virginia/scientific" width="600" height="600")
    span &nbsp;&nbsp;
    form-field(:value="$store.getters['auth/nickname']" type="Field" @input="updateNickname" label="Enter your name here")
    b-modal(:active.sync="graphing" full-screen has-modal-card :destroy-on-hide="false")
      .modal-card
        header.modal-card-head Graphing calculator
        .modal-card-body
          iframe(src="https://www.geogebra.org/graphing" width="100%" height="100%")
    b-modal(:active.sync="geometry" full-screen has-modal-card :destroy-on-hide="false")
      .modal-card
        header.modal-card-head Geometry
        .modal-card-body
          iframe(src="https://www.geogebra.org/geometry" width="100%" height="100%")
    b-modal(:active.sync="solverModal" has-modal-card :destroy-on-hide="false")
      .modal-card
        header.modal-card-head
          p.modal-card-title Solver
          button.delete(type="button" @click="solverModal = false")
        .modal-card-body
          widget-select(@select:widget="changeWidget")
          widget(:type="widget" :generator="true" :config="{edit: true}" :state="{}" :payload="widgetPayload" if="widget")
  .clipboard
    draggable(v-model="clipboard" group="widgets")
      node(v-bind="image" v-for="(image, i) in clipboard" component="widget" :config="config")
</template>

<script>
import draggable from 'vuedraggable'

import FormField from './FormField'
import Node from './Node'
import Widget from './Widget'
import WidgetSelect from './WidgetSelect'

export default {
  props: {
    config: Object,
    slidePayload: Object
  },
  data () {
    return {
      clipboard: [],
      geometry: false,
      graphing: false,
      solverModal: false,
      widgetPayload: {},
      widget: ''
    }
  },
  computed: {
    apiUrl () {
      const params = this.$route.params
      return params.slug ? `slideshows/${params.teacher}/${params.year}/${params.slug}` : false
    }
  },
  created () {
    window.addEventListener('paste', this.onPaste.bind(this))
  },
  destroyed () {
    window.removeEventListener('paste', this.onPaste.bind(this))
  },
  methods: {
    changeWidget (widget) {
      this.widgetPayload = {}
      this.widget = widget
    },
    onPaste (event) {
      const items = (event.clipboardData || event.originalEvent.clipboardData).items

      for (const index in items) {
        const item = items[index]
        if (item.kind === 'file') {
          const blob = item.getAsFile()
          const reader = new FileReader()
          reader.onload = function (e) {
            this.clipboard.push({
              component: 'widget',
              type: 'Image',
              payload: {
                src: e.target.result
              }
            })
          }.bind(this)
          reader.readAsDataURL(blob)
        }
      }
    },
    updateNickname (nickname) {
      this.$store.dispatch('auth/changeNickname', nickname)
    }
  },
  components: {
    draggable,
    FormField,
    Node,
    Widget,
    WidgetSelect
  }
}
</script>

<style scoped>
.clipboard {
  position: absolute;
  opacity: 1;
  z-index: 10000;
  bottom: 0;
  right: 0;
}
.tray {
  position: fixed;
  opacity: 1;
  z-index: 2;
  bottom: 25px;
  left: 20px;
}
</style>
