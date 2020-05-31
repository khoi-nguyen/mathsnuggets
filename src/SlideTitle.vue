<template lang="pug">
div
  h2.title
    .columns
      .column
        input.slide-title(
          placeholder="Slide Title"
          :value="value"
          @click="$event.target.select()"
          @keydown.enter="$event.target.blur()"
          @input="$emit('update:value', $event.target.value)"
        )
      .column.is-narrow.field.date
        div {{ today }}
        div {{ time }}
</template>

<script>
import 'typeface-fira-sans'
var moment = require('moment')

export default {
  props: {
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
  }
}
</script>

<style scoped>
h2 input, h2 input:focus {
  background-color: transparent;
  border: 0 !important;
  color: inherit;
  font-family: inherit;
  font-size: inherit;
  padding-left: 0.4em;
  text-align: left;
  width: 100%;
  outline: none;
}
div h2 {
  background-color: #213332;
  color: #ebf0ef;
  font-family: "Fira Sans";
  font-size: 3em;
  margin-bottom: 0.5em;
  padding: 0.1em;
}
.date {
  font-family: "Fira Sans Thin", "Fira Sans";
  font-size: 0.5em;
  text-align: right;
  margin-right: 0.4em;
}
</style>
