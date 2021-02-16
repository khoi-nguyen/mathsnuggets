<template lang="pug">
div
  section.hero.is-primary
    div.hero-body.has-text-centered
      div.container
        div.is-large
          i.fa-4x.fas.fa-info
        h1.title.is-2 About
  .container
    .columns
      .column
        .card-content.content
          h2.title.is-1 About Mr Nuggets
          p.is-size-4.
            My name is Khoi Nguyen
            (my pupils call me Mr Nuggets because they can't pronounce my name)
            and I teach Mathematics at #[a(href="https://kingscollegeschools.org/madrid/schhool/") King's College] in Madrid.
          p.content.
            I am a pure mathematician by education.
            I got my MMath (Part III) from the
            #[a(href="https://cam.ac.uk") University of Cambridge] in 2012,
            followed by a PhD from
            #[a(href="https://imperial.ac.uk") Imperial College] in 2016.
            I started teaching shortly afterwards,
            and obtained by PGCE from the
            #[a(href="https://ox.ac.uk") University of Oxford] in 2020.
          p.content.
            Outside of teaching, I enjoy playing piano and table tennis.
            I represented Oxford's first team in the 77#[sup th]
            Table Tennis Varsity match against Cambridge.
      .column
        .card-content.content
          h2.title.is-1 About MathsNuggets
          p.is-size-4.
            The aim is to automate the teacher's job as much as possible
            in order to create highly interactive teaching resources.
            The key functionalities are the following.
          ul
            li.
              #[strong Automatic marking.]
              Assess and follow your pupils' progress in real time during the lesson,
              even if they are at home.
            li.
              #[strong Automatic solving.]
              Ensure your solutions are always correct.
            li.
              #[strong Exercise generator.]
              Let the computer create your exercise
              and ensure that the solutions are appropriate.
</template>

<script>
export default {
  title: 'About us',
  name: 'About'
}
</script>
