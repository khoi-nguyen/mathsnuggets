<template lang="pug">
div
  section.hero.is-primary
    div.hero-body.container.has-text-centered
      div(v-if="!loggedIn")
        i.fa-3x.fas.fa-sign-in-alt
        h1.title Login
        h2.subtitle Please login to proceed.
      div(v-show="loggedIn")
        i.fa-3x.fas.fa-clipboard-check
        h1.title Logged In
        h2.subtitle You have successfully logged in!
  .box.container(v-if="!loggedIn")
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
    b-button(type="is-primary" expanded @click="login(false)" v-if="tab === 'login'") Login
    b-button(type="is-success" expanded @click="login(true)" v-else) Register
    b-message(v-if="error != ''" type="is-danger") {{ error }}
</template>

<script>
import { mapState } from 'vuex'

export default {
  title: 'Login',
  computed: mapState('auth', ['loggedIn', 'error']),
  methods: {
    login (register = false) {
      if (register) {
        this.$store.dispatch('auth/register', {
          email: this.email,
          password: this.password,
          registration_password: this.registrationPassword
        })
      } else {
        this.$store.dispatch('auth/login', {
          email: this.email,
          password: this.password
        })
      }
    }
  },
  data () {
    return {
      email: '',
      password: '',
      registrationPassword: '',
      remember: true,
      tab: 'login'
    }
  }
}
</script>
