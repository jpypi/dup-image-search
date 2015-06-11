#!/usr/bin/env python2

# Author: James Jenkins (appplesmacs@yahoo.com)
# Based off handy information/tutorial at
# http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

from PIL import Image
import numpy as np
import DCT

DEFAULT_THUMBNAIL_SIZE = (8,8)


def grey_scale(row):
    return sum(row)/row.size


def process_image(image, thumbnail_size = DEFAULT_THUMBNAIL_SIZE):
    image = image.resize(thumbnail_size).convert("RGB")
    np_array = np.asarray(image.getdata())
    return np.apply_along_axis(grey_scale, axis=1, arr=np_array)


def back_to_image(grey_scale_image):
    return Image.fromarray(np.uint8(grey_scale_image.reshape(thumbnail_size)),mode="L")


def image_hash(image, thumbnail_size = DEFAULT_THUMBNAIL_SIZE):
    image_array = process_image(image, thumbnail_size)
    bits = 0
    mean = np.mean(image_array)
    for i,v in enumerate(image_array):
        bits |= (v > mean) << i

    return bits


def dct_image_hash(image, thumbnail_size = (32,32), frequency_resolution = (8,8)):
    image_array = process_image(image, thumbnail_size).reshape(thumbnail_size)
    # Shift so image is centered around 0 by adding -128
    #DCT.shiftCenter(image_array) # Default is -128
    # We only care about the upper left 8x8 cornder
    dct_image = DCT.DCTII2D(image_array)[:frequency_resolution[0],:frequency_resolution[1]]
    # Calcualte the mean of the DCT, but ignore the first element
    mean = (np.sum(dct_image)-dct_image[0,0])/(frequency_resolution[0]*frequency_resolution[1])
    bits = 0
    for i,v in enumerate(dct_image.flat):
        bits |= (v > mean) << i
    return bits


def hamming_dist(n1,n2):
    dist = 0
    diff = n1^n2

    while diff>0:
        dist += 1
        diff &= diff-1

    return dist


def get_similarity(image1, image2):
    """
    Returns the distance between two images.
    <= 5 likely similar
    >= 10 they're probably quite different
    (Note: these numbers are when the thumbnail size is 8x8)
    """
    return hamming_dist(image_hash(image1),image_hash(image2))


if __name__=="__main__":
    # Just a quick example
    i1 = Image.open("p2.jpg")
    i2 = Image.open("p1copy.jpg")
    h1=dct_image_hash(i1)
    i2.show()
    h2=dct_image_hash(i2)
    print hamming_dist(h1,h2)
    print get_similarity(i1,i2)
