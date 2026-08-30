import math
import pylib.binary as binary
from typing import Any
from io import BufferedIOBase
from dataclasses import dataclass, field
from mashumaro.types import SerializableType


@dataclass
class Parm[T](SerializableType):
    id: str = "dum"  # dummy id
    length: int = 0
    value: T = field(init=False)

    def read(self, stream: BufferedIOBase):
        self.id = str(stream.read(3))
        self.length = binary.read_u8(stream)

    def write(self, stream: BufferedIOBase):
        stream.write(self.id.encode())
        binary.write_u8(stream, self.length)

    def _serialize(self) -> T:
        return self.value

    @classmethod
    def _deserialize(cls, value: T) -> "Parm[T]":
        parm = cls()
        parm.value = value
        return parm


@dataclass
class ParmInt(Parm[int]):
    length: int = 4

    def read(self, stream):
        super().read(stream)
        self.value = binary.read_u32(stream)

    def write(self, stream):
        super().write(stream)
        binary.write_u32(stream, self.value)


@dataclass
class ParmFloat(Parm[float]):
    length: int = 4

    def read(self, stream):
        super().read(stream)
        self.value = binary.read_f32(stream)

    def write(self, stream):
        super().write(stream)
        binary.write_f32(stream, self.value)


@dataclass
class ParmString(Parm[str]):
    length: int = 8

    def read(self, stream):
        super().read(stream)
        str_length = binary.read_u32(stream)
        self.value = stream.read(str_length).decode().rstrip("\u0000")

    def write(self, stream):
        super().write(stream)
        aligned_len = 4 * math.ceil(len(self.value) / 4)
        binary.write_u32(stream, aligned_len)
        stream.write(self.value.encode().ljust(aligned_len, b"\0"))
