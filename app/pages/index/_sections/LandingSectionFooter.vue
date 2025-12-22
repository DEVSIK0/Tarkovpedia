<script setup lang="ts"></script>
<template>
  <footer class="flex flex-col items-center justify-center gap-3">
    <p>&copy {{ new Date().getFullYear() }} tarkovpedia.com. Open Source project.</p>
    <p class="created-by">Created by <a href="https://www.devsiko.com" target="_blank">Devsiko</a></p>
  </footer>
</template>

<style scoped>
footer {
  height: 200px;

  p:not(p.created-by) {
    filter: opacity(0.5);
  }

  p.created-by {
    filter: opacity(0.7);
    a {
      appearance: none;
      color: inherit;
      text-decoration: none;
      color: var(--gold-3);
    }
  }
}
</style>
