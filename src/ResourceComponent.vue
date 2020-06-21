<template lang="pug">
div.widget-container
  div.columns
    div.widget-col.column.is-narrow(
      :class="{'hidden': !edit, 'remove': hideWidgetMenu}"
      @mouseover="edit = true"
      @mouseleave="edit = false"
      tabindex=0
      @focus="edit = true"
    )
      div.columns
        div.column
          ComponentSelect(
            :value="type"
            @update:type="loadFields"
            @has-focus="edit = true"
            @lost-focus="edit = false"
          )
        div.column.is-narrow
          .buttons
            button.delete(
              tabindex="-1"
              @click="$emit('delete')"
            ) Delete
      .buttons.are-small
        div
          button.button.is-success.is-outlined(@click="$emit('add-component')" tabindex="-1")
            span.icon
              i.fas.fa-plus-circle
            span Add
        Generator(
          :fields.sync="fields"
          v-if="(constraints || []).length"
          @button-click="formValidate(true)"
        )
    div.column.is-size-3
      span(v-for="(field, id) in realFields" :key="id")
        FormField(
          v-bind="field"
          :value.sync="field.value"
          :latex.sync="field.latex"
          :html.sync="field.html"
          :show-computed.sync="field.showComputed"
          @form-validate="formValidate"
        )
      div(v-if="error")
        error-message {{ error }}
</template>

<script>
import { getComponentFields, api } from './ajax'
import ComponentSelect from './ComponentSelect'
import FormField from './FormField'
import Generator from './Generator'
import ErrorMessage from './ErrorMessage'

export default {
  props: {
    hideWidgetMenu: Boolean,
    type: String,
    fields: Array
  },
  data () {
    return {
      edit: false,
      error: ''
    }
  },
  computed: {
    constraints () {
      return (this.fields || []).filter(field => { return field.constraint })
    },
    realFields () {
      return (this.fields || []).filter(field => { return !field.constraint })
    }
  },
  mounted () {
    if (this.type) {
      this.loadFields(this.type)
    }
  },
  methods: {
    async formValidate (useGenerator = false) {
      var formData = {}
      var fields = useGenerator ? this.constraints : this.realFields
      for (var i = 0; i < fields.length; i++) {
        var key = fields[i].name
        var value = fields[i].value
        if (value || useGenerator) {
          formData[key] = value || false
        }
      }
      var path = useGenerator ? '/generator' : ''
      const data = await api(`widgets/${this.type}${path}`, 'GET', formData)
      if (data.error) {
        this.error = data.message
        return false
      }
      this.error = ''
      for (var name in data) {
        var field = this.fields.filter((f) => (f.name === name))[0]
        var position = this.fields.indexOf(field)
        field = Object.assign(field, data[name])
        this.$set(this.fields, position, field)
      }
      this.$emit('validate:widget')
    },
    loadFields (type) {
      if (type === this.type && this.realFields.length) {
        return false
      }
      this.$emit('update:type', type)
      getComponentFields(type, function (data) {
        this.$emit('update:fields', data)
      }.bind(this))
    }
  },
  components: {
    ComponentSelect,
    ErrorMessage,
    FormField,
    Generator
  }
}
</script>

<style scoped>
.widget-container {
  padding: 0 10px;
}
.widget-col {
  border-left: lightgray 10px solid;
}
.hidden {
  width: 1px;
}
.hidden > div {
  visibility: hidden;
}
.hidden > .buttons {
  display: none;
}
.remove {
  display: none;
}
</style>
