import api from './ajax.js'

export const auth = {
  state: {
    error: '',
    loggedIn: false
  },
  async isLoggedIn () {
    const data = await api('auth/login')
    this.state.loggedIn = data.is_authenticated
  },
  async register (email, password, registationPassword) {
    const payload = {
      email: email,
      password: password,
      registration_password: registationPassword
    }
    const data = await api('auth/register', 'POST', payload)
    if (data.error) {
      this.state.error = data.message
    } else {
      this.login(email, password)
    }
  },
  async login (email, password, remember) {
    const payload = {
      email: email,
      password: password,
      remember: remember
    }
    const data = await api('auth/login', 'POST', payload)
    if (data.error) {
      this.state.error = data.message
    } else {
      this.state.loggedIn = true
      this.state.error = ''
    }
  },
  async logout () {
    await api('auth/logout')
    this.state.loggedIn = false
  }
}
