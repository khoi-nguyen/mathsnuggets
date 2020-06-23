<template lang="pug">
div.columns
  ul.column.is-narrow.content.has-text-grey-lighter(v-if="toolbar")
    li(v-for="item in menu" v-if="!item.hide")
      span(@click="item.click" v-if="item.click" :class="`widget-${item.icon}`")
        b-tooltip(:label="item.tooltip" position="is-right")
          b-icon(pack="fas" :icon="item.icon")
      b-dropdown(v-if="item.dropdown" :mobile-modal="false")
        span(slot="trigger" :class="`widget-${item.icon}`")
          b-tooltip(:label="item.tooltip" position="is-right")
            b-icon(pack="fas" :icon="item.icon")
        b-dropdown-item(custom v-for="constraint in item.dropdown.fields" v-if="item.dropdown.fields")
          input(type="checkbox" v-model="constraint.value" :disabled="constraint.protected")
          label  {{ constraint.label }}
        b-dropdown-item(custom paddingless v-for="component in item.dropdown.items")
          component(:is="component.tag" v-bind="component.attrs" v-on="component.listeners") {{ component.text }}
  .column.is-size-3
    form-field(
      v-for="(field, id) in realFields"
      v-bind="field"
      :value.sync="field.value"
      :latex.sync="field.latex"
      :html.sync="field.html"
      :show-computed.sync="field.showComputed"
      @form-validate="formValidate"
    )
    error-message(v-if="error") {{ error }}
</template>

<script>
import { api } from './ajax'
import ComponentSelect from './ComponentSelect'
import FormField from './FormField'
import ErrorMessage from './ErrorMessage'

export default {
  props: {
    type: String,
    toolbar: { type: Boolean, default: true },
    fields: { type: Array, default: () => [] }
  },
  data () {
    return {
      error: '',
      dropdown: '',
      menu: [
        {
          icon: 'search',
          tooltip: 'Select another widget',
          dropdown: {
            items: [
              {
                tag: 'component-select',
                attrs: { value: this.type },
                listeners: { 'update:type': this.loadFields }
              }
            ]
          }
        },
        {
          icon: 'cogs',
          tooltip: 'Generate an exercise',
          hide: !(this.fields.filter(f => f.constraint).length > 0),
          dropdown: {
            fields: this.fields.filter(f => f.constraint),
            items: [
              {
                tag: 'b-button',
                attrs: { type: 'is-info is-outlined' },
                text: 'Generate',
                listeners: { click: () => this.formValidate(true) }
              }
            ]
          }
        },
        {
          click: () => this.$emit('add-component'),
          tooltip: 'Add a widget after this one',
          icon: 'plus-circle'
        },
        {
          click: () => this.$emit('delete'),
          tooltip: 'Delete this widget',
          icon: 'trash-alt'
        }
      ]
    }
  },
  computed: {
    constraints () {
      return this.fields.filter(f => f.constraint)
    },
    realFields () {
      return this.fields.filter(f => !f.constraint)
    }
  },
  mounted () {
    if (this.type) {
      this.loadFields(this.type)
    }
  },
  methods: {
    async formValidate (generator = false) {
      const payload = {}
      const fields = generator ? this.constraints : this.realFields
      for (let i = 0; i < fields.length; i++) {
        const key = fields[i].name
        const value = fields[i].value
        if (value || generator) {
          payload[key] = value || false
        }
      }
      const path = generator ? '/generator' : ''
      const method = generator ? 'POST' : 'GET'
      const data = await api(`widgets/${this.type}${path}`, method, payload)
      if (data.error) {
        this.error = data.message
        return false
      }
      this.error = ''
      for (var name in data) {
        let field = this.fields.filter(f => f.name === name)[0]
        const position = this.fields.indexOf(field)
        field = Object.assign(field, data[name])
        this.$set(this.fields, position, field)
      }
      this.$emit('validate:widget')
    },
    async loadFields (type) {
      if (type === this.type && this.realFields.length) {
        return false
      }
      const data = await api(`widgets/${type}`)
      this.$emit('update:type', type)
      this.$emit('update:fields', data)
    }
  },
  components: {
    ComponentSelect,
    ErrorMessage,
    FormField
  }
}
</script>
