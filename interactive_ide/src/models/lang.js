import makeTokenizer from "../assets/js/make_tokenizer.js";

export default class Lang {
  constructor(args) {
    this.name = args.name ?? ''
    this.version = args.version ?? '0.0.0'
    this.tokenizer = null
    this.data = args.data ?? []
    this.styles = args.styles ?? {'default': {}}
  }

  set data(value) {
    this._data = value
    try {
      this.tokenizer = makeTokenizer(this._data)
    } catch (e) {
      this.tokenizer = null
    }
  }

  get data() {
    return this._data
  }

  tokenize(code) {
    try {
      return this.tokenizer(code)
    } catch (e) {
      return []
    }
  }
}
