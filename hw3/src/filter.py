#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from fourier import *

# P183 fig 3.37(d)
laplacian = np.array([[-1, -1, -1],
                      [-1,  8, -1],
                      [-1, -1, -1]])

average = np.full((11, 11), 1.0 / (11 * 11))


def apply_filter(data, kernel):
    M, N = data.shape
    P, Q = pow2_ceil(M), pow2_ceil(N)
    m, n = kernel.shape

    X, Y = np.meshgrid(np.arange(Q), np.arange(P))
    sign = np.power(-1, X + Y)

    fpad = np.zeros((P, Q))
    fpad[:M, :N] = data
    fpad = sign * fpad

    kpad = np.zeros((P, Q))
    kpad[:m, :n] = kernel

    fstar = get_dft(fpad)
    kstar = np.abs(shift_dft(get_dft(kpad)))
    return (get_idft(fstar * kstar).real * sign)[:M, :N]


def pad_then_crop(data, kernel, f):
    m, n = kernel.shape
    M, N = data.shape
    padded = np.lib.pad(data, (m, n), 'edge')
    return f(padded, kernel)[m:m + M, n:n + N]


def filter2d_freq(input_img, filter):
    data = np.reshape(input_img.getdata(), input_img.size[::-1])
    result = pad_then_crop(data, filter, apply_filter)
    return Image.fromarray(result).convert('L')
