<template lang="pug">
.container
  NavBar
  section.hero.is-primary
    div.hero-body
      div.container
        h1.title.has-text-black-bis Welcome to MathsNuggets!
        h2.subtitle.has-text-grey-darker.
          An ingenious website designed to facilitate teaching and learning maths.
  .columns(v-for="row in features")
    .column(v-for="feature in row").feature.has-text-centered
      div.is-large
        i.fa-3x(:class="feature.icon")
      h3.title(:class="row.length === 1 ? 'is-1' : 'is-3'") {{ feature.title }}
      .content(:class="row.length === 1 ? 'is-size-3' : 'is-size-5'") {{ feature.text }}
</template>

<script>
import 'typeface-fira-sans'
import 'bulma/css/bulma.css'
import NavBar from './NavBar'

export default {
  name: 'HomePage',
  components: {
    NavBar
  },
  data () {
    return {
      features: [
        [
          {
            icon: 'fas fa-chalkboard-teacher',
            title: 'Lesson builder',
            text: 'Construct and save your own slideshow lessons using the inbuilt tools below:'
          }
        ],
        [
          {
            icon: 'fas fa-calculator',
            title: 'Solver',
            text: 'Solve any equation you type in.'
          },
          {
            icon: 'fas fa-solar-panel',
            title: 'Generator',
            text: 'Generate exercises to the level of your choice.'
          },
          {
            icon: 'far fa-chart-bar',
            title: 'Plotter',
            text: 'Plot the graph of any equation.'
          }
        ],
        [
          {
            icon: 'fas fa-grin-alt',
            title: 'User-Friendly Interface',
            text: 'No programming knowledge is necessary, your inputted formulae are automatically converted.'
          },
          {
            icon: 'fas fa-school',
            title: 'Inclusivity',
            text: 'All tools on this website are available to pupils and teachers.'
          },
          {
            icon: 'fas fa-archway',
            title: 'Structure',
            text: 'Web components are fully embedded'
          }
        ]
      ],
      feature: [
        {
          icon: 'fas fa-chalkboard-teacher',
          title: 'Lesson builder',
          text: 'Construct and save your own slideshow lessons using the inbuilt tools below:'
        }
      ]
    }
  }
}
</script>

<style scoped>
.feature div:first-of-type {
  margin-top: 1em;
}
.feature, .feature .title {
  color: #414141;
  font-family: "Fira Sans";
  font-weight: 300;
}
.feature .content {
  line-height: 1.4;
}
</style>
