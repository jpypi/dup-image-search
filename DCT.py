#!/usr/bin/env python2

from math import *
import sys
from copy import deepcopy


# DCTII function. Equation found at:
# http://en.wikipedia.org/wiki/Discrete_cosine_transform#DCT-II
def DCTII(vector):
    N = len(vector)
    new_vector = []

    for k in xrange(N):
        sum_value = 0
        for n in xrange(N):
            sum_value += vector[n]*cos(pi/N*(n+1/2)*k)

        # This could alternatively be: new_vector[k]=sum_value
        # if necessary for some reason
        new_vector.append(sum_value)

    return new_vector


def alpha(value):
    # This function has something to do with
    # making the DCTII2D transform orthonormal (not sure what that is)
    if value==0:
        return 1/sqrt(2)
    else:
        return 1


def DCTII2D(matrix):
    X=len(matrix[0])
    Y=len(matrix)

    new_matrix = deepcopy(matrix)

    for v in xrange(Y):
        for u in xrange(X):
            outer_sum = 0
            for y in xrange(Y):
                for x in xrange(X):
                    outer_sum += matrix[y][x] * cos((2*x+1)*u*pi/(2*X)) * cos((2*y+1)*v*pi/(2*Y))

            new_matrix[v][u]=1.0/4*alpha(u)*alpha(v)*outer_sum

    return new_matrix


# Just a handy function for printing out matricies
# in a easier to read manner
def nicePrint(matrix):
    for row in matrix:
        for col in row:
            sys.stdout.write("%.2f "%col)
        sys.stdout.write("\n")


if __name__=="__main__":
    # This matrix is the sample matrix from the following page:
    # http://en.wikipedia.org/wiki/JPEG#Discrete_cosine_transform
    v = [[52,55,61, 66, 70, 61,64,73],
         [63,59,55, 90,109, 85,69,72],
         [62,59,68,113,144,104,66,73],
         [63,58,71,122,154,106,70,69],
         [67,61,68,104,126, 88,68,70],
         [79,65,60, 70, 77, 68,58,75],
         [85,71,64, 59, 55, 61,65,83],
         [87,79,69, 68, 65, 76,78,94]]

    # Decrease the dynamic range
    # (aka shift the values so they're centered about 0
    for i in xrange(len(v)):
        v[i] = map(lambda x:x-128,v[i])

    nicePrint(v)

    dct_v=DCTII2D(v)
    print
    nicePrint(dct_v)
