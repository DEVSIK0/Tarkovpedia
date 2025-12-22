<script setup lang="ts">
const FEATURES = [
  {
    title: "feature.card.database.title",
    description: "feature.card.database.description",
    icon: "ci:search-magnifying-glass",
    backgroundIcon: "meteor-icons:arrow-trend-up",
  },
  {
    title: "feature.card.map.title",
    description: "feature.card.map.description",
    icon: "material-symbols:map-outline-sharp",
  },
  {
    title: "feature.card.squad.title",
    description: "feature.card.squad.description",
    icon: "teenyicons:users-outline",
  },
  {
    title: "feature.card.meta.title",
    description: "feature.card.meta.description",
    icon: "material-symbols:shield-outline",
  },
  {
    title: "feature.card.optimize.title",
    description: "feature.card.optimize.description",
    icon: "ant-design:thunderbolt-outlined",
  },
  {
    title: "feature.card.opensource.title",
    description: "feature.card.opensource.description",
    icon: "mingcute:github-line",
  },
];
</script>
<template>
  <section class="features grid content-center justify-items-center">
    <div class="cards">
      <div v-for="(feature, index) in FEATURES" :key="index" :class="`card card-${index + 1}`">
        <div class="icon-container">
          <Icon class="icon" :name="feature.icon" />
        </div>
        <div>
          <h1>{{ $t(feature.title) }}</h1>
          <p>{{ $t(feature.description) }}</p>
        </div>
        <Icon v-if="feature.backgroundIcon != null" class="background-icon" :name="feature.backgroundIcon" />
      </div>
    </div>
  </section>
</template>

<style scoped>
section.features {
  padding: 60px;

  .cards {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    grid-template-rows: repeat(3, 1fr);
    gap: 30px;
    width: 100%;
    max-width: 1300px;

    @media (width <= 790px) {
      display: flex;
      flex-direction: column;
    }

    .card {
      border: 1px solid var(--gold-8);
      padding: 20px;
      height: 100%;

      position: relative;

      display: flex;
      flex-direction: column;
      gap: 15px;

      &:hover {
        border: 1px solid var(--gold-6);
      }

      h1 {
        font-size: 2.4rem;
      }

      p {
        color: gray;
        font-size: 1.3rem;
      }

      .icon-container {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: var(--gold-9);
        padding: 9px;
        border-radius: 6px;
        width: 53px;
        height: 53px;
        .icon {
          font-size: 2rem;
          color: var(--gold-3);
        }
      }

      .background-icon {
        position: absolute;
        right: 27px;
        bottom: -20px;
        font-size: 14rem;
        filter: opacity(0.1);
      }

      &.card-1 {
        grid-column: span 3 / span 3;
        grid-row: span 2 / span 2;
      }

      &.card-2 {
        grid-column: span 3 / span 3;
        grid-column-start: 4;
        flex-direction: row;
      }

      &.card-3 {
        grid-column: span 3 / span 3;
        grid-column-start: 4;
        grid-row-start: 2;
        flex-direction: row;
      }

      &.card-4 {
        grid-column: span 2 / span 2;
        grid-row-start: 3;
      }

      &.card-5 {
        grid-column: span 2 / span 2;
        grid-column-start: 3;
        grid-row-start: 3;
      }

      &.card-6 {
        grid-column: span 2 / span 2;
        grid-column-start: 5;
        grid-row-start: 3;
      }
    }
  }
}
</style>
