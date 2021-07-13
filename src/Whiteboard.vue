<template lang="pug">
div
  canvas(:id="canvasId")
  .bar.are-medium.buttons
    b-field
      b-numberinput(icon-pack="fas" :min="0" :max="9" :value="config.currentCanvas" type="is-success" @input="changeCanvas")
    span &nbsp;
    div(v-if="!readOnly")
      b-button(@click="toggleDrawingMode" type="is-success is-inverted")
        b-icon(pack="fas" icon="pen")
      b-button(@click="deleteObjects" type="is-danger is-inverted" v-if="!canvas.isDrawingMode")
        b-icon(pack="fas" icon="eraser")
      b-button(@click="canvas.clear(); save()" type="is-danger is-inverted")
        b-icon(pack="fas" icon="chalkboard")
      b-button(@click="canvas.undo()" type="is-warning is-inverted")
        b-icon(pack="fas" icon="undo")
      b-button(@click="canvas.redo()" type="is-link is-inverted")
        b-icon(pack="fas" icon="redo")
      b-button(@click="save" type="is-success is-inverted")
        b-icon(pack="fas" icon="save")
      b-dropdown(v-model="color" :triggers="['hover']")
        b-button(slot="trigger" :type="colorButtonType")
          b-icon(pack="fas" icon="palette")
        b-dropdown-item(value="darkblue") Blue
        b-dropdown-item(value="darkred") Red
        b-dropdown-item(value="darkorange") Orange
        b-dropdown-item(value="darkgreen") Green
        b-dropdown-item(value="black") Black
</template>

<script>
import { mapState, mapMutations } from 'vuex'
import { fabric } from 'fabric'
import 'fabric-history'
import _ from 'lodash'

export default {
  props: {
    active: Boolean,
    name: String,
    readOnly: Boolean,
    value: Object
  },
  computed: {
    canvasId () {
      return this.name.split('.').join('_')
    },
    colorButtonType () {
      const style = {
        darkblue: 'is-info',
        darkred: 'is-danger',
        darkgreen: 'is-success',
        black: ''
      }
      return 'is-inverted ' + style[this.color]
    },
    ...mapState(['config'])
  },
  data () {
    return {
      color: 'darkblue',
      canvas: false
    }
  },
  methods: {
    changeCanvas (index) {
      this.save()
      this.changeCurrentCanvasIndex(index)
    },
    deleteObjects () {
      this.canvas.getActiveObjects().forEach((obj) => {
        this.canvas.remove(obj)
      })
      this.canvas.discardActiveObject().renderAll()
    },
    save () {
      if (!_.isEqual(this.value, this.canvas.toJSON())) {
        this.$emit('input', this.canvas.toJSON())
      }
    },
    toggleDrawingMode () {
      this.canvas.isDrawingMode = !this.canvas.isDrawingMode
      this.canvas.freeDrawingBrush.color = this.color
      this.canvas.freeDrawingBrush.width = 3
    },
    ...mapMutations('config', ['changeCurrentCanvasIndex'])
  },
  watch: {
    active (newValue, oldValue) {
      if (!newValue) {
        this.save()
      }
    },
    color (newColor) {
      this.canvas.freeDrawingBrush.color = newColor
    },
    value: {
      immediate: true,
      handler (json, oldValue) {
        if (json && (this.readOnly || !oldValue)) {
          this.$nextTick(() => {
            this.canvas.loadFromJSON(json)
          })
        }
      }
    }
  },
  mounted () {
    this.canvas = new fabric.Canvas(this.canvasId, { isDrawingMode: false })
    this.canvas.setDimensions({ width: 1920, height: 1080 })
    if (!this.readOnly) {
      this.toggleDrawingMode()
    }
  }
}
</script>

<style scoped>
.bar {
  position: absolute;
  left: 55%;
  top: 0;
}
</style>
