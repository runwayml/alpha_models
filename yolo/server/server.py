# Copyright (C) 2018 Cristobal Valenzuela
#
# This file is part of RunwayML.
#
# RunwayML is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RunwayML is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RunwayML.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import json
import base64
import common
import io
import cv2
import numpy as np
from PIL import Image as PILImage
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

# Darknet
import pydarknet
from pydarknet import Detector, Image

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
def toRGB(image):
  return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

# YOLO
net = Detector(bytes("/darknet/cfg/yolov2-tiny.cfg", encoding="utf-8"), bytes("weights/yolov2-tiny.weights", encoding="utf-8"), 0, bytes("/darknet/cfg/coco.data",encoding="utf-8"))

def main(input_img):
  '''
  Run YOLO on an image
  '''

  if(input_img):
    image = stringToImage(input_img[input_img.find(",")+1:])
    image = toRGB(image)
    height, width, channels = image.shape
    img = Image(image)
    
    results = net.detect(img)
    parsed_results = []
    for cat, score, bounds in results:
      x, y, w, h = bounds
      parsed_results.append({ "cat": cat.decode("utf-8"), "score": score, "bounds": [(x - w/2)/width, (y - h/2)/height, w/width, h/height] })

    return parsed_results

  else:
    # Test with a sample image
    img = cv2.imread(os.path.join("data", "dog.jpg"))
    height, width, channels = img.shape
    img2 = Image(img)

    results = net.detect(img2)
    parsed_results = []
    for cat, score, bounds in results:
      x, y, w, h = bounds
      parsed_results.append({ "cat": cat.decode("utf-8"), "score": score, "bounds": [(x - w/2)/width, (y - h/2)/height, w/width, h/height] })
    
    return parsed_results

    # for cat, score, bounds in results:
    #   x, y, w, h = bounds
    #   cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)
    #   cv2.putText(img,str(cat.decode("utf-8")),(int(x),int(y)),cv2.FONT_HERSHEY_DUPLEX,4,(0,0,255), thickness=2)
    # cv2.imwrite(os.path.join("output",file_name), img)


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
  socketio.run(app, host='0.0.0.0', port=PORT, debug=True)