<template lang="pug">
div
  section.hero.is-primary
    .hero-body.has-text-centered
      .container
        .is-large
          i.fa-4x.fas.fa-chalkboard
        h1.title.is-2 Resources
  .container
    .panel
      p.panel-heading Lessons
      .panel-block
        p.control.has-icons-left
          input.input(type="text" placeholder="Search" v-model="searchString")
          span.icon.is-left
            i.fas.fa-search(aria-hidden='true')
      router-link(:to="parentFolder" v-if="parentFolder").panel-block
        .columns.is-vcentered
          .column.is-narrow.is-narrow.has-text-centered
            i.fa-4x.fas.fa-folder
          .column
            h3.title ..
      div(v-for="folder in folders")
        router-link.panel-block(:to="urlPrefix + folder + '/'")
          .columns.is-vcentered
            .column.is-narrow.is-narrow.has-text-centered
              i.fa-4x.fas.fa-folder
            .column
              h3.title {{ folder }}
      div(v-for="slideshow in slideshowsInFolder")
        a(:href="`/resources/${slideshow.url}`").panel-block
          .columns.is-vcentered
            .column.is-narrow.is-narrow.has-text-centered
              i.fa-4x.fas.fa-chalkboard-teacher
            .column
              h3.title {{ slideshow.url.split('/')[slideshow.url.split('/').length -1] }}
              ul.is-small(v-if="auth.loggedIn")
                li
                  b-icon(pack="fas" icon="location-arrow")
                  form-field(type="Field" :value="slideshow.url" @input="editSlideshow(slideshow, 'url', $event)" :editable="auth.loggedIn")
                li
                  form-field(type="Boolean" :value="slideshow.private" @input="editSlideshow(slideshow, 'private', $event)" label="Private")
                li
                  b-icon(pack="fas" icon="trash")
                  span.link(@click.prevent="openDeleteModal(slideshow)") Delete slideshow
      div.panel-block(v-if="auth.loggedIn")
        button.button.is-primary.is-outlined.is-fullwidth(@click="modal = true") Create slideshow
  b-modal(:active.sync="modal" has-modal-card)
    .modal-card
      header.modal-card-head
        h3.modal-card-title Create a slideshow
        button.delete(@click="modal = false")
      section.modal-card-body
        b-field(label="URL")
          b-input(v-model="newUrl")
      footer.modal-card-foot
        button.button.is-success(@click="createSlideshow") Create
        button.button(@click="modal = false") Cancel
  b-modal(:active.sync="deleteModal" has-modal-card)
    .modal-card
      header.modal-card-head
        h3.modal-card-title Delete
        button.delete(@click="deleteModal = false")
      section.modal-card-body Are you sure you want to delete the slideshow {{ selectedSlideshow.url }}?
      footer.modal-card-foot
        button.button.is-success(@click="deleteSlideshow()") Delete
        button.button(@click="deleteModal = false") Cancel
</template>

<script>
import _ from 'lodash'
import api from './ajax'
import { mapState } from 'vuex'

import FormField from './FormField'

export default {
  title: 'Teaching Resources',
  async mounted () {
    this.slideshows = await api('slideshows', 'GET')
  },
  computed: {
    filteredSlideshows () {
      return this.slideshows.filter((slideshow) => {
        if (slideshow.private && !this.auth.loggedIn) {
          return false
        }
        const url = this.$route.params.url
        if (url && !slideshow.url.startsWith(url)) {
          return false
        }
        if (this.searchString) {
          return slideshow.url.toLowerCase().indexOf(this.searchString.toLowerCase()) >= 0
        }
        return true
      })
    },
    slideshowsInFolder () {
      return this.filteredSlideshows.filter((slideshow) => {
        const relativeUrl = slideshow.url.replace(this.$route.params.url || '', '')
        const folder = relativeUrl.substring(0, relativeUrl.indexOf('/'))
        return !folder
      }).sort()
    },
    folders () {
      return _.reduce(this.filteredSlideshows, (result, slideshow) => {
        const url = this.$route.params.url || ''
        const relativeUrl = (slideshow.url || '').replace(url, '')
        if (relativeUrl.indexOf('/')) {
          const folder = relativeUrl.substring(0, relativeUrl.indexOf('/'))
          if (!result.includes(folder) && folder) {
            result.push(folder)
          }
        }
        return result
      }, []).sort()
    },
    parentFolder () {
      if (this.$route.params.url) {
        const url = this.$route.params.url
        const folder = url.substring(0, url.lastIndexOf('/', url.lastIndexOf('/') - 1))
        return folder ? '/resources/' + folder + '/' : '/resources/'
      }
      return false
    },
    urlPrefix () {
      if (this.$route.params.url) {
        return `/resources/${this.$route.params.url}`
      }
      return '/resources/'
    },
    ...mapState(['auth'])
  },
  watch: {
    '$route.params.url' () {
      this.searchString = ''
    }
  },
  methods: {
    createSlideshow () {
      api('slideshows/', 'POST', { url: this.newUrl })
      this.slideshows.push({ url: this.newUrl })
      this.modal = false
    },
    deleteSlideshow () {
      api('slideshows/' + this.selectedSlideshow.url, 'DELETE')
      this.slideshows.splice(this.slideshows.indexOf(this.selectedSlideshow), 1)
      this.deleteModal = false
    },
    async editSlideshow (slideshow, field, value) {
      await api('slideshows/' + slideshow.url, 'POST', { [field]: value })
      this.$set(slideshow, field, value)
    },
    openDeleteModal (slideshow) {
      this.selectedSlideshow = slideshow
      this.deleteModal = true
    }
  },
  data () {
    return {
      create: false,
      selectedSlideshow: {},
      deleteModal: false,
      modal: false,
      newUrl: '',
      searchString: '',
      slideshows: []
    }
  },
  components: {
    FormField
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
