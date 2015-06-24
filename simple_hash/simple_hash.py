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
from PIL import Image


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

    hash = 0
    for i in xrange(0, len(imgdata)):
        hash |= (imgdata[i] > average) << i

    return hash


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    args = parser.parse_args()

    try:
        image = Image.open(args.filepath)
        hash = simple_hash.calculate_simple_hash(image)
        print "{0!s} {1}".format(hash, args.filepath)
    except:
        print "NaN {0}".format(args.filepath)


if __name__ == "__main__":
    main(sys.argv[1:])
