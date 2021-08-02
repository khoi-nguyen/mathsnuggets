<template lang="pug">
.container
  widget-settings
    config-option(name="Image")
      form-field(v-model="payload.image" :options="images" type="Select")
    config-option(name="Width")
      form-field(v-model="payload.width" type="Expression")
    config-option(name="Bubble position")
      form-field(v-model="payload.position" :options="['left', 'right']" type="Select")
  .columns
    .column(v-if="payload.position === 'left'")
      .speech-bubble-left
        slot
    .column.is-narrow
      img(:src="`/static/${payload.image}.svg`" :width="payload.width" v-if="payload.image")
    .column(v-if="payload.position === 'right'")
      .speech-bubble-right
        slot
</template>

<script>
import ConfigOption from './ConfigOption'
import FormField from './FormField'
import WidgetSettings from './WidgetSettings'

export default {
  props: { payload: { type: Object, default: () => {} } },
  data () {
    return {
      images: ['tuxie', 'jigglypuff', 'pikachu']
    }
  },
  components: {
    ConfigOption,
    FormField,
    WidgetSettings
  }
}
</script>

<style scoped>
.speech-bubble-right, .speech-bubble-left {
  position: relative;
  background: #d2e8e9;
  border-radius: .4em;
  padding: 1em;
}

.speech-bubble-right:after {
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

.speech-bubble-left:after {
  content: '';
  position: absolute;
  right: 0;
  top: 35%;
  width: 0;
  height: 0;
  border: 20px solid transparent;
  border-left-color: #d2e8e9;
  border-right: 0;
  border-top: 0;
  margin-top: -10px;
  margin-right: -20px;
}
</style>
