#!/usr/bin/env python2

# Author: James Jenkins (appplesmacs@yahoo.com)
# Based off handy information/tutorial at
# http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

from PIL import Image
import numpy as np

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
    bits = long(0)
    mean = long(np.mean(image_array))
    for i,n in enumerate(image_array):
        bits |= (n > mean) << i

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
    i1 = Image.open("p1.jpg")
    i2 = Image.open("p2.jpg")

    print get_similarity(i1,i2)
