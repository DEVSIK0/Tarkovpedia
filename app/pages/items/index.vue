<script setup lang="ts">
import { FilterMatchMode } from "@primevue/core/api";

const storeItems = useItems();
const storeTraders = useTraders();

const filters = ref({
  name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  shortName: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
});

filters.value = {
  name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  shortName: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
};
</script>
<template>
  <NuxtLayout name="background" backgroundUrl="/images/backgrounds/items.webp">
    <section class="h-full p-9 flex flex-col justify-center items-center">
      <div :class="['datatable-container', `h-full max-h-159 flex flex-col`, { 'not-loading': !storeItems.isLoading }]">
        <div v-if="storeItems.isLoading" class="w-full h-full flex flex-col gap-3">
          <Skeleton width="100%" height="90px" />
          <Skeleton width="100%" height="100%" />
        </div>
        <DataTable
          v-else
          :value="storeItems.items"
          removableSort
          paginator
          :rows="6"
          :rowsPerPageOptions="[5, 10, 20, 50]"
          v-model:filters="filters"
          filterDisplay="row"
          :globalFilterFields="['name', 'shortName']"
          size="normal"
          autoLayout
          scrollable
          scrollHeight="flex"
        >
          <Column>
            <template #body="{ data }">
              <div class="flex items-center gap-6">
                <a :href="data.link" target="_black" class="flex items-center">
                  <Icon class="icon" name="material-symbols-light:open-in-new-sharp" />
                </a>
                <img class="item-image" :src="data.gridImageLink" :alt="data.gridImageLink" />
              </div>
            </template>
          </Column>
          <!-- SHORT NAME -->
          <Column field="shortName" :header="$t('items.datatable.column.shortName')" sortable>
            <template #body="{ data }">
              <span class="item-shortname">{{ data.shortName }}</span>
            </template>
            <template #filter="{ filterModel, filterCallback }">
              <InputText class="w-40" v-model="filterModel.value" @input="filterCallback" />
            </template>
          </Column>
          <!-- NAME -->
          <Column field="name" :header="$t('items.datatable.column.name')" sortable>
            <template #body="{ data }">
              <span class="item-name">{{ data.name }}</span>
            </template>
            <template #filter="{ filterModel, filterCallback }">
              <InputText class="w-50" v-model="filterModel.value" @input="filterCallback" />
            </template>
          </Column>
          <!-- FLEA LEVEL -->
          <Column field="minLevelForFlea" :header="$t('items.datatable.column.fleaLevel')" sortable />
          <!-- PRICE / TRADER -->
          <Column field="basePrice" :header="$t('items.datatable.column.trader')" sortable>
            <template #body="{ data }">
              <div class="price-container flex flex-col items-center gap-3" v-if="data.sellFor.length >= 1">
                <img
                  class="trader-image"
                  :src="
                    storeTraders.traders?.find((t) => t.normalizedName === data.sellFor[0].vendor.normalizedName)
                      ?.imageLink
                  "
                />
                <span class="price">{{ formatRuble(data.sellFor[0].price) }} ₽</span>
              </div>
            </template>
          </Column>
        </DataTable>
      </div>
    </section>
  </NuxtLayout>
</template>

<style scoped>
.datatable-container {
  width: 100%;
  max-width: 1200px;

  &.not-loading {
    background-color: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(30px);
  }

  .item-shortname {
    display: block;
    width: 100%;
    max-width: 150px;
    text-overflow: ellipsis;
  }

  .item-name {
    display: block;
    width: 100%;
    max-width: 200px;
    text-overflow: ellipsis;
  }

  .item-image,
  .trader-image {
    width: 100%;
    max-width: 60px;
    object-fit: contain;
  }

  .item-image {
    height: 100%;
    max-height: 60px;
  }

  .trader-image {
    height: 100%;
    max-width: 90px;
  }

  a {
    text-decoration: none;
    color: inherit;

    .icon {
      font-size: 1.2rem;
      cursor: pointer;
    }
  }
}
</style>
