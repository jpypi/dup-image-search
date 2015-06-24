#!/usr/bin/env python2
"""
    fast_dct_hash.py

    Generates a hash using the "DCT" method outlined on:

    http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

    :author: Brandon Arrendondo
    :author: James Jenkins
    :license: MIT
"""
import sys
import numpy
import argparse
import glob

from PIL import Image
from scipy import fftpack
from string import ascii_lowercase
from multiprocessing import Pool


def calculate_dct_hash(image):
    """
    Calculates the DCT (discrete cosine transform) hash of an image.

    The basic steps (verbatim from hackerfactor, see heading):
        1. Reduce size to 32x32
        2. Reduce color to greyscale
        3. Calculate the DCT
        4. Take the top left only
        5. Average using the first term of the low frequency values
        6. Compute the 64 bits - 1 if above average, 0 if not
        7. Construct the hash
    """
    # reduce size to 32x32
    image = image.resize((32, 32))

    # convert to greyscale
    image = image.convert("L")

    # calculate the DCT
    imgdata = image.getdata()
    float_imgdata = [float(i) for i in imgdata]
    dct_data = calculate_DCTII_2D(float_imgdata)

    # Top left only
    smaller_dct = dct_data[:8, :8]
    average = numpy.mean(smaller_dct)

    hash = 0
    i = 0
    for x in smaller_dct.flat:
        hash |= (x > average) << i
        i += 1

    return hash


def calculate_DCTII_2D(matrix):
    """
    Calculates the 2D transform of the DCT II algorithm.
    Assumes a square matrix.

    See:
        http://en.wikipedia.org/wiki/Discrete_cosine_transform#DCT-II

    We are using the plain version, which seems to work better.
    """
    a = numpy.reshape(numpy.array(matrix), (32, 32))
    return fftpack.dct(fftpack.dct(a.T).T)


def hash_file(filepath):
    try:
        image = Image.open(filepath)
        hash = calculate_dct_hash(image)
        print "{0!s} {1}".format(hash, filepath)
    except:
        pass


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="directory to scan")
    args = parser.parse_args()

    pool = Pool(8)
    image_hashes = pool.map(hash_file, glob.iglob("{0!s}/*".format(args.directory)))


if __name__ == "__main__":
    main(sys.argv[1:])
