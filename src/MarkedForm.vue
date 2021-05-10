<template lang="pug">
.container(v-if="form")
  b-field(grouped position="is-centered")
    b-field(label="First name")
      b-input(v-model="firstName")
    b-field(label="Last name")
      b-input(v-model="lastName")
    b-field(label="Form")
      b-select(placeholder="Form" v-model="year")
        option(v-for="y in years" :value="y") {{ y }}
  b-field(grouped position="is-centered")
    b-field(label="Email" position="is-centered")
      b-input(v-model="email")
  b-field(grouped position="is-centered")
    b-button(type="is-primary" @click="submitForm") Submit
  b-message(type="is-success" v-if="score.length")
    p You have obtained {{score[0]}} / {{score[1]}}
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
      lastName: '',
      score: [],
      year: '',
      years: ['4A', '4B', '4G', '4K', '4S', '4T', '5B', '5C', '5F', '5M', '5P', '5W', '6B', '6C', '6E', '6M', '6R', '6S', '6T']
    }
  },
  methods: {
    async submitForm () {
      this.config.feedback = true
      const score = await api('mark', 'POST', {
        email: this.email,
        form: this.form,
        firstName: this.firstName,
        lastName: this.lastName,
        url: this.url,
        year: this.year
      })
      this.$set(this, 'score', score)
    }
  }
}
</script>
