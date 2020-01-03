"""
load data serves for importing the image data in a format for further
processing

"""
# pylint: disable=no-member, unused-variable

import numpy as np
import cv2
import os
import glob
import matplotlib.pyplot as plt
from PIL import Image, ImageChops

FRUITS = ['Orange', 'Banana', 'Strawberry', 'Kiwi', 'Lemon',
          'Pineapple', 'Avocado', 'Nectarine', 'Nectarine Flat',
          'Passion Fruit', 'Apricot']


def load_fruit_data(fruits, data_type, dim=100, print_n=False, k_fold=False):
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
        img = cv2.cvtColor(np.array(image_path), cv2.COLOR_RGB2BGR)
    else:
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (dim, dim))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = np.array([img])

    return img


def trim(path):
    im = Image.open(path)
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    # Bounding box given as a 4-tuple defining the left, upper, right, and
    # lower pixel coordinates.
    # If the image is completely empty, this method returns None.
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        return im


def class_number(y):
    v = []
    i = 0
    count = 0
    for index in y:
        if(index == i):
            count += 1
        else:
            v.append(count)
            count = 1
            i += 1
    v.append(count)
    return v


def plot_image_grid(images, nb_rows, nb_cols, figsize=(15, 15)):
    assert len(images) == nb_rows*nb_cols, "Number of images should be the "\
                                           "same as (nb_rows*nb_cols)"
    fig, axs = plt.subplots(nb_rows, nb_cols, figsize=figsize)

    n = 0
    for i in range(0, nb_rows):
        for j in range(0, nb_cols):
            axs[i, j].axis('off')
            axs[i, j].imshow(images[n])
            n += 1
