<template lang="pug">
.container
  .columns
    .column.is-narrow
      img(src="assets/tuxie.svg" :width="width" v-if="image === 'tuxie'")
      img(src="assets/jigglypuff.svg" :width="width" v-if="image === 'jigglypuff'")
      img(src="assets/pikachu.svg" :width="width" v-if="image === 'pikachu'")
    .column
      .speech-bubble
        slot
</template>

<script>
export default {
  props: {
    image: { type: String, default: 'tuxie' },
    width: { type: Number, default: 400 }
  }
}
</script>

<style scoped>
.speech-bubble {
  position: relative;
  background: #d2e8e9;
  border-radius: .4em;
  padding: 1em;
}

.speech-bubble:after {
  content: '';
  position: absolute;
  left: 0;
  top: 35%;
  width: 0;
  height: 0;
  border: 20px solid transparent;
  border-right-color: #d2e8e9;
  border-left: 0;
  border-top: 0;
  margin-top: -10px;
  margin-left: -20px;
}
</style>
