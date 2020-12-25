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

export default {
  props: {
    name: String,
    showStats: Boolean,
    correct: Boolean,
    value: String
  },
  data () {
    return {
      voteData: []
    }
  },
  computed: {
    correctAnswers () {
      return this.totalAnswers ? this.voteData.filter(vote => vote.value).length : 0
    },
    totalAnswers () {
      return this.voteData.length
    },
    percentageCorrectAnswers () {
      return this.totalAnswers ? this.correctAnswers * 100 / this.totalAnswers : 0
    }
  },
  methods: {
    deleteVotes () {
      api(`surveys/${this.name}`, 'DELETE')
      this.voteData = []
    },
    async getVoteData () {
      if (this.name) {
        this.voteData = await api(`surveys/${this.name}`, 'GET')
      }
    }
  },
  async mounted () {
    if (this.showStats) {
      setInterval(this.getVoteData, 5000)
    }
    if (this.value) {
      api(`surveys/${this.name}`, 'POST', { value: this.correct })
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
