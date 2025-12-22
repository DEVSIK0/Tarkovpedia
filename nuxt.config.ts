import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: false },
  // =====================
  // CONFIGURATION
  // =====================
  modules: ["@nuxtjs/i18n", "@nuxt/fonts", "@nuxt/icon", "@pinia/nuxt"],
  ssr: false,
  routeRules: {
    "/": {
      ssr: true,
      // prerender: true,
    },
  },
  // =====================
  // i18n
  // =====================
  i18n: {
    defaultLocale: "en",
    strategy: "no_prefix",
    locales: [{ code: "en", name: "English", shortName: "united-kingdom", file: "en.json" }],
    // detectBrowserLanguage: {
    // useCookie: true,
    // cookieKey: "i18n_redirected",
    // redirectOn: "no prefix",
    // },
  },
  // =====================
  // STYLES
  // =====================
  css: ["@/assets/css/main.css"],
  vite: {
    plugins: [tailwindcss()],
  },
  // =====================
  // SEO + META
  // =====================
  app: {
    head: {
      title: "Tarkovpedia",
      htmlAttrs: {
        lang: "en",
      },
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    },
  },
});
