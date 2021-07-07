import api from '../ajax.js'

const auth = {
  namespaced: true,
  state: {
    error: '',
    loggedIn: false,
    nickname: ''
  },
  mutations: {
    login (state) {
      state.loggedIn = true
      state.error = ''
    },
    logout (state) {
      state.loggedIn = false
      state.error = ''
    },
    nickname (state, nick) {
      state.nickname = nick
    },
    error (state, error) {
      state.loggedIn = false
      state.error = error
    }
  },
  actions: {
    changeNickname ({ commit }, nickname) {
      commit('nickname', nickname)
      api('auth/nickname', 'POST', { nickname })
    },
    async checkAuthStatus ({ commit, state }) {
      const data = await api('auth/login')
      const identity = await api('auth/nickname')
      commit(data.is_authenticated ? 'login' : 'logout')
      commit('nickname', identity.nickname)
    },
    async login ({ commit }, payload) {
      const data = await api('auth/login', 'POST', payload)
      if (data.error) {
        commit('error', data.message)
      } else {
        commit('login')
      }
    },
    async logout ({ commit }) {
      await api('auth/logout')
      commit('logout')
    },
    async register ({ commit, dispatch }, payload) {
      const data = await api('auth/register', 'POST', payload)
      if (data.error) {
        commit('error', data.message)
      } else {
        dispatch('login', payload)
      }
    }
  },
  getters: {
    isLoggedIn (state) {
      return state.loggedIn
    },
    getState (state) {
      return state
    },
    nickname (state) {
      return state.nickname
    }
  }
}

export default auth
