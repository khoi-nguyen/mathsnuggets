<template lang="pug">
b-message(type="is-danger" has-icon icon-pack="fas" icon="exclamation-triangle" v-if="message")
  p {{ message }}
  b-button(type="is-danger" v-if="!showTraceback" @click="showTraceback = true") Show traceback
  pre(@click="showTraceback = false" v-if="showTraceback") {{ traceback }}
</template>

<script>
export default {
  name: 'ErrorMessage',
  props: {
    message: String,
    traceback: String
  },
  data () {
    return {
      showTraceback: false
    }
  }
}
</script>
