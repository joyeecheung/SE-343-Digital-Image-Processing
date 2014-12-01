#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from fourier import *

# P183 fig 3.37(d)
laplacian = np.array([[-1, -1, -1],
                      [-1,  8, -1],
                      [-1, -1, -1]])

# 11 x 11 averagin filter
average = np.full((11, 11), 1.0 / (11 * 11))


def apply_filter(data, kernel):
    """Apply the filter(kernel) to the data directly."""
    M, N = data.shape
    P, Q = pow2_ceil(M), pow2_ceil(N)
    m, n = kernel.shape

    fpad = np.zeros((P, Q))
    fpad[:M, :N] = data

    kpad = np.zeros((P, Q))
    kpad[:m, :n] = kernel

    fstar = get_dft(fpad)
    kstar = np.abs(get_dft(kpad))
    return (get_idft(fstar * kstar).real)[:M, :N]


def pad_then_crop(data, kernel):
    """Pad the data with boundaries, then apply the filter(kernel),
       returned the cropped result."""
    m, n = kernel.shape
    M, N = data.shape
    padded = np.lib.pad(data, (m, n), 'edge')
    return apply_filter(padded, kernel)[m:m + M, n:n + N]


def filter2d_freq(input_img, filter):
    """Filter the image with the given filter."""
    data = np.reshape(input_img.getdata(), input_img.size[::-1])
    result = pad_then_crop(data, filter)
    return Image.fromarray(result).convert('L')
