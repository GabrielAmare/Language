<template>
  <div class="ide">
    <div class="ide-header">
      <select v-model="context.lang"
              @change="reload">
        <option v-for="(lang, index) in langs"
                :key="index">
          {{ lang }}
        </option>
      </select>
      <button @click="showTokens = !showTokens">
        Show Tokens ?
      </button>
    </div>
    <div class="ide-body">
      <Loader v-if="reloadLang"/>
      <Terminal ref="terminal"
                :context="context"
                @update="updateTokens"/>
      <TokenList v-if="showTokens"
                 :context="context"
                 @select="selectToken"/>
    </div>
  </div>
</template>

<script>
import makeTokenizer from "../assets/js/make_tokenizer.js";
import TokenList from "./TokenList.vue";
import Terminal from "./Terminal.vue";
import Loader from "./Loader.vue";

export default {
  name: "Ide",
  components: {Loader, TokenList, Terminal},
  props: [],
  data() {
    return {
      langs: [],
      showTokens: false,
      reloadLang: false,
      context: {
        lang: null,
        tokenizer: null,
        styles: {},
        code: "// Showcase the syntax highlighter.\n" +
          "\n" +
          "table Example {\n" +
          "  !required[int]\n" +
          "  *multiple[str]\n" +
          "}\n" +
          "\n" +
          "/*\n" +
          "  have some troubles with the syntax ??\n" +
          "*/\n" +
          "\n" +
          "table User {\n" +
          "  !id[int]=auto\n" +
          "  !username[str]\n" +
          "  !password[str]\n" +
          "  *friends[User]\n" +
          "  *role[str]=\"MEMBER\"\n" +
          "}\n",
        tokens: []
      }
    }
  },
  computed: {
    lang() {
      return this.context.lang
    }
  },
  watch: {
    lang() {
      this.$route.query.lang = this.lang
    }
  },
  async mounted() {
    this.langs = (await import('../assets/langs/langs.json')).default
    if (this.context.lang === null) {
      this.context.lang = this.$route.query?.lang ?? this.langs[0]
    }
    await this.reload()
  },
  methods: {
    async reload() {
      this.reloadLang = true

      try {
        this.context.tokenizer = makeTokenizer((await import(`../assets/langs/${this.context.lang}/data.json`)).default)
      } catch (e) {
        console.log(`undefined tokenizer for '${this.context.lang}'.`)
        this.context.tokenizer = null
      }

      try {
        this.context.styles = (await import(`../assets/langs/${this.context.lang}/styles.json`)).default
      } catch (e) {
        console.log(`undefined tokenizer for '${this.context.lang}'.`)
        this.context.styles = {default: {}}
      }
      this.reloadLang = false
    },
    selectToken(token) {
      this.$refs.input.setSelectionRange(token.at, token.to, "forward")
      this.$refs.input.focus()
    },
    updateTokens(code) {
      if (this.context.tokenizer) {
        this.context.tokens = this.context.tokenizer(code)
      } else {
        this.context.tokens = []
      }
    },
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/themes.scss';
@import '../assets/mixins.scss';

.ide {
  width: 100%;
  height: 100%;
  @include col($content: start, $items: stretch);

  .ide-header {
    width: 100%;
    @include row($content: start, $items: stretch);

    button, select {
      padding: 0.375rem 0.5rem;
      margin-left: 0.75rem;
      margin-right: 0.75rem;
    }
  }

  .ide-body {
    @include row($content: start, $items: stretch);
    position: relative;
    overflow: hidden;
    padding: 0.5rem;
    flex-grow: 1;
    max-width: 2000px;
    max-height: 1333px;
    border: 1px solid gray;

    background-image: url('../assets/img/terminal-background.jpg');
    background-position: 0 0;
    background-clip: border-box;
    background-repeat: no-repeat;
    background-size: cover;
  }
}

</style>