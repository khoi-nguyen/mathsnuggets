<template lang="pug">
  .tray.buttons.are-medium
    b-button(@click="graphing = true" type="is-link")
      b-icon(pack="fas" icon="chart-line")
    b-button(@click="config.whiteboardMode = !config.whiteboardMode" type="is-success")
      b-icon(pack="fas" icon="chalkboard")
    b-button(@click="config.graphPaper = !config.graphPaper" type="is-danger")
      b-icon(pack="fas" icon="th")
    b-button(type="is-warning" @click="config.columns = !config.columns")
      b-icon(pack="fas" icon="columns")
    b-button(@click="geometry = true")
      b-icon(pack="fas" icon="drafting-compass")
    b-button(@click="config.edit = !config.edit" v-if="config.authState.loggedIn")
      b-icon(pack="fas" icon="edit")
    b-button(@click="solverModal = true" type="is-link")
      b-icon(pack="fab" icon="python")
    b-dropdown(position="is-top-right" :mobile-modal="false")
      b-button(slot="trigger" type="is-info")
        b-icon(pack="fas" icon="calculator")
      iframe(src="https://www.desmos.com/testing/virginia/scientific" width="600" height="600")
    b-dropdown(position="is-top-right" :mobile-modal="false" @active-change="openChat" :close-on-click="false")
      b-button(:type="chatButtonType" slot="trigger")
        b-icon(pack="fas" icon="comment")
      .chat
        b-dropdown-item(v-for="(message, index) in chat" @click="deleteChatMessage(index)")
          h5 {{ message.nickname }}
          form-field(type="Markdown" :value="message.message" :editable="false")
      b-input(v-model="chatMessage" @keydown.enter.native="sendMessage")
    span &nbsp;&nbsp;
    form-field(:value="nickname" type="Field" @input="updateNickname" label="Enter your name here")
    b-modal(:active.sync="graphing" full-screen has-modal-card :destroy-on-hide="false")
      .modal-card
        header.modal-card-head Graphing calculator
        .modal-card-body
          iframe(src="https://www.geogebra.org/graphing" width="100%" height="100%")
    b-modal(:active.sync="geometry" full-screen has-modal-card :destroy-on-hide="false")
      .modal-card
        header.modal-card-head Geometry
        .modal-card-body
          iframe(src="https://www.geogebra.org/geometry" width="100%" height="100%")
    b-modal(:active.sync="solverModal" has-modal-card :destroy-on-hide="false")
      .modal-card
        header.modal-card-head
          p.modal-card-title Solver
          button.delete(type="button" @click="solverModal = false")
        .modal-card-body
          widget-select(@select:widget="changeWidget")
          widget(:type="widget" :generator="true" :config="{edit: true}" :state="{}" :payload="widgetPayload" if="widget")
    .clipboard
      draggable(v-model="clipboard" group="widgets")
        node(v-bind="image" v-for="(image, i) in clipboard" component="widget" :config="config")
</template>

<script>
import _ from 'lodash'
import draggable from 'vuedraggable'

import api from './ajax'
import FormField from './FormField'
import Widget from './Widget'
import WidgetSelect from './WidgetSelect'

export default {
  props: {
    config: Object
  },
  data () {
    return {
      chat: [],
      clipboard: [],
      displayChat: false,
      geometry: false,
      graphing: false,
      nickname: '',
      newMessages: false,
      solverModal: false,
      widgetPayload: {},
      widget: ''
    }
  },
  computed: {
    apiUrl () {
      const params = this.$route.params
      return params.slug ? `slideshows/${params.teacher}/${params.year}/${params.slug}` : false
    },
    chatButtonType () {
      return this.newMessages ? 'is-danger' : 'is-success'
    }
  },
  created () {
    window.addEventListener('paste', this.onPaste.bind(this))
  },
  destroyed () {
    window.removeEventListener('paste', this.onPaste.bind(this))
  },
  async mounted () {
    const identity = await api('auth/nickname')
    this.nickname = identity.nickname || ''
  },
  methods: {
    changeWidget (widget) {
      this.widgetPayload = {}
      this.widget = widget
    },
    deleteChatMessage (index) {
      if (this.config.authState.loggedIn) {
        api('chat/delete', 'POST', this.chat[index])
      }
    },
    onPaste (event) {
      const items = (event.clipboardData || event.originalEvent.clipboardData).items

      for (const index in items) {
        const item = items[index]
        if (item.kind === 'file') {
          const blob = item.getAsFile()
          const reader = new FileReader()
          reader.onload = function (e) {
            this.clipboard.push({
              component: 'widget',
              type: 'Image',
              payload: {
                src: e.target.result
              }
            })
          }.bind(this)
          reader.readAsDataURL(blob)
        }
      }
    },
    openChat (event) {
      this.displayChat = event
      if (event) {
        this.newMessages = false
      }
    },
    sendMessage () {
      if (this.chatMessage !== '') {
        api('chat', 'POST', { message: this.chatMessage, url: this.apiUrl })
        this.chatMessage = ''
      }
    },
    updateNickname (nickname) {
      this.nickname = nickname
      api('auth/nickname', 'POST', { nickname })
    }
  },
  sockets: {
    deleteMessage (data) {
      for (var i = 0; i < this.chat.length; i++) {
        if (_.isEqual(this.chat[i], data)) {
          this.chat.splice(i, 1)
        }
      }
    },
    messageReceived (data) {
      if (!_.isEqual(this.chat[this.chat.length - 1], data) && data.url === this.apiUrl) {
        this.$set(this.chat, this.chat.length, data)
        if (!this.displayChat) {
          this.newMessages = true
        }
      }
    }
  },
  components: {
    draggable,
    FormField,
    Widget,
    WidgetSelect
  }
}
</script>

<style scoped>
.chat {
  max-height: 400px;
  overflow-y: auto;
}
.clipboard {
  position: absolute;
  opacity: 1;
  z-index: 10000;
  bottom: 0;
  right: 0;
}
.tray {
  position: absolute;
  opacity: 1;
  z-index: 2;
  bottom: 25px;
  left: 20px;
}
</style>