<template lang="pug">
div
  nav.navbar
    div.navbar-brand
      section.hero
        div.hero-body
          div.container
            h1.title.has-text-black-bis MathsNuggets
    div.navbar-menu
      div.navbar-start
        a.navbar-item
          i.fas.fa-home
          span Home
        a.navbar-item
          i.fas.fa-chalkboard-teacher
          span Lesson Builder
        div.navbar-item.has-dropdown.is-hoverable
          a.navbar-link
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
  section.hero.is-primary
    div.hero-body
      div.container
        h1.title.has-text-black-bis Welcome to MathsNuggets!
        h2.subtitle.has-text-grey-darker.
          An ingenious website designed to facilitate teaching and learning maths.

    .card
  .card-image
  .card-content
    .media
      .media-left
      .media-content
        span.card-header-icon.is-large.is-left
          i.fas.fa-chalkboard-teacher.fa-3x
        p.card-header-title.is-4 Lesson Builder
    .content
      | Construct and save your own
      br
      | slideshow lessons using:
      br
      | Generator, Solver and Plotter
      br
      | and all other basic slideshow
      br
      | creating tools.
</template>

<script>
import SlideshowBuilder from './SlideshowBuilder'
import 'bulma/css/bulma.css'

export default {
  name: 'HomePage',
  components: {
    SlideshowBuilder
  }
}
</script>
