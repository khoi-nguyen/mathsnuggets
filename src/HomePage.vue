<template lang="pug">
.container
  NavBar
  .columns
    .column(v-for="card in cards")
      div.feature.has-text-centered
        span.card-header-icon.is-large.is-left
          i.fa-3x(:class="card.icon")
        h3.title.is-3.has-text-centered {{ card.title }}
        .content.is-size-5 {{ card.text }}
</template>

<script>
import 'typeface-fira-sans'
import 'bulma/css/bulma.css'
import NavBar from './NavBar'

export default {
  name: 'HomePage',
  data () {
    return {
      cards: [
        {
          icon: 'fas fa-chalkboard-teacher',
          title: 'Lesson builder',
          text: 'Construct and save your own slideshow lessons using: Generator, Solver and Plotter and all other basic slideshow creating tools.'
        },
        {
          icon: 'fas fa-calculator',
          title: 'Solver',
          text: 'Construct and save your own slideshow lessons using: Generator, Solver and Plotter and all other basic slideshow creating tools.'
        }
      ]
    }
  },
  components: {
    NavBar
  }
}
</script>

<style scoped>
.feature, .feature .title {
  color: #414141;
  font-family: "Fira Sans";
  font-weight: 300;
}
.feature .content {
  line-height: 1.4;
}
</style>
