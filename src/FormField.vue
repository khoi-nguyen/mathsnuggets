<template lang="pug">
span
  span(v-html="before")
  input.has-text-danger.is-family-monospace(
    v-if="!computed && !valid"
    ref="input"
    :placeholder="label"
    :size="size"
    :value="value"
    @dblclick="$event.target.select()"
    @focus="valid = false"
    @keydown.enter="blur"
    @input="$emit('update:value', $event.target.value)"
    @blur="blur"
  )
  span(
    tabindex="0"
    v-html="renderedHtml"
    v-if="valid && !computed && renderedHtml"
    @focus="enterEditMode"
    @click="enterEditMode"
  )
  div.has-text-centered(
    v-if="computed && renderedHtml"
    @click="$emit('update:show-computed', !showComputed)"
  )
    button.button.is-small.is-success.is-outlined(v-if="!showComputed")
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
import { validateField } from './ajax'
import katex from 'katex'
import 'katex/dist/katex.min.css'

export default {
  props: {
    after: String,
    before: String,
    computed: Boolean,
    default: String,
    displayMode: Boolean,
    html: String,
    label: String,
    latex: String,
    showComputed: Boolean,
    type: String,
    value: String
  },
  watch: {
    html (value) {
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
    size () {
      return this.value ? this.value.length : this.label.length
    }
  },
  data () {
    return {
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
      this.$nextTick(() => { this.$refs.input.select() })
    },
    validate (value, validateForm) {
      validateField(this.type, { value: value }, data => {
        for (const prop in data) {
          if (prop !== 'valid') {
            this.$emit('update:' + prop, data[prop])
          }
        }
        this.valid = data.valid
        if (validateForm) {
          this.$nextTick(() => { this.$emit('form-validate') })
        }
      })
    }
  }
}
</script>

<style scoped>
input, input:focus {
  background: transparent;
  border: 0px;
  font-size: inherit;
  text-align: center;
  outline: none;
}
</style>
