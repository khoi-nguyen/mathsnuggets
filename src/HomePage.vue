<template lang="pug">
.container
  nav.navbar
    div.navbar-brand
      a.navbar-item mathsnuggets
    div.navbar-menu
      div.navbar-start
        a.navbar-item
          span.icon
            i.fas.fa-home
          span Home
        router-link(to="/slideshow_builder").navbar-item
          span.icon
            i.fas.fa-chalkboard-teacher
          span Lesson Builder
        div.navbar-item.has-dropdown.is-hoverable
          a.navbar-link
            span.icon
              i.fas.fa-tools
            span Utilities
          div.navbar-dropdown
            a.navbar-item Generator
            a.navbar-item Solver
            a.navbar-item Plotter
        a.navbar-item About us
      div.navbar-end
        div.navbar-item
          div.buttons
            a.button.is-primary
              strong Signup
            a.button.is-light Log in
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
  }
}
</script>

<style>
.navbar-brand .navbar-item {
  color: black;
  font-family: "Fira Sans";
  font-size: 1.5em;
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
