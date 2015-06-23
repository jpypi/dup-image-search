"""
    image_utils.py

    Some generic functions used for our image hashes.

    :author: Brandon Arrendondo
    :author: James Jenkins
    :license: MIT
"""
import sys


def hamming_distance(a, b):
    """
    Per https://en.wikipedia.org/wiki/Hamming_weight:
        The Hamming distance can be defined as the:
            Hamming Weight of (a xor b)
    """
    return hamming_weight(a ^ b)


def hamming_weight(x):
    """
    Per stackoverflow.com/questions/407587/python-set-bits-count-popcount
    It is succint and describes exactly what we are doing.
    """
    return bin(x).count('1')


def grey_scale(row):
    return sum(row)/row.size


def matrix_pretty_print(matrix):
    """
    Prints out matrices in an easy to read format.
    """
    for row in matrix:
        for col in row:
            sys.stdout.write("%.2f " % col)
        sys.stdout.write("\n")
