export default class Repo {
  constructor(args) {
    this.name = args.name ?? 'public'
    this.files = args.files ?? []
  }
}