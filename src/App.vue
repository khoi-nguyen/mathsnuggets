<template lang="pug">
router-view
</template>

<script>
import 'typeface-fira-sans'

export default {
  name: 'App'
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

@import "~reveal.js/css/reveal.scss";
@import "../node_modules/bulma/bulma.sass";

html, body {
  overflow: auto;
  overflow-x: hidden;
}
.title {
  font-weight: 400;
}
</style>
