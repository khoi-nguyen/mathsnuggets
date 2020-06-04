<template lang="pug">
div
  NavBar
  section.hero.is-primary
    div.hero-body.has-text-centered
      div.container
        div.is-large
          i.fa-4x.fas.fa-info
        h1.title.is-2 About us
        p.content.is-4.
          Hello to you, reader! We are two Teachers of Mathematics seeking to facilitate teaching and learning
          mathematics. Having met at the #[a(href="https://ox.ac.uk") University of Oxford] and enjoyed a short-lived
          PGCE course together, we decided to create this website to facilitate the creation of teaching resources.
  .container
    .columns
      .column.has-text-centered
        h3.title.is-3 Khoi Nguyen
      .column.has-text-centered
        h3.title.is-3 Tom Chambaud
        h4.subtitle.is-5 Apprentice Developer
        p.content.
          As you may have guessed, I am part French (half to be precise) and, as of September
          2020, a Teacher of Mathematics at Sandwell Academy. In 2019, I graduated from #[a(href="https://keele.ac.uk") Keele University]
          with a First-Class honours degree in Mathematics and obtained my PGCE qualification from the
          #[a(href="https://ox.ac.uk") University of Oxford] the following year.
        p.content.
          I am passionate about helping young people and enjoying life outside of teaching. My hobbies include
          competitive badminton, cooking great food and playing piano!
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
