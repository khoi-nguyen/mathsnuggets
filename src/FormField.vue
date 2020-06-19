<template lang="pug">
span
  span(v-html="before")
  component.has-text-danger.is-family-monospace(
    :class="{'select': options}"
    v-if="!computed && !valid && !hidden"
    ref="field"
    :rows="rows"
    :cols="cols"
    :disabled="protected"
    :placeholder="label"
    :is="tag"
    :value="value"
    @dblclick="$event.target.select()"
    @focus="valid = false"
    @keydown.191.stop=""
    @keydown.enter.exact.prevent="blur"
    @input="$emit('update:value', $event.target.value)"
    @blur="blur"
  )
    option(v-for="option in options" :value="option") {{ option }}
  span(
    tabindex="0"
    v-html="renderedHtml"
    v-if="valid && !computed && renderedHtml"
    @focus="enterEditMode"
    @click="enterEditMode"
  )
  div(v-if="error")
    error-message {{ error }}
  div.has-text-centered(
    v-if="computed && renderedHtml"
    @click="$emit('update:show-computed', !showComputed)"
  )
    button.button.is-success.is-outlined.computed-field(v-if="!showComputed")
      span.icon
        i.fas.fa-square-root-alt
      span {{ label }}
    div(
      v-html="renderedHtml"
      v-if="showComputed"
    )
  span(v-html="after")
</template>

<script>
import { api } from './ajax'
import katex from 'katex'
import 'katex/dist/katex.min.css'
import _ from 'lodash'

import ErrorMessage from './ErrorMessage'

export default {
  props: {
    after: String,
    before: String,
    computed: Boolean,
    default: String,
    displayMode: Boolean,
    hidden: Boolean,
    html: String,
    label: String,
    latex: String,
    options: Array,
    showComputed: Boolean,
    protected: Boolean,
    type: String,
    value: String
  },
  components: {
    ErrorMessage
  },
  watch: {
    renderedHtml (value) {
      this.valid = !!value
    }
  },
  computed: {
    renderedHtml () {
      if (this.latex) {
        return katex.renderToString(this.latex, { displayMode: this.displayMode || this.computed })
      }
      return this.html
    },
    cols () {
      if (!this.value) {
        return this.label.length
      }
      return _.maxBy(this.value.split('\n'), (line) => (line.length)).length + 0
    },
    rows () {
      return this.value ? this.value.split('\n').length : 1
    },
    tag () {
      return (this.options || []).length ? 'select' : 'textarea'
    }
  },
  data () {
    return {
      error: '',
      valid: false
    }
  },
  mounted () {
    const value = this.value ? this.value : this.default
    if (value && !this.computed) {
      this.validate(value)
    }
  },
  methods: {
    blur (ev) {
      if (ev.target.value) {
        this.validate(ev.target.value, ev.key === 'Enter')
      }
    },
    enterEditMode () {
      this.valid = false
      this.$nextTick(() => { this.$refs.field.select() })
    },
    async validate (value, validateForm) {
      const payload = { value: value }
      if ((this.options || []).length) {
        payload.options = this.options
      }
      const data = await api(`fields/${this.type}`, 'GET', payload)
      if (data.error) {
        this.error = data.message
        this.valid = false
        return false
      }
      this.error = ''
      for (const prop in data) {
        if (prop !== 'valid') {
          this.$emit('update:' + prop, data[prop])
        }
      }
      this.valid = data.valid
      if (validateForm) {
        this.$nextTick(() => { this.$emit('form-validate') })
      }
    }
  }
}
</script>

<style scoped>
textarea, textarea:focus {
  background: transparent;
  border: 0;
  display: inline;
  font-size: inherit;
  line-height: 1;
  outline: none;
  overflow: hidden;
  margin: 0;
  padding: 0;
  resize: none;
  vertical-align: middle;
}
</style>
