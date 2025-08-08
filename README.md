# Nice Constructions & Building — Virtual Paint Preview

A web-based virtual paint preview application for Nice Constructions & Building. Upload photos of your spaces and visualize paint colors in real-time.

## Features
- Photo upload and real-time color application using OpenCV.js (k-means region selection)
- Deluxe color palette selection with virtual paint preview
- AI-powered (rule-based) color recommendations by room style
- Services section with painting offerings and eco-friendly options
- Before/after comparison slider and downloadable result

## Tech Stack
- HTML, CSS (responsive, card-based UI)
- JavaScript (Canvas, HSV blending)
- OpenCV.js (client-side image processing)

## Run Locally
- Python: `python3 -m http.server 8080`
- Node: `npx serve --single -l 8080`

Then open: `http://localhost:8080/index.html`

## Usage
1. Upload a photo and click the area to recolor.
2. Choose a color from the palette or AI recommendations.
3. Adjust Regions (K), Expand selection, and Strength as needed, then Re-segment after changing K.
4. Drag the slider to compare before/after. Download when ready.

## Notes
- All processing is local in your browser; no server upload.
- Complex scenes may require tuning K and tolerance.

## License
MIT
