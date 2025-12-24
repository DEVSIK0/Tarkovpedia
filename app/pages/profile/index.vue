<script setup lang="ts">
import MyAccountTab from "./_tabs/MyAccountTab.vue";
import SettingsTab from "./_tabs/SettingsTab.vue";

const PROFILE_TABS = [
  {
    key: "profile.tab.account",
    disabled: true,
    component: MyAccountTab,
  },
  {
    key: "profile.tab.settings",
    disabled: false,
    component: SettingsTab,
  },
];

const currentTab = shallowRef(PROFILE_TABS[1]);
</script>
<template>
  <NuxtLayout name="background" backgroundUrl="/images/backgrounds/profile.webp" class="grid justify-items-center">
    <section class="w-full max-w-190 h-full flex flex-col gap-3 items-center py-9">
      <h1 class="flex w-full items-center gap-3 justify-center text-5xl">
        <Icon name="mdi:account-cog" />
        <span>{{ $t("profile.title").toUpperCase() }}</span>
      </h1>
      <header class="w-full">
        <nav class="tabs flex gap-3">
          <button
            v-for="(tab, index) in PROFILE_TABS"
            :key="tab.key"
            class="px-3 py-1 text-2xl"
            @click="() => (currentTab = PROFILE_TABS[index])"
            :disabled="tab.disabled"
          >
            {{ $t(tab.key).toUpperCase() }}
          </button>
        </nav>
      </header>
      <main class="container full w-full">
        <component :is="currentTab?.component" />
      </main>
    </section>
  </NuxtLayout>
</template>

<style scoped>
section {
  h1 {
    color: var(--white-1);
    filter: drop-shadow(0 6px 3px rgba(0, 0, 0, 0.1));
  }

  nav {
    button {
      background: none;
      border: none;

      &:disabled {
        cursor: not-allowed;
      }

      &:not(:disabled) {
        cursor: pointer;
        &:hover {
          background-color: rgba(0, 0, 0, 0.3);
          backdrop-filter: blur(10px);
        }
      }
    }
  }

  .container {
    background-color: rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
    width: 100%;
    height: 100%;
  }
}
</style>
