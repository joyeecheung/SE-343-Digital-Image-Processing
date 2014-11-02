#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import arange
import numpy as np


class ImagePatches(object):
    def __init__(self, im, patch_size):
        self._im = im
        self.W, self.H = self._im.size
        self.w, self.h = patch_size
        self.len = (self.W - self.w + 1) * (self.H - self.h + 1)
        data = list(self._im.getdata())
        self.pixels = [data[i:i+self.W] for i in range(0, len(data), self.W)]

    def get_patch(self, key):
        startx, starty = key / (self.W-self.w+1), key % (self.W-self.w+1)
        patch = []
        for i in range(startx, startx + self.h):
            patch.append(self.pixels[i][starty:starty+self.w])
        return patch

    def __getitem__(self, key):
        return self.get_patch(key)

    def __len__(self):
        return self.len


def view_as_window(img, patch_size):
    return ImagePatches(img, patch_size)
