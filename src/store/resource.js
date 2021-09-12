import _ from 'lodash'
import api from '../ajax.js'

const emptySlide = function () {
  return { payload: { canvasses: [{}, {}] }, children: [[]] }
}

const resource = {
  namespaced: true,
  state: {
    children: [emptySlide(), emptySlide()],
    saveStack: []
  },
  getters: {
    url (state, getters, rootState) {
      const params = rootState.route.params
      return params.url ? `slideshows/${params.url}` : false
    }
  },
  mutations: {
    addSlide (state) {
      state.children.push(emptySlide())
    },
    addToStack (state, element) {
      state.saveStack.push(element)
    },
    clearStack (state) {
      state.saveStack = []
    },
    insertSlide (state, index) {
      state.children.splice(index, 0, emptySlide())
    },
    deleteSlide (state, index) {
      state.children.splice(index, 1)
    },
    loadSlideshow (state, slides) {
      state.children = slides
    }
  },
  actions: {
    async insertSlide ({ commit, dispatch, rootState }) {
      const index = rootState.config.currentSlide
      commit('insertSlide', index)
      dispatch('save', { action: 'insert', [`children.${index}`]: emptySlide() })
    },
    async deleteSlide ({ commit, dispatch, rootState }) {
      const index = rootState.config.currentSlide
      commit('deleteSlide', index)
      dispatch('save', { action: 'delete', [`children.${index}`]: '' })
    },
    async loadSlideshow ({ commit, state, getters }) {
      if (getters.url) {
        const data = await api(getters.url)
        if (data.length) {
          commit('loadSlideshow', data)
        }
      }
    },
    async save ({ state, commit, getters }, patch) {
      const lastSlide = state.children[state.children.length - 1]
      if (!_.isEqual(lastSlide, emptySlide())) {
        commit('addSlide')
      }
      commit('addToStack', patch)
      setTimeout(async () => {
        await api(getters.url, 'POST', state.saveStack)
        commit('clearStack')
      }, 200)
    },
    async saveSlideshow ({ state, dispatch }) {
      await dispatch('save', {
        action: 'update',
        children: state.children
      })
    }
  }
}

export default resource
