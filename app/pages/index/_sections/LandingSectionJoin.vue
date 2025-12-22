<script setup lang="ts">
const emit = defineEmits<{
  (event: "@join"): void;
}>();
</script>
<template>
  <section class="flex flex-col items-center text-center gap-6">
    <h1 class="text-5xl">{{ $t("join.title").toUpperCase() }}</h1>
    <h2>{{ $t("join.subtitle") }}</h2>
    <BaseButton
      class="px-44 py-10 text-3xl"
      variant="secondary"
      @@click="() => emit('@join')"
      :text="$t('join.button')"
    ></BaseButton>
    <p>{{ $t("join.description") }}</p>
  </section>
</template>

<style scoped>
section {
  height: 100%;
  max-width: 1000px;
  padding: 0 20px;
}
</style>
