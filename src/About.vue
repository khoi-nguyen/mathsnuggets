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
        h3.title.is-3 Khôi Nguyen
        h4.subtitle.is-5 Full Stack Developer
        p.content.
          Hello! My name is Khoi and I am the main developer on this project.
          My responsibility is to implement new features
          and ensure the software works well.
        p.content.
          I am a pure mathematician by education.
          I got my MMath from the
          #[a(href="https://cam.ac.uk") University of Cambridge] in 2012,
          followed by a PhD from
          #[a(href="https://imperial.ac.uk") Imperial College] in 2016.
          I started teaching shortly afterwards,
          and obtained by PGCE from the
          #[a(href="https://ox.ac.uk") University of Oxford] in 2020.
          I now work as a Teacher of Mathematics at the
          #[a(href="https://kingscollegeschools.org/madrid/school/") British School of Madrid].
        p.content.
          Outside of teaching, I enjoy playing piano and table tennis.
          I represented Oxford's first team in the 77#[sup th]
          Table Tennis Varsity match against Cambridge.
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
