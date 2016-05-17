from math import sqrt

class Complex:
    def __init__(self, realpart=0, imagpart=0):
        self.r = realpart
        self.i = imagpart

    def __add__(self, other):
        return Complex(self.r + other.r, self.i + other.i)

    def __mul__(self, other):
        return Complex(self.r*other.r - self.i*other.i, self.r*other.i + self.i*other.r)

    def __str__(self):
        return "%f+%f*i" % (self.r, self.i)

    def radius(self):
        return sqrt(self.r**2 + self.i**2)
    def __repr__(self):
        return str(self)

class Quaternion(Complex):
    def __init__(self, realpart=0, imagpart=0, j=0, k=0):
        Complex.__init__(self, realpart, imagpart)
        self.j = j
        self.k = k
