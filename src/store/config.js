const config = {
  namespaced: true,
  state: {
    currentCanvas: 0,
    currentSlide: 0,
    edit: false,
    whiteboard: true
  },
  mutations: {
    changeCurrentCanvasIndex (state, index) {
      state.currentCanvas = index
    },
    changeSlide (state, newSlide) {
      state.currentSlide = newSlide
      state.currentCanvas = 0
    },
    toggleEdit (state) {
      state.edit = !state.edit
      if (state.edit) {
        state.whiteboard = false
      }
    },
    toggleWhiteboard (state) {
      state.whiteboard = !state.whiteboard
      if (state.whiteboard) {
        state.edit = false
      }
    }
  }
}

export default config
