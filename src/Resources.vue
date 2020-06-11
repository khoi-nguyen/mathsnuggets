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
        div(v-for="lesson in lessons")
          a(:href="`/resources/${lesson.id}`").panel-block
            .columns.is-vcentered
              .column.is-narrow
                i.fa-4x.fas.fa-chalkboard-teacher
              .column
                h1.title {{ lesson.title }}
                dl
                  div(v-for="field in fields" v-if="lesson[field[0]]")
                    dt {{ field[1] }}
                    dd {{ Array.isArray(lesson[field[0]]) ? lesson[field[0]].join(', ') : lesson[field[0]] }}
</template>

<script>
import NavBar from './NavBar'
import { getSlideshowList } from './ajax'

export default {
  components: { NavBar },
  mounted () {
    getSlideshowList(function (data) {
      this.lessons = data
    }.bind(this))
  },
  data () {
    return {
      fields: [['authors', 'Authors'], ['date', 'Date']],
      lessons: []
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
