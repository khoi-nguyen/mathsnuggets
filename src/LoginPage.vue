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
    b-field(label="Email")
      b-input(icon="envelope" icon-pack="fas" type="email" v-model="email")
    b-field(label="Password")
      b-input(icon="lock" icon-pack="fas" type="password" ref="fields" v-model="password")
    b-field
      b-checkbox Remember me
    b-button(type="is-info" expanded @click="login") Login
    article.message.is-danger(v-if="authState.error != ''")
      div.message-body {{ authState.error }}
</template>

<script>
import NavBar from './NavBar'
import { auth } from './auth.js'

export default {
  components: { NavBar },
  title: 'Login',
  name: 'Login',
  methods: {
    login () {
      auth.login(this.email, this.password)
    }
  },
  data () {
    return {
      authState: auth.state,
      email: '',
      password: ''
    }
  }
}
</script>
