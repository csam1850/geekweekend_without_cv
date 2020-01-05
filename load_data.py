"""
load data serves for importing the image data in a format for further
processing

"""
# pylint: disable=no-member, unused-variable

import numpy as np
import cv2
import os
import glob
from PIL import Image
from utilities import crop_center, segmentation, trim, display_one  # noqa: F401, E501
from utilities import hu_moments, col_histogram, hog_features

FRUITS = ['Orange', 'Banana', 'Strawberry', 'Kiwi', 'Lemon',
          'Pineapple', 'Avocado', 'Nectarine', 'Nectarine Flat',
          'Passion Fruit', 'Apricot']


def preprocess_data(img, dim=100):
    img = crop_center(img)
    img = cv2.resize(img, (dim, dim))

    img_seg = segmentation(img)
    img_seg = trim(img_seg)
    img_seg = cv2.resize(img_seg, (dim, dim))

    img_gaus = cv2.GaussianBlur(img, (5, 5), 0)
    img_gaus = cv2.cvtColor(img_gaus, cv2.COLOR_RGB2BGR)

    img_hog = hog_features(img)
    img_hu = hu_moments(img)
    img_col = col_histogram(img)
    img = np.hstack([img_seg.flatten(), img_hog, img_hu, img_col])

    return img


def load_fruit_data(fruits, data_type, dim=100, print_n=True, k_fold=False):
    paths = []
    images = []
    labels = []
    base_path = os.getcwd()
    path = os.path.join(base_path, 'fruits-360', data_type)
    print('loading data')
    for i, f in enumerate(fruits):
        p = os.path.join(path, f)
        j = 0
        for image_path in glob.glob(os.path.join(p, "*.jpg")):
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            img = preprocess_data(img, dim=100)

            images.append(img)
            labels.append(i)
            paths.append(image_path)
            j += 1
        if(print_n):
            print("There are ", j, " ", data_type.upper(),
                  " images of ", fruits[i].upper())
    images = np.array(images)
    labels = np.array(labels)
    return images, labels


def load_single_image(image_path, dim=100):
    """
    This function loads the data of a single image scales and augments the
    image
    """
    if not isinstance(image_path, str):
        img = Image.open(image_path)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        img = preprocess_data(img, dim=100)
    else:
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        img = preprocess_data(img, dim=100)

    img = np.array([img])

    return img


load_single_image('C:\\Users\\tim.lechner\\source\\productionizing_ML_models\\application_without_cv\\fruits-360\\Test\\Strawberry\\20191208_185513.jpg')  # noqa: E501
load_single_image('C:\\Users\\tim.lechner\\source\\productionizing_ML_models\\application_without_cv\\fruits-360\\Test\\Orange\\20191214_144012.jpg')  # noqa: E501
load_single_image('C:\\Users\\tim.lechner\\source\\productionizing_ML_models\\application_without_cv\\fruits-360\\Test\\Banana\\20191208_105306.jpg')  # noqa: E501
load_single_image('C:\\Users\\tim.lechner\\source\\productionizing_ML_models\\application_without_cv\\fruits-360\\Test\\Banana\\20191214_143705.jpg')  # noqa: E501
load_single_image('C:\\Users\\tim.lechner\\source\\productionizing_ML_models\\application_without_cv\\fruits-360\\Training\\Banana\\20191214_143631.jpg')  # noqa: E501
load_single_image('C:\\Users\\tim.lechner\\source\\productionizing_ML_models\\application_without_cv\\fruits-360\\Training\\Pineapple\\20191231_131641.jpg')  # noqa: E501
load_single_image('C:\\Users\\tim.lechner\\source\\productionizing_ML_models\\application_without_cv\\fruits-360\\Training\\Avocado\\20191231_131543.jpg')  # noqa: E501
