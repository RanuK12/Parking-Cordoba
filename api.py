from flask import Flask, request, jsonify
import cv2
import numpy as np
from detect_parking import detect_parking_spaces

app = Flask(__name__)

@app.route('/check_availability', methods=['POST'])
def check_availability():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        available_spaces = detect_parking_spaces(image)
        return jsonify({'available_spaces': available_spaces})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

if __name__ == '__main__':
    app.run(debug=True)