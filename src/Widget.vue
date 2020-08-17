<template lang="pug">
form.avoid-column
  v-runtime-template(:template="generatorTemplate" v-if="hasGenerator")
  v-runtime-template.is-size-3(:template="widgetData.template")
  error-message(v-bind="error" v-if="error")
</template>

<script>
import { isEmpty, isEqual, filter, forEach, pickBy } from 'lodash'
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
    return {
      computed: {},
      error: {}
    }
  },
  computed: {
    solverPayload () {
      return pickBy(this.payload, (value, fieldName) => {
        const field = this.widgetData.fields[fieldName]
        return !field.random && !field.constraint
      })
    },
    generatorPayload () {
      return pickBy(this.payload, (value, fieldName) => {
        const field = this.widgetData.fields[fieldName]
        return field.random || field.constraint
      })
    },
    generatorTemplate () {
      return `
        <div class="modal-card modal-card-body">
          ${this.widgetData.generator_template}
          <div class="columns">
              <div class="column">${this.widgetData.random_numbers}</div>
              <div class="column">${this.widgetData.constraints}</div>
          </div>
          <div class="buttons">
            <b-button @click="solve(true)">Generate</b-button>
          </div>
        </div>
      `
    },
    hasGenerator () {
      return !isEmpty(filter(this.widgetData.fields, f => f.random || f.constraint))
    }
  },
  methods: {
    async solve (generator = false) {
      const method = generator ? 'POST' : 'GET'
      const payload = generator ? this.generatorPayload : this.solverPayload
      const data = await api(`widgets/${this.type}`, method, payload)
      this.error = data.error ? data : {}
      forEach(data, (value, fieldName) => {
        const payload = this.widgetData.fields[fieldName].computed ? this.computed : this.payload
        if (payload[fieldName] !== value) {
          this.$set(payload, fieldName, value)
        }
      })
    }
  },
  watch: {
    solverPayload: {
      handler (newValue, oldValue) {
        const isValid = !isEmpty(this.widgetData.fields) && isEmpty(filter(this.widgetData.fields, f => {
          return f.required && !f.default && !this.payload[f.name]
        }))
        if (isValid && !isEqual(newValue, oldValue)) {
          this.solve()
        }
      },
      deep: true,
      immediate: true
    }
  },
  asyncComputed: {
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
