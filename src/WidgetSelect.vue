<template lang="pug">
b-autocomplete(
  :append-to-body="true"
  :data="filteredData"
  @select="onSelect"
  field="name"
  icon-pack="fas"
  icon="plus"
  keep-first
  open-on-focus
  placeholder="Add a widget"
  v-model="localValue"
  :size="size"
)
</template>

<script>
import api from './ajax'
export default {
  props: {
    value: { type: String, default: '' },
    size: String
  },
  computed: {
    filteredData () {
      return this.list.filter(function (option) {
        return option.name.toLowerCase().indexOf(this.localValue.toLowerCase()) >= 0
      }.bind(this))
    }
  },
  methods: {
    onSelect (event) {
      if (event && 'path' in event) {
        this.$emit('select:widget', event.path)
      }
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
