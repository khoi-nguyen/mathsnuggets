<template lang="pug">
.is-size-3.widget
  b-dropdown.has-text-grey-lighter(v-if="generator" hoverable)
    span(slot="trigger")
      b-icon(pack="fas" icon="cogs")
      span &nbsp;
    b-dropdown-item(custom v-for="constraint in (fields || []).filter(f => f.constraint)")
      input(
        :checked="constraint.name in payload ? payload[constraint.name] : constraint.value"
        :disabled="constraint.protected"
        @input="updatePayload(constraint.name, $event.target.checked)"
        type="checkbox"
        v-if="!constraint.hidden"
      )
      label {{ constraint.label }}
    b-dropdown-item(custom paddingless)
      b-button(type="is-info is-outlined" @click="formValidate(true)") Generate
  form-field(
    v-for="(field, id) in (fields || []).filter(f => !f.constraint && !f.random)"
    v-bind="field"
    :value="fieldValue(field)"
    @update:value="updatePayload(field.name, $event)"
    @form-validate="formValidate"
  )
  error-message(v-if="error")
    p {{ error }}
    b-button(type="is-danger" v-if="!showTraceback" @click="showTraceback = true") Show more details
    pre(@click="showTraceback = false" v-if="showTraceback") {{ traceback }}
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
      error: '',
      showTraceback: false,
      traceback: '',
      computed: {}
    }
  },
  computed: {
    generator () {
      return (this.fields || []).filter(f => f.constraint).length
    }
  },
  asyncComputed: {
    async fields () {
      return await api(`widgets/${this.type}`)
    }
  },
  methods: {
    fieldValue (field) {
      const payload = field.computed ? this.computed : this.payload
      return field.name in payload ? payload[field.name] : ''
    },
    async formValidate (generator = false) {
      const data = await api(`widgets/${this.type}`, generator ? 'POST' : 'GET', this.payload)
      this.error = data.error ? data.message : ''
      this.traceback = data.error ? data.traceback : ''
      forEach(data, (value, key) => this.updatePayload(key, value.html || value.value))
      this.$emit('validate:widget')
    },
    updatePayload (fieldName, value) {
      const field = this.fields.filter(f => f.name === fieldName)[0]
      if (!field.computed && value !== undefined) {
        const payload = this.payload
        payload[fieldName] = value
        this.$emit('update:payload', payload)
      } else {
        this.computed[fieldName] = value
      }
    }
  },
  async mounted () {
    if (this.payload) {
      this.formValidate()
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
