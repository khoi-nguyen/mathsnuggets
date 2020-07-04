<template lang="pug">
b-field
  b-autocomplete(
    :data="filteredData"
    @select="$emit('select:widget', $event.path)"
    field="name"
    icon-pack="fas"
    icon="plus"
    keep-first
    open-on-focus
    placeholder="Add a widget"
    v-model="localValue"
  )
</template>

<script>
import { api } from './ajax'
export default {
  props: {
    value: { type: String, default: '' }
  },
  computed: {
    filteredData () {
      return this.list.filter(function (option) {
        return option.name.toLowerCase().indexOf(this.localValue.toLowerCase()) >= 0
      }.bind(this))
    }
  },
  watch: {
    value (val) {
      this.localValue = val
    }
  },
  async mounted () {
    this.list = await api('widgets')
  },
  data () {
    return {
      localValue: this.value,
      list: []
    }
  }
}
</script>
