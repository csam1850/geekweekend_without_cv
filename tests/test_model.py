import os
import pickle
from load_data import load_single_image, trim, FRUITS

DIM = 100


def test_classifier(image_name, expected):
    # load image data
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(dir_path, image_name)

    # crop image and save to disk
    cropped_image = trim(image_path)
    cropped_image = cropped_image.convert('RGB')
    image_path = os.path.join(dir_path, image_name[:-4] + "_crop.jpeg")
    cropped_image.save(image_path, format='jpeg')

    # loading data from specified path
    img = load_single_image(image_path)

    # loading scaling data and scaling data
    filename = 'models/scaler.sav'
    scaler = pickle.load(open(filename, 'rb'))
    image_data = scaler.transform([i.flatten() for i in img])

    # loading model and predicting values
    filename = 'models/svm_model.sav'
    svm_model = pickle.load(open(filename, 'rb'))
    result = int(svm_model.predict(image_data))

    print(FRUITS[result])
    assert FRUITS[result] == expected


test_classifier('Orange.jpg', 'Orange')
test_classifier('Banana.jpg', 'Banana')
test_classifier('Kiwi.jpg', 'Kiwi')
test_classifier('Lemon.jpg', 'Lemon')
test_classifier('Pineapple.jpg', 'Pineapple')
test_classifier('Strawberry.jpg', 'Strawberry')
