<template lang="pug">
.is-size-3.avoid-column
  form-field(
    v-for="(field, id) in fields"
    v-bind="field"
    :value="fieldValue(field)"
    @input="updatePayload(field.name, $event)"
  )
  error-message(:error="error" :traceback="traceback" v-if="error")
</template>

<script>
import { forEach } from 'lodash'

import api from './ajax'
import FormField from './FormField'
import ErrorMessage from './ErrorMessage'

export default {
  props: {
    payload: Object,
    type: String
  },
  data () {
    return {
      error: '',
      traceback: ''
    }
  },
  asyncComputed: {
    computed: {
      async get () {
        const computed = {}
        const data = await api(`widgets/${this.type}`, 'GET', this.payload)
        this.error = data.error ? data.message : ''
        this.traceback = data.error ? data.traceback : ''
        forEach(data, (field, fieldName) => {
          if (field.computed) {
            computed[fieldName] = field.value || field.html
          } else if (!field.constraint && fieldName in (this.payload || {}) && this.payload[fieldName] !== (field.html || field.value)) {
            this.updatePayload(fieldName, field.value || field.html)
          }
        })
        return computed
      },
      default: {},
      shouldUpdate () {
        let valid = true
        forEach(this.fields.filter(f => f.required), (field) => {
          if (!(field.name in this.payload) && !field.default) {
            valid = false
          }
        })
        return valid
      }
    },
    fields: {
      async get () {
        return (await api(`widgets/${this.type}`)).filter(f => !f.constraint && !f.random)
      },
      default: []
    }
  },
  methods: {
    fieldValue (field) {
      const payload = field.computed ? this.computed : this.payload
      return field.name in (payload || {}) && payload[field.name] ? payload[field.name] : ''
    },
    updatePayload (fieldName, value) {
      const field = this.fields.filter(f => f.name === fieldName)
      if (!field.length || field[0].protected || field[0].computed) {
        return false
      }
      if (value === undefined || value === '') {
        delete this.payload[fieldName]
      } else {
        this.$set(this.payload, fieldName, value)
      }
    }
  },
  components: {
    ErrorMessage,
    FormField
  }
}
</script>
