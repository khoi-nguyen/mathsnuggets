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
    .container
      .field(v-for="field in fields")
        label.label(:for="field.name") {{ field.label }}
          .control.has-icons-left
            input.input(:name="field.name" :type="field.name" ref="fields")
            span.icon.is-small.is-left
              i.fa(:class="field.icon")
        article.message.is-danger(v-if="errors[field.name] != ''")
          div.message-body {{ errors[field.name] }}
      .field
        label.checkbox(for='')
          input(type='checkbox')
          |  Remember me
      .field
        button.button.is-info.is-fullwidth(@click="login") Login
      article.message.is-danger(v-if="authState.error != ''")
        div.message-body {{ authState.error }}
</template>

<script>
import NavBar from './NavBar'
import { auth } from './auth.js'

export default {
  components: { NavBar },
  name: 'Login',
  methods: {
    login () {
      this.errors.email = ''
      this.errors.password = ''
      if (!this.$refs.fields[1].value) {
        this.errors.password = 'Password is empty'
      }
      if (!this.$refs.fields[0].value) {
        this.errors.email = 'Email is empty'
      }
      if (!this.errors.email && !this.errors.password) {
        auth.login(this.$refs.fields[0].value, this.$refs.fields[1].value)
      }
    }
  },
  data () {
    return {
      authState: auth.state,
      error: '',
      errors: {
        email: '',
        password: ''
      },
      fields: [
        {
          label: 'Email',
          name: 'email',
          icon: 'fa-envelope'
        },
        {
          label: 'Password',
          name: 'password',
          icon: 'fa-lock'
        }
      ]
    }
  }
}
</script>
