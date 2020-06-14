<template lang="pug">
router-view(v-if="slides")
div(v-else="!slides")
  NavBar
  router-view
</template>

<script>
import { auth } from './auth.js'
import NavBar from './NavBar'
import 'typeface-fira-sans'

export default {
  name: 'App',
  props: {
    slides: Boolean
  },
  components: {
    NavBar
  },
  mounted () {
    auth.isLoggedIn()
  }
}
</script>

<style lang="scss">
@charset "utf-8";
$body-font-size: 1.2em;
$body-weight: 300;
$family-sans-serif: "Fira Sans", sans-serif;
$primary: #172838;
$weight-normal: 300;
$weight-medium: 300;
$weight-semibold: 400;
$weight-bold: 500;

@import "reveal.js/dist/reveal.css";
@import "~bulma/bulma.sass";
@import "~buefy/src/scss/buefy";

.title {
  font-weight: 400;
}
</style>
