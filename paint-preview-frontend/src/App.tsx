import React, { useRef, useState } from 'react';
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

const BACKEND_URL = 'http://localhost:5000';

function PhotoUpload({ onUpload }: { onUpload: (filepath: string, preview: string) => void }) {
  const fileInput = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    setUploading(true);
    setError(null);
    const formData = new FormData();
    formData.append('image', file);
    try {
      const res = await fetch(`${BACKEND_URL}/upload`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (data.status === 'success') {
        const reader = new FileReader();
        reader.onload = () => {
          onUpload(data.filepath, reader.result as string);
        };
        reader.readAsDataURL(file);
      } else {
        setError(data.error || 'Upload failed');
      }
    } catch (err) {
      setError('Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-component">
      <input
        type="file"
        accept="image/*"
        style={{ display: 'none' }}
        ref={fileInput}
        onChange={handleFileChange}
      />
      <button className="upload-btn" onClick={() => fileInput.current?.click()} disabled={uploading}>
        {uploading ? 'Uploading...' : 'Choose Photo'}
      </button>
      {error && <div className="upload-error">{error}</div>}
    </div>
  );
}

function App() {
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);
  const [previewImg, setPreviewImg] = useState<string | null>(null);

  return (
    <div className="main-bg">
      <header className="app-header">
        <h1>Nice Constructions & Building - Virtual Paint Preview</h1>
      </header>
      <div className="card-grid">
        <div className="card upload-card">
          <h2>1. Upload Your Space</h2>
          <PhotoUpload onUpload={(filepath, preview) => { setUploadedFile(filepath); setPreviewImg(preview); }} />
          {previewImg && <img src={previewImg} alt="Uploaded preview" className="uploaded-preview" />}
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
