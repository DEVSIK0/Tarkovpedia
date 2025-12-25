export default defineNuxtPlugin(async (nuxtApp) => {
  const { setLocale, loadLocaleMessages, locales } = nuxtApp.$i18n as any;

  let lang = localStorage.getItem("lang");

  if (!lang) {
    const browserLang = navigator.language.split("-")[0] ?? null;
    const isSupported = locales.value.some((l: any) => l.code === browserLang);

    if (isSupported) {
      lang = browserLang;
    }
  }

  if (!lang) return;

  await loadLocaleMessages(lang);
  await setLocale(lang);
});
