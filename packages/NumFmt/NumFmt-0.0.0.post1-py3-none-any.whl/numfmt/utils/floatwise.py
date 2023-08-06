import struct
import sys


def float_to_bits(f: float):
    return struct.unpack('@I', struct.pack('@f', f))[0]


def bits_to_float(b: int):
    return struct.unpack('@f', struct.pack('@I', b))[0]


def double_to_bits(f: float):
    return struct.unpack('@Q', struct.pack('@d', f))[0]


def bits_to_double(b: int):
    return struct.unpack('@d', struct.pack('@Q', b))[0]


if __name__ == '__main__':
    print(sys.float_info)
    x = 123.123
    print(x)
    print(double_to_bits(x))
    print(bits_to_double(double_to_bits(x)))
