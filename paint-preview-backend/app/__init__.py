from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import os
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return {'status': 'ok', 'message': 'Paint Preview Backend Ready'}

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filepath = f'/tmp/{file.filename}'
    file.save(filepath)
    return jsonify({'status': 'success', 'filepath': filepath})

@app.route('/process', methods=['POST'])
def process_image():
    data = request.json
    filepath = data.get('filepath')
    color_hex = data.get('color')
    if not filepath or not color_hex:
        return jsonify({'error': 'Missing filepath or color'}), 400
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    # Convert hex to BGR
    color_hex = color_hex.lstrip('#')
    rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    bgr = (rgb[2], rgb[1], rgb[0])
    # Read image
    img = cv2.imread(filepath)
    if img is None:
        return jsonify({'error': 'Invalid image'}), 400
    overlay = np.full(img.shape, bgr, dtype=np.uint8)
    alpha = 0.5  # Blend factor
    blended = cv2.addWeighted(img, 1 - alpha, overlay, alpha, 0)
    # Encode to base64
    _, buffer = cv2.imencode('.jpg', blended)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return jsonify({'status': 'success', 'image': img_base64})

# Image upload and processing endpoints will be added here

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)