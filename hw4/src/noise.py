#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image

from random import random
from math import sin, cos, log, sqrt, pi


class Gauss(object):
    def __init__(self, mu, sigma):
        """Gaussian distribution.

        mu is the mean, and sigma is the standard deviation.
        """
        self.gauss_next = None
        self.mu = mu
        self.sigma = sigma

    def next(self):

        # When x and y are two variables from [0, 1), uniformly
        # distributed, then
        #
        #    cos(2*pi*x)*sqrt(-2*log(1-y))
        #    sin(2*pi*x)*sqrt(-2*log(1-y))
        #
        # are two *independent* variables with normal distribution
        # (mu = 0, sigma = 1).

        z = self.gauss_next
        self.gauss_next = None
        if z is None:
            a = random() * 2 * pi
            b = sqrt(-2.0 * log(1.0 - random()))
            z = cos(a) * b
            self.gauss_next = sin(a) * b

        return self.mu + z * self.sigma


def sap_noise(img, level, ps=None, pp=None, psap=None):
    data = np.array(img.getdata()).reshape(img.size[::-1])

    def salt(z, ps):
        return level - 1 if random() < ps else z

    def pepper(z, pp):
        return 0 if random() < pp else z

    def sap(z, psap):
        p = random()
        if p < psap:
            return level - 1
        elif p > (1 - psap):
            return 0
        else:
            return z

    if ps:
        vf = np.vectorize(salt)
        return Image.fromarray(vf(data, ps)).convert(img.mode)
    elif pp:
        vf = np.vectorize(pepper)
        return Image.fromarray(vf(data, pp)).convert(img.mode)
    elif psap:
        vf = np.vectorize(sap)
        return Image.fromarray(vf(data, psap)).convert(img.mode)
    else:
        raise Exception("No probability specified.")


def gauss_noise(img, mean, var):
    data = np.array(img.getdata()).reshape(img.size[::-1])
    grand = Gauss(mean, var)

    def additive(z):
        return z + grand.next()

    vf = np.vectorize(additive)
    return Image.fromarray(vf(data)).convert(img.mode)
