<template lang="pug">
span
  span(v-html="before")
  input.has-text-danger.is-size-4.is-family-monospace(
    v-if="!computed"
    ref="input"
    :class="{hidden: valid}"
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
    v-html="renderedHtml"
    v-if="valid && !computed"
    @click="$refs.input.select()"
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
    html: String,
    label: String,
    latex: Boolean,
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
      if (this.latex && this.html) {
        return katex.renderToString(this.html, { displayMode: this.computed })
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
    if (this.value && !this.computed) {
      this.validate(this.value)
    }
  },
  methods: {
    blur (ev) {
      if (ev.target.value) {
        this.validate(ev.target.value, ev.key === 'Enter')
      }
    },
    validate (value, validateForm) {
      validateField(this.type, { value: value }, data => {
        this.$emit('update:html', data.sanitized)
        this.$emit('update:value', data.value)
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
  border: 0px;
  text-align: center;
  outline: none;
}
.hidden {
  width: 1px
}
</style>
