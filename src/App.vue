<template lang="pug">
router-view(v-if="slideshowEditor")
div(v-else-if="!slideshowEditor")
  NavBar
  router-view
</template>

<script>
import { auth } from './auth.js'
import NavBar from './NavBar'
import 'typeface-fira-sans'

export default {
  name: 'App',
  components: {
    NavBar
  },
  computed: {
    slideshowEditor () {
      if (this.$route.path.startsWith('/resources/') || this.$route.path === '/slideshow_builder') {
        return true
      }
      return false
    }
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
@import "../node_modules/bulma/bulma.sass";

.title {
  font-weight: 400;
}
.tooltip {
  z-index: 100000;

  .tooltip-inner {
    background: $primary;
    border-radius: 16px;
    color: white;
    font-size: 0.8rem;
    padding: 5px 10px;
  }
}
</style>
