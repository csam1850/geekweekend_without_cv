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

FRUITS = ['Orange', 'Banana', 'Strawberry', 'Kiwi', 'Lemon',
          'Pineapple', 'Avocado', 'Nectarine', 'Nectarine Flat',
          'Passion Fruit', 'Apricot']


def crop_center(image):
    h, w = image.shape[:2]
    min_dim = min(w, h)
    startx = w // 2 - (min_dim // 2)
    starty = h // 2 - (min_dim // 2)
    return image[starty:starty+min_dim, startx:startx+min_dim]


def load_fruit_data(fruits, data_type, dim=100, print_n=True, k_fold=False):
    paths = []
    images = []
    labels = []
    data_types = ['Training', 'Test']
    if not k_fold:
        base_path = os.getcwd()
        path = os.path.join(base_path, 'fruits-360', data_type)
        print('loading data')
        for i, f in enumerate(fruits):
            p = os.path.join(path, f)
            j = 0
            for image_path in glob.glob(os.path.join(p, "*.jpg")):
                img = cv2.imread(image_path, cv2.IMREAD_COLOR)
                img = crop_center(img)
                img = cv2.resize(img, (dim, dim))
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
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
    else:
        for dtype in data_types:
            path = os.path.join(base_path, dtype)
            for i, f in enumerate(fruits):
                p = os.path.join(path, f)
                j = 0
                for image_path in glob.glob(os.path.join(p, "*.jpg")):
                    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
                    img = crop_center(img)
                    img = cv2.resize(img, (dim, dim))
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    images.append(img)
                    labels.append(i)
                    j += 1
        images = np.array(images)
        labels = np.array(labels)
        return images, labels


# def load_full_dataset():
#     fruits = []
#     base_path = os.getcwd()
#     for fruit_path in glob.glob(os.path.join(base_path, 'fruits-360',
#                                              "Training", "*")):
#         fruit = fruit_path.split("/")[-1]
#         fruits.append(fruit)
#     return fruits


def load_single_image(image_path, dim=100):
    """
    This function load the data of a single image and scales it to the right
    format
    """
    if not isinstance(image_path, str):
        img = Image.open(image_path)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    else:
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img = crop_center(img)
    img = cv2.resize(img, (dim, dim))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = np.array([img])

    return img
