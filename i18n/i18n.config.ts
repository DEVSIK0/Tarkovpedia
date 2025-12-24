import en from "./locales/en.json";
import es from "./locales/es.json";

export default defineI18nConfig(() => ({
  legacy: false,
  locale: "en",
  messages: {
    en,
    es,
  },
}));
