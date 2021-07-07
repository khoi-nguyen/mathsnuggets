<template lang="pug">
.container.avoid-column
  widget-settings(v-if="config.edit")
    config-option(name="Icon")
      form-field(:editable="true" v-model="payload.icon" type="Field")
  b-collapse.message.is-medium(:class="`is-${payload.style || 'primary'}`" :open="!payload.collapsed")
    h3.message-header(slot="trigger")
      .columns
        .column.is-narrow(v-if="payload.icon")
          b-icon(pack="fas" :icon="payload.icon" :key="payload.icon")
        .column
          form-field(:editable="config.edit" v-model="payload.title" type="Markdown")
    article
      .message-body
        slot
</template>

<script>
import ConfigOption from './ConfigOption'
import FormField from './FormField'
import WidgetSettings from './WidgetSettings'

export default {
  props: { config: Object, payload: { type: Object, default: () => {} } },
  components: {
    ConfigOption,
    FormField,
    WidgetSettings
  }
}
</script>
