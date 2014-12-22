#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utilities."""

import numpy as np
from PIL import Image


def img_to_array(img, dtype=None):
    """Convert an image to an 2-d array.

    Parameters
    ----------
    img: the input image
    dtype: the data type of the output array, if not specified,
           it will use the smallest data type that can hold all the data
           without overflow or underflow.

    Return
    ----------
    If the mode of the image is RGB, then three 2-d arrays will be returned
    """
    if img.mode == 'RGB':
        # convert each channel to a numpy array
        return [img_to_array(ch) for ch in img.split()]
    else:
        return np.array(img.getdata(), dtype=dtype).reshape(img.size[::-1])


def array_to_img(data, mode=None):
    """Convert a 2-d numpy array to an image.

    Parameters
    ----------
    img: the input image
    mode:
    """
    if not mode:
        return Image.fromarray(data)
    elif mode == 'RGB':
        channels = [array_to_img(ch, 'L') for ch in data]
        return Image.merge('RGB', channels)
    else:
        return Image.fromarray(data).convert(mode)
