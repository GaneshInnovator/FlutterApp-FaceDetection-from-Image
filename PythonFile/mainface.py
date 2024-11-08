from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)

# Load a pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces_and_draw_rectangle(image_file):
    # Read the image
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Encode the image to base64
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

@app.route('/process-image', methods=['POST'])
def process_image():
    file = request.files.get('image')
    if file:
        # Process the image for face detection
        processed_image_base64 = detect_faces_and_draw_rectangle(file)
        
        return jsonify({'processedImage': processed_image_base64})
    else:
        return jsonify({'error': 'No image provided'}), 400

if __name__ == '__main__':
    app.run(host="192.168.177.206", port=5000, debug=True)
