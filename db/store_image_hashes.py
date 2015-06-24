#!/usr/bin/env python2
"""
    store_image_hashes.py

    Generates hashes of each image in the given directory, recording which
    images are duplicates or erroneous.

    :author: Brandon Arrendondo
    :author: James Jenkins
    :license: MIT
"""
import sys
import argparse
import glob

from PIL import Image

from db import hash_db
from algorithms import simple_hash
from algorithms import dct_hash
from algorithms import image_utils


def check_if_similar_image_found(db_conn, type, hash):
    row = hash_db.hash_exists(db_conn, type, hash)
    if(row):
        return (True, True, row[2])
    else:
        db_result = hash_db.get_closest(db_conn, "simple", hash)
        row = db_result.fetchone()
        while row:
            row_hash = int(row[0])
            distance = image_utils.hamming_distance(row_hash, hash)
            if(distance < 3):
                return (False, True, row[2])

            row = db_result.fetchone()

    return (False, False, "")


def try_insert_image(db_conn, filename):
    hash = 0

    try:
        image = Image.open(filename)
        hash = simple_hash.calculate_simple_hash(image)
    except IndexError:
        print "Caught IndexError. Image is corrupt: {0}".format(filename)
        return
    except IOError:
        # This can happen sometimes randomly
        #print "Caught IOError. Image is corrupt: {0}".format(filename)
        return

    (exactly, likely, source_filename) = check_if_similar_image_found(db_conn, "simple", hash)

    if(exactly):
        print "Duplicate: {0}, {1}".format(source_filename, filename)
    elif(likely):
        # TODO: will calculate DCT hash
        print "Likely duplicate: {0}, {1}".format(source_filename, filename)
    else:
        hash_db.insert_hash(db_conn, "simple", hash, filename)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("image_dir")
    parser.add_argument("db_filepath")
    args = parser.parse_args()

    db_conn = hash_db.db_open(args.db_filepath)

    file_count = 0
    image_filetypes = ["png", "PNG", "jpg", "JPG", "gif", "GIF"]
    for type in image_filetypes:
        for filename in glob.iglob("{0}/*.{1}".format(args.image_dir, type)):
            try_insert_image(db_conn, filename)
            file_count += 1

    db_conn.commit()
    db_conn.close()

    print "Scanned {0!s} files.".format(file_count)


if __name__ == "__main__":
    main(sys.argv[1:])
