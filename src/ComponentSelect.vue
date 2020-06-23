<template lang="pug">
b-field
  b-autocomplete(
    :data="filteredData"
    @select="$emit('update:type', $event.path)"
    field="name"
    icon-pack="fas"
    icon="search"
    keep-first
    open-on-focus
    placeholder="Select widget"
    v-model="localValue"
  )
</template>

<script>
import { api } from './ajax'
export default {
  props: {
    value: String
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
