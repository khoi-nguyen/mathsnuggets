<template lang="pug">
div.container
  ResourceComponent(:type.sync="type" :fields.sync="fields" :hide-widget-menu="true")
</template>

<script>
import ResourceComponent from './ResourceComponent'

export default {
  components: {
    ResourceComponent
  },
  data () {
    return {
      fields: [],
      type: 'Plot'
    }
  }
}
</script>
