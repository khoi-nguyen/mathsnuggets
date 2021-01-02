<template lang="pug">
  .container
    p(v-if="!showStats")
      span Your answer: &nbsp;
      slot
      b-icon.has-text-success(pack="fas" icon="check" v-if="correct")
      b-icon.has-text-danger(pack="fas" icon="times" v-if="value && !correct")
    .survey.columns(v-if="showStats")
      .column
        b-progress(:value="correctAnswers" :max="totalAnswers" :showValue="true") {{ correctAnswers }} / {{ totalAnswers }}
      .column.is-narrow.buttons
        b-button(@click.prevent="deleteVotes" type="is-danger") Reset
</template>

<script>
import api from './ajax'
import _ from 'lodash'

export default {
  props: {
    name: String,
    showStats: Boolean,
    correct: Boolean,
    maxAttempts: { type: Number, default: 3 },
    value: String
  },
  data () {
    return {
      voteData: {}
    }
  },
  computed: {
    correctAnswers () {
      return _.reduce(this.voteData, function (sum, value, user) {
        return sum + (value ? 1 : 0)
      }, 0)
    },
    totalAnswers () {
      return Object.keys(this.voteData).length
    },
    percentageCorrectAnswers () {
      return this.totalAnswers ? this.correctAnswers * 100 / this.totalAnswers : 0
    }
  },
  sockets: {
    voteReceived (data) {
      if (data.survey === this.name) {
        this.$set(this.voteData, data.user, data.value)
      }
    }
  },
  methods: {
    deleteVotes () {
      api(`surveys/${this.name}`, 'DELETE')
      this.voteData = {}
    },
    async getVoteData () {
      if (this.name) {
        this.$set(this, 'voteData', {})
        const data = await api(`surveys/${this.name}`, 'GET')
        for (var i = 0; i < data.length; i++) {
          this.$set(this.voteData, data[i].user, data[i].value)
        }
      }
    }
  },
  async mounted () {
    if (this.name && this.showStats) {
      await this.getVoteData()
      this.$socket.emit('join', this.name)
    }
    if (this.value) {
      api(`surveys/${this.name}`, 'POST', { value: this.correct, maxAttempts: this.maxAttempts })
    }
  }
}
</script>

<style>
.reveal .survey .progress {
  display: block;
  height: 1.2em;
  position: static;
}
</style>
