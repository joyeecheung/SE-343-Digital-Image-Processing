#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image


def img_to_array(img, dtype=None):
    if img.mode == 'RGB':
        return map(lambda ch: img_to_array(ch), img.split())
    else:
        return np.array(img.getdata(), dtype=dtype).reshape(img.size[::-1])


def array_to_img(data, mode=None):
    if not mode:
        return Image.fromarray(data)
    elif mode == 'RGB':
        channels = map(lambda ch: array_to_img(ch, 'L'), data)
        return Image.merge('RGB', channels)
    else:
        return Image.fromarray(data).convert(mode)
