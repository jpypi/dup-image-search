#!/usr/bin/env python2
"""
    Note: This does not sort the output.
    For sorting simply run:
        $ sort md5sums.txt > md5sums_sorted.txt
"""
import sys
import glob
import csv
import hashlib

from multiprocessing import Pool


def md5_file(filename):
    with open(filename) as f:
        return (hashlib.md5(f.read()).hexdigest(),filename)


directories = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
               "n","o","p","q","r","s","t","the","u","v","w","x","y"]

try:
    base_directory = sys.argv[1]

    pool = Pool(8)
    with open("md5sums.txt","w") as f:
        writer = csv.writer(f)
        for d in directories:
            print "Calculating hashes for the {} directory.".format(d)

            image_files = glob.iglob("{}/{}/*".format(base_directory,d))
            for hash_and_name in pool.imap(md5_file, image_files):
                writer.writerow(hash_and_name)

except IndexError:
    print "{0}: Syntax: {0} <album covers base directory>".format(sys.argv[0])
    sys.exit(0)

