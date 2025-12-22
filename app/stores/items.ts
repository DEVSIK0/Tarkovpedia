import { defineStore } from "pinia";

import { ItemService } from "@/services/tarkov/ItemService";
import type { IItem } from "@/models/IItem";
import { ref } from "vue";

export const useItems = defineStore("items", () => {
  const items = ref<IItem[] | null>(null);
  const isLoading = ref(true);

  const fetchItems = () => {
    isLoading.value = true;
    ItemService.getAllItems()
      .then((response) => {
        items.value = response.map((item: IItem) => {
          item.sellFor = item.sellFor.filter((sell) => sell.vendor.normalizedName !== "ref");
          item.sellFor = item.sellFor.sort((a, b) => b.priceRUB - a.priceRUB);
          return item;
        });
      })
      .finally(() => {
        isLoading.value = false;
      });
  };

  return {
    items,
    fetchItems,
    isLoading,
  };
});
