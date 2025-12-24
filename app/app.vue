<script setup lang="ts">
import type { LayoutKey } from "#build/types/layouts";

const layout = computed<LayoutKey | false>(() => (useRoute().path === "/" ? false : "navbar-footer"));
</script>

<template>
  <div>
    <NuxtLayout :name="layout">
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>
