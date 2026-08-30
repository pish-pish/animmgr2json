import math
import json
import argparse
import pylib.binary as binary
from pathlib import Path
from io import BufferedIOBase
from typing import Any, Optional
from pylib.parm import ParmInt, ParmFloat, ParmString
from pylib.models import CamelCaseModel
from dataclasses import dataclass, field, astuple
from mashumaro.types import SerializableType


@dataclass
class AnimKey(CamelCaseModel, SerializableType):
    frame_index: Optional[int] = None
    event_type: Optional[int] = None  # short int
    event_cmd: Optional[int] = None  # byte
    key_type: Optional[int] = None  # byte

    def read(self, stream: BufferedIOBase):
        self.frame_index = binary.read_u32(stream)
        self.event_type = binary.read_u16(stream)
        self.event_cmd = binary.read_u8(stream)
        self.key_type = binary.read_u8(stream)

    def write(self, stream: BufferedIOBase):
        binary.write_u32(stream, self.frame_index or 0)
        binary.write_u16(stream, self.event_type or 0)
        binary.write_u8(stream, self.event_cmd or 0)
        binary.write_u8(stream, self.key_type or 0)

    def _serialize(self) -> list[int]:
        out = [x for x in astuple(self) if x != None]
        return out[0] if len(out) == 1 else out

    @classmethod
    def _deserialize(cls, value: int | list[int]) -> Any:
        if isinstance(value, list):
            return cls(*value)
        else:
            animkey = cls()
            animkey.frame_index = value
            return cls


@dataclass
class AnimInfo(CamelCaseModel):
    name: str = ""
    flags: ParmInt = field(default_factory=lambda: ParmInt("p00"))
    speed: ParmFloat = field(default_factory=lambda: ParmFloat("spd"))
    anim_keys: list[AnimKey] = field(default_factory=lambda: [])
    info_keys: list[AnimKey] = field(default_factory=lambda: [])
    event_keys: list[AnimKey] = field(default_factory=lambda: [])

    def read(self, version: int, stream: BufferedIOBase):
        str_length = binary.read_u32(stream)
        self.name = stream.read(str_length).decode().rstrip("\u0000")
        print(f"\treading {self.name}...")

        self.flags.read(stream)
        self.speed.read(stream)
        binary.read_u32(stream)  # terminator

        # Anim Keys
        anim_key_count = binary.read_u32(stream)
        for _ in range(anim_key_count):
            anim_key = AnimKey()
            anim_key.frame_index = binary.read_u32(stream)
            self.anim_keys.append(anim_key)

        # Info Keys
        if version >= 1:
            info_key_count = binary.read_u32(stream)
            for _ in range(info_key_count):
                info_key = AnimKey()
                info_key.read(stream)
                self.info_keys.append(info_key)

        # Event Keys
        event_key_count = binary.read_u32(stream)
        for _ in range(event_key_count):
            event_key = AnimKey()
            event_key.read(stream)
            self.event_keys.append(event_key)

    def write(self, stream: BufferedIOBase):
        print(f"\twriting {self.name}...")

        aligned_len = 4 * math.ceil(len(self.name) / 4)
        binary.write_u32(stream, aligned_len)
        stream.write(self.name.encode().ljust(aligned_len, b"\0"))

        self.flags.write(stream)
        self.speed.write(stream)
        binary.write_u32(stream, binary.UINT_MAX)  # terminator

        # Anim Keys
        binary.write_u32(stream, len(self.anim_keys))
        for anim_key in self.anim_keys:
            binary.write_u32(stream, anim_key.frame_index or 0)

        # Info Keys
        binary.write_u32(stream, len(self.info_keys))
        for info_key in self.info_keys:
            info_key.write(stream)

        # Event Keys
        binary.write_u32(stream, len(self.event_keys))
        for event_key in self.event_keys:
            event_key.write(stream)


@dataclass
class AnimMgr(CamelCaseModel):
    version: int = 0
    flags: ParmInt = field(default_factory=lambda: ParmInt(id="a00"))
    base_path: ParmString = field(default_factory=lambda: ParmString("a01"))
    anim_infos: list[AnimInfo] = field(default_factory=lambda: [])

    def write(self, filepath: str | Path):
        with open(filepath, "wb") as stream:
            binary.write_u32(stream, self.version)
            binary.write_u32(stream, len(self.anim_infos))

            self.flags.write(stream)
            self.base_path.write(stream)
            binary.write_u32(stream, binary.UINT_MAX)  # terminator

            for info in self.anim_infos:
                info.write(stream)

    @classmethod
    def from_file(cls, filepath: str | Path):
        mgr = cls()
        with open(filepath, "rb") as stream:
            mgr.version = binary.read_u32(stream)
            info_count = binary.read_u32(stream)

            mgr.flags.read(stream)
            mgr.base_path.read(stream)
            binary.read_u32(stream)  # terminator

            for _ in range(info_count):
                info = AnimInfo()
                info.read(mgr.version, stream)
                mgr.anim_infos.append(info)
        return mgr


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, required=True)
    parser.add_argument("--tojson", action="store_true")
    parser.add_argument("--tobinary", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    if args.tojson:
        mgr = AnimMgr.from_file(input_path)
        with open(output_path, "w") as f:
            json.dump(mgr.to_dict(), f, indent=4)
    elif args.tobinary:
        with open(input_path, "r") as f:
            mgr = AnimMgr.from_json(f.read())
        mgr.write(output_path)
    else:
        raise SyntaxError(
            "Missing arguments: either --tojson or --tobinary must be present"
        )

    print("Finished!")
