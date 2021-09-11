<template lang="pug">
.clipboard
  draggable(v-model="clipboard" :group="'widgets-slide-' + config.currentSlide")
    node(v-bind="image" v-for="(image, i) in clipboard" :state="{}")
</template>

<script>
import draggable from 'vuedraggable'
import { mapState } from 'vuex'
import Node from './Node'

export default {
  created () {
    window.addEventListener('paste', this.onPaste.bind(this))
  },
  destroyed () {
    window.removeEventListener('paste', this.onPaste.bind(this))
  },
  data () {
    return {
      clipboard: []
    }
  },
  computed: {
    ...mapState(['config'])
  },
  methods: {
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
    }
  },
  components: {
    draggable,
    Node
  }
}
</script>
