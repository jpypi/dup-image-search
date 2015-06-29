#!/usr/bin/env python2
"""
    simple_hash.py

    Generates a hash using the "simple" method outlined on:

    http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

    :author: Brandon Arrendondo
    :author: James Jenkins
    :license: MIT
"""
import sys
import argparse
import numpy
import glob

from PIL import Image
from multiprocessing import Pool


def calculate_simple_hash(image):
    """
    Calculates the simple hash of an image.

    The basic steps (verbatim from hackerfactor, see heading):
        1. Reduce size to 8x8
        2. Reduce color to greyscale
        3. Average the colors
        4. Compute the 64 bits - 1 if above average, 0 if not
        5. Construct the hash
    """
    # reduce size to 8x8
    image = image.resize((8, 8))

    # convert to greyscale
    image = image.convert("L")

    # average the colors
    imgdata = image.getdata()
    average = numpy.mean(imgdata)

    image_hash = 0
    for i in xrange(0, len(imgdata)):
        image_hash |= (imgdata[i] > average) << i

    return image_hash


def hash_directory(directory):
    with open("simple_hashes.txt", "a") as f:
        for filepath in glob.iglob("{0!s}/*".format(directory)):
            try:
                image = Image.open(filepath)
                image_hash = calculate_simple_hash(image)
                f.write("{0!s},{1!s}\n".format(image_hash, filepath))
            except:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="directory to scan")
    args = parser.parse_args()

    hash_directory(args.directory)
