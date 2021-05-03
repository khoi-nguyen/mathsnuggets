<template lang="pug">
div(:class="{ form: config.form, slide: !config.form, box: !config.form }")
  h2.title(:class="{ 'is-1': config.form }")
    .columns.is-vcentered
      .column
        form-field(:editable="config.edit" @input="$emit('input', $event)" :value="value" type="Markdown")
      .column.is-narrow.date(v-if="!config.form")
        div {{ today }}
        div {{ time }}
</template>

<script>
import 'typeface-fira-sans'

import FormField from './FormField'

var moment = require('moment')

export default {
  props: {
    config: Object,
    value: String
  },
  data () {
    return {
      today: moment().format('dddd Do MMM'),
      interval: false,
      time: moment().format('hh:mm a')
    }
  },
  mounted () {
    this.updateTime()
    this.interval = setInterval(this.updateTime, 1000)
  },
  methods: {
    updateTime () {
      this.time = moment().format('h.mma')
    }
  },
  components: {
    FormField
  }
}
</script>

<style scoped>
.box.slide h2.title {
  background-color: #172838;
  color: #ebf0ef;
  font-size: 3em;
  margin-bottom: 0.5em;
  padding: 0.2em;
}
.date {
  font-size: 0.5em;
  font-weight: 300;
  text-align: right;
  margin-right: 0.4em;
}
.slide.box {
  padding: 0;
}
.form h2.title {
  border-bottom: 1px solid #dddddd;
  padding: 0.3em 0;
  margin: 0.5em 0;
}
</style>
