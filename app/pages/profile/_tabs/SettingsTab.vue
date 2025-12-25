<script setup lang="ts">
const { locale, locales, setLocale, loadLocaleMessages } = useI18n();

const saveLocale = async (code: string) => {
  const newLocale = locales.value.find((l) => l.code === code);

  if (!newLocale) {
    console.warn(`Locale with code ${code} not found`);
    return;
  }

  await loadLocaleMessages(newLocale.code);
  await setLocale(newLocale.code);
  localStorage.setItem("lang", code);
};
</script>

<template>
  <section>
    <form @submit.prevent class="flex flex-col p-6">
      <label class="flex items-center gap-3">
        <span>{{ $t("profile.tab.settings.language.label") }}</span>
        <Select
          :model-value="locale"
          :options="locales"
          option-label="name"
          option-value="code"
          @change="(ev) => saveLocale(ev.value)"
        />
      </label>
    </form>
  </section>
</template>
