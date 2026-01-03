<script setup lang="ts">
import OpenSeadragon from "openseadragon";

interface Point {
  x: number;
  y: number;
}

interface Stroke {
  points: Point[];
  color: string;
  width: number;
  type: "brush";
}

const props = withDefaults(
  defineProps<{
    imageUrl: string;
    aspectRatio?: [number, number];
    editable?: boolean;
  }>(),
  {
    editable: false,
  }
);

const OSD_REF = useTemplateRef<HTMLElement>("OSD_REF");
const CANVAS_REF = useTemplateRef<HTMLCanvasElement>("CANVAS_REF");

const viewer = shallowRef<OpenSeadragon.Viewer | null>(null);
const isDrawing = ref(false);
const currentTool = ref<"pan" | "brush" | "eraser">("pan");
const strokes = ref<Stroke[]>([]);
const currentStroke = ref<Stroke | null>(null);
const settings = reactive({
  color: "#14ffb4",
  width: 5,
});

onMounted(() => {
  if (!OSD_REF.value) return;

  const v = OpenSeadragon({
    element: OSD_REF.value,
    prefixUrl: "https://openseadragon.github.io/openseadragon/images/",
    tileSources: {
      type: "image",
      url: props.imageUrl,
    },
    showNavigator: true,
    visibilityRatio: 1.0,
    constrainDuringPan: true,
    defaultZoomLevel: 0,
    minZoomImageRatio: 0.1,
    maxZoomPixelRatio: 2,
    animationTime: 0.3,
    mouseNavEnabled: true,
    autoHideControls: false,
  });

  viewer.value = v;

  v.addHandler("open", () => {
    resizeCanvas();
    redraw();
  });

  v.addHandler("animation", () => {
    redraw();
  });

  v.addHandler("resize", () => {
    resizeCanvas();
    redraw();
  });

  v.addHandler("rotate", () => {
    redraw();
  });

  resizeCanvas();
});

const resizeCanvas = () => {
  if (!CANVAS_REF.value || !OSD_REF.value) return;
  const { clientWidth, clientHeight } = OSD_REF.value;
  CANVAS_REF.value.width = clientWidth;
  CANVAS_REF.value.height = clientHeight;
};

const getImagePoint = (e: MouseEvent): Point | null => {
  if (!viewer.value || !CANVAS_REF.value) return null;
  const rect = CANVAS_REF.value.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  const viewportPoint = viewer.value.viewport.pointFromPixel(new OpenSeadragon.Point(x, y));
  const imagePoint = viewer.value.viewport.viewportToImageCoordinates(viewportPoint);

  return { x: imagePoint.x, y: imagePoint.y };
};

const startDrawing = (e: MouseEvent) => {
  if (currentTool.value === "pan") return;
  isDrawing.value = true;

  const point = getImagePoint(e);
  if (!point) return;

  if (currentTool.value === "brush") {
    const scale = getCurrentScale();
    currentStroke.value = {
      points: [point],
      color: settings.color,
      width: settings.width / scale,
      type: "brush",
    };
    strokes.value.push(currentStroke.value);
    redraw();
  } else if (currentTool.value === "eraser") {
    eraseStrokesAt(point);
  }
};

const draw = (e: MouseEvent) => {
  if (!isDrawing.value) return;

  const point = getImagePoint(e);
  if (!point) return;

  if (currentTool.value === "brush" && currentStroke.value) {
    currentStroke.value.points.push(point);
    redraw();
  } else if (currentTool.value === "eraser") {
    eraseStrokesAt(point);
  }
};

const stopDrawing = () => {
  isDrawing.value = false;
  currentStroke.value = null;
};

const eraseStrokesAt = (point: Point) => {
  const scale = getCurrentScale();
  const eraserRadiusScreen = 10;
  const eraserRadiusImage = eraserRadiusScreen / scale;

  const strokesToRemove: number[] = [];

  strokes.value.forEach((stroke, index) => {
    if (isPointNearStroke(point, stroke, eraserRadiusImage)) {
      strokesToRemove.push(index);
    }
  });

  if (strokesToRemove.length > 0) {
    for (let i = strokesToRemove.length - 1; i >= 0; i--) {
      const index = strokesToRemove[i];
      if (index !== undefined) {
        strokes.value.splice(index, 1);
      }
    }
    redraw();
  }
};

const isPointNearStroke = (point: Point, stroke: Stroke, tolerance: number): boolean => {
  const strokeHalfWidth = stroke.width / 2;
  const totalThreshold = tolerance + strokeHalfWidth;

  if (stroke.points.length === 0) return false;

  for (let i = 0; i < stroke.points.length - 1; i++) {
    const p1 = stroke.points[i];
    const p2 = stroke.points[i + 1];
    if (p1 && p2 && distToSegment(point, p1, p2) <= totalThreshold) {
      return true;
    }
  }
  if (stroke.points.length === 1) {
    const p0 = stroke.points[0];
    if (p0 && dist(point, p0) <= totalThreshold) {
      return true;
    }
  }

  return false;
};

const distToSegment = (p: Point, v: Point, w: Point) => {
  const l2 = distSq(v, w);
  if (l2 === 0) return dist(p, v);
  let t = ((p.x - v.x) * (w.x - v.x) + (p.y - v.y) * (w.y - v.y)) / l2;
  t = Math.max(0, Math.min(1, t));
  return dist(p, { x: v.x + t * (w.x - v.x), y: v.y + t * (w.y - v.y) });
};

const distSq = (p1: Point, p2: Point) => {
  return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2;
};

const dist = (p1: Point, p2: Point) => {
  return Math.sqrt(distSq(p1, p2));
};

const redraw = () => {
  if (!CANVAS_REF.value || !viewer.value) return;
  const v = viewer.value;
  const ctx = CANVAS_REF.value.getContext("2d");
  if (!ctx) return;

  ctx.clearRect(0, 0, CANVAS_REF.value.width, CANVAS_REF.value.height);

  const currentScale = getCurrentScale();

  strokes.value.forEach((stroke) => {
    if (stroke.points.length < 1) return;

    ctx.beginPath();

    const firstPoint = stroke.points[0];
    if (!firstPoint) return;

    const firstP = v.viewport.imageToViewerElementCoordinates(new OpenSeadragon.Point(firstPoint.x, firstPoint.y));
    ctx.moveTo(firstP.x, firstP.y);

    for (let i = 1; i < stroke.points.length; i++) {
      const point = stroke.points[i];
      if (!point) continue;
      const p = v.viewport.imageToViewerElementCoordinates(new OpenSeadragon.Point(point.x, point.y));
      ctx.lineTo(p.x, p.y);
    }
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.strokeStyle = stroke.color;
    ctx.lineWidth = stroke.width * currentScale;
    ctx.globalCompositeOperation = "source-over";
    ctx.stroke();
  });
};

const getCurrentScale = () => {
  if (!viewer.value) return 1;
  const p0 = viewer.value.viewport.imageToViewerElementCoordinates(new OpenSeadragon.Point(0, 0));
  const p1 = viewer.value.viewport.imageToViewerElementCoordinates(new OpenSeadragon.Point(1000, 0));
  return (p1.x - p0.x) / 1000;
};

const clearAll = () => {
  strokes.value = [];
  redraw();
};
</script>

<template>
  <div class="viewer-container relative group">
    <div ref="OSD_REF" class="osd-viewer"></div>
    <canvas
      ref="CANVAS_REF"
      class="absolute inset-0 z-10"
      :class="{ 'pointer-events-none': currentTool === 'pan', 'cursor-crosshair': currentTool !== 'pan' }"
      @mousedown="startDrawing"
      @mousemove="draw"
      @mouseup="stopDrawing"
      @mouseleave="stopDrawing"
    ></canvas>

    <div v-if="editable" class="controls__container flex items-center gap-6 px-3 py-2">
      <div class="flex items-center gap-2">
        <button
          @click="currentTool = 'pan'"
          title="Pan / Move"
          :class="{ active: currentTool === 'pan' }"
        >
          <Icon name="mdi:hand-back-right" />
        </button>
        <button
          @click="currentTool = 'brush'"
          title="Brush"
          :class="{ active: currentTool === 'brush' }"
        >
          <Icon name="mdi:pencil" />
        </button>
        <button
          @click="currentTool = 'eraser'"
          title="Eraser"
          :class="{ active: currentTool === 'eraser' }"
        >
          <Icon name="mdi:eraser" />
        </button>
      </div>

      <div class="flex items-center gap-3">
        <input type="color" v-model="settings.color" class="w-8 h-6 rounded cursor-pointer bg-transparent" />

        <div class="size__container flex flex-col gap-1 w-24">
          <label class="flex justify-between">
            {{ $t('map.controls.size') }} <span>{{ settings.width }}px</span>
          </label>
          <input type="range" v-model="settings.width" min="1" max="50" />
        </div>
      </div>
      <button @click="clearAll" title="Clear All">
        <Icon name="mdi:trash-can-outline" />
      </button>
    </div>
  </div>
</template>

<style scoped>
.viewer-container {
  width: 100%;
  height: 100%;
  max-width: 1600px;
  max-height: 800px;
  background: #111;
  margin: 0 auto;
  border: 1px solid #333;
}

.controls__container {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  z-index: 20;

  background-color: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(6px);
  border: 1px solid var(--white-8);
  border-top: none;

  .size__container {
    width: 100%;
    label {
      user-select: none;
      font-size: 10px;
      color: var(--white-40);
      text-transform: uppercase;
    }
    input[type="range"] {
      width: 100%;
    }
  }

  button {
    aspect-ratio: 1/1;
    font-size: 1rem;
    background: none;
    border: none;
    transition: all 0.15s ease-in-out;
    .icon {
      font-size: 1.6rem;
    }
  }

  button:not(:disabled) {
    cursor: pointer;
    &:hover,
    &.active {
      color: var(--white-10);
      background-color: var(--white-5);
    }
  }
}

.osd-viewer {
  width: 100%;
  height: 100%;
}
</style>
