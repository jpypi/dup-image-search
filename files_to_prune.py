#!/usr/bin/python
"""
    files_to_prune.py

    :author: Brandon Arrendondo
    :license: MIT
"""
import sys
import argparse
import glob
import hashlib
import os

from PIL import Image


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    args = parser.parse_args()

    sha_hashes = {}

    image_filetypes = ["png", "PNG", "jpg", "JPG", "gif", "GIF"]
    for type in image_filetypes:
        for filename in glob.iglob("{0}/*.{1}".format(args.dir, type)):
            try:
                image = Image.open(filename)
                image = image.resize((8, 8))
            except IndexError:
                print "{0} Index Error".format(filename)
                return
            except IOError:
                print "{0} IO Error".format(filename)
                return

            hasher = hashlib.md5()
            with open(filename, "rb") as f:
                buf = f.read()
                hasher.update(buf)

            digest = hasher.hexdigest()
            if(digest in sha_hashes.keys()):
                match_file = sha_hashes[digest]
                if(os.path.getsize(match_file) == os.path.getsize(filename)):
                    print "{0} Duplicate".format(filename)
            else:
                sha_hashes[digest] = filename


if __name__ == "__main__":
    main(sys.argv[1:])
