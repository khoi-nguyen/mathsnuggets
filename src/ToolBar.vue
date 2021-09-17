<template lang="pug">
div
  .tray.buttons.are-medium
    b-button(v-for="button in buttons" v-bind="button" v-if="!button.hide" @click="button.click")
      b-icon(:pack="button.pack || 'fas'" :icon="button.icon")
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
    form-field(:value="auth.nickname" type="Field" @input="changeNickname" label="Enter your name here")
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
</template>

<script>
import { mapActions, mapMutations, mapState } from 'vuex'

import FormField from './FormField'
import Node from './Node'
import Widget from './Widget'
import WidgetSelect from './WidgetSelect'

export default {
  props: {
    payload: Object
  },
  data () {
    return {
      geometry: false,
      graphing: false,
      solverModal: false,
      widgetPayload: {},
      widget: ''
    }
  },
  computed: {
    buttons () {
      return [
        {
          click: this.saveSlideshow,
          icon: 'save',
          inverted: true,
          type: 'is-primary',
          hide: !this.auth.loggedIn
        },
        {
          click: this.toggleEdit,
          icon: 'edit',
          inverted: !this.config.edit,
          type: 'is-danger',
          hide: !this.auth.loggedIn
        },
        {
          click: () => this.$set(this.payload, 'split', !this.payload.split),
          icon: 'columns',
          inverted: !this.payload.split,
          type: 'is-link'
        },
        {
          click: this.toggleWhiteboard,
          icon: 'chalkboard',
          inverted: !this.config.whiteboard,
          type: 'is-success'
        },
        {
          click: this.loadSlideshow,
          icon: 'sync',
          inverted: true,
          type: 'is-warning'
        },
        {
          click: this.forceSlideChange,
          icon: 'slideshare',
          inverted: true,
          pack: 'fab',
          type: 'is-success',
          hide: !this.auth.loggedIn
        },
        {
          click: () => { this.solverModal = true },
          icon: 'python',
          inverted: true,
          pack: 'fab',
          type: 'is-link'
        }
      ]
    },
    ...mapState(['auth', 'config'])
  },
  methods: {
    changeWidget (widget) {
      this.widgetPayload = {}
      this.widget = widget
    },
    ...mapActions('auth', ['changeNickname']),
    ...mapMutations('config', ['toggleEdit', 'toggleWhiteboard']),
    ...mapActions('resource', ['loadSlideshow', 'saveSlideshow', 'forceSlideChange'])
  },
  components: {
    FormField,
    Node,
    Widget,
    WidgetSelect
  }
}
</script>

<style scoped>
.tray {
  position: fixed;
  opacity: 1;
  z-index: 2;
  bottom: 25px;
  left: 20px;
}
</style>
