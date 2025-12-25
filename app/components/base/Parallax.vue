<script setup lang="ts">
const bgStrength = 16;
const fgStrength = 26;
const scale = 1.06;
const hoverFriction = 0.34;
const activationMargin = 80;

const props = defineProps<{
  backgroundSrc: string;
  foregroundSrc: string;
  gradient?: {
    color: `rgba(${number}, ${number}, ${number}, ${number})`;
  };
}>();

const root = useTemplateRef<HTMLDivElement>("REF_ROOT");

const tx = ref(0);
const ty = ref(0);
const cx = ref(0);
const cy = ref(0);

const bgStyle = computed(() => {
  return {
    transform: `translate3d(${cx.value * bgStrength}px, ${cy.value * bgStrength}px, 0) scale(${scale})`,
  };
});
const fgStyle = computed(() => {
  return {
    transform: `translate3d(${cx.value * fgStrength}px, ${cy.value * fgStrength}px, 0) scale(${scale})`,
  };
});

let animId = 0;
let rect = { left: 0, top: 0, width: 1, height: 1 };
let ro: ResizeObserver | null = null;
let lastT = 0;

const updateRect = () => {
  const r = root.value!.getBoundingClientRect();
  rect = { left: r.left, top: r.top, width: r.width || 1, height: r.height || 1 };
};

const onGlobalMove = (e: PointerEvent) => {
  if (!rect.width) {
    return;
  }
  const inside =
    e.clientX >= rect.left - activationMargin &&
    e.clientX <= rect.left + rect.width + activationMargin &&
    e.clientY >= rect.top - activationMargin &&
    e.clientY <= rect.top + rect.height + activationMargin;

  if (inside) {
    const nx = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
    const ny = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
    tx.value = Math.max(-1, Math.min(1, nx));
    ty.value = -Math.max(-1, Math.min(1, ny));
  } else {
    tx.value = 0;
    ty.value = 0;
  }
  loop();
};

const onVisibilityChange = () => {
  if (document.hidden) {
    tx.value = 0;
    ty.value = 0;
    loop();
  }
};

const loop = () => {
  if (animId) {
    return;
  }
  lastT = performance.now();
  const step = (now: number) => {
    const dt = Math.min((now - lastT) / 1000, 1 / 30);
    lastT = now;
    const base = Math.max(0, Math.min(0.99, hoverFriction));
    const alpha = 1 - Math.pow(1 - base, dt * 60);
    cx.value += (tx.value - cx.value) * alpha;
    cy.value += (ty.value - cy.value) * alpha * 0.3;
    animId = requestAnimationFrame(step);
  };
  animId = requestAnimationFrame(step);
};

onMounted(() => {
  updateRect();
  ro = new ResizeObserver(updateRect);
  if (root.value) {
    ro.observe(root.value);
  }
  window.addEventListener("scroll", updateRect, { passive: true });
  window.addEventListener("pointermove", onGlobalMove, { passive: true });
  document.addEventListener("visibilitychange", onVisibilityChange);
});

onBeforeUnmount(() => {
  if (animId) {
    cancelAnimationFrame(animId);
  }
  if (ro && root.value) {
    ro.unobserve(root.value);
  }
  window.removeEventListener("scroll", updateRect);
  window.removeEventListener("pointermove", onGlobalMove);
  document.removeEventListener("visibilitychange", onVisibilityChange);
});
</script>

<template>
  <section ref="REF_ROOT" class="parallax-abs" aria-label="Parallax decorativo" role="img">
    <div class="content h-dvh">
      <slot class="" />
    </div>
    <img class="layer bg" :src="props.backgroundSrc" alt="" draggable="false" :style="bgStyle" />
    <img class="layer fg" :src="props.foregroundSrc" alt="" draggable="false" :style="fgStyle" />
    <span
      v-if="props.gradient != null"
      class="gradient"
      :style="`background: linear-gradient(1deg, ${props.gradient?.color} 0%, rgba(255, 255, 255, 0) 30%)`"
    ></span>
  </section>
</template>

<style scoped>
.parallax-abs {
  position: relative;
  height: 100dvh;
  width: 100%;
  inset: 0;
  overflow: hidden;
  perspective: 1000px;
}

.content {
  position: relative;
  z-index: 10;
}

.layer,
.gradient {
  pointer-events: none;
}

.gradient {
  width: 100%;
  height: 100%;
  position: absolute;
  inset: 0;
  z-index: 2;
}

.layer {
  position: absolute;
  inset: 0;
  width: 110%;
  height: 110%;
  object-fit: cover;
  will-change: transform;
  user-select: none;
  -webkit-user-drag: none;
}

.bg {
  z-index: -2;
}
.fg {
  z-index: -1;
}
</style>
