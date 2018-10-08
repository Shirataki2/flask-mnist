from flask import Flask, jsonify, make_response
from flask import request, render_template, abort
from datetime import datetime
from PIL import Image
from binascii import a2b_base64
from io import BytesIO
from flask_cors import CORS
import tensorflow as tf
import cv2
import keras
import cgi
import numpy as np


app = Flask(__name__)
model = keras.models.load_model('./model/model.h5')
global graph
graph = tf.get_default_graph()

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
    return render_template("index.html")


@app.route('/run', methods=['POST'])
def mnist():
    data = request.json['img']
    img_str = str(data)
    if img_str:
        b64_str = img_str.split(',')[1]
        img = Image.open(BytesIO(a2b_base64(b64_str))).convert('L')
        img = np.array(img).reshape((500,500))
        img = cv2.resize(img, (28, 28))
        print(img.shape)
        img = img.reshape((1, 784)).astype(np.float32)/255.
        print(img.max())
        with graph.as_default():
            ret = model.predict(img)
        result = int(np.argmax(ret))
        print("\tPrediction Result:",result)

        Image.fromarray((img*255).reshape((28,28)).astype(np.uint8)).save('archives/%s.png'%(
            datetime.now().strftime("%Y%m%d%H%M%S"))
            )
        return make_response(jsonify({
            "result": result,
            "data": ret.tolist(),
        }))
    return make_response(jsonify({
        "result": None,
    }))



if __name__ == "__main__":
    app.run(debug=True)
