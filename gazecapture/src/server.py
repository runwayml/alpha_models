import os
import json
import base64
import io
import numpy as np
from PIL import Image as PILImage
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

import features
import gaze

# ---
# Server Configurations
# This should remain unchanged for the most part
# ---

PORT = 33000 # as a standard, port 33000 should be exposed in all docker containers
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# Take in base64 string and return PIL image
def stringToImage(base64_string):
  imgdata = base64.b64decode(base64_string)
  return PILImage.open(io.BytesIO(imgdata))

# Convert PIL Image to an RGB image(technically a numpy array) that's compatible with opencv
def main(input_img):
  pil_image = stringToImage(input_img[input_img.find(",")+1:])
  bgr_image = np.array(pil_image)
  img, faces, face_features = features.extract_image_features(bgr_image)
  estimated_gazes = gaze.test_faces(img, faces, face_features)

  results = []
  for gaze_detected in estimated_gazes:
    if gaze_detected is not None:
      results.append(gaze_detected.tolist())

  parsed_results = {
    "estimated_gazes": results
  }

  return parsed_results

# Base route, functions a simple testing
@app.route('/')
def index():
  return jsonify(status="200", message='YOLO is running', query_route='/query', test_route='/test')

# Test the model with a fix to see if it's working
@app.route('/test')
def query():
  results = main(None)
  return jsonify(status="200", model='YOLO', response=results)

# When a client socket connects
@socketio.on('connect', namespace='/query')
def new_connection():
  emit('successful_connection', {"data": "connection established"})

# When a client socket disconnects
@socketio.on('disconnect', namespace='/query')
def disconnect():
  print('Client Disconnect')

# When a client sends data. This should call the main() function
@socketio.on('update_request', namespace='/query')
def new_request(request):
  results = main(request["data"])
  emit('update_response', {"results": results})

# Run the app
if __name__ == "__main__":
  socketio.run(app, host='0.0.0.0', port=PORT, debug=False)