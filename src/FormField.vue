<template lang="pug">
span(:name="name")
  span(v-html="before")
  span(v-if="!computed")
    component.field(
      :class="{'select': options.length, 'has-text-danger': !options.length, 'is-family-monospace': !options.length}"
      v-if="editing || !html"
      ref="field"
      :rows="rows"
      :cols="cols"
      :disabled="protected"
      :placeholder="label"
      :is="tag"
      :value="value"
      @dblclick="$event.target.select()"
      @focus="editing = true"
      @keydown.enter.exact.stop.prevent="blur"
      @input="inputValue = $event.target.value"
      @onchange="blur"
      @blur="blur"
    ) {{ options.length ? '' : value }}
      option(v-for="option in options" :value="option") {{ option }}
    span.field.content(
      tabindex="0"
      v-html="html"
      v-if="!editing && html"
      @focus="enterEditMode"
      @click="enterEditMode"
    )
    error-message(v-if="error") {{ error }}
  span(v-html="after")
  .has-text-centered(v-if="computed && html" @click="showComputed = !showComputed")
    b-button.computed-field(type="is-success is-outlined" v-if="!showComputed" icon-left="square-root-alt" icon-pack="fas") {{ label }}
    div(v-html="html" v-if="showComputed")
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
    label: String,
    name: String,
    options: { type: Array, default: () => [] },
    protected: Boolean,
    type: String,
    value: String
  },
  components: {
    ErrorMessage
  },
  asyncComputed: {
    async html () {
      const value = !this.value && this.default ? this.default : this.value
      if (!value || this.type === 'Html') {
        return value
      }
      const payload = { value: value, options: this.options }
      const data = await api(`fields/${this.type}`, 'GET', payload, true)
      if (data.error) {
        this.error = data.message
        this.editing = true
        return ''
      }
      this.error = ''
      this.editing = false
      if ('latex' in data) {
        return katex.renderToString(data.latex, { displayMode: this.displayMode || this.computed })
      }
      return data.html || data.value
    }
  },
  computed: {
    cols () {
      if (!this.inputValue) {
        return (this.label || '').length
      }
      return _.maxBy(this.inputValue.split('\n'), (line) => (line.length)).length + 0
    },
    rows () {
      return this.inputValue ? this.inputValue.split('\n').length : 1
    },
    tag () {
      return this.options.length ? 'select' : 'textarea'
    }
  },
  watch: {
    value () {
      this.inputValue = this.value
    }
  },
  data () {
    return {
      error: '',
      editing: !this.value && !this.default,
      inputValue: this.value,
      showComputed: false
    }
  },
  methods: {
    blur (ev) {
      this.$emit('update:value', ev.target.value)
      this.editing = false
    },
    enterEditMode () {
      this.editing = true
      this.$nextTick(() => { this.$refs.field.select() })
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
