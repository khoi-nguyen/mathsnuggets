<template lang="pug">
form.avoid-column
  v-runtime-template.is-size-3(:template="widgetData.template")
  v-runtime-template(:template="generatorTemplate")
  error-message(v-bind="error" v-if="error")
</template>

<script>
import { isEmpty, isEqual, filter, forEach, map, pickBy } from 'lodash'
import VRuntimeTemplate from 'v-runtime-template'

import api from './ajax'
import FormField from './FormField'
import ErrorMessage from './ErrorMessage'
import Survey from './Survey'

export default {
  props: {
    blacklist: Array,
    config: Object,
    payload: Object,
    state: Object,
    type: String
  },
  data () {
    return {
      computed: {},
      error: {},
      showGenerator: false
    }
  },
  computed: {
    solverPayload () {
      if (!(this.widgetData || {}).fields) {
        return {}
      }
      return pickBy(this.payload, (value, fieldName) => {
        const field = this.widgetData.fields[fieldName]
        if (!field) {
          return false
        }
        return !field.random && !field.constraint && !(value === '')
      })
    },
    survey () {
      if (!(this.widgetData || {}).template) {
        return false
      }
      return this.widgetData.template.includes('<survey')
    },
    generatorPayload () {
      if (!(this.widgetData || {}).fields) {
        return {}
      }
      return pickBy(this.payload, (value, fieldName) => {
        const field = this.widgetData.fields[fieldName]
        return field.random || field.constraint
      })
    },
    generatorTemplate () {
      return `
        <b-modal :active.sync="state.showGenerator">
          <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">Generator</p>
              <button type="button" class="delete" @click="state.showGenerator = false" />
            </header>
            <section class="modal-card-body">
              <p class="is-size-3">${this.widgetData.template}</p>
              <hr />
              ${this.widgetData.generator_template}
              <div class="columns">
                  <div class="column">${this.widgetData.random_numbers}</div>
                  <div class="column">${this.widgetData.constraints}</div>
              </div>
            </section>
            <footer class="modal-card-foot buttons">
              <b-button type="is-primary" @click="solve(true)">Generate</b-button>
              <b-button type="is-danger" @click="state.showGenerator = false">Close</b-button>
            </footer>
          </div>
        </b-modal>
      `
    },
    hasGenerator () {
      return !isEmpty(filter(this.widgetData.fields, f => f.random || f.constraint))
    }
  },
  methods: {
    async solve (generator = false) {
      const method = (generator || this.survey) ? 'POST' : 'GET'
      const payload = generator ? this.generatorPayload : this.solverPayload
      const data = await api(`widgets/${this.type}`, method, payload, !generator)
      this.error = data.error ? data : {}
      forEach(data, (value, fieldName) => {
        if (!(fieldName in this.widgetData.fields)) {
          return false
        }
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
        if (!this.widgetData) {
          return false
        }
        const isValid = !isEmpty(this.widgetData.fields) && isEmpty(filter(this.widgetData.fields, f => {
          return f.required && !f.default && !this.payload[f.name]
        }))
        if (isValid && !isEqual(newValue, oldValue)) {
          this.solve()
        }
      },
      deep: true
    },
    widgetData (data) {
      this.$emit('update:blacklist', map(filter(this.widgetData.fields, f => f.nosave), f => f.name))
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
  async mounted () {
    if (this.payload) {
      await this.$nextTick()
      this.solve()
    }
  },
  components: {
    ErrorMessage,
    FormField,
    Survey,
    VRuntimeTemplate
  }
}
</script>
