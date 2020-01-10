"""
in this module are helper functions implemented
"""
# pylint: disable=no-member, unused-variable, expression-not-assigned
# pylint: disable=invalid-name

import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageChops
from skimage.feature import hog
from skimage.color import rgb2grey


def display_one(a, title="Original"):
    '''
    displaying the image - useful for debugging and to look in the engine
    '''
    plt.imshow(a), plt.title(title)
    plt.xticks([]), plt.yticks([])
    plt.show()


def crop_center(image):
    '''
    this function crops the center of an image, if the length and width are not
    identical
    '''
    h, w = image.shape[:2]
    min_dim = min(w, h)
    startx = w // 2 - (min_dim // 2)
    starty = h // 2 - (min_dim // 2)
    return image[starty:starty+min_dim, startx:startx+min_dim]


def trim(image):
    '''
    this methods crops the image if there is a white margin around the image
    in a squared format - it is useful for centering an image but stability of
    method is limited
    '''
    img = Image.fromarray(image)
    bg = Image.new(img.mode, img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    # Bounding box given as a 4-tuple defining the left, upper, right, and
    # lower pixel coordinates.
    # If the image is completely empty, this method returns None.
    bbox = diff.getbbox()
    # display_one(np.array(img))

    if bbox:
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        diff = abs(w - h)
        if w < h:
            startw = bbox[0] - diff // 2
            endw = bbox[2] + diff // 2
            starth = bbox[0]
            endh = bbox[3]

        else:
            starth = bbox[1] - diff // 2
            endh = bbox[3] + diff // 2
            startw = bbox[0]
            endw = bbox[2]

        bbox = (startw, starth, endw, endh)
        # display_one(np.array(img.crop(bbox)), 'cropped')
        return cv2.cvtColor(np.array(img.crop(bbox)), cv2.COLOR_RGB2BGR)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def hog_features(image):
    '''
    this method extracts hog features
    '''
    # convert image to greyscale
    grey_image = rgb2grey(image)
    # get HOG features from greyscale image
    hog_feat = hog(grey_image, block_norm='L2-Hys', pixels_per_cell=(16, 16))
    return hog_feat


# feature-descriptor-1: Hu Moments
def hu_moments(image):
    '''
    this methods extracts hu moments
    '''
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    feature = cv2.HuMoments(cv2.moments(image)).flatten()
    return feature


# feature-descriptor-3: Color Histogram
def col_histogram(image, bins=8):
    '''
    this method generates a color histogram of the image
    '''
    # convert the image to HSV color-space
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # compute the color histogram
    hist = cv2.calcHist([image], [0, 1, 2], None, [bins, bins, bins],
                        [0, 256, 0, 256, 0, 256])
    # normalize the histogram
    cv2.normalize(hist, hist)

    # return the histogram
    return hist.flatten()


def segmentation(image):
    '''
    this methods segments background from foreground - it is similar to the
    watershed algorithm
    '''
    # Segmentation
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Otsu's thresholding
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV +
                                cv2.THRESH_OTSU)

    # Further noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    # display_one(opening, 'background before noise')

    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    # display_one(sure_bg, 'background after noise')
    markers = sure_bg

    # Make the background white, and what we want to keep black
    markers[markers > 1] = 255
    markers[markers == 1] = 0

    # Displaying markers on the image
    # display_one(image, 'Original')
    # display_one(markers, 'Marked')

    # Use a kernel to dilate the image, to not lose any detail on the outline
    # I used a kernel of 3x3 pixels
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(markers.astype(np.float32), kernel, iterations=1)

    # Plot again to check whether the dilation is according to our needs
    # If not, repeat by using a smaller/bigger kernel, or more/less iterations
    # plt.imshow(dilation, cmap='gray')
    # plt.show()

    # Now apply the mask we created on the initial image
    image = cv2.bitwise_and(image, image, mask=dilation.astype(np.uint8))
    image[image == 0] = 255

    # display_one(image, 'final image after watershed')
    return image


def rotate_image(image):
    '''
    rotates an image by 90 degrees
    '''
    # get the width and height
    height, width = image.shape[:2]

    # get the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), 90, 1)

    # rotate the image
    image_rotated = cv2.warpAffine(image, rotation_matrix, (width, height))

    return image_rotated
