try {
  console.log("[*] Loading analytics...");
  window.dataLayer = window.dataLayer || [];
  function gtag() {
    dataLayer.push(arguments);
  }
  gtag("js", new Date());
  gtag("config", "G-19QFPPGCW0");
  console.log("[*] Analytics loaded");
} catch (error) {
  console.error("[!] Error loading analytics", error);
}
