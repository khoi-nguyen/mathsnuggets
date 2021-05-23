<template lang="pug">
div
  section.hero.is-primary
    div.hero-body.has-text-centered
      div.container
        div.is-large
          i.fa-4x.fas.fa-chalkboard
        h1.title.is-2 Resources
  div.container
    div.panel
      p.panel-heading Lessons
        .panel-block
          p.control.has-icons-left
            input.input(type="text" placeholder="Search" v-model="searchString")
            span.icon.is-left
              i.fas.fa-search(aria-hidden='true')
        p.panel-tabs
          router-link(to="/resources") All teachers
          router-link(:to="`/resources/${teacher}`" v-for="teacher in teachers") {{ teacher }}
        p.panel-tabs(v-if="$route.params.teacher")
          router-link(to="/resources") All year groups
          router-link(:to="`/resources/${$route.params.teacher}/` + group" v-for="group in yearGroups") {{ group }}
        div(v-for="(lesson, index) in filteredLessons" v-if="lesson['last_modified']")
          a(:href="`/resources/${lesson.teacher}/${lesson.year}/${lesson.slug}`").panel-block
            .columns.is-vcentered
              .column.is-narrow.is-narrow.has-text-centered
                i.fa-4x.fas.fa-chalkboard-teacher
                ul.is-small(v-if="authState.loggedIn")
                  li
                    b-icon(pack="fas" icon="edit")
                    span.link(@click.stop.prevent="openModal(index)") Edit metadata
                  li
                    b-icon(pack="fas" icon="trash")
                    span.link(@click.prevent="openDeleteModal(index)") Delete slideshow
              .column
                h3.title {{ lesson.title }}
                dl
                  div(v-for="field in fields" v-if="lesson[field.name]")
                    dt {{ field.label }}
                    dd {{ Array.isArray(lesson[field.name]) ? lesson[field.name].join(', ') : lesson[field.name] }}
      div.panel-block(v-if="authState.loggedIn")
        button.button.is-primary.is-outlined.is-fullwidth(@click="openModal(filteredLessons.length - 1, true)") Create slideshow
  b-modal(:active.sync="modal" has-modal-card)
    .modal-card
      header.modal-card-head
        h3.modal-card-title Edit
        button.delete(@click="modal = false")
      section.modal-card-body
        b-field(:label="field.label" v-for="field in fields" v-if="field.editable")
          b-input(:value="lesson[field.name]" ref="modalFields" :name="field.name")
      footer.modal-card-foot
        button.button.is-success(@click="editMetadata") Save
        button.button(@click="modal = false") Cancel
  b-modal(:active.sync="deleteModal" has-modal-card)
    .modal-card
      header.modal-card-head
        h3.modal-card-title Delete
        button.delete(@click="deleteModal = false")
      section.modal-card-body Are you sure you want to delete the slideshow {{ lesson.title }}?
      footer.modal-card-foot
        button.button.is-success(@click="deleteSlideshow(lessonIndex)") Delete
        button.button(@click="deleteModal = false") Cancel
</template>

<script>
import { auth } from './auth'
import api from './ajax'
import _ from 'lodash'

export default {
  title: 'Teaching Resources',
  async mounted () {
    const data = await api('slideshows', 'GET')
    this.lessons = data.concat([{ title: '' }])
  },
  computed: {
    filteredLessons () {
      const teacher = this.$route.params.teacher || false
      const year = this.$route.params.year || false
      return this.lessons.filter((lesson) => {
        if ((year && lesson.year !== year) || (teacher && lesson.teacher !== teacher)) {
          return false
        }
        if (this.searchString) {
          return lesson.title.toLowerCase().indexOf(this.searchString.toLowerCase()) >= 0
        }
        return true
      }).concat([{ title: '' }])
    },
    lesson () {
      return this.realIndex > -1 ? this.lessons[this.realIndex] : {}
    },
    realIndex () {
      return this.lessons.indexOf(this.filteredLessons[this.lessonIndex])
    },
    teachers () {
      return _.uniq(this.lessons.map((lesson) => lesson.teacher))
    },
    url () {
      let url = 'slideshows/'
      if (!this.create) {
        url += `${this.lesson.teacher}/${this.lesson.year}/${this.lesson.slug}`
      }
      return url
    },
    yearGroups () {
      if (this.$route.params.teacher) {
        return _.uniq(this.lessons.filter(l => l.teacher === this.$route.params.teacher).map(l => l.year))
      }
      return _.uniq(this.lessons.map((lesson) => lesson.year))
    }
  },
  methods: {
    openModal (index, create = false) {
      this.lessonIndex = index
      this.modal = true
      this.create = create
    },
    openDeleteModal (index) {
      this.deleteModal = true
      this.lessonIndex = index
    },
    deleteSlideshow (index) {
      this.lessonIndex = index
      api(this.url, 'DELETE')
      this.lessons.splice(this.realIndex, 1)
      this.deleteModal = false
    },
    async editMetadata () {
      const payload = {}
      _.forEach(this.$refs.modalFields, function (field) {
        payload[field.$attrs.name] = field.$el.children[0].value
      })
      const data = await api(this.url, 'POST', payload)
      this.$set(this.lessons, this.create ? this.lessons.length : this.realIndex, data)
      if (this.create) {
        this.$set(this.lessons, this.lessons.length, { title: '' })
      }
      this.modal = false
    }
  },
  data () {
    return {
      authState: auth.state,
      create: false,
      deleteModal: false,
      searchString: '',
      slug: '',
      teacher: '',
      year: '',
      lessonIndex: 0,
      fields: [
        {
          name: 'title',
          label: 'Title',
          editable: true
        },
        {
          name: 'year',
          label: 'Year Group',
          editable: true
        },
        {
          name: 'teacher',
          label: 'Teacher',
          editable: true
        },
        {
          name: 'date',
          label: 'Date',
          editable: false
        }
      ],
      lessons: [{ title: '' }],
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
