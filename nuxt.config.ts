import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: false },
  // CONFIGURATION
  modules: ["@nuxtjs/i18n", "@nuxt/fonts", "@nuxt/icon", "@pinia/nuxt", "@primevue/nuxt-module"],
  ssr: false,
  routeRules: {
    "/": {
      ssr: true,
    },
    "/dashboard": {
      redirect: "/maps",
    },
  },
  // i18n
  i18n: {
    vueI18n: "./i18n.config.ts",
    defaultLocale: "es",
    strategy: "no_prefix",
    locales: [
      {
        code: "en",
        name: "English",
        shortName: "united-kingdom",
        language: "en-US",
      },
      {
        code: "es",
        name: "Español",
        shortName: "spain",
        language: "es-ES",
      },
    ],

    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: "i18n_redirected",
      redirectOn: "no prefix",
    },
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
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
      script: [
        { src: "https://www.googletagmanager.com/gtag/js?id=G-19QFPPGCW0", async: true },
        { src: "/js/google_analytics.js" },
      ],
    },
  },
});
