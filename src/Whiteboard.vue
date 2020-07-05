<template lang="pug">
div
  canvas#test(width="600" height="400")
</template>

<script>
import { fabric } from 'fabric'

export default {
  data () {
    return {
      canvas: false
    }
  },
  mounted () {
    this.canvas = new fabric.Canvas('test')
    this.canvas.isDrawingMode = true
    this.canvas.freeDrawingBrush.width = 3
  }
}
</script>

<style scoped>
canvas {
  border: 1px solid black;
}
</style>
