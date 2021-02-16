<template lang="pug">
div
  canvas(:id="canvasId")
  .bar.buttons.are-medium(v-if="!readOnly")
    b-button(@click="toggleDrawingMode" type="is-success is-inverted")
      b-icon(pack="fas" icon="pen")
    b-button(@click="deleteObjects" type="is-danger is-inverted" v-if="!canvas.isDrawingMode")
      b-icon(pack="fas" icon="eraser")
    b-button(@click="canvas.clear()" type="is-danger is-inverted")
      b-icon(pack="fas" icon="chalkboard")
    b-button(@click="save" type="is-info is-inverted")
      b-icon(pack="fas" icon="save")
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

import api from './ajax'

export default {
  props: {
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
    }
  },
  sockets: {
    writingReceived (data) {
      if (data.url === this.$route.path && data.name === this.name) {
        this.$emit('input', data.value)
      }
    }
  },
  data () {
    return {
      color: 'darkblue',
      canvas: false
    }
  },
  methods: {
    deleteObjects () {
      this.canvas.getActiveObjects().forEach((obj) => {
        this.canvas.remove(obj)
      })
      this.canvas.discardActiveObject().renderAll()
    },
    getWindowDimensions () {
      this.canvas.setWidth(window.innerWidth)
      this.canvas.setHeight(window.innerHeight)
    },
    save () {
      this.$emit('input', this.canvas.toJSON())
      api('whiteboard', 'POST', {
        name: this.name,
        url: this.$route.path,
        value: this.canvas.toJSON()
      })
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
    },
    value: {
      immediate: true,
      handler (json) {
        if (json) {
          this.$nextTick(() => {
            this.canvas.loadFromJSON(json, () => {
              this.canvas.renderAll()
            })
          })
        }
      }
    }
  },
  mounted () {
    this.canvas = new fabric.Canvas(this.canvasId, { isDrawingMode: false })
    if (!this.readOnly) {
      this.toggleDrawingMode()
    }
    this.canvas.renderAll()
    this.$nextTick(function () {
      window.addEventListener('resize', this.getWindowDimensions)
      this.getWindowDimensions()
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
