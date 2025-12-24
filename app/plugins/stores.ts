export default defineNuxtPlugin((nuxtApp) => {
  const storeItems = useItems();
  const storeTradrers = useTraders();

  storeItems.fetchItems();
  storeTradrers.fetchTraders();
});
