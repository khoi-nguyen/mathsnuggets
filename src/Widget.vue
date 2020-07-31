<template lang="pug">
form.is-size-3.avoid-column
  v-runtime-template(:template="widgetData.template")
  error-message(v-bind="error" v-if="error")
</template>

<script>
import { isEmpty, filter, forEach } from 'lodash'
import VRuntimeTemplate from 'v-runtime-template'

import api from './ajax'
import FormField from './FormField'
import ErrorMessage from './ErrorMessage'

export default {
  props: {
    payload: Object,
    type: String
  },
  data () {
    return { error: {} }
  },
  asyncComputed: {
    computed: {
      async get () {
        const computed = {}
        const data = await api(`widgets/${this.type}`, 'GET', this.payload)
        this.error = data.error ? data : {}
        forEach(data, (field, fieldName) => {
          if (field.computed) {
            computed[fieldName] = field.value || field.html
          } else if (!field.constraint && !field.random) {
            this.$set(this.payload, fieldName, field.value || field.html)
          }
        })
        return computed
      },
      default: {},
      shouldUpdate () {
        let valid = !isEmpty(this.widgetData.fields)
        forEach(filter(this.widgetData.fields, f => f.required && !f.default), (field) => {
          if (!this.payload[field.name]) {
            valid = false
          }
        })
        return valid
      }
    },
    widgetData: {
      async get () {
        return await api(`widgets/${this.type}`)
      },
      default: { template: '', fields: {} }
    }
  },
  components: {
    ErrorMessage,
    FormField,
    VRuntimeTemplate
  }
}
</script>
