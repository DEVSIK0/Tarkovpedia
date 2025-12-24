<script setup lang="ts">
const { locale, locales } = useI18n();
</script>

<template>
  <section>
    <form @submit.prevent class="flex flex-col p-6">
      <label class="flex items-center gap-3">
        <span>{{ $t("profile.tab.settings.language.label") }}</span>
        <Select
          v-model="locale"
          :options="locales"
          option-label="name"
          option-value="code"
          @change="(item) => (locale = item.value)"
        />
      </label>
    </form>
  </section>
</template>

<style scoped></style>
