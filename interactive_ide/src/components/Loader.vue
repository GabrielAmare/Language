<template>
  <div class="outer">
    <img src="../assets/img/loading-icon.png" alt="loading icon">
  </div>
</template>

<script>
export default {
  name: "Loader"
}
</script>

<style lang="scss" scoped>
@import '../assets/mixins.scss';


@keyframes rotating {
  0% {
    -ms-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -ms-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}

.outer {
  @include col($content: center, $items: center);
  position: absolute;
  inset: 0;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.5);

  img {
    width: 5vh;
    transform: scale(0.1);
    mix-blend-mode: overlay;
    image-rendering: smooth;

    -webkit-animation: rotating 3s linear infinite;
    -moz-animation: rotating 3s linear infinite;
    -o-animation: rotating 3s linear infinite;
    animation: rotating 3s linear infinite;
  }

}
</style>