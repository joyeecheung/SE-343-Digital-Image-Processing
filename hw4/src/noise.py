#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Noise generators."""

import numpy as np

from random import random
from math import sin, cos, log, sqrt, pi

from util import img_to_array, array_to_img

L = 256  # default intensity levels


class Gauss(object):
    """Random number generator with gaussian distribution."""
    def __init__(self, mu, sigma):
        """ Parameters
        --------------
            mu: the mean
            sigma: the standard deviation.
        """
        self.gauss_next = None
        self.mu = mu
        self.sigma = sigma

    def next(self):
        """Generate next gaussian random number."""
        # Box-Muller Transform, map two samples x, y from the
        # uniform distribution on the interval (0, 1]
        # to two standard(mu = 0, sigma = 1),
        # normally distributed samples u, v.
        #
        # u = cos(2*pi*x)*sqrt(-2*log(1-y))
        # v = sin(2*pi*x)*sqrt(-2*log(1-y))

        z = self.gauss_next
        self.gauss_next = None

        if z is None:
            theta = random() * 2 * pi
            r = sqrt(-2.0 * log(1.0 - random()))
            z = r * cos(theta)
            self.gauss_next = r * sin(theta)

        return self.mu + z * self.sigma


def sap_noise(img, level=L, ps=None, pp=None):
    """Add salt-and/or-pepper noise to an image.

    Parameters
    -----------
    img: the input image
    level: intensity level, default to 256
    ps: probability of salt noise
    pp: probability of pepper noise
    """
    data = img_to_array(img)

    def salt(z, ps):
        return level - 1 if random() < ps else z

    def pepper(z, pp):
        return 0 if random() < pp else z

    def sap(z, ps, pp):
        p = random()
        if p < ps:
            return level - 1
        elif p > (1 - pp):
            return 0
        else:
            return z

    if ps and not pp:  # salt noise
        vf = np.vectorize(salt)
        return array_to_img(vf(data, ps), img.mode)
    elif pp and not pp:  # pepper noise
        vf = np.vectorize(pepper)
        return array_to_img(vf(data, pp), img.mode)
    elif ps and pp:  # salt-and-pepper noise
        vf = np.vectorize(sap)
        return array_to_img(vf(data, ps, pp), img.mode)
    else:
        raise Exception("No probability specified")


def gauss_noise(img, mean, var):
    """Add guassian noise to an image.

    Parameters
    -----------
    img: the input image
    mean: the mean of the guassian noise
    var: the standard variance of the gaussian noise
    """
    data = img_to_array(img)
    grand = Gauss(mean, var)  # the guassian random number generator

    def additive(z):  # generate f(x, y) + eta(x, y)
        return z + grand.next()

    vf = np.vectorize(additive)
    return array_to_img(vf(data), img.mode)


def add_noise(img, ntype, mean=None, var=None, ps=None, pp=None):
    """Add specified type of noise to an image.

    Parameters
    -----------
    img: the input image
    ntype: type of noise, only supports 'guass'(gaussian noise)
           and 'sap'(salt-and-pepper noise) now.
    mean: the mean of the guassian noise
    var: the standard variance of the gaussian noise
    ps: probability of salt noise
    pp: probability of pepper noise
    """
    if ntype == 'gauss':
        return gauss_noise(img, mean, var)
    elif ntype == 'sap':
        return sap_noise(img, ps=ps, pp=pp)
    else:
        raise Exception("Undefined noise type")
