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

# Runway ML 
# Python Socket Server Template  
#
# A python server to be used as a reference or staring point 
# when creating new models for Runway. This is just the server
# with no model dependencies
# 
# Cristóbal Valenzuela
# April - 2018
# hello@runwayml.com
# ======================================================================

import os
import json
import base64
import common
import io
import cv2
import numpy as np
from PIL import Image
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

# --- 
# Server Configurations
# This should remain unchanged for the most part
# --- 
PORT = 33000 # as a standard, port 33000 should be exposed in all docker containers
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

def main(SOME_INPUT, OPTIONS):
  '''
  This could be the main function that queries the model
  and returns something based on SOME_INPUT with OPTIONS
  '''
  return true

# --- 
# Server Routes
# This is the bare minimum for any server
# Routes can depend based on the model type and input
# This should match the meta description in models.js
# --- 

# Base route, functions a simple testing 
@app.route('/')
def index():
  return jsonify(status="200", message='DEMO_MODEL is running', query_route='/query', test_route='/test')

# Test the model with a fix to see if it's working
@app.route('/test')
def query():
  results = main()
  return jsonify(status="200", model='openpose', response=results)

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
  results = main()
  emit('update_response', {"results": results})

# Run the app
if __name__ == "__main__":
  socketio.run(app, host='0.0.0.0', port=PORT, debug=False)

# --- 
# Utils
# Utility functions to convert images
# --- 
# Take in base64 string and return PIL image
def stringToImage(base64_string):
  imgdata = base64.b64decode(base64_string)
  return Image.open(io.BytesIO(imgdata))

# Convert PIL Image to an RGB image(technically a numpy array) that's compatible with opencv
def toRGB(image):
  return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

