# from unittest import result
import flask
# import numpy as np
from PIL import Image, ExifTags
from keras import backend as K
import numpy as np
from keras import models
from time import perf_counter


app = flask.Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

def load():
    model = models.load_model('./model.h5')
    return model

@app.route("/help", methods = ["GET"])
def help():
    response = {"Content-Type": "application/json", 'help': None}
    if flask.request.method == "GET":
        msg = 'exp. curl -F "file=[filename].jpg" "http://localhost:5000/predict/"'
        response["help"] = msg
    return flask.jsonify(response)

def allowed_file(filename):
    """画像型の拡張子になっているか確認する"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def transform_img(img):
    """読み込んだimageのshapeをMNISTのshape(28, 28)にする"""
    img = img.convert("L")
    img = np.resize(img, (28,28,1))
    img_array = np.array(img)
    img_array = img_array.reshape(1,28,28,1)
    return img_array

def deal_rotation(img):
    """postした画像が回転してしまった場合、元に戻す"""

    for orientation in ExifTags.TAGS.keys() : 
        if ExifTags.TAGS[orientation]=='Orientation' : break 
    exif=dict(img._getexif().items())
    if   exif[orientation] == 3 : 
        img=img.rotate(180, expand=True)
    elif exif[orientation] == 6 : 
        img=img.rotate(270, expand=True)
    elif exif[orientation] == 8 : 
        img=img.rotate(90, expand=True)
    return img


model = load()

response = {"Content-Type": "application/json",
            "result": None, 
            "probability": None,
            "progress_time": None
            }

@app.route("/predict", methods=["POST"])
def predict():
    progress_start = perf_counter()  
    if flask.request.method == "POST":
        if flask.request.files["file"]:
            K.clear_session()
            img = Image.open(flask.request.files["file"])
            # img = deal_rotation(img)
            img_array = transform_img(img)
            result = model.predict(img_array,verbose=0)
            response["result"] = str(np.argmax(result))
            response["probability"] = str(np.max(result))
            progress_end = perf_counter()  
            response["progress_time"] = '{:.03f}'.format((progress_end - progress_start) * 10**3)
            # result = 0
    return flask.jsonify(response)


if __name__ == '__main__':
    app.run()