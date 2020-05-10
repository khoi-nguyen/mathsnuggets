<template lang="pug">
span.dropdown.is-hoverable(
  v-if="(fields || []).length"
)
  .dropdown-trigger
    button.button.is-info.is-outlined(
      @click="$emit('button-click')"
      tabindex="-1"
    )
      span.icon
        i.fas.fa-tools
      span Generate
      span.icon
        i.fas.fa-angle-down
  .dropdown-menu
    div.dropdown-content
     div(v-for="field in fields" v-if="field.constraint")
      div.dropdown-item.control.field
        label.checkbox
          input(
            type="checkbox"
            v-model="field.value"
            @change="$emit('update:fields', fields)"
          )
          span &nbsp; {{ field.label }}
</template>

<script>
export default {
  props: {
    fields: Array
  }
}
</script>
