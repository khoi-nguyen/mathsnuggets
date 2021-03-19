<template lang="pug">
div
  section.hero.is-primary
    div.hero-body.container.has-text-centered
      div(v-if="!authState.loggedIn")
        i.fa-3x.fas.fa-sign-in-alt
        h1.title Login
        h2.subtitle Please login to proceed.
      div(v-show="authState.loggedIn")
        i.fa-3x.fas.fa-clipboard-check
        h1.title Logged In
        h2.subtitle You have successfully logged in!
  .box.container(v-if="!authState.loggedIn")
    b-tabs(v-model="tab" type="is-boxed")
      b-tab-item(label="Login" value="login")
      b-tab-item(label="Register" value="register")
    b-field(label="Email")
      b-input(icon="envelope" icon-pack="fas" type="email" v-model="email")
    b-field(label="Password")
      b-input(icon="lock" icon-pack="fas" type="password" ref="fields" v-model="password")
    b-field(label="Registration password" v-if="tab === 'register'")
      b-input(icon="lock" icon-pack="fas" type="password" ref="fields" v-model="registrationPassword")
    b-field(v-if="tab === 'login'")
      b-checkbox(v-model="remember") Remember me
    b-button(type="is-primary" expanded @click="login" v-if="tab === 'login'") Login
    b-button(type="is-success" expanded @click="login(true)" v-else) Register
    b-message(v-if="authState.error != ''" type="is-danger") {{ authState.error }}
</template>

<script>
import { auth } from './auth.js'

export default {
  title: 'Login',
  methods: {
    login (register = false) {
      if (register) {
        auth.register(this.email, this.password, this.registrationPassword)
      } else {
        auth.login(this.email, this.password, this.remember)
      }
    }
  },
  data () {
    return {
      authState: auth.state,
      email: '',
      password: '',
      registrationPassword: '',
      remember: true,
      tab: 'login'
    }
  }
}
</script>
