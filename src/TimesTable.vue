<template lang="pug">
table.table.is-bordered.is-narrow.is-striped.is-hoverable
  thead
    tr
      th
      th(v-for="i in cols.split(',')") {{ i }}
  tbody
    tr(v-for="i in range")
      th {{ rows.split(',')[i] }}
      td(v-for="j in range" :class="cellClass(i, j)")
        form-field(v-model="table[i * size + j]" type="Expression" @input="input(i * size + j, $event)" label=" ")
</template>

<script>
import _ from 'lodash'

import FormField from './FormField'

export default {
  props: {
    cols: String,
    size: { type: Number, default: 10 },
    marking: String,
    rows: String,
    value: String
  },
  computed: {
    range () {
      return _.range(this.size)
    },
    markingArray () {
      if (this.marking) {
        return this.marking.replace(/[\[\]]/g, '').split(',')
      } else {
        return []
      }
    }
  },
  data () {
    return {
      table: this.value.split(',')
    }
  },
  methods: {
    cellClass (i, j) {
      const mark = Number(this.markingArray[i * this.size + j])
      return ['has-text-danger', '', 'has-text-success'][mark + 1]
    },
    input (key, val) {
      this.$emit('input', this.table.join(','))
    }
  },
  watch: {
    value (newValue) {
      this.table = newValue.split(',')
    }
  },
  components: {
    FormField
  }
}
</script>
