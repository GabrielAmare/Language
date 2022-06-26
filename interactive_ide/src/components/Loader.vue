<template>
  <div class="outer">
    <LoadingIcon size="5vh"/>
  </div>
</template>

<script>
import LoadingIcon from "./LoadingIcon.vue";

export default {
  name: "Loader",
  components: {LoadingIcon}
}
</script>

<style lang="scss" scoped>
@import '../assets/mixins.scss';

.outer {
  @include col($content: center, $items: center);
  position: absolute;
  inset: 0;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.5);

}
</style>