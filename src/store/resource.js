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
      commit('insertSlide', rootState.config.currentSlide)
      dispatch('saveSlideshow')
    },
    async deleteSlide ({ commit, dispatch, rootState }) {
      commit('deleteSlide', rootState.config.currentSlide)
      dispatch('saveSlideshow')
    },
    async forceSlideChange ({ rootState, getters }) {
      await api('change_slide', 'POST', {
        url: getters.url,
        slide: rootState.config.currentSlide
      })
    },
    async loadSlideshow ({ commit, state, getters }) {
      if (getters.url) {
        const data = await api(getters.url)
        if (data.length) {
          commit('loadSlideshow', data)
        }
      }
    },
    async save ({ state, commit, getters, rootState }, patch) {
      if (!rootState.auth.loggedIn) {
        return false
      }
      const lastSlide = state.children[state.children.length - 1]
      if (!_.isEqual(lastSlide, emptySlide())) {
        commit('addSlide')
      }
      commit('addToStack', patch)
      const sendSaveStack = _.debounce(async () => {
        if (state.saveStack) {
          await api(getters.url, 'POST', state.saveStack)
          commit('clearStack')
        }
      }, 600)
      sendSaveStack()
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
