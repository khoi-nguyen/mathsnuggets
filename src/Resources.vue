<template lang="pug">
div
  NavBar
  section.hero.is-primary
    div.hero-body.has-text-centered
      div.container
        h1.title.is-2 Resources
  div.container
    div.panel
      p.panel-heading Lessons
        .panel-block
          p.control.has-icons-left
            input.input(type='text' placeholder='Search')
            span.icon.is-left
              i.fas.fa-search(aria-hidden='true')
        p.panel-tabs
          a All
          a Khoi
          a Tom
        .columns.panel-block(v-for="lesson in lessons")
          .column.is-narrow
            i.fa-4x.fas.fa-book
          .column
            h1.title {{ lesson.title }}
            dl
              dt Creator
              dd {{ lesson.creator }}
              dt Key Stage
              dd {{ lesson.keystage }}
              dt Subject
              dd {{ lesson.subject }}
              dt Date
              dd {{ lesson.date }}
</template>

<script>
import NavBar from './NavBar'

export default {
  components: { NavBar },
  data () {
    return {
      lessons: [
        {
          title: 'Linear Equations',
          creator: 'Tom',
          keystage: '3',
          subject: 'Algebra',
          date: '09/06/20'
        }
      ]
    }
  }
}
</script>

<style scoped>
dt {
  float: left;
  font-weight: 500;
}
dt::after {
  content: ":\00a0";
}
.panel {
  margin-top: 1em;
}
</style>
