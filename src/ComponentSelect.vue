<template lang="pug">
div
  div.select.is-small
    select(
      :value="value"
      @change="selectComponent"
      @focus="$emit('has-focus')"
      @blur="$emit('lost-focus')"
    )
      option(selected value) Select component
      option(
        v-for="component in list"
        :value="component.path"
      ) {{ component.name }}
</template>

<script>
import { getComponentList } from './ajax'
export default {
  props: {
    value: String
  },
  mounted () {
    getComponentList((data) => { this.list = data })
  },
  methods: {
    selectComponent (ev) {
      var value = ev.target.value
      this.$emit('update:type', value)
      ev.target.blur()
    }
  },
  data () {
    return {
      list: []
    }
  }
}
</script>

<style scoped>
input, input:focus {
  border: 0;
  max-width: 100%;
  outline: 0;
}
</style>
