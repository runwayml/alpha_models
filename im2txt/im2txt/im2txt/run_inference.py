# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
import base64
import tensorflow as tf
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from im2txt import configuration
from im2txt import inference_wrapper
from im2txt.inference_utils import caption_generator
from im2txt.inference_utils import vocabulary

# Server configs
PORT = 33000
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# Model Paths
CHECKPOINTS_PATH = '/root/im2txt_pretrained/model.ckpt-2000000'
VOCAB_FILE = '/root/im2txt_pretrained/word_counts.txt'
DEMO_FILE = 'imgs/bikes.jpg'

# Hide warning messages
tf.logging.set_verbosity(tf.logging.ERROR)

# Build the inference graph.
g = tf.Graph()
with g.as_default():
  model = inference_wrapper.InferenceWrapper()
  restore_fn = model.build_graph_from_config(configuration.ModelConfig(), CHECKPOINTS_PATH )
g.finalize()

# Create the vocabulary.
vocab = vocabulary.Vocabulary(VOCAB_FILE)

def main(input_img):

  image = input_img[input_img.find(",")+1:]
  image = base64.decodestring(image)
  #print(image_decoded)

  with tf.Session(graph=g) as sess:
    # Load the model from checkpoint.
    restore_fn(sess)
    generator = caption_generator.CaptionGenerator(model, vocab)

    # Use a demo image
    #with tf.gfile.GFile(DEMO_FILE, "r") as f:
      #image = f.read()
    
    captions = generator.beam_search(sess, image)
    
    results = []
    for i, caption in enumerate(captions):
      # Ignore begin and end words.
      sentence = [vocab.id_to_word(w) for w in caption.sentence[1:-1]]
      sentence = " ".join(sentence)
      results.append({
        "caption": sentence,
        "prob": math.exp(caption.logprob)
      })

    return results

# Server routes
@app.route('/')
def index():
  return jsonify(status="200", message='im2text Running', query_route='/query')

@app.route('/query_once')
def query(input_img):
  results = main(input_img["data"])
  return jsonify(status="200", model='im2text', response=results)

@socketio.on('connect', namespace='/query')
def new_connection():
  print('got new connection')
  #emit('successful_connection', {"data": "yes!!"})

@socketio.on('disconnect', namespace='/query')
def disconnect():
  print('client disconnect')

@socketio.on('update_request', namespace='/query')
def new_request(input_img):
  results = main(input_img["data"])
  emit('update_response', {"results": results})

if __name__ == "__main__":
  socketio.run(app, host='0.0.0.0', port=PORT, debug=True)
