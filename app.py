"""
This is the classifier API

"""

import pickle
import os
from flask import Flask, request, render_template, send_from_directory
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from load_data import load_single_image, FRUITS, trim
from custom_vision.load_data import load_image
from custom_vision.load_model import load_model_and_tags
from custom_vision.predict import predict_image

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Instantiate Flask App
app = Flask(__name__)
CORS(app)

# Liveness test
@app.route('/healthcheck', methods=['GET', 'POST'])
def liveness2():
    return 'API Live!', 200


@app.route('/index')
@app.route("/")
def index():
    return render_template("upload.html", fruits=FRUITS)


@app.route("/upload", methods=["POST"])
def upload():
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print("{} is the file name".format(upload.filename))
        filename = upload.filename

        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".jpeg"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not" /
                                                  " supported...")

        # crop image
        cropped_image = trim(upload)
        cropped_image = cropped_image.convert('RGB')

        # loading data in desired form
        img = load_single_image(cropped_image)

        # loading scaling data and scale
        file_path = 'models/scaler.sav'
        scaler = pickle.load(open(file_path, 'rb'))
        image_data = scaler.transform([i.flatten() for i in img])

        # loading model and predicting values
        file_path = 'models/svm_model.sav'
        svm_model = pickle.load(open(file_path, 'rb'))
        result = int(svm_model.predict(image_data))
        prediction_value = FRUITS[result]
        print(prediction_value)
        sample_image = prediction_value + '.jpg'
        prediction = {'value': prediction_value, 'sample_image': sample_image}

    return render_template("complete_display_image.html",
                           prediction=prediction,
                           fruits=FRUITS)


@app.route('/upload_cv', methods=["POST"])
def upload_cv():
    for upload in request.files.getlist("file"):

        # load model and tags
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = os.path.join(dir_path, 'custom_vision')
        labels = load_model_and_tags(dir_path)

        # Load image
        augmented_image = load_image(upload)

        # predict image
        prediction_value = predict_image(augmented_image, labels)
        print(prediction_value)

        sample_image = prediction_value + '.jpg'
        prediction = {'value': prediction_value, 'sample_image': sample_image}

    return render_template("complete_display_image.html",
                           prediction=prediction,
                           fruits=labels)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory('images', filename)


# running REST interface
# use debug=True when debugging
if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
    # app.run(host='0.0.0.0', debug=True)
