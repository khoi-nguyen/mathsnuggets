<template lang="pug">
div.columns
  .column.is-narrow
    table.table.is-bordered.is-striped
      tr
        th.has-centered-text(v-for="(digit, i) in digits") {{ base ** (digits.length - 1 - i)  }}
        th(v-if="showDecimal") Decimal
      tr
        td(v-for="(digit, i) in digits")
          b-button(@click="changeDigit(i)") {{ digit }}
        td(v-if="showDecimal") {{ decimalNumber }}
</template>

<script>
export default {
  props: {
    bits: { type: Number, default: 4 },
    base: { type: Number, default: 2 },
    showDecimal: { type: Boolean, default: true }
  },
  computed: {
    decimalNumber () {
      let result = 0
      for (let i = 0; i < this.digits.length; i++) {
        result += this.digits[i] * this.base ** (this.digits.length - 1 - i)
      }
      return result
    }
  },
  methods: {
    changeDigit (position) {
      if (this.digits[position] === this.base - 1) {
        this.$set(this.digits, position, 0)
      } else {
        this.$set(this.digits, position, this.digits[position] + 1)
      }
    }
  },
  data () {
    return {
      digits: new Array(this.bits).fill(0)
    }
  }
}
</script>
