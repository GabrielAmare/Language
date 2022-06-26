<template>
  <div class="container">
    <img src="../assets/langs/json_1_0_0/graph.svg"
         alt="graphviz representation">
  </div>
</template>

<script>
export default {
  name: "LangView"
}
</script>

<style lang="scss" scoped>
.container {
  height: 100%;
  width: 100%;
  overflow-x: scroll;
  overflow-y: hidden;
  position: relative;

  img {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: auto;
  }
}
</style>