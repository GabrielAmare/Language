import axios from "axios";

const root = 'http://localhost:3001';


const api = {
  async loadLang(lang) {
    let res = await axios.get(`${root}/langs/${lang.name}/${lang.version}`)
    return res.data
  },
  async loadLangList() {
    let res = await axios.get(`${root}/langs`)
    return res.data
  },
  async loadRepoList() {
    let res = await axios.get(`${root}/repos`)
    return res.data
  },
  async loadFile(repo, filename) {
    let res = await axios.get(`${root}/repos/${repo}/files/${filename}`)
    return res.data
  },
  async saveFile(repo, file) {
    let res = await axios.put(`${root}/repos/${repo}/files/${file.name}`, {'content': file.content, 'lang': file.lang})
    return res.data
  },
  async loadRepo(repo) {
    let res = await axios.get(`${root}/repos/${repo}`)
    return res.data
  }
}

export default api