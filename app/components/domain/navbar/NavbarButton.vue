<script setup lang="ts">
const props = defineProps<{
  buttons: {
    key: string | null;
    icon: string;
    disabled: boolean;
    onCLick: () => void;
  }[];
}>();
</script>
<template>
  <button
    v-for="(item, index) in props.buttons"
    :key="index"
    :disabled="item.disabled"
    class="flex items-center gap-2 px-3"
    @click="item.onCLick"
  >
    <Icon class="icon" :name="item.icon" />
    <span v-if="item.key !== null">{{ $t(item.key) }}</span>
  </button>
</template>

<style scoped>
button {
  font-size: 1rem;
  background: none;
  border: none;
  .icon {
    font-size: 1.6rem;
  }
}

button:disabled {
  cursor: not-allowed;
}

button:not(:disabled) {
  cursor: pointer;
  &:hover {
    color: var(--white-10);
    background-color: var(--white-5);
  }
}
</style>
