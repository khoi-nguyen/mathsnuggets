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
    :value="field.name in payload ? payload[field.name] : ''"
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
    return { error: '', showTraceback: false, traceback: '' }
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
    async formValidate (generator = false) {
      const data = await api(`widgets/${this.type}`, generator ? 'POST' : 'GET', this.payload)
      this.error = data.error ? data.message : ''
      this.traceback = data.error ? data.traceback : ''
      forEach(data, (value, key) => this.updatePayload(key, value.html || value.value))
      this.$emit('validate:widget')
    },
    updatePayload (fieldName, value) {
      const payload = this.payload
      payload[fieldName] = value
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
