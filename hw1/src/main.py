#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

from PIL import Image

from scale import scale
from quantize import quantize


def case_message(message):
    return "    " + message


def expect(condition, pass_message, fail_message):
    if not condition:
        raise Exception(case_message(fail_message))
    else:
        print case_message(pass_message)


def test_scale(filename, result_dir=None):
    input_img = Image.open(filename)

    cases = []
    cases.append([(192, 128), (96, 64), (48, 32), (24, 16), (12, 8)])
    cases.append([(300, 200), ])
    cases.append([(450, 300), ])
    cases.append([(500, 200), ])
    count = 1

    for case in cases:
        for size in case:
            print "Scaling Case %d" % (count, )
            result = scale(input_img, size)
            result_size = result.size
            comparison = "expected size %s, actual size %s" % (
                str(size), str(result_size))

            count += 1

            expect(
                result_size == size,
                "[PASS] Scaling: " + comparison,
                "[FAIL] Scaling: " + comparison)

            if result_dir:
                result_name = 'scale-%d-%d.png' % size
                result_path = os.path.join(result_dir, result_name)
                result.save(result_path)
                print case_message('[Saved] ' + result_path)


def test_quantize(filename, result_dir=None):
    input_img = Image.open(filename)

    cases = [128, 32, 8, 4, 2]
    count = 1

    for level in cases:
        print "Quantization Case %d" % (count, )
        result = quantize(input_img, level)
        result_level = len(result.getcolors())
        comparison = "expected level %d, actual level %d" % (
            level, result_level)

        count += 1
        expect(
            result_level == level,
            "[PASS] Quantization: " + comparison,
            "[FAIL] Quantization: " + comparison)

        if result_dir:
            result_name = 'quantize-%d.png' % (level, )
            result_path = os.path.join(result_dir, result_name)
            result.save(result_path)
            print case_message('[Saved] ' + result_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", type=str, default="02.png")
    source = parser.parse_args().source

    # absolute path to the directory of this .py
    file_dir = os.path.dirname(os.path.realpath(__file__))
    # absolute path to the parent directory of this .py
    parent_dir, _ = os.path.split(file_dir)
    # absolute path to the image file to process
    filename = os.path.join(parent_dir, 'img', source)
    # absolute path to the result directory
    result_dir = os.path.join(parent_dir, 'result')

    print 'Source path: ' + filename
    if not os.path.exists(filename):
        raise Exception("Source file doesn't exists!")
    print 'Result directory: ' + result_dir

    test_scale(filename, result_dir)
    test_quantize(filename, result_dir)

if __name__ == "__main__":
    main()
