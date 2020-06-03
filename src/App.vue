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

@import "../node_modules/bulma/bulma.sass";

.container {
  line-height: 1.5;
}
</style>
