#!/usr/bin/env python2
"""
    image_hash.py

    Generate a hash of an image.

    :author: Brandon Arrendondo
    :author: James Jenkins
    :license: MIT
"""
import sys
import argparse
from PIL import Image

from algorithms import simple_hash
from algorithms import dct_hash


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    parser.add_argument("-a", "--algorithm", default="simple",
                        help="Algorithm to use.  One of: [simple, dct]")
    args = parser.parse_args()
    args.algorithm = args.algorithm.lower()

    image = Image.open(args.filepath)
    if(args.algorithm == "simple"):
        hash = simple_hash.calculate_simple_hash(image)
        print "Simple hash = {0!s}".format(hash)
    elif(args.algorithm == "dct"):
        hash = dct_hash.calculate_dct_hash(image)
        print "DCT hash = {0!s}".format(hash)


if __name__ == "__main__":
    main(sys.argv[1:])
