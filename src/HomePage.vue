<template lang="pug">
div
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
</template>

<script>
import 'typeface-fira-sans'
import 'bulma/css/bulma.css'

export default {
  name: 'HomePage'
}
</script>

<style>
.navbar-brand .navbar-item {
  color: black;
  font-family: "Fira Sans";
  font-size: 1.5em;
}
</style>