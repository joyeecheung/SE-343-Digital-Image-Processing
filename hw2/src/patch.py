#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


class ImagePatches(object):
    """A list-like object of patches in an image.

    Usage:
        patches = ImagePatches(img, (patch_width, patch_height))
        first_patch = patches[0]
        last_patch = patches[patches.len - 1]
    """
    def __init__(self, im, patch_size):
        self._im = im
        self.W, self.H = self._im.size
        self.w, self.h = patch_size
        self.len = (self.W - self.w + 1) * (self.H - self.h + 1)
        data = list(self._im.getdata())
        self.pixels = np.reshape(data, (self.H, self.W))

    def __getitem__(self, key):
        x, y = key / (self.W - self.w + 1), key % (self.W - self.w + 1)
        return self.pixels[x:x+self.h, y:y+self.w]

    def __len__(self):
        return self.len


def view_as_window(img, patch_size):
    """
    Given an image and the desired patch size,
    return a list-like object of patches.
    """
    return ImagePatches(img, patch_size)
