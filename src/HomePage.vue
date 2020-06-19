<template lang="pug">
div
  div.hero.is-primary
    .reveal.hero-body
      .slides
        section
          h1.title.is-1 Welcome to MathsNuggets
          div.is-size-2.content.katex(v-html="formula")
        section
          h1.title.is-1 Easily edit formulas
          p.content.is-size-2
            form-field(v-bind.sync="field")
          p.content.
            Try it out by clicking the formula above.
        section
          h1.title.is-1 Automatic Solving
          div.content.is-gapless
            resource-component(type="Equation" :fields.sync="widget" :hide-widget-menu="true")
          ul.content
            li Click the equation to change it
            li Click the 'Solution' button to see the solution
  .container
    .columns(v-for="row in features")
      .column(v-for="feature in row").feature.has-text-centered
        div.is-large
          i.fa-3x(:class="feature.icon")
        h3.title(:class="row.length === 1 ? 'is-1' : 'is-3'") {{ feature.title }}
        .content(:class="row.length === 1 ? 'is-size-3' : 'is-size-5'") {{ feature.text }}
</template>

<script>
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
  watch: {
    widget (newVal, oldVal) {
      if (!oldVal.length) {
        const field = newVal[0]
        field.value = 'x^2 - 5x + 6'
        this.$set(this.widget, 0, field)
        const solution = newVal[2]
        solution.latex = '\\{2, 3\\}'
        this.$set(this.widget, 2, solution)
      }
    }
  },
  data () {
    return {
      field: { label: 'Equation', displayMode: true, type: 'Expression', value: '(sin x)/(sqrt(x) + 1)', latex: '\\frac {\\sin x} {\\sqrt x + 1}' },
      widget: [],
      formula: katex.renderToString('\\int_{-\\infty}^{+\\infty} e^{-x^2} \\,\\mathrm{d}x = \\sqrt \\pi', { displayMode: true }),
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
