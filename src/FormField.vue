<template lang="pug">
span(:name="name" v-if="!hidden")
  b-field(:label="label" v-if="random" horizontal)
    b-slider(:min="-12" :max="12" :ticks="true" v-model="rangeValue" lazy)
  .field(v-if="constraint")
    b-checkbox(v-model="checkboxValue" :disabled="protected") {{ label }}
  span(v-if="!computed && !constraint && !random")
    component.field(
      v-if="editing || !html"
      v-bind="attrs"
      @dblclick="$event.target.select()"
      @focus="editing = true"
      @keypress="keyPress"
      @keydown.enter.exact.stop.prevent="blur"
      @input="inputValue = $event.target.value"
      @change="blur"
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
    error-message(:message="error" :traceback="traceback" v-if="error")
  .has-text-centered(v-if="computed && html" @click="showComputed = !showComputed")
    b-button.computed-field(type="is-success" v-if="!showComputed" icon-left="square-root-alt" icon-pack="fas") {{ label }}
    div(v-html="html" v-if="showComputed")
</template>

<script>
import api from './ajax'
import katex from 'katex'
import 'katex/dist/katex.min.css'
import _ from 'lodash'

import ErrorMessage from './ErrorMessage'

export default {
  props: {
    computed: Boolean,
    constraint: Boolean,
    default: [String, Array, Boolean],
    displayMode: Boolean,
    hidden: Boolean,
    label: String,
    name: String,
    options: { type: Array, default: () => [] },
    protected: Boolean,
    random: Boolean,
    type: String,
    value: [String, Array, Boolean]
  },
  components: {
    ErrorMessage
  },
  asyncComputed: {
    async html () {
      const value = !this.value && this.default ? this.default : this.value
      if (!value || this.type === 'Html' || this.random || this.constraint) {
        return value
      }
      const payload = { value: value, options: this.options }
      const data = await api(`fields/${this.type}`, 'GET', payload, true)
      if (data.error) {
        this.error = data.message
        this.traceback = data.traceback
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
    attrs () {
      const value = this.inputValue ? this.inputValue : this.label || ''
      return {
        class: {
          'has-text-danger': !this.options.length,
          'is-family-monospace': !this.options.length,
          select: this.options.length
        },
        cols: _.maxBy(value.split('\n'), (line) => (line.length)).length,
        disabled: this.protected,
        is: this.options.length ? 'select' : 'textarea',
        placeholder: this.label,
        ref: 'field',
        rows: value.split('\n').length,
        value: this.value
      }
    },
    rangeValue: {
      get () {
        let value = this.value || this.default
        if (typeof value === 'string' || value instanceof String) {
          value = _.map(value.split(','), parseFloat)
        }
        return [_.min(value), _.max(value)]
      },
      set (value) {
        this.$emit('input', _.range(value[0], value[1] + 1))
      }
    },
    checkboxValue: {
      get () {
        return Boolean(this.value || this.default)
      },
      set (value) {
        this.$emit('input', value)
      }
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
      showComputed: false,
      traceback: ''
    }
  },
  updated () {
    var mathElements = document.getElementsByClassName('math')
    for (var i = 0; i < mathElements.length; i++) {
      var displayMode = !mathElements[i].classList.contains('inline')
      var texText = mathElements[i].firstChild
      if (texText && texText.data) {
        katex.render(texText.data, mathElements[i], { displayMode })
      }
    }
  },
  methods: {
    blur (ev) {
      this.$emit('input', ev.target.value)
      this.editing = false
    },
    enterEditMode () {
      this.editing = true
      this.$nextTick(() => { this.$refs.field.select() })
    },
    keyPress (event) {
      if (event.shiftKey && event.charCode === 63) {
        event.stopPropagation()
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
