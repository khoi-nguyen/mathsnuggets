<template lang="pug">
.message.is-danger
  .message-body
    b-icon(pack="fas" icon="exclamation-triangle")
    slot
</template>

<script>
export default {
  name: 'ErrorMessage'
}
</script>
