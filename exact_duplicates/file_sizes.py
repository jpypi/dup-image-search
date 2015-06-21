#!/usr/bin/python
"""
    file_sizes.py

    Given an input file with 1 file per line, calculate the sum of the size of
    each file.

    :author: Brandon Arrendondo
    :license: MIT
"""
import sys
import os
import argparse


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file containing list of files")
    args = parser.parse_args()

    with open(args.filename, "r") as f:
        line = f.readline()
        total = 0
        while line:
            filepath =  (line.strip().split(","))[0]
            statinfo = os.stat(filepath)
            total += statinfo.st_size
            line = f.readline()

        print "Total: {0!s} bytes, {1!s} kilobytes, {2!s} megabytes".format(
            total, total / 1024.0, total / 1024.0 / 1024.0)


if __name__ == "__main__":
    main(sys.argv[1:])
