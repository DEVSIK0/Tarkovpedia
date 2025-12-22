<script setup lang="ts">
import OpenSeadragon from "openseadragon";

const props = defineProps<{
  imageUrl: string;
  aspectRatio?: [number, number];
}>();

const OSD_REF = useTemplateRef<HTMLElement>("OSD_REF");

onMounted(() => {
  if (!OSD_REF.value) return;

  OpenSeadragon({
    element: OSD_REF.value,
    prefixUrl: "https://openseadragon.github.io/openseadragon/images/",
    tileSources: {
      type: "image",
      url: props.imageUrl,
    },
    showNavigator: true,
    visibilityRatio: 1.0,
    constrainDuringPan: true,
    defaultZoomLevel: 0,
    minZoomImageRatio: 0.1,
    maxZoomPixelRatio: 2,
    animationTime: 0.3,
  });
});
</script>

<template>
  <div class="viewer-container">
    <div ref="OSD_REF" class="osd-viewer"></div>
  </div>
</template>

<style scoped>
.viewer-container {
  width: 100%;
  height: 100%;
  max-width: 1600px;
  max-height: 800px;
  /* height: 100%; */
  background: #111;
  margin: 0 auto;
  border: 1px solid #333;
}

.osd-viewer {
  width: 100%;
  height: 100%;
}
</style>
