#!/usr/bin/env python3

import argparse
import math
import sys


def srgb_to_linear(f: float) -> float:
    assert(f >= 0 and f <= 1.0)

    if f <= 0.04045:
        return f / 12.92

    return math.pow((f + 0.055) / 1.055, 2.4)


def linear_to_srgb(f: float) -> float:
    if f < 0.0031308:
        return f * 12.92

    return 1.055 * math.pow(f, 1 / 2.4) - 0.055



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('c_output', type=argparse.FileType('w'))
    parser.add_argument('h_output', type=argparse.FileType('w'))
    opts = parser.parse_args()

    linear_table: list[int] = []
    srgb_table: list[int] = []

    for i in range(256):
        linear_table.append(int(srgb_to_linear(float(i) / 255) * 65535 + 0.5))

    for i in range(4096):
        srgb_table.append(int(linear_to_srgb(float(i) / 4095) * 255 + 0.5))

    for i in range(256):
        while True:
            linear = linear_table[i]
            srgb = srgb_table[linear >> 4]

            if i == srgb:
                break

            linear_table[i] += 1


    opts.h_output.write("#pragma once\n")
    opts.h_output.write("#include <stdint.h>\n")
    opts.h_output.write("\n")
    opts.h_output.write('/* 8-bit input, 16-bit output */\n')
    opts.h_output.write("extern const uint16_t srgb_decode_8_to_16_table[256];")

    opts.h_output.write('\n')
    opts.h_output.write('static inline uint16_t\n')
    opts.h_output.write('srgb_decode_8_to_16(uint8_t v)\n')
    opts.h_output.write('{\n')
    opts.h_output.write('    return srgb_decode_8_to_16_table[v];\n')
    opts.h_output.write('}\n')

    opts.h_output.write('\n')
    opts.h_output.write('/* 8-bit input, 8-bit output */\n')
    opts.h_output.write("extern const uint8_t srgb_decode_8_to_8_table[256];\n")

    opts.h_output.write('\n')
    opts.h_output.write('static inline uint8_t\n')
    opts.h_output.write('srgb_decode_8_to_8(uint8_t v)\n')
    opts.h_output.write('{\n')
    opts.h_output.write('    return srgb_decode_8_to_8_table[v];\n')
    opts.h_output.write('}\n')

    opts.c_output.write('#include "srgb.h"\n')
    opts.c_output.write('\n')

    opts.c_output.write("const uint16_t srgb_decode_8_to_16_table[256] = {\n")
    for i in range(256):
        opts.c_output.write(f'    {linear_table[i]},\n')
    opts.c_output.write('};\n')

    opts.c_output.write("const uint8_t srgb_decode_8_to_8_table[256] = {\n")
    for i in range(256):
        opts.c_output.write(f'    {linear_table[i] >> 8},\n')
    opts.c_output.write('};\n')


if __name__ == '__main__':
    sys.exit(main())
