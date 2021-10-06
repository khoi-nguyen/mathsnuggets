<template lang="pug">
div
  canvas(:id="canvasId")
  .bar.are-medium.buttons
    b-field
      b-numberinput(icon-pack="fas" :min="0" :max="9" :value="index" type="is-success" @input="changeCanvas")
    span &nbsp;
    div(v-if="!readOnly")
      b-button(@click="toggleDrawingMode" type="is-success is-inverted")
        b-icon(pack="fas" icon="pen")
      b-button(@click="deleteObjects" type="is-danger is-inverted" v-if="!canvas.isDrawingMode")
        b-icon(pack="fas" icon="eraser")
      b-button(@click="insertEmptyBoard" type="is-inverted")
        b-icon(pack="fas" icon="plus")
      b-button(@click="clearCanvas" type="is-danger is-inverted")
        b-icon(pack="fas" icon="trash")
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
        b-dropdown-item(value="rgba(241, 231, 64, 0.5)") Highlighter yellow
        b-dropdown-item(value="rgba(93, 226, 60, 0.5)") Highlighter green
</template>

<script>
import { mapState } from 'vuex'
import { fabric } from 'fabric'
import 'fabric-history'
import _ from 'lodash'

export default {
  props: {
    boards: Array,
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
    },
    currentBoard () {
      return this.boards[this.index]
    },
    readOnly () {
      return !this.auth.loggedIn
    },
    ...mapState(['auth', 'config'])
  },
  data () {
    return {
      color: 'darkblue',
      canvas: false,
      index: 0
    }
  },
  methods: {
    changeCanvas (index, save = true) {
      if (save) {
        this.save()
      }
      this.index = index
      if (this.index < this.boards.length) {
        this.canvas.loadFromJSON(this.boards[this.index])
      } else {
        this.canvas.clear()
      }
    },
    clearCanvas () {
      this.boards.splice(this.index, 1)
      if (this.index) {
        this.changeCanvas(this.index - 1, false)
      } else {
        this.changeCanvas(0, false)
      }
    },
    deleteObjects () {
      this.canvas.getActiveObjects().forEach((obj) => {
        this.canvas.remove(obj)
      })
      this.canvas.discardActiveObject().renderAll()
    },
    insertEmptyBoard () {
      this.boards.splice(this.index, 0, {})
      this.canvas.clear()
    },
    save () {
      this.$set(this.boards, this.index, this.canvas.toJSON())
    },
    toggleDrawingMode () {
      this.canvas.isDrawingMode = !this.canvas.isDrawingMode
      this.canvas.freeDrawingBrush.color = this.color
      this.canvas.freeDrawingBrush.width = newColor.startsWith('rgba') ? 12 : 3
    }
  },
  watch: {
    color (newColor) {
      this.canvas.freeDrawingBrush.color = newColor
      this.canvas.freeDrawingBrush.width = newColor.startsWith('rgba') ? 12 : 3
    },
    'config.currentSlide' (newValue, oldValue) {
      if (oldValue === parseInt(this.name.split('.')[1])) {
        this.save()
      }
    },
    currentBoard: {
      handler (newValue) {
        if (!_.isEqual(newValue[this.index], this.canvas.toJSON())) {
          this.changeCanvas(this.index, false)
        }
      },
      deep: true
    }
  },
  mounted () {
    this.canvas = new fabric.Canvas(this.canvasId, { isDrawingMode: false })
    this.canvas.setDimensions({ width: 1920, height: 1080 })
    if (!this.readOnly) {
      this.toggleDrawingMode()
    }
    this.changeCanvas(0, false)
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
