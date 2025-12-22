<script setup lang="ts">
const attrs = useAttrs();
</script>
<template>
  <main :style="`background-image: url(${attrs.backgroundUrl})`">
    <slot />
  </main>
</template>

<style scoped>
main {
  background-size: cover;
  background-position: center center;

  height: 100dvh;
  overflow: auto;
}
</style>
