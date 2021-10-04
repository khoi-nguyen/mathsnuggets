<template lang="pug">
table.table.is-striped.is-narrow
  tr
    th carry
    td
    td(v-for="(digit, i) in carry")
      b-button(@click="changeDigit(carry, i)") {{ digit }}
  tr
    th 1#[sup st] number
    td
    td(v-for="(digit, i) in firstNumber")
      b-button(@click="changeDigit(firstNumber, i)") {{ digit }}
  tr
    th 2#[sup nd] number
    td +
    td(v-for="(digit, i) in secondNumber")
      b-button(@click="changeDigit(secondNumber, i)") {{ digit }}
  tr
    th result
    td
    td(v-for="(digit, i) in result")
      b-button(@click="changeDigit(result, i)") {{ digit }}
</template>

<script>
export default {
  props: {
    bits: { type: Number, default: 8 }
  },
  methods: {
    changeDigit (numberArray, position) {
      this.$set(numberArray, position, numberArray[position] ? 0 : 1)
    }
  },
  data () {
    return {
      carry: new Array(this.bits).fill(0),
      firstNumber: new Array(this.bits).fill(0),
      secondNumber: new Array(this.bits).fill(0),
      result: new Array(this.bits).fill(0)
    }
  }
}
</script>
