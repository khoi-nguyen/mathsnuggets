<template lang="pug">
b-message(type="is-danger" has-icon icon-pack="fas" icon="exclamation-triangle")
  slot
</template>

<script>
export default {
  name: 'ErrorMessage'
}
</script>
