import React from 'react';
import './App.css';

const COLORS = [
  '#2E7D32', // construction green
  '#FF6F00', // warm orange
  '#FAFAFA', // light grey
  '#212121', // charcoal
  '#1976D2', // trust blue
  '#4CAF50', // approval green
  '#FFFFFF', '#F5F5F5', '#BDBDBD', '#E0E0E0', '#FFD600', '#D32F2F', '#0288D1', '#388E3C', '#FBC02D', '#7B1FA2', '#C51162', '#00B8D4', '#AEEA00', '#FFAB00', '#6D4C41', '#263238'
];

function App() {
  return (
    <div className="main-bg">
      <header className="app-header">
        <h1>Nice Constructions & Building - Virtual Paint Preview</h1>
      </header>
      <div className="card-grid">
        <div className="card upload-card">
          <h2>1. Upload Your Space</h2>
          <div className="upload-placeholder">[Upload Component]</div>
        </div>
        <div className="card palette-card">
          <h2>2. Choose a Color</h2>
          <div className="palette-grid">
            {COLORS.map(color => (
              <div key={color} className="color-swatch" style={{ background: color }}></div>
            ))}
          </div>
        </div>
        <div className="card preview-card">
          <h2>3. Preview</h2>
          <div className="preview-placeholder">[Preview Area]</div>
        </div>
      </div>
    </div>
  );
}

export default App;
