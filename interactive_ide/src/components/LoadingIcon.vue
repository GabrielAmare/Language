<template>
  <img src="../assets/img/loading-icon.png"
       :style="style"
       alt="loading icon">
</template>

<script>
export default {
  name: "LoadingIcon",
  props: ['size'],
  computed: {
    style() {
      return {
        width: this.size,
        height: this.size
      }
    }
  }
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

img {
  transform: scale(0.1);
  mix-blend-mode: overlay;
  image-rendering: smooth;

  -webkit-animation: rotating 3s linear infinite;
  -moz-animation: rotating 3s linear infinite;
  -o-animation: rotating 3s linear infinite;
  animation: rotating 3s linear infinite;
}

</style>