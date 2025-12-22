<script setup lang="ts">
const props = defineProps<{
  variant: "primary" | "secondary" | "tertiary";
  text: string;
  disabled?: boolean;
}>();

const emits = defineEmits<{
  (e: "@click"): void;
}>();
</script>
<template>
  <button
    :class="`base-button flex items-center gap-3 ${props.variant}`"
    @click="() => emits('@click')"
    :disabled="props.disabled"
  >
    <slot name="left" />
    <span>{{ props.text }}</span>
    <slot name="right" />
  </button>
</template>

<style scoped>
.base-button {
  color: white;
  cursor: pointer;
  border: none;
  background: none;

  &.primary {
    background-color: var(--gold-5);
    &:hover {
      background-color: var(--gold-6);
    }
  }

  &.secondary {
    border: 1px solid var(--gold-7);

    &:hover {
      background-color: hsl(from var(--gold-7) h s l / 0.3);
    }
  }

  &.tertiary {
    background-color: red;
  }
}
</style>
