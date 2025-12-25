import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  // CONFIGURATION
  modules: ["@nuxtjs/i18n", "@nuxt/fonts", "@nuxt/icon", "@pinia/nuxt", "@primevue/nuxt-module"],
  ssr: false,
  // i18n
  i18n: {
    strategy: "no_prefix",
    defaultLocale: "en",
    langDir: "locales",
    locales: [
      {
        code: "en",
        name: "English",
        shortName: "united-kingdom",
        language: "en-US",
        file: "en.json",
      },
      {
        code: "es",
        name: "Español",
        shortName: "spain",
        language: "es-ES",
        file: "es.json",
      },
    ],
    detectBrowserLanguage: false,
  },
  // STYLES
  css: ["@/assets/css/main.css"],
  vite: {
    plugins: [tailwindcss()],
  },
  primevue: {
    importTheme: {
      from: "@/assets/primevue/theme.js",
    },
  },
  // SEO + META
  app: {
    head: {
      title: "Tarkovpedia",
      htmlAttrs: {
        lang: "en",
      },
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { name: "author", content: "devisko" },
        {
          name: "description",
          content:
            "Your tactical companion for Escape from Tarkov. Real-time prices, interactive maps, and squad coordination.",
        },
        {
          name: "keywords",
          content: "Tarkov, Escape from Tarkov, EFT, Maps, Items, Prices, Squad, Wiki, Database, Tarkovpedia",
        },
        { property: "og:site_name", content: "Tarkovpedia" },
        { property: "og:type", content: "website" },
        { property: "og:image", content: "/images/parallax_background.webp" },
        { property: "og:see_also", content: "https://github.com/DEVSIK0/Tarkovpedia" },
        { name: "twitter:card", content: "summary_large_image" },
        { name: "twitter:site", content: "@DEVSIK0" },
        { name: "twitter:creator", content: "@DEVSIK0" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
      script: [
        { src: "https://www.googletagmanager.com/gtag/js?id=G-19QFPPGCW0", async: true },
        { src: "/js/google_analytics.js" },
      ],
    },
  },
});
