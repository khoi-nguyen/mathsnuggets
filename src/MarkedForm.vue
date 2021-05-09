<template lang="pug">
.container(v-if="form")
  b-field(grouped position="is-centered")
    b-field(label="First name")
      b-input(v-model="firstName")
    b-field(label="Last name")
      b-input(v-model="lastName")
  b-field(grouped position="is-centered")
    b-field(label="Email" position="is-centered")
      b-input(v-model="email")
  b-field(grouped position="is-centered")
    b-button(type="is-primary" @click="submitForm") Submit
</template>

<script>
import api from './ajax'

export default {
  props: {
    config: Object,
    form: Object,
    url: String
  },
  data () {
    return {
      email: '',
      firstName: '',
      lastName: ''
    }
  },
  methods: {
    submitForm () {
      this.config.feedback = true
      api('mark', 'POST', {
        email: this.email,
        form: this.form,
        firstName: this.firstName,
        lastName: this.lastName,
        url: this.url
      })
    }
  }
}
</script>
