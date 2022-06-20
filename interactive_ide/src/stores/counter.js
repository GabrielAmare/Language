import { defineStore } from 'pinia'

export const useCounterStore = defineStore({
  id: 'code',
  state: () => ({
    code: ''
  }),
  getters: {
    doubleCount: (state) => state.counter * 2
  },
  actions: {
    increment() {
      this.counter++
    }
  }
})
