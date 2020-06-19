<template lang="pug">
div
  div.hero.is-primary
    .reveal.hero-body
      .slides
        section
          div.is-size-2.content.katex(v-html="formula")
          h1.title.is-1 Welcome to MathsNuggets
        section
          h1.title.is-1 Easily edit formulas
          p.content.is-size-2
            FormField(v-bind.sync="expressionField")
          p.content.
            Try it out by clicking the formula above.
        section
          h1.title.is-1 Automatic Solving
          p.content
            ResourceComponent(type="Equation" :fields.sync="equationWidget" :hide-widget-menu="true")
        section
          h1.title.is-1 Plotter
          p.content
            ResourceComponent(type="Plot" :fields.sync="plotWidget" :hide-widget-menu="true")
        section
          p.content
            img(src='https://www.teachhub.com/sites/default/files/field/image/technology-in-the-classroom-benefits-of-smart-boards.jpg')
        section
          p.content
            ResourceComponent(type="YouTube" :fields.sync="youtubeWidget" :hide-widget-menu="true")
            p.content.
              Add any YouTube link to your Slideshow.
  .container
    .columns(v-for="row in features")
      .column(v-for="feature in row").feature.has-text-centered
        div.is-large
          i.fa-3x(:class="feature.icon")
        h3.title(:class="row.length === 1 ? 'is-1' : 'is-3'") {{ feature.title }}
        .content(:class="row.length === 1 ? 'is-size-3' : 'is-size-5'") {{ feature.text }}
</template>

<script>
import 'typeface-fira-sans'
import FormField from './FormField'
import ResourceComponent from './ResourceComponent'
import katex from 'katex'
import 'katex/dist/katex.min.css'
import Reveal from 'reveal.js'

export default {
  name: 'HomePage',
  title: 'Home',
  components: {
    FormField,
    ResourceComponent
  },
  mounted () {
    Reveal.initialize({
      embedded: true,
      height: '100%'
    })
  },
  data () {
    return {
      expressionField: { label: 'Equation', displayMode: true, type: 'Expression', value: '(sin x)/(sqrt(x) + 1)', latex: '\\frac {\\sin x} {\\sqrt x + 1}' },
      equationWidget: [],
      formula: katex.renderToString('\\int_{-\\infty}^{+\\infty} e^{-x^2} \\,\\mathrm{d}x = \\sqrt \\pi', { displayMode: true }),
      plotWidget: [],
      youtubeWidget: [],
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
}
.reveal {
  background: inherit;
  color: white;
  height: 400px;
}
</style>
