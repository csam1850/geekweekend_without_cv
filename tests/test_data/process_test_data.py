"""
This module serves the preprocessing of sample images used to train and
test the classification algorithms. Images are cropped and it can be checked
that images are still valid for training. It is also possible to reduce the
size for the custom vision classifier.

"""
# pylint: disable=no-member, unused-variable


import os
import glob
import cv2
from load_data import trim


def preprocess_image_for_ml_algo():
    base_path = os.getcwd()
    dir_path = os.path.join(base_path, 'tests', 'test_data')
    print(base_path)

    for i, f in enumerate(os.listdir(dir_path)):
        image_dir_path = os.path.join(dir_path, f)
        print(image_dir_path)

        for image_path in glob.glob(os.path.join(image_dir_path, "*.jfif")):

            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (100, 100))
            base_path = '.'.join([image_path.split('.')[0],
                                  image_path.split('.')[1]])
            new_path = '.'.join([base_path, image_path.split('.')[2]])
            cv2.imwrite(new_path, img)

            # crop image and save to disk
            cropped_image = trim(new_path)
            cropped_image = cropped_image.convert('RGB')
            new_path = base_path + '_cropped' + ".jpeg"
            cropped_image.save(new_path, format='jpeg')
            pass


def preprocess_image_for_custom_vision():
    base_path = os.getcwd()
    dir_path = os.path.join(base_path, 'tests', 'test_data')
    print(base_path)

    for i, f in enumerate(os.listdir(dir_path)):
        image_dir_path = os.path.join(dir_path, f)
        print(image_dir_path)

        for image_path in glob.glob(os.path.join(image_dir_path, "*.jpg")):
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (250, 250))
            base_path = '.'.join([image_path.split('.')[0],
                                 image_path.split('.')[1]])
            new_path = '.'.join([base_path, image_path.split('.')[2]])
            cv2.imwrite(new_path, img)
