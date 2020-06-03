<template lang="pug">
div
  NavBar
  section.hero.is-primary
    div.hero-body.has-text-centered
      div.container
        div.is-large
          i.fa-4x.fas.fa-info
        h1.title.is-2 About us
  .container
    .columns
      .column.has-text-centered
        h3.title.is-3 Khoi Nguyen
      .column.has-text-centered
        h3.title.is-3 Tom Chambaud
</template>

<script>
import NavBar from './NavBar'

export default {
  components: { NavBar },
  name: 'About'
}
</script>

<style scoped>
section.hero {
  margin-bottom: 1em;
}
</style>
