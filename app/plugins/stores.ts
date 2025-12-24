export default defineNuxtPlugin((nuxtApp) => {
  const storeMaps = useMaps();
  const storeItems = useItems();
  const storeTradrers = useTraders();

  storeMaps.fetchMaps();
  storeItems.fetchItems();
  storeTradrers.fetchTraders();
});
