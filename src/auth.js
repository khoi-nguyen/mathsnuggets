import { isLoggedIn, login, logout } from './ajax.js'

export const auth = {
  state: {
    error: '',
    loggedIn: false
  },
  isLoggedIn () {
    isLoggedIn(function (data) {
      this.state.loggedIn = data.is_authenticated
    }.bind(this))
  },
  login (email, password) {
    const payload = {
      email: email,
      password: password
    }
    login(payload, function (data) {
      if (data.error) {
        this.state.error = data.message
      } else {
        this.state.loggedIn = true
        this.state.error = ''
      }
    }.bind(this))
  },
  logout () {
    logout(() => (this.state.loggedIn = false))
  }
}
