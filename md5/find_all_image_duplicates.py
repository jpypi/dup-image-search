#!/usr/bin/python
"""
    find_all_image_duplicates.py

    Given an input of hashes and corresponding filenames, generates 2 files:

        exact_duplicates.txt - contains the listing of image filenames that are
        duplicates and what they are duplicates of

        corrupt_images.txt - contains a list of images that were corrupt in
        some way

    :author: Brandon Arrendondo
    :license: MIT
"""
import sys
import argparse
import filecmp

from PIL import Image


def is_valid_image(filepath):
    try:
        image = Image.open(filepath)
        image.verify()
    except IndexError:
        return False
    except IOError:
        return False

    return True


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file containing hashes")
    args = parser.parse_args()

    duplicates_file = open("exact_duplicates.txt", "w")
    corruption_file = open("corrupt_images.txt", "w")

    line_counter = 0
    duplicate_counter = 0
    corruption_counter = 0
    hash_collisions = 0

    with open(args.filename, "r") as f:

        last_hash = None
        identical_hash_filenames = []

        line = f.readline()
        while line:
            line_arr = line.strip().split()
            hash = line_arr[0]
            image_filename = " ".join(line_arr[1:])

            if(hash == last_hash):
                found = False
                for file in identical_hash_filenames:
                    if(filecmp.cmp(image_filename, file)):
                        duplicates_file.write(
                            "{0},{1}\n".format(image_filename, file))
                        duplicate_counter += 1
                        found = True
                        break

                if(not found):
                    if(is_valid_image(image_filename)):
                        identical_hash_filenames.append(image_filename)
                        hash_collisions += 1
                    else:
                        corruption_file.write(
                            "{0}\n".format(image_filename))
                        corruption_counter += 1

            else:
                if(is_valid_image(image_filename)):
                    identical_hash_filenames = [image_filename]
                else:
                    identical_hash_filenames = []
                    corruption_file.write(
                        "{0}\n".format(image_filename))
                    corruption_counter += 1

            last_hash = hash
            line_counter += 1
            if(line_counter % 50000 == 0):
                print "Update: scanned {0!s} files.".format(line_counter)

            line = f.readline()

    print "Scanned {0!s} files.".format(line_counter)
    print "Total exact duplicates: {0!s}.".format(duplicate_counter)
    print "Total corrupt files: {0!s}.".format(corruption_counter)
    print "Hash collisions: {0!s}.".format(hash_collisions)
    print "See {0} and {1} for more details.".format(
        "exact_duplicates.txt", "corrupt_images.txt")

if __name__ == "__main__":
    main(sys.argv[1:])
