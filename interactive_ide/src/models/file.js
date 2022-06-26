class FileState {
  constructor(args) {
    this.content = args.content ?? ''
    this.lang = args.lang ?? null
  }
}

export default class File {
  constructor(args) {
    this.repo = args.repo ?? 'public'
    this.name = args.name ?? ''
    this.ext = args.ext ?? '.txt'
    this.original = new FileState(args)
    this.content = this.original.content
    this.lang = this.original.lang
  }

  update(args) {
    this.repo = args.repo ?? 'public'
    this.name = args.name

    this.content = args.content
    this.lang = args.lang

    this.original.content = this.content
    this.original.lang = this.lang
  }

  get notModified() {
    // Return True when the file has been locally modified.
    return this.original.content === this.content
      && this.original.lang?.name === this.lang?.name
      && this.original.lang?.version === this.lang?.version
  }
}
