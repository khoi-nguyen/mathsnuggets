<template lang="pug">
div
  canvas(:id="canvasId" :width="width" :height="height")
  .bar.buttons.are-medium
    b-button(@click="toggleDrawingMode" type="is-success is-inverted")
      b-icon(pack="fas" icon="pen")
    b-button(@click="canvas.clear()" type="is-danger is-inverted")
      b-icon(pack="fas" icon="eraser")
    b-button(@click="canvas.undo()" type="is-warning is-inverted")
      b-icon(pack="fas" icon="undo")
    b-button(@click="canvas.redo()" type="is-link is-inverted")
      b-icon(pack="fas" icon="redo")
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
    }
  },
  data () {
    return {
      canvas: false,
      height: window.innerHeight,
      width: window.innerWidth
    }
  },
  methods: {
    toggleDrawingMode () {
      this.canvas.isDrawingMode = !this.canvas.isDrawingMode
      this.canvas.freeDrawingBrush.color = 'darkblue'
      this.canvas.freeDrawingBrush.width = 3
    }
  },
  mounted () {
    this.canvas = new fabric.Canvas(this.canvasId, { isDrawingMode: false })
    this.canvas.historyInit()
    this.canvas.renderAll()
    window.addEventListener('resize', () => {
      this.height = window.innerHeight
      this.width = window.innerWidth
    })
  }
}
</script>

<style scoped>
.bar {
  position: absolute;
  text-align: center;
  top: 0;
  right: 0;
}
</style>
