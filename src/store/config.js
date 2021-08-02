const config = {
  namespaced: true,
  state: {
    currentSlide: 0,
    edit: false,
    whiteboard: true
  },
  mutations: {
    changeSlide (state, newSlide) {
      state.currentSlide = newSlide
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
