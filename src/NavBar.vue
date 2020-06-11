<template lang="pug">
nav.navbar.container
  div.navbar-brand
    a(href="/").navbar-item
      span.icon.has-text-info
        i.fas.fa-square-root-alt
      span mathsnuggets
    a(
      @click="forceShowMenu = !forceShowMenu"
    ).navbar-burger.burger
      span(aria-hidden="true")
      span(aria-hidden="true")
      span(aria-hidden="true")
  div(
    :class="{'is-active': forceShowMenu}"
  )#navbarBasic.navbar-menu
    div.navbar-start
      a(href="/").navbar-item
        span.icon.has-text-info
          i.fas.fa-home
        span Home
      router-link(to="/resources").navbar-item
        span.icon.has-text-info
          i.fas.fa-chalkboard-teacher
        span Lesson Builder
      div.navbar-item.has-dropdown.is-hoverable
        a.navbar-link
          span.icon.has-text-info
            i.fas.fa-tools
          span Utilities
        div.navbar-dropdown
          a.navbar-item Generator
          a.navbar-item Solver
          router-link(to="/plot").navbar-item Plotter
      router-link(to="/about").navbar-item
          span.icon.has-text-info
            i.fas.fa-info-circle
          span About us
    div.navbar-end
      div.navbar-item
        div.buttons
          router-link(to="/login" v-if="!authState.loggedIn").button.is-primary Login
          span(@click="logout" v-if="authState.loggedIn").button.is-light Logout
</template>

<script>
import { auth } from './auth.js'

export default {
  methods: {
    logout () {
      auth.logout()
    }
  },
  data () {
    return {
      authState: auth.state,
      forceShowMenu: false
    }
  }
}
</script>

<style scoped>
.navbar-brand .navbar-item {
  font-weight: 400;
  font-size: 1.3em;
}
span.icon {
  margin-right: 0.25em;
}
</style>
