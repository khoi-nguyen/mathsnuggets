<template lang="pug">
form.widget
  v-runtime-template.is-size-3(:template="widgetData.template")
  div(v-if="generator && hasGenerator")
    v-runtime-template(:template="generatorTemplate")
    b-button(type="is-primary" @click="solve(true)") Generate
  v-runtime-template(:template="generatorTemplateWithModal")
  error-message(v-bind="error" v-if="error")
</template>

<script>
import _ from 'lodash'
import { mapState } from 'vuex'
import VRuntimeTemplate from 'v-runtime-template'

import api from './ajax'
import ConfigOption from './ConfigOption'
import FormField from './FormField'
import ErrorMessage from './ErrorMessage'
import Survey from './Survey'
import Tuxie from './Tuxie'
import WidgetSettings from './WidgetSettings'

export default {
  props: {
    blacklist: Array,
    generator: Boolean,
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
      return _.pickBy(this.payload, (value, fieldName) => {
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
      return _.pickBy(this.payload, (value, fieldName) => {
        const field = this.widgetData.fields[fieldName]
        return field.random || field.constraint
      })
    },
    generatorTemplateWithModal () {
      return `
        <b-modal :active.sync="state.showGenerator">
          <div class="modal-card">
            <header class="modal-card-head">
              <p class="modal-card-title">Generator</p>
              <button type="button" class="delete" @click="state.showGenerator = false" />
            </header>
            <section class="modal-card-body">
              <p class="is-size-3">${this.widgetData.template}</p>
              ${this.generatorTemplate}
            </section>
            <footer class="modal-card-foot buttons">
              <b-button type="is-primary" @click="solve(true)">Generate</b-button>
              <b-button type="is-danger" @click="state.showGenerator = false">Close</b-button>
            </footer>
          </div>
        </b-modal>
      `
    },
    generatorTemplate () {
      return `
        <div>
          <hr />
          ${this.widgetData.generator_template}
          <div class="columns">
              <div class="column">${this.widgetData.random_numbers}</div>
              <div class="column">${this.widgetData.constraints}</div>
          </div>
        </div>
      `
    },
    hasGenerator () {
      return !_.isEmpty(_.filter(this.widgetData.fields, f => f.random || f.constraint))
    },
    ...mapState('auth', ['loggedIn']),
    ...mapState(['config'])
  },
  methods: {
    async solve (generator = false) {
      const method = (generator) ? 'POST' : 'GET'
      const payload = generator ? this.generatorPayload : this.solverPayload
      const data = await api(`widgets/${this.type}`, method, payload)
      this.error = data.error ? data : {}
      _.forEach(data, (value, fieldName) => {
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
        const isValid = !_.isEmpty(this.widgetData.fields) && _.isEmpty(_.filter(this.widgetData.fields, f => {
          return f.required && !f.default && !this.payload[f.name]
        }))
        if (isValid && !_.isEqual(newValue, oldValue)) {
          this.solve()
        }
      },
      deep: true
    },
    widgetData (data) {
      this.$emit('update:blacklist', _.map(_.filter(this.widgetData.fields, f => f.nosave), f => f.name))
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
    ConfigOption,
    ErrorMessage,
    FormField,
    Survey,
    Tuxie,
    VRuntimeTemplate,
    WidgetSettings
  }
}
</script>

<style scoped>
.widget {
  position: relative;
}
</style>
