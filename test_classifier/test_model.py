"""
the module serves for testing the classifier
"""
import os
import pickle
import warnings
from load_data import load_single_image, FRUITS

warnings.simplefilter("ignore", UserWarning)

DIM = 100


def test_classifier(image_name, expected):
    '''
    this function tests if expected and actual classification are the same
    '''
    # load image data
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(dir_path, image_name)

    # loading image
    image = load_single_image(image_path)

    # loading scaling data and scaling data
    filename = 'models/scaler.sav'
    scaler = pickle.load(open(filename, 'rb'))
    image_data = scaler.transform([i.flatten() for i in image])

    # loading model and predicting values
    filename = 'models/svm_model.sav'
    svm_model = pickle.load(open(filename, 'rb'))
    result = int(svm_model.predict(image_data))
    print(f'Expected result is {expected}')
    print(f'Actual result is {FRUITS[result]}')
    print()
    assert FRUITS[result] == expected


test_classifier('Orange.jpg', 'Orange')
test_classifier('Banana.jpg', 'Banana')
test_classifier('Kiwi.jpg', 'Kiwi')
test_classifier('Lemon.jpg', 'Lemon')
test_classifier('Pineapple.jpg', 'Pineapple')
test_classifier('Strawberry.jpg', 'Strawberry')
