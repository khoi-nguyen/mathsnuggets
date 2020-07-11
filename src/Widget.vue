<template lang="pug">
.is-size-3.widget
  b-dropdown.has-text-grey-lighter(v-if="generator" hoverable)
    span(slot="trigger")
      b-icon(pack="fas" icon="cogs")
      span &nbsp;
    b-dropdown-item(custom v-for="constraint in fields.filter(f => f.constraint)")
      input(
        :checked="constraint.name in payload ? payload[constraint.name] : constraint.value"
        :disabled="constraint.protected"
        @input="updatePayload(constraint.name, $event.target.checked)"
        type="checkbox"
        v-if="!constraint.hidden"
      )
      label {{ constraint.label }}
    b-dropdown-item(custom paddingless)
      b-button(type="is-info is-outlined" @click="generate()") Generate
  form-field(
    v-for="(field, id) in fields.filter(f => !f.constraint && !f.random)"
    v-bind="field"
    :value="fieldValue(field)"
    @update:value="updatePayload(field.name, $event)"
  )
  error-message(v-if="error") {{ error }}
</template>

<script>
import { forEach } from 'lodash'

import { api } from './ajax'
import FormField from './FormField'
import ErrorMessage from './ErrorMessage'

export default {
  props: {
    payload: { type: Object, default: () => {} },
    type: String
  },
  data () {
    return {
      error: ''
    }
  },
  computed: {
    generator () {
      return this.fields.filter(f => f.constraint).length
    }
  },
  asyncComputed: {
    async computed () {
      const computed = {}
      const data = await api(`widgets/${this.type}`, 'GET', this.payload)
      this.error = data.error ? data.message : ''
      forEach(data, (field, fieldName) => {
        if (field.computed) {
          computed[fieldName] = field.html || field.value
        } else if (!field.constraint && fieldName in (this.payload || {}) && this.payload[fieldName] !== (field.html || field.value)) {
          this.updatePayload(fieldName, field.html || field.value)
        }
      })
      return computed
    },
    fields: {
      async get () {
        return await api(`widgets/${this.type}`)
      },
      default: []
    }
  },
  methods: {
    fieldValue (field) {
      const payload = field.computed ? this.computed : this.payload
      return field.name in (payload || {}) && payload[field.name] ? payload[field.name] : ''
    },
    async generate () {
      const data = await api(`widgets/${this.type}`, 'POST', this.payload)
      this.error = data.error ? data.message : ''
      forEach(data, (field, fieldName) => {
        if (!field.constraint) {
          this.updatePayload(fieldName, field.html || field.value)
        }
      })
    },
    updatePayload (fieldName, value) {
      const field = this.fields.filter(f => f.name === fieldName)
      if (!field.length || field[0].protected || field[0].computed) {
        return false
      }
      const payload = this.payload
      if (value === undefined || value === '') {
        delete payload[fieldName]
      } else {
        payload[fieldName] = value
      }
      this.$emit('update:payload', payload)
    }
  },
  components: {
    ErrorMessage,
    FormField
  }
}
</script>

<style scoped>
.widget {
  break-inside: avoid-column;
}
</style>
