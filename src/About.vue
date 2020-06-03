<template lang="pug">
.container
  NavBar
  .has-text-centered
    div.is-large
      i.fa-5x.fas.fa-info
    h1.title.is-1 About Us
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
</style>
