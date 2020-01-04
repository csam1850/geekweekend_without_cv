import os
import pickle
from load_data import load_single_image, trim, FRUITS
import warnings

warnings.simplefilter("ignore", UserWarning)

DIM = 100


def test_classifier(image_name, expected):
    # load image data
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(dir_path, image_name)

    # crop image
    image = trim(image_path)
    image = image.convert('RGB')

    # loading image
    img = load_single_image(image)

    # loading scaling data and scaling data
    filename = 'models/scaler.sav'
    scaler = pickle.load(open(filename, 'rb'))
    image_data = scaler.transform([i.flatten() for i in img])

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
