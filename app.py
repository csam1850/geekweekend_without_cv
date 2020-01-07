"""
This is the classifier API

"""
# pylint: disable=invalid-name

import pickle
import os
from flask import Flask, request, render_template, send_from_directory
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from load_data import load_single_image, FRUITS


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Instantiate Flask App
app = Flask(__name__)
CORS(app)

# Liveness test
@app.route('/healthcheck', methods=['GET', 'POST'])
def liveness2():
    '''
    simple function to check if the app is online
    '''
    return 'API Live!', 200


@app.route('/index')
@app.route("/")
def index():
    '''
    returning the html template with the start screen to upload an image
    '''
    return render_template("upload.html", fruits=FRUITS)


@app.route("/upload", methods=["POST"])
def upload():
    '''
    handling the uploaded file, predicting the fruit and sending it to the
    results html template
    '''
    print(request.files.getlist("file"))
    for image in request.files.getlist("file"):
        print("{} is the file name".format(image.filename))
        filename = image.filename

        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".jpeg"):
            print("File supported moving on...")
        else:
            render_template("Error.html",
                            message="Files uploaded are not supported...")

        # loading data in desired form
        img = load_single_image(image)

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


@app.route('/upload/<filename>', methods=['GET', 'POST'])
def send_image(filename):
    '''
    sending an image from a directory - built in flask method
    this method is used to display to predicted image on the results screen
    '''
    return send_from_directory('UPLOAD_FOLDER', filename)


# running REST interface
# use debug=True when debugging
if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
    # app.run(host='0.0.0.0', debug=True)
