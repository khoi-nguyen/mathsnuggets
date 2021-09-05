<template lang="pug">
.container
  widget-settings
    config-option(name="Icon")
      form-field(:editable="true" v-model="payload.icon" type="Field")
  article.message(:class="`is-${payload.style || 'primary'}`")
    h3.message-header(slot="trigger")
      .columns
        .column.is-narrow(v-if="payload.icon")
          b-icon(pack="fas" :icon="payload.icon" :key="payload.icon")
        .column
          form-field(:editable="config.edit" v-model="payload.title" type="Markdown")
    .message-body
      slot
</template>

<script>
import { mapState } from 'vuex'
import ConfigOption from './ConfigOption'
import FormField from './FormField'
import WidgetSettings from './WidgetSettings'

export default {
  props: { payload: { type: Object, default: () => {} } },
  computed: mapState(['config']),
  components: {
    ConfigOption,
    FormField,
    WidgetSettings
  }
}
</script>
