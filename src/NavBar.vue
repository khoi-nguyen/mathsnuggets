<template lang="pug">
nav.navbar.container
  div.navbar-brand
    a.navbar-item
      span.icon.has-text-info
        i.fas.fa-square-root-alt
      span mathsnuggets
  div.navbar-menu
    div.navbar-start
      router-link(to="/").navbar-item
        span.icon.has-text-info
          i.fas.fa-home
        span Home
      a(href="/slideshow_builder").navbar-item
        span.icon.has-text-info
          i.fas.fa-chalkboard-teacher
        span Lesson Builder
      div.navbar-item.has-dropdown.is-hoverable
        a.navbar-link
          span.icon.has-text-info
            i.fas.fa-tools
          span Utilities
        div.navbar-dropdown
          a.navbar-item Generator
          a.navbar-item Solver
          a.navbar-item Plotter
      router-link(to="/about").navbar-item
          span.icon.has-text-info
            i.fas.fa-info
          span About us
    div.navbar-end
      div.navbar-item
        div.buttons
          a.button.is-primary
            strong Signup
          a.button.is-light Log in
</template>

<script>
export default {
}
</script>

<style scoped>
.navbar-brand .navbar-item {
  font-weight: 400;
  font-size: 1.3em;
}
span.icon {
  margin-right: 0.25em;
}
</style>
