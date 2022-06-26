<template>
  <header>
    <nav>
      <RouterLink to="/">{{ $t('pages.home') }}</RouterLink>
      <RouterLink to="/ide">{{ $t('pages.ide') }}</RouterLink>
      <RouterLink to="/langs">{{ $t('pages.langs') }}</RouterLink>
    </nav>
  </header>
  <main>
    <RouterView/>
  </main>
</template>

<script setup>
import {RouterLink, RouterView} from 'vue-router'</script>

<style lang="scss" scoped>
@import './assets/mixins.scss';
@import './assets/dark-theme.css';

header {
  width: 100%;
  height: 5vh;

  nav {
    @include row($content: space-around, $items: center);
    gap: 1vh;

    a {
      flex-grow: 1;
      text-align: center;
      border: 1px solid gray;
      border-radius: 5px;
      padding: 0.5em 1em;
      text-decoration: none;
      transition: background-color ease-in-out 0.33s;

      &:hover {
        background-color: rgba(0, 0, 0, 0.2);
      }
    }
  }
}

main {
  width: 100%;
  height: 95vh;
}
</style>
