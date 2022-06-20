<template>
  <div class="terminal">
    <div class="terminal-code">
      <div class="terminal-lines terminal-text">
      <span v-for="lineNo in numberOfLines"
            :key="lineNo"
            class="hov-highlight terminal-text">
        {{ lineNo }}
      </span>
      </div>
      <div class="terminal-view">
        <span v-for="(token, index) in context.tokens"
              :key="index"
              class="hov-highlight terminal-text"
              :style="getTokenStyle(token)">
          {{ token.content }}
        </span>
      </div>
      <textarea ref="input"
                v-model="context.code"
                spellcheck="false"
                class="terminal-text"
                :style="getTextAreaStyle()"
                @keydown="onKeyDown"></textarea>
    </div>
  </div>
</template>

<script>
export default {
  name: "Terminal",
  props: ['context'],
  mounted() {
    this.sendUpdate()
  },
  watch: {
    code() {
      this.sendUpdate()
    },
    tokenizer() {
      this.sendUpdate()
    }
  },
  computed: {
    code() {
      return this.context.code
    },
    tokenizer() {
      return this.context.tokenizer
    },
    numberOfLines() {
      return this.code.split(/\r\n|\r|\n/).length
    }
  },
  methods: {
    getTokenStyle(token) {
      if ('types' in this.context.styles) {
        return this.context.styles.types[token.type] ?? this.context.styles.default
      } else {
        return this.context.styles.default
      }
    },
    insertText(event, textToInsert) {
      this.$refs.input.setRangeText(textToInsert, this.$refs.input.selectionStart, this.$refs.input.selectionEnd, 'end')
      this.context.code = this.$refs.input.value
    },
    onKeyDown(event) {
      if (event.key === "Tab") {
        this.insertText(event, '  ')
        event.preventDefault()
      }
    },
    sendUpdate() {
      this.$emit('update', this.context.code)
    },
    getTextAreaStyle() {
      if (this.tokenizer) {
        return {'color': 'transparent'}
      } else {
        return {'color': 'white'}
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/themes.scss';
@import '../assets/mixins.scss';

.terminal-text {
  white-space: pre !important;
  font-family: monospace !important;
  font-size: 1.2rem !important;
  font-weight: normal !important;
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1.4rem !important;
  border: none !important;
}

.terminal {
  flex-grow: 1;
  @include row($items: stretch);
  overflow-y: scroll;
  overflow-x: hidden;


  .terminal-code {
    @include row($items: stretch);

    .terminal-lines {
      @include col();
      text-align: right;
      translate: -150% 0;
    }

    padding-left: 2rem;
    flex-grow: 1;
    position: relative;

    .terminal-view {
      @include theme-dark();
      background-color: transparent;
      position: absolute;
      width: 100%;
      height: 100%;
      border: none;
      margin: 0;
      padding: 0;

      span {
        background-color: transparent;
      }
    }

    textarea {
      overflow: scroll;
      @include theme-dark();
      background-color: transparent;
      caret-color: white;
      position: absolute;
      width: 100%;
      height: 100%;
      border: none;
      outline: none;
      margin: 0;
      padding: 0;
      resize: none;
    }
  }
}

</style>