from flask import Flask, request, jsonify
from PIL import Image
from pyzbar.pyzbar import decode
import io
import base64
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

@app.route('/process-image', methods=['POST'])
def process_image():
    data = request.get_json()
    if 'image_base64' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    image_data = data['image_base64']
    image_data = image_data.split(",")[-1]  # Remove o prefixo da URL de dados, se presente

    try:
        decoded_image = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(decoded_image))
        decoded_objects = decode(image)
        results = [{'data': obj.data.decode('utf-8'), 'type': obj.type} for obj in decoded_objects]
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/readiness_check')
def readiness_check():
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)