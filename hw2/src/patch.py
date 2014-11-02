#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


class ImagePatches(object):
    def __init__(self, im, patch_size):
        self._im = im
        self.W, self.H = self._im.size
        self.w, self.h = patch_size
        self.len = (self.W - self.w + 1) * (self.H - self.h + 1)
        data = list(self._im.getdata())
        self.pixels = np.reshape(data, (self.H, self.W))

    def get_patch(self, key):
        x, y = key / (self.W - self.w + 1), key % (self.W - self.w + 1)
        return self.pixels[x:x+self.h, y:y+self.w]

    def __getitem__(self, key):
        return self.get_patch(key)

    def __len__(self):
        return self.len


def view_as_window(img, patch_size):
    return ImagePatches(img, patch_size)
