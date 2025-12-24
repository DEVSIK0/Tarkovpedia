<script setup lang="ts">
import LandingSectionFeatures from "./_sections/LandingSectionFeatures.vue";
import LandingSectionJoin from "./_sections/LandingSectionJoin.vue";
import LandingSectionFooter from "./_sections/LandingSectionFooter.vue";

const router = useRouter();

const primaryButton = () => {
  router.push("/dashboard");
};

const secondaryButton = () => {
  document.querySelector("#features")?.scrollIntoView({
    behavior: "smooth",
  });
};
</script>
<template>
  <main class="flex flex-col items-center">
    <client-only>
      <BaseParallax
        background-src="/images/parallax_background.webp"
        foreground-src="/images/parallax_lightbulb.webp"
        :gradient="{ color: 'rgba(0, 0, 0, 1)' }"
      >
        <div class="content h-full flex flex-col items-center justify-center gap-7">
          <h1>{{ $t("hero.title") }}</h1>
          <p class="text-2xl">{{ $t("hero.subtitle") }}</p>
          <div class="flex gap-6">
            <BaseButton
              class="px-6 py-4 text-2xl"
              variant="primary"
              @@click="primaryButton"
              :text="$t('hero.button.primary')"
            ></BaseButton>
            <BaseButton
              class="px-6 py-4 text-2xl"
              variant="secondary"
              @@click="secondaryButton"
              :text="$t('hero.button.features')"
            ></BaseButton>
          </div>
          <small>{{ $t("hero.subtitle.variant") }}</small>
        </div>
      </BaseParallax>
    </client-only>
    <LandingSectionFeatures id="features" class="scroll-mt-25" />
    <LandingSectionJoin @@join="primaryButton" />
    <LandingSectionFooter />
  </main>
</template>

<style scoped>
.content {
  text-align: center;
  text-shadow: 0 0 16px black;
  h1 {
    font-size: clamp(3rem, 13vw, 13rem);
  }

  small {
    font-size: 1rem;
  }
}
</style>
