<template lang="pug">
div
  div.hero.is-primary
    .reveal.hero-body
      .slides
        section
          h1.title.is-1 Welcome to MathsNuggets
          div.is-size-2.content.katex(v-html="formula")
          p.content Press the right arrow key to see our main features.
        section
          h1.title.is-1 Easily edit formulas
          p.content.is-size-2
            form-field(v-bind.sync="field")
          p.content.
            Try it out by clicking the formula above.
        section
          h1.title.is-1 Automatic Solving
          div.content.is-gapless
            widget(type="Equation" :payload="widget" :toolbar="false")
          ul.content
            li Click the equation to change it
            li Click the 'Solution' button to see the solution
  .container
    .columns(v-for="row in features")
      .column(v-for="feature in row").feature.has-text-centered
        div.is-large
          i.fa-4x(:class="feature.icon")
        h3.title(:class="row.length === 1 ? 'is-1' : 'is-3'") {{ feature.title }}
        .content(:class="row.length === 1 ? 'is-size-3' : 'is-size-5'") {{ feature.text }}
</template>

<script>
import FormField from './FormField'
import Widget from './Widget'
import katex from 'katex'
import 'katex/dist/katex.min.css'
import Reveal from 'reveal.js'

export default {
  name: 'HomePage',
  title: 'Home',
  components: {
    FormField,
    Widget
  },
  mounted () {
    Reveal.initialize({
      embedded: true,
      height: '100%'
    })
  },
  data () {
    return {
      field: { label: 'Equation', displayMode: true, type: 'Expression', value: '(sin x)/(sqrt(x) + 1)', latex: '\\frac {\\sin x} {\\sqrt x + 1}' },
      widget: { equation: 'x^2 - 5x + 6', solution: '[Eq(x, 2), Eq(x, 3)]' },
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
            title: 'Automatic solving',
            text: 'Solutions are always correct and computed for you.'
          },
          {
            icon: 'fas fa-cogs',
            title: 'Exercise generator',
            text: 'Exercises can be generated for you, with fine-grained control over the difficulty.'
          },
          {
            icon: 'fas fa-users',
            title: 'User-friendly',
            text: 'The interface is intuitive and works out of the box on every device.'
          }
        ],
        [
          {
            icon: 'fas fa-photo-video',
            title: 'Dynamic',
            text: 'Draw on the slides or embed videos. The possibilities are endless.'
          },
          {
            icon: 'fas fa-puzzle-piece',
            title: 'Easily extensible',
            text: 'If you can program, make sure it fits your needs'
          },
          {
            icon: 'fas fa-handshake',
            title: 'Free',
            text: 'As in \'free coffee\' and \'free speech\'.'
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
