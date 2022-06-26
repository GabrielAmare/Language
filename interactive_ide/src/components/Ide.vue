<template>
  <div class="ide">
    <div class="ide-header">
      <div class="button-group">
        <!-- REPO SELECTOR -->
        <label>{{ $t('folder') }}</label>
        <select v-model="repo.name"
                @change="loadRepo">
          <option v-for="(repo, index) in repos"
                  :key="index"
                  :value="repo">
            {{ repo }}
          </option>
        </select>

        <!-- FILE SELECTOR -->
        <label>{{ $t('file') }}</label>
        <select v-model="file.name"
                @change="loadFile">
          <option v-for="(filename, index) in repo.files"
                  :key="index"
                  :value="filename">
            {{ filename }}
          </option>
        </select>

        <!-- LANG SELECTOR -->
        <label>{{ $t('lang') }}</label>
        <select v-model="file.lang"
                @change="loadLang">
          <option v-for="(lang, index) in langs"
                  :key="index"
                  :value="lang">
            {{ lang.name }} v{{ lang.version }}
          </option>
        </select>
      </div>

      <button :disabled="file.notModified || isSaving"
              @click="saveFile">
        {{ $t('action.file.save') }}
        <LoadingIcon v-if="isSaving"
                     size="1em"/>
      </button>

      <button @click="showTokens = !showTokens">
        {{ $t(`action.tokens.${showTokens ? 'hide' : 'show'}`) }} ?
      </button>
    </div>
    <div class="ide-body">
      <Loader v-if="reloadLang"/>
      <Terminal ref="terminal"
                :lang="lang"
                :file="file"
                :tokens="context.tokens"
                @update="updateTokens"
                @save="saveFile"/>
      <TokenList v-if="showTokens"
                 :context="context"
                 @select="selectToken"/>
    </div>
  </div>
</template>

<script>
import TokenList from "./TokenList.vue";
import Terminal from "./Terminal.vue";
import Loader from "./Loader.vue";
import api from "../api.js";
import File from "../models/file.js";
import Lang from "../models/lang.js";
import Repo from "../models/repo.js";
import LoadingIcon from "./LoadingIcon.vue";

export default {
  name: "Ide",
  components: {LoadingIcon, Loader, TokenList, Terminal},
  props: [],
  data() {
    return {
      showModalFilename: false,
      isSaving: false,
      langs: [],
      repos: [],
      repo: new Repo({name: this.$route.query['repo'] ?? 'public'}),
      file: new File({name: this.$route.query['file'] ?? ''}),
      lang: new Lang({name: ''}),
      showTokens: false,
      reloadLang: false,
      context: {
        tokenizer: null,
        tokens: []
      }
    }
  },
  computed: {
    content() {
      return this.file.content
    }
  },
  watch: {},
  async mounted() {
    await this.loadLangList()
    await this.loadRepoList()
    await this.loadRepo()
    await this.loadFile()
  },
  methods: {
    async loadLangList() {
      this.langs = await api.loadLangList();
    },
    async loadRepoList() {
      this.repos = await api.loadRepoList();
    },
    async loadLang() {
      if (this.file.lang) {
        let lang = await api.loadLang(this.file.lang)
        this.lang.name = lang.name
        this.lang.version = lang.version
        this.lang.data = lang.data
        this.lang.styles = lang.styles
        this.updateTokens()
      }
    },
    async loadRepo() {
      let repo = await api.loadRepo(this.repo.name)
      this.repo.name = repo.name
      this.repo.files = repo.files
    },
    async loadFile() {
      if (this.file.name) {
        let file = await api.loadFile(this.repo.name, this.file.name)
        this.file.name = file.name
        this.file.content = file.content
        this.file.original.content = file.content
        this.file.lang = file.lang
        this.file.original.lang = file.lang
        await this.loadLang()
      }
    },
    async saveFile() {
      if (!this.file.name) {
        this.showModalFilename = true
        return
      }
      if (this.isSaving || this.file.notModified)
        return
      this.isSaving = true;
      let file = await api.saveFile(this.repo.name, this.file)
      this.file.name = file.name
      this.file.content = file.content
      this.file.original.content = file.content
      this.file.lang = file.lang
      this.file.original.lang = file.lang
      this.isSaving = false;
      await this.loadLang()
    },
    selectToken(token) {
      this.$refs.terminal.$refs.input.setSelectionRange(token.at, token.to, "forward")
      this.$refs.terminal.$refs.input.focus()
    },
    updateTokens() {
      this.context.tokens = this.lang.tokenize(this.file.content)
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
      text-align: center;
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