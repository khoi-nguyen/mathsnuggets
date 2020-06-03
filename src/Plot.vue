<template lang="pug">
div
  NavBar
  div.container
    ResourceComponent(:type.sync="type" :fields.sync="fields" :hide-widget-menu="true")
</template>

<script>
import NavBar from './NavBar'
import ResourceComponent from './ResourceComponent'

export default {
  components: {
    ResourceComponent,
    NavBar
  },
  data () {
    return {
      fields: [],
      type: 'Plot'
    }
  }
}
</script>
