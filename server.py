from flask import Flask, jsonify, make_response
from flask import request, render_template, abort
from datetime import datetime
from PIL import Image
import glob
from binascii import a2b_base64
from io import BytesIO
from flask_cors import CORS
import tensorflow as tf
import cv2
import os
import keras
import cgi
import numpy as np

os.makedirs('archives', exist_ok=True)
app = Flask(__name__)
model = keras.models.load_model('./model/model.h5')
cnn = keras.models.load_model('./model/cnn.h5')
global graph
graph = tf.get_default_graph()
files = glob.glob('./static/imgs/*')

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


CORS(app)

@app.errorhandler(404)
def notfound(e):
    return "404: Not Found"


@app.route('/')
def index():
    print(len(files))
    return render_template("index.html")

@app.route('/change_img', methods=['POST'])
def change_img():
    idx = request.json['idx']
    idx = int(idx)
    print(idx)
    return make_response(jsonify({
            "data": files[idx]
        }))

@app.route('/dev', methods=['POST'])
def dev():
    data = request.json['img']
    name = request.json['name']
    os.makedirs('lines', exist_ok=True)
    img_str = str(data)
    if img_str:
        b64_str = img_str.split(',')[1]
        img = Image.open(BytesIO(a2b_base64(b64_str)))
        img = np.array(img).reshape((256, 256, 3))

        Image.fromarray(img.astype(np.uint8)).save('lines/%s'%name)
    return make_response(jsonify({
        "result": None,
    }))

@app.route('/run', methods=['POST'])
def mnist():
    data = request.json['img']
    img_str = str(data)
    if img_str:
        b64_str = img_str.split(',')[1]
        img = Image.open(BytesIO(a2b_base64(b64_str))).convert('L')
        img = np.array(img).reshape((256, 256))
        img = cv2.resize(img, (28, 28))
        img = img.reshape((1, 784)).astype(np.float32)/255.
        with graph.as_default():
            ret = model.predict(img)
        result = int(np.argmax(ret))
        print("\tPrediction Result:",result)

        Image.fromarray((img*255).reshape((28,28)).astype(np.uint8)).save('archives/%d_%s.png'%(
            result,
            datetime.now().strftime("%Y%m%d%H%M%S"))
            )
        return make_response(jsonify({
            "result": result,
            "data": ret.tolist(),
        }))
    return make_response(jsonify({
        "result": None,
    }))

@app.route('/run_cnn', methods=['POST'])
def mnist_cnn():
    data = request.json['img']
    img_str = str(data)
    if img_str:
        b64_str = img_str.split(',')[1]
        img = Image.open(BytesIO(a2b_base64(b64_str))).convert('L')
        img = np.array(img).reshape((256, 256))
        img = cv2.resize(img, (28, 28))
        img = img.reshape((1, 28, 28, 1)).astype(np.float32)/255.
        with graph.as_default():
            ret = cnn.predict(img)
        result = int(np.argmax(ret))
        print("\tPrediction Result:",result)
        Image.fromarray((img*255).reshape((28,28)).astype(np.uint8)).save('archives/%s_CNN_%d.png'%(
            datetime.now().strftime("%Y%m%d%H%M%S"),
            result)
            )
        return make_response(jsonify({
            "result": result,
            "data": ret.tolist(),
        }))
    return make_response(jsonify({
        "result": None,
    }))



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=40000)
