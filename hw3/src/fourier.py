#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy import fftpack, misc
from PIL import Image


def dftmtx(N):
    """Get discrete fourier transform matrix of size N x N."""
    n = np.asmatrix(np.arange(N))
    return np.exp((-2j * np.pi / N) * n.T * n)


def idftmtx(N):
    """Get inverse discrete fourier transform matrix of size N x N."""
    n = np.asmatrix(np.arange(N))
    return np.exp((2j * np.pi / N) * n.T * n)


def get_dft(data):
    """Get discrete fourier transform of data(numpy matrix/array)."""
    if len(data.shape) == 1:
        return (dftmtx(len(data)) * data[:, np.newaxis]).A1
    M, N = data.shape
    return np.asarray(dftmtx(M) * data * dftmtx(N))


def get_idft(data):
    """Get inverse discrete fourier transform of data(numpy matrix/array)."""
    if len(data.shape) == 1:
        return (idftmtx(len(data)) * data[:, np.newaxis] / len(data)).A1
    M, N = data.shape
    return np.asarray(idftmtx(M) * data * idftmtx(N) / (M * N))


def pow2_ceil(x):
    """Get the nearest power of 2 ceiling."""
    return 2 ** int(np.ceil(np.log2(x)))


def recursive_fft(x):
    """Recursive FFT."""
    N = len(x)
    if N > 16:
        even = recursive_fft(x[0::2])
        odd = recursive_fft(x[1::2])
        coff = np.exp((-2j * np.pi / N) * np.arange(N / 2))
        return np.hstack((even + coff * odd, even - coff * odd))
    else:
        return get_dft(x)


def fft(x):
    """Iterative & vectorized FFT.

    Parameters
    ---------
    x: 1D numpy array
        The vector to transform. Its length should be power of 2.
    """
    N = len(x)
    cutoff = min(16, N)
    subprob = np.asarray(dftmtx(cutoff) * x.reshape((cutoff, -1)))

    # builds up the fft, from (1, N) to (N, 1)
    while subprob.shape[1] != 1:
        m, n = subprob.shape
        # concatenate all `odd` part in sub problems
        # it will turn out to be subprob[:, n / 2:].
        # e.g. f([1,3,5,7]) -> f([1,5]) + f([3,7])
        #                   -> f(f([1]) + f([5])) + f(f([3]) + f([7]))
        #      f([2,4,6,8]) -> f([2,6]) + f([4,8])
        #                   -> f(f([2]) + f([6])) + f(f([4]) + f([8]))
        #      so odd parts are [5], [6], [7], [8]
        #        even parts are [1], [2], [3], [4]
        odd, even = subprob[:, n / 2:], subprob[:, :n / 2]
        # since the input is real, the coefficients are symmetric
        # so we can use each coff to multiply across the same row of `odd`
        # because of the concatenation, m = 2N(N as in subproblem)
        # so -2j -> -1j
        coff = np.exp((-1j * np.pi / m) * np.arange(m)[:, np.newaxis])
        twiddle = coff * odd
        subprob = np.vstack((even + twiddle, even - twiddle))

    return subprob.ravel()


def get_2d(data, fn):
    """Apply `fn` to each row, then to each column."""
    result = np.apply_along_axis(fn, 0, data)
    return np.apply_along_axis(fn, 1, result)


def get_fft(data):
    """1D or 2D fft."""
    return fft(data) if len(data.shape) == 1 else get_2d(data, fft)


def get_ifft(data):
    """1D or 2D ifft."""
    Fstar = np.conj(data)
    fstar = get_fft(Fstar) / reduce(np.multiply, data.shape, 1.0)
    return np.conj(fstar)


def scale_intensity(f, typef=np.uint8, L=256):
    """Scale the intensities in the matrix to [0, L-1]."""
    fm = f - np.min(f)
    fs = (L - 1) * (fm / np.max(fm))
    return typef(fs)


def shift_dft(f):
    """Shift the fourier transform so that F(0,0) is in the center."""
    y = np.array(f)  # copy
    for k, n in enumerate(f.shape):
        mid = (n + 1) / 2
        indices = np.concatenate((np.arange(mid, n), np.arange(mid)))
        y = np.take(y, indices, k)  # rearrange each axes
    return y


def dft2d(input_img, flags):
    return get_dft(input_img) if flags == 1 else get_idft(input_img)


def fft2d(input_img, flags):
    return get_fft(input_img) if flags == 1 else get_ifft(input_img)


def pad_to_pow2(data):
    """Pad each direction to the nearest power of 2(ceiling)."""
    M, N = data.shape
    P, Q = pow2_ceil(M), pow2_ceil(N)
    padded = np.zeros((P, Q))
    padded[:M, :N] = data
    return padded


def test_my_func(data, my_func, lib_func, name, all_right=np.allclose):
    """Check if my implementation is close to the one in the library."""
    my_result, lib_result = my_func(data), lib_func(data)
    error = np.abs(lib_result - my_result)
    error_range = (np.min(error), np.max(error))
    if all_right(lib_result, my_result):
        print "[PASSED] %s, " % name,
        print "Error in (%.6e, %.6e)" % error_range
    else:
        print "[FAILED] %s" % name


if __name__ == "__main__":
    lena = np.reshape(misc.lena(), (1024, 256))
    data = np.random.rand(1024)

    test_my_func(lena, shift_dft, fftpack.fftshift, 'Shift', np.array_equal)
    test_my_func(lena, get_dft, fftpack.fft2, '2D-DFT')
    test_my_func(lena, get_idft, fftpack.ifft2, '2D-IDFT')
    test_my_func(lena, get_fft, fftpack.fft2, '2D-FFT')
    test_my_func(lena, get_ifft, fftpack.ifft2, '2D-IFFT')

    test_my_func(data, get_dft, fftpack.fft, '1D-DFT')
    test_my_func(data, get_idft, fftpack.ifft, '1D-IDFT')
    test_my_func(data, get_fft, fftpack.fft, '1D-FFT')
    test_my_func(data, get_ifft, fftpack.ifft, '1D-IFFT')
    test_my_func(data, recursive_fft, fftpack.fft, '1D-IFFT-Recursive')
