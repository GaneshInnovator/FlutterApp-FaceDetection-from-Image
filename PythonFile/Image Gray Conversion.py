from flask import Flask, request, jsonify
import base64
from PIL import Image
import io

app = Flask(__name__)

def convert_to_grayscale(image_file):
    # Open the image file
    image = Image.open(image_file)
    # Convert the image to grayscale
    grayscale_image = image.convert("L")
    # Save the grayscale image to a bytes buffer
    buffer = io.BytesIO()
    grayscale_image.save(buffer, format="JPEG")
    return buffer.getvalue()

@app.route('/process-image', methods=['POST'])
def process_image():
    file = request.files.get('image')
    if file:
        # Convert image to grayscale
        processed_image = convert_to_grayscale(file)
        # Encode the processed image as base64
        processed_image_base64 = base64.b64encode(processed_image).decode('utf-8')
        return jsonify({'processedImage': processed_image_base64})
    else:
        return jsonify({'error': 'No image provided'}), 400

if __name__ == '__main__':
    app.run(host="192.168.177.206", port=5000, debug=True)
