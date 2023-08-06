from ..parser.errors import *


def decode_var_uint(reader, size: int):
    result = 0
    i = 0
    while True:
        a = reader.read(1)
        b = int.from_bytes(a, "little")  # bytes转int，否则没法&

        if i == size / 7:
            if b & 0x80 != 0:
                raise ErrIntTooLong
            if b >> (size - i * 7) > 0:
                raise ErrIntTooLarge
        result |= (b & 0x7f) << (i * 7)  # 取低7位并左移七位
        if b & 0x80 == 0:
            return result, i + 1
        i += 1
    raise ErrUnexpectedEnd


def decode_var_uint111(data, size: int):
    result = 0
    i = 0
    while True:
        b = int.from_bytes(data[:1], "little")  # bytes转int，否则没法&
        data = data[1:]

        if i == size / 7:
            if b & 0x80 != 0:
                raise ErrIntTooLong
            if b >> (size - i * 7) > 0:
                raise ErrIntTooLarge
        result |= (b & 0x7f) << (i * 7)  # 取低7位并左移七位
        if b & 0x80 == 0:
            return result, i + 1
        i += 1
    raise ErrUnexpectedEnd


def decode_var_int(reader, size):
    result = 0
    i = 0
    while True:
        b = int.from_bytes(reader.read(1), "little")  # bytes转int，否则没法&

        if i == size / 7:
            if b & 0x80 != 0:
                raise ErrIntTooLong
            if b & 0x40 == 0 and b >> (size - i * 7 - 1) != 0 or \
                    b & 0x40 != 0 and int(b | 0x80) >> (size - i * 7 - 1) != -1:
                raise ErrIntTooLarge
        result |= (b & 0x7f) << (i * 7)
        if b & 0x80 == 0:
            if (i * 7 < size) and (b & 0x40 != 0):  # 判断是否为负数
                result |= -1 << ((i + 1) * 7)  # 前几位补1
            return result, i + 1
        i += 1
    raise ErrUnexpectedEnd


def decode_var_uint_from_data(data, size: int):
    result = 0
    for i, b in enumerate(data):
        if i == size / 7:
            if b & 0x80 != 0:
                raise ErrIntTooLong
            if b >> (size - i * 7) > 0:
                raise ErrIntTooLarge
        result |= (b & 0x7f) << (i * 7)
        if b & 0x80 == 0:
            return result, i + 1
    raise ErrUnexpectedEnd
