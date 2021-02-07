<template lang="pug">
div
  canvas(:id="canvasId" :width="width" :height="height")
</template>

<script>
import { fabric } from 'fabric'

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
  mounted () {
    this.canvas = new fabric.Canvas(this.canvasId, { isDrawingMode: true })
    this.canvas.isDrawingMode = true
    this.canvas.freeDrawingBrush.color = 'darkblue'
    this.canvas.freeDrawingBrush.width = 2
    this.canvas.renderAll()
    window.addEventListener('resize', () => {
      this.height = window.innerHeight
      this.width = window.innerWidth
    })
  }
}
</script>
