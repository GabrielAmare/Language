<template>
  <main class="container">
    <Ide/>
  </main>
</template>

<script>
import Ide from "../components/Ide.vue";

export default {
  name: "TerminalView",
  components: {
    Ide
  }
}
</script>

<style lang="scss">
@import "../assets/mixins.scss";
@import "../assets/themes.scss";

body {
  @include theme-dark();
}

#app {
  position: absolute;
  inset: 0;
}

.container {
  @include col($items: center);
  width: 100%;
  height: 100%;
}
</style>