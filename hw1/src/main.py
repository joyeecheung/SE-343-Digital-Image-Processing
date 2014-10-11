#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
from scale import scale
from quantize import quantize
from PIL import Image


def test_scale(filename, result_dir):
    input_img = Image.open(filename)
    cases = []
    cases.append([(192, 128), (96, 64), (48, 32), (24, 16), (12, 8)])
    cases.append([(300, 200), ])
    cases.append([(450, 300), ])
    cases.append([(500, 200), ])

    for case in cases:
        for size in case:
            result = scale(input_img, size)
            result_name = 'scale-%d-%d.png' % size
            result_path = os.path.join(result_dir, result_name)
            result.save(result_path)
            print 'Saved ' + result_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", type=str, default="02.png")
    source = parser.parse_args().source

    file_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir, _ = os.path.split(file_dir)
    filename = os.path.join(parent_dir, 'img', source)
    result_dir = os.path.join(parent_dir, 'result')

    print 'Source path: ' + filename
    if not os.path.exists(filename):
        raise Exception("Source file doesn't exists!")
    print 'Result directory: ' + result_dir

    test_scale(filename, result_dir)

if __name__ == "__main__":
    main()
