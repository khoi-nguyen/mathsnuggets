<template lang="pug">
div
  h2.title
    .columns
      .column
        input(
          placeholder="Slide Title"
          :value="value"
          @click="$event.target.select()"
          @keydown.enter="$event.target.blur()"
          @input="$emit('update:value', $event.target.value)"
        )
      .column.is-narrow.field.date
        div {{ new Date().toLocaleString('en-GB', dateOptions) }}
</template>

<script>
import 'typeface-fira-sans'

export default {
  props: {
    value: String
  },
  data () {
    return {
      dateOptions: {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }
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
  font-family: "Fira Sans Thin";
  font-size: 0.5em;
  text-align: right;
  margin-right: 0.4em;
}
</style>
