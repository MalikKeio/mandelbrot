#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Calculate the Mandelbrot set (500 iterations)")
parser.add_argument('-p', '--precision', default=0.1, type=float, help="Precision of the 'net'")
parser.add_argument('-n', '--max', default=500, type=int, help="Number of iterations")
args = parser.parse_args()


from complex import Complex

MAX = args.max
OUT_OF_MANDELBROT = 2

def f(c, z):
    return z*z + c

def isInside(c):
    zN = Complex()
    for i in range(MAX):
        if zN.radius() > OUT_OF_MANDELBROT:
            return i
        zN = f(c, zN)
    return -1

PRECISION = args.precision

import numpy as np
import matplotlib.pyplot as plt
import tweakmatplotlib

SIZE = int(4/PRECISION)
out = np.zeros((SIZE, SIZE), dtype=int)

for i in range(0, SIZE):
    print("%d/%d\r" % (i,SIZE), end="")
    for j in range(0, SIZE):
        c = Complex(-2+i*PRECISION, -2+j*PRECISION)
        out[j,i] = isInside(c)
print("%d/%d" % (SIZE,SIZE))
np.savetxt("out.csv", out, delimiter=",")
plt.imshow(out)
colorbar = plt.colorbar()
plt.show()
