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
        div(v-for="(lesson, index) in lessons")
          a(:href="`/resources/${lesson.id}`").panel-block
            .columns.is-vcentered
              .column.is-narrow
                i.fa-4x.fas.fa-chalkboard-teacher
              .column
                h3.title {{ lesson.title }}
                dl
                  div(v-for="field in fields" v-if="lesson[field.name]")
                    dt {{ field.label }}
                    dd {{ Array.isArray(lesson[field.name]) ? lesson[field.name].join(', ') : lesson[field.name] }}
              .column.is-narrow(@click.stop.prevent="openModal(index)")
                i.fa-2x.fas.fa-edit
  .modal(:class="{'is-active': modal}")
    .modal-background
    .modal-card
      header.modal-card-head
        h3.modal-card-title Edit
        button.delete(@click="modal = false")
      section.modal-card-body
        .field(v-for="field in fields" v-if="field.editable")
          label.label {{ field.label }}
          input.input(:value="lessons[lessonIndex][field.name]" ref="modalFields" :name="field.name")
      footer.modal-card-foot
        button.button.is-success(@click="editMetadata") Save
        button.button(@click="modal = false") Cancel
</template>

<script>
import NavBar from './NavBar'
import { saveSlideshow, getSlideshowList } from './ajax'
import _ from 'lodash'

export default {
  components: { NavBar },
  mounted () {
    getSlideshowList(function (data) {
      this.lessons = data
    }.bind(this))
  },
  methods: {
    openModal (index) {
      this.lessonIndex = index
      this.modal = true
    },
    editMetadata () {
      const payload = {}
      _.forEach(this.$refs.modalFields, function (field) {
        payload[field.name] = field.value
      })
      saveSlideshow(this.lessons[this.lessonIndex].id, payload, function (data) {
        this.lessons[this.lessonIndex] = data
        this.modal = false
      }.bind(this))
    }
  },
  data () {
    return {
      lessonIndex: 0,
      fields: [
        {
          name: 'title',
          label: 'Title',
          editable: true
        },
        {
          name: 'authors',
          label: 'Authors',
          editable: true
        },
        {
          name: 'date',
          label: 'Date',
          editable: false
        }
      ],
      lessons: [],
      modal: false
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
