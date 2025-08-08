/* Globals */
const state = {
  cvReady: false,
  image: null,
  width: 0,
  height: 0,
  originalImageData: null,
  labels: null, // Uint32Array of cluster ids per pixel
  centroids: [], // [{r,g,b}]
  selectedLabelIds: new Set(),
  selectedColor: '#2E7D32',
  k: 5,
  tolerance: 20,
  strength: 70,
};

/* Elements */
const els = {};
function qs(sel) { return document.querySelector(sel); }
function byId(id) { return document.getElementById(id); }

/* Palette Data */
const DELUXE_PALETTE = [
  { name: 'Construction Green', hex: '#2E7D32' },
  { name: 'Warm Orange', hex: '#FF6F00' },
  { name: 'Trust Blue', hex: '#1976D2' },
  { name: 'Approval Green', hex: '#4CAF50' },
  { name: 'Charcoal', hex: '#212121' },
  { name: 'Soft Sand', hex: '#D7CCC8' },
  { name: 'Warm Gray', hex: '#BDBDBD' },
  { name: 'Ivory Mist', hex: '#F5F5F5' },
  { name: 'Sunlit Beige', hex: '#E0C097' },
  { name: 'Urban Slate', hex: '#455A64' },
  { name: 'Harbor Blue', hex: '#3F51B5' },
  { name: 'Terracotta', hex: '#D96C3F' },
  { name: 'Olive Grove', hex: '#8E9A5B' },
  { name: 'Muted Sage', hex: '#9CCC65' },
  { name: 'Dusty Rose', hex: '#C48B9F' },
  { name: 'Deep Teal', hex: '#00695C' },
  { name: 'Storm Cloud', hex: '#607D8B' },
  { name: 'Crisp White', hex: '#FFFFFF' },
  { name: 'Stone', hex: '#9E9E9E' },
  { name: 'Coffee', hex: '#6D4C41' },
];

/* AI Trends (rule-based) */
const STYLE_RECOMMENDATIONS = {
  modern: [ '#FAFAFA', '#212121', '#1976D2', '#BDBDBD', '#2E7D32' ],
  cozy: [ '#E0C097', '#6D4C41', '#C48B9F', '#D96C3F', '#F5F5F5' ],
  minimalist: [ '#FFFFFF', '#FAFAFA', '#BDBDBD', '#9E9E9E', '#212121' ],
  industrial: [ '#607D8B', '#455A64', '#9E9E9E', '#3F51B5', '#212121' ],
  bohemian: [ '#C48B9F', '#D96C3F', '#8E9A5B', '#00695C', '#F5F5F5' ],
  classic: [ '#FFFFFF', '#212121', '#3F51B5', '#4CAF50', '#FF6F00' ],
};

/* Utils */
function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
function hexToRgb(hex) {
  const m = hex.replace('#','');
  const bigint = parseInt(m.length === 3 ? m.split('').map(c=>c+c).join('') : m, 16);
  return { r: (bigint >> 16) & 255, g: (bigint >> 8) & 255, b: bigint & 255 };
}
function rgbToHsv(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  let h, s, v = max;
  const d = max - min;
  s = max === 0 ? 0 : d / max;
  if (max === min) {
    h = 0; // achromatic
  } else {
    switch (max) {
      case r: h = (g - b) / d + (g < b ? 6 : 0); break;
      case g: h = (b - r) / d + 2; break;
      case b: h = (r - g) / d + 4; break;
    }
    h /= 6;
  }
  return { h, s, v };
}
function hsvToRgb(h, s, v) {
  let r, g, b;
  let i = Math.floor(h * 6);
  let f = h * 6 - i;
  let p = v * (1 - s);
  let q = v * (1 - f * s);
  let t = v * (1 - (1 - f) * s);
  switch (i % 6) {
    case 0: r = v, g = t, b = p; break;
    case 1: r = q, g = v, b = p; break;
    case 2: r = p, g = v, b = t; break;
    case 3: r = p, g = q, b = v; break;
    case 4: r = t, g = p, b = v; break;
    case 5: r = v, g = p, b = q; break;
  }
  return { r: Math.round(r * 255), g: Math.round(g * 255), b: Math.round(b * 255) };
}

function onReady() {
  // Elements
  els.fileInput = byId('fileInput');
  els.browseBtn = byId('browseBtn');
  els.dropzone = byId('dropzone');
  els.originalCanvas = byId('originalCanvas');
  els.resultCanvas = byId('resultCanvas');
  els.compareOverlay = byId('compareOverlay');
  els.compareSlider = byId('compareSlider');
  els.kInput = byId('kInput');
  els.toleranceInput = byId('toleranceInput');
  els.resegmentBtn = byId('resegmentBtn');
  els.resetSelectionBtn = byId('resetSelectionBtn');
  els.strengthInput = byId('strengthInput');
  els.downloadBtn = byId('downloadBtn');
  els.paletteGrid = byId('paletteGrid');
  els.styleSelect = byId('styleSelect');
  els.recommendBtn = byId('recommendBtn');
  els.recommendations = byId('recommendations');

  byId('year').textContent = new Date().getFullYear();

  // Upload interactions
  els.browseBtn.addEventListener('click', () => els.fileInput.click());
  els.fileInput.addEventListener('change', handleFiles);
  ;['dragenter','dragover'].forEach(evt => els.dropzone.addEventListener(evt, e => { e.preventDefault(); e.stopPropagation(); els.dropzone.classList.add('drag'); }));
  ;['dragleave','drop'].forEach(evt => els.dropzone.addEventListener(evt, e => { e.preventDefault(); e.stopPropagation(); els.dropzone.classList.remove('drag'); }));
  els.dropzone.addEventListener('drop', e => {
    if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
      loadImageFile(e.dataTransfer.files[0]);
    }
  });

  // Compare slider
  els.compareSlider.addEventListener('input', () => {
    const val = parseInt(els.compareSlider.value, 10);
    els.compareOverlay.style.width = val + '%';
  });

  // Tools
  els.kInput.addEventListener('input', () => state.k = parseInt(els.kInput.value, 10));
  els.toleranceInput.addEventListener('input', () => state.tolerance = parseInt(els.toleranceInput.value, 10));
  els.strengthInput.addEventListener('input', () => { state.strength = parseInt(els.strengthInput.value, 10); if (state.image) applyColor(); });
  els.resegmentBtn.addEventListener('click', () => { if (state.image) segmentImage(); });
  els.resetSelectionBtn.addEventListener('click', () => { state.selectedLabelIds.clear(); applyColor(); });
  els.downloadBtn.addEventListener('click', downloadResult);

  // Canvas click to select cluster
  els.resultCanvas.addEventListener('click', onCanvasClick);

  // Palette and AI
  renderPalette();
  els.recommendBtn.addEventListener('click', renderRecommendations);
  renderRecommendations();
}

document.addEventListener('DOMContentLoaded', onReady);

// OpenCV runtime ready
if (typeof cv !== 'undefined') {
  cv['onRuntimeInitialized'] = () => {
    state.cvReady = true;
  };
} else {
  // If script loads later, set on window
  window.Module = {
    onRuntimeInitialized() {
      state.cvReady = true;
    }
  };
}

/* Upload */
function handleFiles(e) {
  const file = e.target.files && e.target.files[0];
  if (file) loadImageFile(file);
}

function loadImageFile(file) {
  const reader = new FileReader();
  reader.onload = () => {
    const img = new Image();
    img.onload = () => {
      setupCanvases(img);
      state.image = img;
      extractOriginalImageData();
      waitForCvAndSegment();
    };
    img.src = reader.result;
  };
  reader.readAsDataURL(file);
}

function setupCanvases(img) {
  const maxW = 1200;
  const scale = img.width > maxW ? maxW / img.width : 1;
  state.width = Math.round(img.width * scale);
  state.height = Math.round(img.height * scale);
  const canvases = [els.originalCanvas, els.resultCanvas];
  canvases.forEach(c => { c.width = state.width; c.height = state.height; });
  els.compareOverlay.style.width = '50%';
  const ctx = els.originalCanvas.getContext('2d');
  ctx.clearRect(0,0,state.width,state.height);
  ctx.drawImage(img, 0, 0, state.width, state.height);
  const rctx = els.resultCanvas.getContext('2d');
  rctx.clearRect(0,0,state.width,state.height);
  rctx.drawImage(img, 0, 0, state.width, state.height);
}

function extractOriginalImageData() {
  const ctx = els.originalCanvas.getContext('2d');
  state.originalImageData = ctx.getImageData(0, 0, state.width, state.height);
}

function waitForCvAndSegment() {
  if (state.cvReady) {
    segmentImage();
  } else {
    setTimeout(waitForCvAndSegment, 100);
  }
}

/* Segmentation using OpenCV k-means */
function segmentImage() {
  if (!state.originalImageData) return;
  const { data } = state.originalImageData;
  const sampleCount = state.width * state.height;

  // Build samples Nx3 float32
  const samples = new cv.Mat(sampleCount, 3, cv.CV_32F);
  for (let i = 0; i < sampleCount; i++) {
    const idx = i * 4;
    samples.floatPtr(i)[0] = data[idx + 0]; // R
    samples.floatPtr(i)[1] = data[idx + 1]; // G
    samples.floatPtr(i)[2] = data[idx + 2]; // B
  }

  const K = state.k;
  const labels = new cv.Mat();
  const criteria = new cv.TermCriteria(cv.TermCriteria_EPS + cv.TermCriteria_MAX_ITER, 20, 1.0);
  const attempts = 1;
  const flags = cv.KMEANS_PP_CENTERS;
  const centers = new cv.Mat();
  cv.kmeans(samples, K, labels, criteria, attempts, flags, centers);

  // Save labels and centroids
  const labelsArr = new Uint32Array(sampleCount);
  for (let i = 0; i < sampleCount; i++) labelsArr[i] = labels.intAt(i, 0);
  state.labels = labelsArr;
  state.centroids = [];
  for (let k = 0; k < K; k++) {
    const r = centers.floatAt(k, 0);
    const g = centers.floatAt(k, 1);
    const b = centers.floatAt(k, 2);
    state.centroids.push({ r, g, b });
  }

  samples.delete(); labels.delete(); centers.delete();

  // Reset selection
  state.selectedLabelIds.clear();
  applyColor();
}

/* Selection by click */
function onCanvasClick(evt) {
  if (!state.labels) return;
  const rect = els.resultCanvas.getBoundingClientRect();
  const x = Math.floor((evt.clientX - rect.left) * (state.width / rect.width));
  const y = Math.floor((evt.clientY - rect.top) * (state.height / rect.height));
  const idx = y * state.width + x;
  const label = state.labels[idx];

  // Toggle selection with shift, otherwise set selection
  if (evt.shiftKey) {
    if (state.selectedLabelIds.has(label)) state.selectedLabelIds.delete(label); else state.selectedLabelIds.add(label);
  } else {
    state.selectedLabelIds.clear();
    state.selectedLabelIds.add(label);
  }

  // Expand selection based on centroid similarity
  const tol = state.tolerance; // 0-100
  if (tol > 0) {
    const base = state.centroids[label];
    const baseHsv = rgbToHsv(base.r, base.g, base.b);
    for (let k = 0; k < state.centroids.length; k++) {
      if (k === label) continue;
      const c = state.centroids[k];
      const hsv = rgbToHsv(c.r, c.g, c.b);
      const hueDiff = Math.min(Math.abs(hsv.h - baseHsv.h), 1 - Math.abs(hsv.h - baseHsv.h));
      const satDiff = Math.abs(hsv.s - baseHsv.s);
      const score = (hueDiff * 100) * 0.7 + (satDiff * 100) * 0.3;
      if (score <= tol) state.selectedLabelIds.add(k);
    }
  }

  applyColor();
}

/* Apply color to selected regions */
function applyColor() {
  if (!state.originalImageData) return;
  const src = state.originalImageData.data;
  const dstCtx = els.resultCanvas.getContext('2d');
  const out = dstCtx.createImageData(state.width, state.height);
  const outData = out.data;

  const strength = clamp(state.strength / 100, 0, 1); // 0..1
  const { r: tr, g: tg, b: tb } = hexToRgb(state.selectedColor);
  const targetHsv = rgbToHsv(tr, tg, tb);

  const selected = state.selectedLabelIds;
  const labels = state.labels;

  for (let i = 0; i < state.width * state.height; i++) {
    const si = i * 4;
    const r = src[si + 0];
    const g = src[si + 1];
    const b = src[si + 2];

    if (labels && selected.size > 0 && !selected.has(labels[i])) {
      outData[si + 0] = r;
      outData[si + 1] = g;
      outData[si + 2] = b;
      outData[si + 3] = 255;
      continue;
    }

    const hsv = rgbToHsv(r, g, b);
    const newH = targetHsv.h;
    const newS = targetHsv.s * strength + hsv.s * (1 - strength);
    const newV = hsv.v; // keep luminance/value to preserve texture
    const rgb = hsvToRgb(newH, newS, newV);

    // Blend with original for smoother result
    outData[si + 0] = Math.round(rgb.r * strength + r * (1 - strength));
    outData[si + 1] = Math.round(rgb.g * strength + g * (1 - strength));
    outData[si + 2] = Math.round(rgb.b * strength + b * (1 - strength));
    outData[si + 3] = 255;
  }

  dstCtx.putImageData(out, 0, 0);
}

/* Download */
function downloadResult() {
  const link = document.createElement('a');
  link.download = 'ncb-virtual-paint.png';
  link.href = els.resultCanvas.toDataURL('image/png');
  link.click();
}

/* Palette */
function renderPalette() {
  els.paletteGrid.innerHTML = '';
  DELUXE_PALETTE.forEach((c) => {
    const item = document.createElement('button');
    item.className = 'palette-item';
    item.setAttribute('role', 'listitem');
    item.innerHTML = `
      <div class="palette-swatch" style="background:${c.hex}"></div>
      <div class="palette-meta">
        <div class="name">${c.name}</div>
        <div class="hex">${c.hex}</div>
      </div>
    `;
    item.addEventListener('click', () => {
      state.selectedColor = c.hex;
      applyColor();
    });
    els.paletteGrid.appendChild(item);
  });
}

/* AI Recommendations */
function renderRecommendations() {
  const style = els.styleSelect.value;
  const palette = STYLE_RECOMMENDATIONS[style] || [];
  els.recommendations.innerHTML = '';

  // Create a couple of combo cards using permutations
  const combos = [palette.slice(0, 5), palette.slice().reverse().slice(0, 5)];
  combos.forEach((colors, idx) => {
    const card = document.createElement('div');
    card.className = 'reco-card';
    const title = style.charAt(0).toUpperCase() + style.slice(1);
    card.innerHTML = `
      <div class="reco-title"><strong>${title} ${idx === 0 ? 'Set A' : 'Set B'}</strong></div>
      <div class="reco-swatches">${colors.map(h => `<div class="reco-swatch" style="background:${h}"></div>`).join('')}</div>
      <div class="reco-actions">
        <button class="btn" data-idx="0">Preview Primary</button>
        <button class="btn ghost" data-idx="1">Preview Alt</button>
      </div>
    `;
    const buttons = card.querySelectorAll('button');
    buttons[0].addEventListener('click', () => { state.selectedColor = colors[0]; applyColor(); });
    buttons[1].addEventListener('click', () => { state.selectedColor = colors[1] || colors[0]; applyColor(); });
    els.recommendations.appendChild(card);
  });
}