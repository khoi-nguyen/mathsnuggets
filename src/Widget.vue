<template lang="pug">
form.is-size-3.avoid-column
  .is-size-6
    v-runtime-template(:template="widgetData.generator_template")
    v-runtime-template.constraints(:template="widgetData.random_numbers")
    v-runtime-template.constraints(:template="widgetData.constraints")
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
        forEach(data, (value, fieldName) => {
          const payload = this.widgetData.fields[fieldName].computed ? computed : this.payload
          this.$set(payload, fieldName, value)
        })
        return computed
      },
      default: {},
      shouldUpdate () {
        return !isEmpty(this.widgetData.fields) && isEmpty(filter(this.widgetData.fields, f => {
          return f.required && !f.default && !(f.name in this.payload)
        }))
      }
    },
    widgetData: {
      async get () {
        return await api(`widgets/${this.type}`)
      },
      default: {
        template: '',
        fields: {},
        generator_template: '',
        constraints: '',
        random_numbers: ''
      }
    }
  },
  components: {
    ErrorMessage,
    FormField,
    VRuntimeTemplate
  }
}
</script>
