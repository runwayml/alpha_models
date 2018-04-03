import os
import json
import base64
import common
import io
import cv2
import time
import numpy as np
from PIL import Image
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from estimator import TfPoseEstimator
from networks import get_graph_path, model_wh

# Server configs
PORT = 33000
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

HUMAN_COCO_PART = {
  0: 'Nose',
  1: 'Neck',
  2: 'Right_Shoulder',
  3: 'Right_Elbow',
  4: 'Right_Wrist',
  5: 'Left_Shoulder',
  6: 'Left_Elbow',
  7: 'Left_Wrist',
  8: 'Right_Hip',
  9: 'Right_Knee',
  10: 'Right_Ankle',
  11: 'Left_Hip',
  12: 'Left_Knee',
  13: 'Left_Ankle',
  14: 'Right_Eye',
  15: 'Left_Eye',
  16: 'Right_Ear',
  17: 'Left_Ear',
  18: 'Background',
}

def current_time():
  return int(round(time.time() * 1000))

# Hide warning messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Take in base64 string and return PIL image
def stringToImage(base64_string):
  imgdata = base64.b64decode(base64_string)par
  return Image.open(io.BytesIO(imgdata))

# convert PIL Image to an RGB image( technically a numpy array ) that's compatible with opencv
def toRGB(image):
  return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

# load the graph
e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(432, 368))

def main(input_img, model, e):
  '''
  Query the model given an image
  '''
  if(input_img):
    image = stringToImage(input_img[input_img.find(",")+1:])
    image = toRGB(image)

    if(model == None):
      model = 'mobilenet_thin'

    humans = e.inference(image)
    coords = []
    for human in humans:
      coords.append([[HUMAN_COCO_PART[k], b.x, b.y] for k, b in human.body_parts.items()])

    outdata = {
      'humans': coords
    }
    return outdata

  else:
    # Test with a sample image
    image = common.read_imgfile('./images/p1.jpg', None, None)
    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(432, 368))
    humans = e.inference(image)
    coords = []
    for human in humans:
      coords.append([[HUMAN_COCO_PART[k], b.x, b.y] for k, b in human.body_parts.items()])

    outdata = {
      'humans': coords
    }
    return outdata


# Server routes
@app.route('/')
def index():
  return jsonify(status="200", message='openpose is running', query_route='/query', test_route='/test')

@app.route('/test')
def query():
  start_ms = current_time()
  results = main(None, None, e)
  return jsonify(status="200", model='openpose', response=results)

@socketio.on('connect', namespace='/query')
def new_connection():
  print('got new connection')
  #emit('successful_connection', {"data": "yes!!"})

@socketio.on('disconnect', namespace='/query')
def disconnect():
  print('client disconnect')

@socketio.on('update_request', namespace='/query')
def new_request(request):
  start_ms = current_time()
  results = main(request["data"], request["model"], e)
  emit('update_response', {"results": results})

if __name__ == "__main__":
  socketio.run(app, host='0.0.0.0', port=PORT, debug=True)
