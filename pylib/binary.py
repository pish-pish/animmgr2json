### Credit to tarsa129

import struct
from io import BufferedIOBase

UINT_MAX = 4294967295

# region binary_read


def read_u32(f: BufferedIOBase) -> int:
    return struct.unpack(">I", f.read(4))[0]


def read_u16(f: BufferedIOBase) -> int:
    return struct.unpack(">H", f.read(2))[0]


def read_s16(f: BufferedIOBase) -> int:
    return struct.unpack(">h", f.read(2))[0]


def read_u8(f: BufferedIOBase) -> int:
    return struct.unpack(">B", f.read(1))[0]


def read_s8(f: BufferedIOBase) -> int:
    return struct.unpack(">b", f.read(1))[0]


def read_f32(f: BufferedIOBase) -> float:
    return struct.unpack(">f", f.read(4))[0]


def read_f32_table(f: BufferedIOBase, offset: int, count: int) -> list[float]:
    f.seek(offset)
    return [read_f32(f) for _ in range(count)]


def read_s16_table(f: BufferedIOBase, offset: int, count: int) -> list[int]:
    f.seek(offset)
    return [read_s16(f) for _ in range(count)]


def read_s8_table(f: BufferedIOBase, offset: int, count: int) -> list[int]:
    f.seek(offset)
    return [read_s8(f) for _ in range(count)]


def skip_padding(f: BufferedIOBase, size: int):
    next_aligned = (f.tell() + (size - 1)) & ~(size - 1)
    diff = next_aligned - f.tell()
    print(diff)
    f.read(diff)


# endregion

# region binary_write


def write_u32(f: BufferedIOBase, val: int):
    f.write(struct.pack(">I", val))


def write_u16(f: BufferedIOBase, val: int):
    f.write(struct.pack(">H", val))


def write_s16(f: BufferedIOBase, val: int):
    f.write(struct.pack(">h", val))


def write_u8(f: BufferedIOBase, val: int):
    f.write(struct.pack(">B", val))


def write_s8(f: BufferedIOBase, val: int):
    f.write(struct.pack(">b", val))


def write_f32(f: BufferedIOBase, val: float):
    f.write(struct.pack(">f", val))


def write_f32_table(f: BufferedIOBase, data: list[float]):
    for val in data:
        write_f32(f, val)


def write_s16_table(f: BufferedIOBase, data: list[int]):
    for val in data:
        write_s16(f, val)


# endregion
