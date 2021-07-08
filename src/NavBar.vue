<template lang="pug">
b-navbar.container
  template(slot="brand")
    b-navbar-item(tag="a" href="/")
      b-icon(pack="fas" icon="square-root-alt" type="is-info")
      span mathsnuggets
  template(slot="start")
    b-navbar-item(v-bind="link.attrs" v-for="link in links")
      b-icon(v-bind="link.icon" type="is-info")
      span  {{ link.text }}
  template(slot="end")
    b-navbar-item(tag="div").buttons
      b-button(tag="router-link" to="/login" type="is-link" v-if="!loggedIn") Login
      b-button(@click="logout" v-else type="logout") Logout
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  methods: mapActions('auth', ['logout']),
  computed: mapState('auth', ['loggedIn']),
  data () {
    return {
      links: [
        {
          icon: { pack: 'fas', icon: 'home' },
          attrs: { tag: 'a', href: '/' },
          text: 'Home'
        },
        {
          icon: { pack: 'fas', icon: 'chalkboard-teacher' },
          attrs: { tag: 'router-link', to: '/resources' },
          text: 'Resources'
        },
        {
          icon: { pack: 'fas', icon: 'info-circle' },
          attrs: { tag: 'router-link', to: '/about' },
          text: 'About'
        }
      ]
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
