<script setup lang="ts">
import { useMaps } from "@/stores/maps";
import type { IMap } from "@/models/IMap";

const route = useRoute();
const { maps } = useMaps();

const map = ref<IMap | null>(null);

onBeforeMount(() => {
  map.value = maps.find((m) => m.shortName === route.params.id) ?? null;
});
</script>
<template>
  <NuxtLayout name="background" backgroundUrl="/images/backgrounds/map.webp">
    <section v-if="map == null">
      <h1>404 - Not found</h1>
    </section>
    <section v-else>
      <BaseMap :image-url="`/images/maps/${map.fileName}`" :aspect-ratio="map.aspectRatio" />
    </section>
  </NuxtLayout>
</template>

<style scoped>
section {
  height: 100%;
  padding: 30px;
  display: grid;
  place-items: center;
}
</style>
