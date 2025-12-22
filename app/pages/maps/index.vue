<script setup lang="ts">
import type { IMap } from "@/models/IMap";
import { useMaps } from "@/stores/maps";

const router = useRouter();
const { maps } = useMaps();

const goToMap = (map: IMap) => {
  router.push(`/maps/${map.shortName}`);
};
</script>

<template>
  <NuxtLayout name="background" backgroundUrl="/images/backgrounds/map.webp">
    <section class="h-full w-full grid place-items-center p-6">
      <div class="maps-container grid grid-cols-1 md:grid-cols-3 place-items-center content-center gap-6 w-full max-w-325">
        <button
          v-for="map in maps"
          :key="map.name"
          @click="() => goToMap(map)"
          class="p-8 md:p-20 w-full h-full"
          :style="`background-image: url(/images/maps/${map.fileThumbnail})`"
        >
          <span>{{ map.name }}</span>
        </button>
      </div>
    </section>
  </NuxtLayout>
</template>

<style scoped>
section {
  button {
    position: relative;

    border: none;
    font-size: 1.6rem;
    text-shadow: 3px 3px 6px black;
    cursor: pointer;

    background-size: cover;
    background-position: center center;

    &::after {
      content: "";
      position: absolute;
      bottom: 0;
      left: 0;
      height: 100%;
      width: 100%;
      background: linear-gradient(1deg, rgba(0, 0, 0, 1) 0%, rgba(255, 255, 255, 0) 100%);
    }

    &:hover {
      filter: brightness(1.3);
    }

    span {
      position: sticky;
      z-index: 2;
    }
  }
}

@media screen and (width < 768px) {
  /* .maps-container {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  button {
    padding: 2rem
  } */
}
</style>
