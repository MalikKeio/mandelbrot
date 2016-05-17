#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Calculate the Mandelbrot set (500 iterations)")
parser.add_argument('-p', '--precision', default=0.1, type=float, help="Precision of the 'net'")
parser.add_argument('-n', '--max', default=100, type=int, help="Number of iterations")
parser.add_argument('-r', '--centerreal', default=0, type=float, help="Real part of figure center")
parser.add_argument('-i', '--centerimag', default=0, type=float, help="Imaginary part of figure center")
args = parser.parse_args()


from complex import Complex

MAX = args.max
OUT_OF_MANDELBROT = 2
CENTER = Complex(args.centerreal, args.centerimag)
USE_SYMMETRY = CENTER.i == 0

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
from matplotlib import cm
import tweakmatplotlib

if USE_SYMMETRY:
    SIZE = int(4/PRECISION)//2*2
else:
    SIZE = int(4/PRECISION)

out = np.zeros((SIZE, SIZE), dtype=int)

for i in range(0, SIZE):
    print("%d/%d\r" % (i,SIZE), end="")
    RANGE = SIZE//2+1 if USE_SYMMETRY else SIZE
    for j in range(0, RANGE):
        c = Complex(CENTER.r-2+i*PRECISION, CENTER.i-2+j*PRECISION)
        out[j,i] = isInside(c)
    # Use symmetry of set to gain time
    for j in range(RANGE, SIZE):
        out[j,i] = out[SIZE-j, i]
print("%d/%d" % (SIZE,SIZE))
np.savetxt("out.csv", out, fmt="%d", delimiter=",")
plt.imshow(out)
colorbar = plt.colorbar()
plt.show()
