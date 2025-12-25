import { ItemService } from "@/services/tarkov/ItemService";
import type { IItem } from "@/models/IItem";
import { ref } from "vue";

export const useItems = defineStore("items", () => {
  const items = ref<IItem[]>([]);
  const isLoading = ref(true);

  const fetchItems = async () => {
    isLoading.value = true;
    try {
      items.value = await ItemService.getAllItems();
    } catch (error) {
      console.error(error);
    } finally {
      isLoading.value = false;
    }
  };

  return {
    items,
    fetchItems,
    isLoading,
  };
});
