<template>
  <div class="scroll-container">
    <table class="token-table">
      <thead>
      <tr>
        <th>at</th>
        <th>to</th>
        <th>type</th>
        <th>content</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(token, index) in context.tokens"
          :key="index"
          class="hov-highlight"
          @click="$emit('select', token)">
        <td>{{ token.at }}</td>
        <td>{{ token.to }}</td>
        <td>{{ token.type }}</td>
        <td>{{ maxLength(token.content) }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "TokenList",
  emits: ['select'],
  props: ['context'],
  methods: {
    maxLength(text) {
      if(text.length > 30) {
        return text.substring(0, 30 - 1) + '…'
      } else {
        return text
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/mixins.scss';
@import '../assets/themes.scss';

.scroll-container {
  @include theme-dark($opacity: 0.2);
  height: 100%;

  overflow-y: scroll;

  table, td, th {
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-collapse: collapse;
  }

  .token-table {

    td {
      padding: 0.2em 0.4em;
    }

    tbody {
      tr {
        cursor: pointer;
      }
    }
  }
}

</style>