<template lang="pug">
  .container
    div(v-if="config.edit || (!lock && !auth.loggedIn)")
      slot
      span
        span &nbsp;
        b-icon.has-text-success(pack="fas" icon="check" v-if="correct")
        b-icon.has-text-danger(pack="fas" icon="times" v-if="value && !correct")
    .survey.columns(v-if="auth.loggedIn")
      .column
        b-progress(:value="correctAnswers" :max="totalAnswers" :type="type")
      .column.is-narrow
        span {{ correctAnswers }} / {{ totalAnswers }}
      .column.is-narrow
        b-button(@click.prevent="toggleLockSurvey" :type="lock ? 'is-success' : 'is-danger'")
          b-icon(pack="fas" :icon="lock ? 'lock-open' : 'lock'")
      .column.is-narrow.buttons(v-if="config.edit")
        b-button(@click.prevent="deleteVotes" type="is-danger") Reset
</template>

<script>
import { mapState } from 'vuex'
import api from './ajax'
import _ from 'lodash'

export default {
  props: {
    name: String,
    correct: Boolean,
    lock: Boolean,
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
    },
    type () {
      if (this.percentageCorrectAnswers > 66) {
        return 'is-success'
      }
      if (this.percentageCorrectAnswers < 33) {
        return 'is-danger'
      }
      return 'is-primary'
    },
    ...mapState(['auth', 'config'])
  },
  sockets: {
    voteReceived (data) {
      if (data.survey === this.name) {
        this.$set(this.voteData, data.user, data.value)
      }
    },
    lockToggled (data) {
      if (data.survey === this.name) {
        this.$emit('update:lock', data.value)
      }
    }
  },
  methods: {
    toggleLockSurvey () {
      api(`surveys/${this.name}/lock`, 'POST', { value: !this.lock })
    },
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
    if (this.name && this.auth.loggedIn) {
      await this.getVoteData()
    }
    this.$socket.emit('join', this.name)
    if (this.value) {
      // API calls are performed twice
      // since correct and value are not updated simultaneously
      api(`surveys/${this.name}`, 'POST', { value: this.correct, maxAttempts: 2 * this.maxAttempts })
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
