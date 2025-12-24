import { defineStore } from "pinia";

import type { IMap } from "@/models/IMap";
import { MapService } from "~/services/tarkov/MapService";

export const useMaps = defineStore("maps", () => {
  const maps = ref<IMap[]>([]);

  const fetchMaps = async () => {
    maps.value = await MapService.getAllMaps();
  };

  return {
    maps,
    fetchMaps
  };
});
