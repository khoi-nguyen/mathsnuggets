<template lang="pug">
div
  canvas(:id="canvasId")
  .bar.buttons.are-medium
    b-button(@click="toggleDrawingMode" type="is-success is-inverted")
      b-icon(pack="fas" icon="pen")
    b-button(@click="canvas.clear()" type="is-danger is-inverted")
      b-icon(pack="fas" icon="eraser")
    b-button(@click="canvas.undo()" type="is-warning is-inverted")
      b-icon(pack="fas" icon="undo")
    b-button(@click="canvas.redo()" type="is-link is-inverted")
      b-icon(pack="fas" icon="redo")
    b-dropdown(v-model="color" :triggers="['hover']")
      b-button(slot="trigger" :type="colorButtonType")
        b-icon(pack="fas" icon="palette")
      b-dropdown-item(value="darkblue") Blue
      b-dropdown-item(value="darkred") Red
      b-dropdown-item(value="darkgreen") Green
      b-dropdown-item(value="black") Black
</template>

<script>
import { fabric } from 'fabric'
import 'fabric-history'

export default {
  title: 'Whiteboard',
  props: {
    name: String
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
    }
  },
  data () {
    return {
      color: 'darkblue',
      canvas: false
    }
  },
  methods: {
    getWindowDimensions () {
      this.canvas.setWidth(window.innerWidth)
      this.canvas.setHeight(window.innerHeight)
    },
    toggleDrawingMode () {
      this.canvas.isDrawingMode = !this.canvas.isDrawingMode
      this.canvas.freeDrawingBrush.color = this.color
      this.canvas.freeDrawingBrush.width = 3
    }
  },
  watch: {
    color (newColor) {
      this.canvas.freeDrawingBrush.color = newColor
    }
  },
  mounted () {
    this.canvas = new fabric.Canvas(this.canvasId, { isDrawingMode: false })
    this.toggleDrawingMode()
    this.canvas.renderAll()
    this.$nextTick(function () {
      window.addEventListener('resize', this.getWindowDimensions)
      this.getWindowDimensions()
      this.canvas.historyInit()
    })
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.getWindowDimensions)
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
