import gzip
import hashlib
import html
import io
import math
import os
import queue
import re
import uuid
import shutil
import sqlite3
import struct
import json
import sys
import ctypes
import ctypes.wintypes
import urllib.request
import webbrowser
import tempfile
import subprocess
import zipfile
import base64
import winreg
import threading
import time
import platform
import xml.etree.ElementTree as ET
import tkinter as tk
from PIL import Image, ImageTk
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable
from tkinter import filedialog, simpledialog, messagebox, ttk
from tkinter import font as tkfont
from typing import Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

UI_THEME = "clam"

THEMES = {
    "Midnight": {
        "bg_dark": "#1b1b1c", "bg_medium": "#252526", "bg_light": "#3a3a3c",
        "bg_hover": "#464648", "fg": "#dcdcdc", "accent": "#7f8cff", "border": "#444446",
    },
    "Ocean": {
        "bg_dark": "#0f2436", "bg_medium": "#153248", "bg_light": "#1f425e",
        "bg_hover": "#2a5474", "fg": "#d7e6f0", "accent": "#3aa0ff", "border": "#28506e",
    },
    "Hacker": {
        "bg_dark": "#0a0f0a", "bg_medium": "#0f180f", "bg_light": "#1a2a1a",
        "bg_hover": "#223522", "fg": "#b8ffb0", "accent": "#2fff2f", "border": "#2a4a2a",
    },
    "Amethyst": {
        "bg_dark": "#1a1423", "bg_medium": "#241b31", "bg_light": "#35284a",
        "bg_hover": "#453665", "fg": "#e0d6f0", "accent": "#b06bff", "border": "#4a3a63",
    },
    "Onyx": {
        "bg_dark": "#101010", "bg_medium": "#171717", "bg_light": "#262626",
        "bg_hover": "#303030", "fg": "#cfcfcf", "accent": "#c0c0c0", "border": "#333333",
    },
}
THEMES.update({
    "Nord": {"bg_dark":"#1e2430","bg_medium":"#252d3a","bg_light":"#303a4a","bg_hover":"#3a4658","fg":"#d8dee9","accent":"#88c0d0","border":"#414b5d"},
    "Dracula": {"bg_dark":"#282a36","bg_medium":"#303241","bg_light":"#44475a","bg_hover":"#565a70","fg":"#f8f8f2","accent":"#bd93f9","border":"#44475a"},
    "Monokai": {"bg_dark":"#272822","bg_medium":"#2e2f2a","bg_light":"#3e3d32","bg_hover":"#49483e","fg":"#f8f8f2","accent":"#a6e22e","border":"#49483e"},
    "Solarized": {"bg_dark":"#002b36","bg_medium":"#073642","bg_light":"#586e75","bg_hover":"#657b83","fg":"#eee8d5","accent":"#2aa198","border":"#586e75"},
    "Rose Pine": {"bg_dark":"#191724","bg_medium":"#1f1d2e","bg_light":"#26233a","bg_hover":"#403d52","fg":"#e0def4","accent":"#ebbcba","border":"#403d52"},
    "Catppuccin": {"bg_dark":"#1e1e2e","bg_medium":"#313244","bg_light":"#45475a","bg_hover":"#585b70","fg":"#cdd6f4","accent":"#cba6f7","border":"#45475a"},
    "Gruvbox": {"bg_dark":"#282828","bg_medium":"#3c3836","bg_light":"#504945","bg_hover":"#665c54","fg":"#ebdbb2","accent":"#fabd2f","border":"#504945"},
    "Tokyo Night": {"bg_dark":"#16161e","bg_medium":"#1f2335","bg_light":"#292e42","bg_hover":"#3b4261","fg":"#c0caf5","accent":"#7aa2f7","border":"#3b4261"},
    "Synthwave": {"bg_dark":"#241b2f","bg_medium":"#30233d","bg_light":"#45304f","bg_hover":"#5a3e64","fg":"#f5d7fe","accent":"#ff7edb","border":"#5a3e64"},
    "Forest": {"bg_dark":"#102018","bg_medium":"#183025","bg_light":"#254638","bg_hover":"#315a48","fg":"#d8f3dc","accent":"#74c69d","border":"#315a48"},
    "Ruby": {"bg_dark":"#241417","bg_medium":"#351b20","bg_light":"#4a252d","bg_hover":"#63323d","fg":"#f7dfe3","accent":"#ff6b81","border":"#63323d"},
    "Amber": {"bg_dark":"#211a0e","bg_medium":"#33270f","bg_light":"#4a3815","bg_hover":"#61491d","fg":"#fff0c2","accent":"#ffb84d","border":"#61491d"},
    "Arctic": {"bg_dark":"#17212b","bg_medium":"#21303d","bg_light":"#304554","bg_hover":"#405b6d","fg":"#e7f5ff","accent":"#66c7ff","border":"#405b6d"},
    "Lavender": {"bg_dark":"#211d2b","bg_medium":"#2d263b","bg_light":"#3c3350","bg_hover":"#514466","fg":"#eee7ff","accent":"#c4a7ff","border":"#514466"},
    "Coffee": {"bg_dark":"#211915","bg_medium":"#30231d","bg_light":"#45332a","bg_hover":"#5b4437","fg":"#f1dfd0","accent":"#d69e78","border":"#5b4437"},
    "Slate": {"bg_dark":"#181c20","bg_medium":"#232a30","bg_light":"#313a42","bg_hover":"#414c56","fg":"#d9e1e8","accent":"#8ab4c7","border":"#414c56"},
    "Cyber": {"bg_dark":"#080b12","bg_medium":"#101522","bg_light":"#182033","bg_hover":"#26334d","fg":"#d9f7ff","accent":"#00e5ff","border":"#26334d"},
    "Sunset": {"bg_dark":"#241516","bg_medium":"#35201e","bg_light":"#4a2b27","bg_hover":"#633b35","fg":"#ffe4d6","accent":"#ff8a65","border":"#633b35"},
    "Mint": {"bg_dark":"#10211e","bg_medium":"#17312c","bg_light":"#24473f","bg_hover":"#315d52","fg":"#dcfff5","accent":"#62e6c8","border":"#315d52"},
    "Deep Blue": {"bg_dark":"#0b1424","bg_medium":"#10213a","bg_light":"#193153","bg_hover":"#24446f","fg":"#dcecff","accent":"#5ca9ff","border":"#24446f"},
})
THEME_NAMES = list(THEMES.keys())
DEFAULT_THEME = "Midnight"
_CURRENT_PALETTE = dict(THEMES[DEFAULT_THEME])

STARTUP_GEOMETRY = "1400x800"
PANED_TOP_FRACTION = 0.78
HPANED_LEFT_FRACTION = 0.55
VIEWER_MIN_WIDTH = 480
REPLACER_MIN_WIDTH = 320
WATCH_INTERVAL_SEC = 0.5
BASE_DIR = os.path.dirname(os.path.abspath(__file__))




_LOCAL_APPDATA = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
DATA_DIR = os.path.join(_LOCAL_APPDATA, "RoUtils")
os.makedirs(DATA_DIR, exist_ok=True)

APP_VERSION = "3.3"
HISTORY_PATH = os.path.join(DATA_DIR, "history.json")
SETTINGS_PATH = os.path.join(DATA_DIR, "routils_settings.json")

TEMP_EMU_DIR = os.path.join(tempfile.gettempdir(), "RobloxStudio_TempView")
os.makedirs(TEMP_EMU_DIR, exist_ok=True)

import enum
from dataclasses import dataclass, field
from typing import Any

class PropertyFormat(enum.IntEnum):
    
    UNKNOWN = 0
    STRING = 1
    BOOL = 2
    INT = 3
    FLOAT = 4
    DOUBLE = 5
    UDIM = 6
    UDIM2 = 7
    RAY = 8
    FACES = 9
    AXES = 10
    BRICK_COLOR = 11
    COLOR3 = 12
    VECTOR2 = 13
    VECTOR3 = 14
    VECTOR2INT16 = 15
    CFRAME_MATRIX = 16
    CFRAME_QUAT = 17
    ENUM = 18
    REF = 19
    VECTOR3INT16 = 20
    NUMBER_SEQUENCE = 21
    COLOR_SEQUENCE = 22
    NUMBER_RANGE = 23
    RECT2D = 24
    PHYSICAL_PROPERTIES = 25
    COLOR3UINT8 = 26
    INT64 = 27
    SHARED_STRING = 28
    BYTECODE = 29
    OPTIONAL_CFRAME = 30
    UNIQUE_ID = 31
    FONT = 32
    SECURITY_CAPABILITIES = 33
    CONTENT = 34

PROPERTY_FORMAT_TO_XML_TAG: dict[PropertyFormat, str] = {
    PropertyFormat.STRING: 'string',
    PropertyFormat.BOOL: 'bool',
    PropertyFormat.INT: 'int',
    PropertyFormat.FLOAT: 'float',
    PropertyFormat.DOUBLE: 'double',
    PropertyFormat.UDIM: 'UDim',
    PropertyFormat.UDIM2: 'UDim2',
    PropertyFormat.RAY: 'Ray',
    PropertyFormat.FACES: 'Faces',
    PropertyFormat.AXES: 'Axes',
    PropertyFormat.BRICK_COLOR: 'BrickColor',
    PropertyFormat.COLOR3: 'Color3',
    PropertyFormat.VECTOR2: 'Vector2',
    PropertyFormat.VECTOR3: 'Vector3',
    PropertyFormat.VECTOR2INT16: 'Vector2int16',
    PropertyFormat.CFRAME_MATRIX: 'CoordinateFrame',
    PropertyFormat.CFRAME_QUAT: 'CoordinateFrame',
    PropertyFormat.ENUM: 'token',
    PropertyFormat.REF: 'Ref',
    PropertyFormat.VECTOR3INT16: 'Vector3int16',
    PropertyFormat.NUMBER_SEQUENCE: 'NumberSequence',
    PropertyFormat.COLOR_SEQUENCE: 'ColorSequence',
    PropertyFormat.NUMBER_RANGE: 'NumberRange',
    PropertyFormat.RECT2D: 'Rect2D',
    PropertyFormat.PHYSICAL_PROPERTIES: 'PhysicalProperties',
    PropertyFormat.COLOR3UINT8: 'Color3uint8',
    PropertyFormat.INT64: 'int64',
    PropertyFormat.SHARED_STRING: 'SharedString',
    PropertyFormat.BYTECODE: 'BinaryString',
    PropertyFormat.OPTIONAL_CFRAME: 'OptionalCoordinateFrame',
    PropertyFormat.UNIQUE_ID: 'UniqueId',
    PropertyFormat.FONT: 'Font',
    PropertyFormat.SECURITY_CAPABILITIES: 'SecurityCapabilities',
    PropertyFormat.CONTENT: 'Content',
}

@dataclass
class RbxProperty:
    
    name: str
    fmt: PropertyFormat
    value: Any

@dataclass
class RbxInstance:
    
    class_name: str
    referent: int
    properties: dict[str, RbxProperty] = field(default_factory=dict[str, RbxProperty])
    children: list['RbxInstance'] = field(default_factory=list['RbxInstance'])  
    is_service: bool = False

@dataclass
class RbxMetadata:
    
    entries: dict[str, str] = field(default_factory=dict[str, str])

@dataclass
class RbxTypeInfo:
    
    type_index: int
    class_name: str
    is_service: bool
    instance_ids: list[int]

@dataclass
class RbxRawPropertyChunk:
    
    class_name: str
    prop_name: str
    fmt_byte: int
    value_data: bytes
    instance_count: int

@dataclass
class RbxRawChunk:
    
    name: str
    data: bytes

@dataclass
class RbxDocument:
    
    version: int
    type_count: int
    object_count: int
    metadata: RbxMetadata
    instances: dict[int, RbxInstance]
    roots: list[RbxInstance]
    shared_strings: list[bytes] = field(default_factory=list[bytes])
    raw_property_chunks: list[RbxRawPropertyChunk] = field(
        default_factory=list[RbxRawPropertyChunk]
    )
    raw_chunks: list[RbxRawChunk] = field(default_factory=list[RbxRawChunk])

import struct
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

def read_u8(data: bytes, offset: int) -> tuple[int, int]:
    
    return data[offset], offset + 1

def read_u16(data: bytes, offset: int) -> tuple[int, int]:
    
    val = struct.unpack_from('<H', data, offset)[0]
    return val, offset + 2

def read_u32(data: bytes, offset: int) -> tuple[int, int]:
    
    val = struct.unpack_from('<I', data, offset)[0]
    return val, offset + 4

def read_i32(data: bytes, offset: int) -> tuple[int, int]:
    
    val = struct.unpack_from('<i', data, offset)[0]
    return val, offset + 4

def read_f32(data: bytes, offset: int) -> tuple[float, int]:
    
    val = struct.unpack_from('<f', data, offset)[0]
    return val, offset + 4

def read_f64(data: bytes, offset: int) -> tuple[float, int]:
    
    val = struct.unpack_from('<d', data, offset)[0]
    return val, offset + 8

def read_bytes(data: bytes, offset: int, length: int) -> tuple[bytes, int]:
    
    return data[offset : offset + length], offset + length

def read_string(data: bytes, offset: int) -> tuple[str, int]:
    
    length, offset = read_u32(data, offset)
    raw, offset = read_bytes(data, offset, length)
    return raw.decode('utf-8', errors='replace'), offset

def read_binary_string(data: bytes, offset: int) -> tuple[bytes, int]:
    
    length, offset = read_u32(data, offset)
    raw, offset = read_bytes(data, offset, length)
    return raw, offset

def decode_zigzag(value: int) -> int:
    
    return (value >> 1) ^ (-(value & 1))

def encode_zigzag(value: int) -> int:
    
    return (value << 1) ^ (value >> 31)

def deinterleave_u32(data: bytes, offset: int, count: int) -> list[int]:
    
    values: list[int] = []
    total = count * 4
    block = data[offset : offset + total]
    for i in range(count):
        b0 = block[i]
        b1 = block[count + i]
        b2 = block[2 * count + i]
        b3 = block[3 * count + i]
        values.append((b0 << 24) | (b1 << 16) | (b2 << 8) | b3)
    return values

def deinterleave_i32(data: bytes, offset: int, count: int) -> list[int]:
    
    raw = deinterleave_u32(data, offset, count)
    return [decode_zigzag(v) for v in raw]

def deinterleave_f32(data: bytes, offset: int, count: int) -> list[float]:
    
    raw = deinterleave_u32(data, offset, count)
    result: list[float] = []
    for v in raw:
        
        bits = (v >> 1) | ((v & 1) << 31)
        result.append(struct.unpack('<f', struct.pack('<I', bits))[0])
    return result

def deinterleave_i64(data: bytes, offset: int, count: int) -> list[int]:
    
    values: list[int] = []
    total = count * 8
    block = data[offset : offset + total]
    for i in range(count):
        val = 0
        for byte_idx in range(8):
            val = (val << 8) | block[byte_idx * count + i]
        
        values.append((val >> 1) ^ (-(val & 1)))
    return values

def deinterleave_u64(data: bytes, offset: int, count: int) -> list[int]:
    
    values: list[int] = []
    total = count * 8
    block = data[offset : offset + total]
    for i in range(count):
        val = 0
        for byte_idx in range(8):
            val = (val << 8) | block[byte_idx * count + i]
        values.append(val)
    return values

def deinterleave_bytes(data: bytes, offset: int, count: int, width: int) -> list[bytes]:
    
    block = data[offset : offset + count * width]
    return [bytes(block[byte_idx * count + i] for byte_idx in range(width)) for i in range(count)]

def decode_ids(data: bytes, offset: int, count: int) -> tuple[list[int], int]:
    
    deltas = deinterleave_i32(data, offset, count)
    ids: list[int] = []
    acc = 0
    for d in deltas:
        acc += d
        ids.append(acc)
    return ids, offset + count * 4

import struct

def write_u8(value: int) -> bytes:
    return bytes([value & 0xFF])

def write_u16(value: int) -> bytes:
    return struct.pack('<H', value)

def write_u32(value: int) -> bytes:
    return struct.pack('<I', value)

def write_i32(value: int) -> bytes:
    return struct.pack('<i', value)

def write_f32(value: float) -> bytes:
    return struct.pack('<f', value)

def write_f64(value: float) -> bytes:
    return struct.pack('<d', value)

def write_string(value: str) -> bytes:
    
    encoded = value.encode('utf-8')
    return write_u32(len(encoded)) + encoded

def write_binary_string(value: bytes) -> bytes:
    
    return write_u32(len(value)) + value

def encode_zigzag32(value: int) -> int:
    
    return ((value << 1) ^ (value >> 31)) & 0xFFFF_FFFF

def encode_zigzag64(value: int) -> int:
    
    return ((value << 1) ^ (value >> 63)) & 0xFFFF_FFFF_FFFF_FFFF

def interleave_u32(values: list[int]) -> bytes:
    
    count = len(values)
    out = bytearray(count * 4)
    for i, v in enumerate(values):
        out[i] = (v >> 24) & 0xFF
        out[count + i] = (v >> 16) & 0xFF
        out[2 * count + i] = (v >> 8) & 0xFF
        out[3 * count + i] = v & 0xFF
    return bytes(out)

def interleave_i32(values: list[int]) -> bytes:
    
    return interleave_u32([encode_zigzag32(v) for v in values])

def interleave_f32(values: list[float]) -> bytes:
    
    raw_ints: list[int] = []
    for v in values:
        bits = struct.unpack('<I', struct.pack('<f', v))[0]
        rotated = (((bits & 0x7FFFFFFF) << 1) | (bits >> 31)) & 0xFFFF_FFFF
        raw_ints.append(rotated)
    return interleave_u32(raw_ints)

def interleave_i64(values: list[int]) -> bytes:
    
    count = len(values)
    out = bytearray(count * 8)
    for i, v in enumerate(values):
        zz = encode_zigzag64(v)
        for byte_idx in range(8):
            
            out[byte_idx * count + i] = (zz >> (56 - byte_idx * 8)) & 0xFF
    return bytes(out)

def interleave_u64(values: list[int]) -> bytes:
    
    count = len(values)
    out = bytearray(count * 8)
    for i, v in enumerate(values):
        v &= 0xFFFF_FFFF_FFFF_FFFF
        for byte_idx in range(8):
            out[byte_idx * count + i] = (v >> (56 - byte_idx * 8)) & 0xFF
    return bytes(out)

def interleave_bytes(values: list[bytes], width: int) -> bytes:
    
    count = len(values)
    out = bytearray(count * width)
    for i, value in enumerate(values):
        if len(value) != width:
            msg = f'Expected {width}-byte record, got {len(value)} bytes'
            raise ValueError(msg)
        for byte_idx, byte in enumerate(value):
            out[byte_idx * count + i] = byte
    return bytes(out)

def encode_ids(ids: list[int]) -> bytes:
    
    deltas: list[int] = []
    prev = 0
    for v in ids:
        deltas.append(v - prev)
        prev = v
    return interleave_i32(deltas)

import struct
from collections import defaultdict
from typing import Any

import lz4.block  

MAGIC_HEADER = b'<roblox!\x89\xff\x0d\x0a\x1a\x0a'
FILE_VERSION = 0  

def write_rbxm(doc: RbxDocument) -> bytes:
    
    s = RbxmSerializer(doc)
    return s.serialize()

class RbxmSerializer:
    
    def __init__(self, doc: RbxDocument) -> None:
        self._doc = doc

        self._type_index: dict[str, int] = {}
        self._type_instances: dict[int, list[RbxInstance]] = defaultdict(list)
        self._all_instances: list[RbxInstance] = []
        self._shared_strings: list[bytes] = []
        self._shared_string_index: dict[bytes, int] = {}
        self._assign_types()
        self._collect_shared_strings()

    def _walk(self) -> list[RbxInstance]:
        
        result: list[RbxInstance] = []
        queue = list(self._doc.roots)
        while queue:
            inst = queue.pop(0)
            result.append(inst)
            queue.extend(inst.children)
        return result

    def _assign_types(self) -> None:
        self._all_instances = self._walk()
        for inst in self._all_instances:
            if inst.class_name not in self._type_index:
                idx = len(self._type_index)
                self._type_index[inst.class_name] = idx
            self._type_instances[self._type_index[inst.class_name]].append(inst)

    def _collect_shared_strings(self) -> None:
        
        for inst in self._all_instances:
            for prop in inst.properties.values():
                if prop.fmt == PropertyFormat.SHARED_STRING and isinstance(prop.value, bytes):
                    if prop.value not in self._shared_string_index:
                        self._shared_string_index[prop.value] = len(self._shared_strings)
                        self._shared_strings.append(prop.value)

    def serialize(self) -> bytes:
        type_count = len(self._type_index)
        object_count = len(self._all_instances)

        chunks = bytearray()

        if self._doc.metadata.entries:
            chunks.extend(self._build_chunk('META', self._build_meta()))

        if self._shared_strings:
            chunks.extend(self._build_chunk('SSTR', self._build_sstr()))

        for class_name, type_idx in self._type_index.items():
            chunks.extend(self._build_chunk('INST', self._build_inst(type_idx, class_name)))

        for type_idx, instances in self._type_instances.items():
            for prop_name in self._collect_prop_names(instances):
                prop_data = self._build_prop(type_idx, prop_name, instances)
                if prop_data is not None:
                    chunks.extend(self._build_chunk('PROP', prop_data))

        for prop_data in self._build_raw_props():
            chunks.extend(self._build_chunk('PROP', prop_data))

        for raw_chunk in self._doc.raw_chunks:
            chunks.extend(self._build_chunk(raw_chunk.name, raw_chunk.data))

        chunks.extend(self._build_chunk('PRNT', self._build_prnt()))
        chunks.extend(self._build_chunk('END\x00', b'</roblox>'))

        header = (
            MAGIC_HEADER
            + struct.pack('<H', FILE_VERSION)
            + struct.pack('<I', type_count)
            + struct.pack('<I', object_count)
            + b'\x00' * 8  
        )
        return header + bytes(chunks)

    @staticmethod
    def _build_chunk(name: str, data: bytes) -> bytes:
        
        name_b = name.encode('ascii')[:4].ljust(4, b'\x00')
        uncompressed_size = len(data)

        if uncompressed_size == 0:
            return name_b + struct.pack('<III', 0, 0, 0)

        compressed = lz4.block.compress(data, store_size=False)
        if len(compressed) < uncompressed_size:
            return name_b + struct.pack('<III', len(compressed), uncompressed_size, 0) + compressed
        else:
            
            return name_b + struct.pack('<III', 0, uncompressed_size, 0) + data

    def _build_meta(self) -> bytes:
        buf = bytearray()
        entries = self._doc.metadata.entries
        buf.extend(write_u32(len(entries)))
        for key, value in entries.items():
            buf.extend(write_string(key))
            buf.extend(write_string(value))
        return bytes(buf)

    def _build_sstr(self) -> bytes:
        import base64
        import hashlib  

        buf = bytearray()
        buf.extend(write_u32(0))  
        buf.extend(write_u32(len(self._shared_strings)))
        for blob in self._shared_strings:
            md5 = hashlib.md5(blob).digest()  
            buf.extend(md5)
            buf.extend(write_binary_string(blob))
        return bytes(buf)

    def _build_inst(self, type_idx: int, class_name: str) -> bytes:
        instances = self._type_instances[type_idx]
        ids = [inst.referent for inst in instances]
        is_service = any(inst.is_service for inst in instances)

        buf = bytearray()
        buf.extend(write_u32(type_idx))
        buf.extend(write_string(class_name))
        buf.extend(write_u8(1 if is_service else 0))
        buf.extend(write_u32(len(ids)))
        buf.extend(encode_ids(ids))

        if is_service:
            for inst in instances:
                buf.extend(write_u8(1 if inst.is_service else 0))

        return bytes(buf)

    @staticmethod
    def _collect_prop_names(instances: list[RbxInstance]) -> list[str]:
        
        names: set[str] = set()
        for inst in instances:
            names.update(inst.properties.keys())
        return sorted(names)

    def _build_prop(
        self,
        type_idx: int,
        prop_name: str,
        instances: list[RbxInstance],
    ) -> bytes | None:
        
        fmt: PropertyFormat | None = None
        values: list[Any] = []
        for inst in instances:
            prop = inst.properties.get(prop_name)
            if prop is not None:
                if fmt is None:
                    fmt = prop.fmt
                values.append(prop.value)
            else:
                values.append(None)

        if fmt is None:
            return None  

        values = [self._default_value(fmt) if v is None else v for v in values]

        encoded = self._encode_prop_values(fmt, values)
        if encoded is None:
            return None

        buf = bytearray()
        buf.extend(write_u32(type_idx))
        buf.extend(write_string(prop_name))
        buf.extend(write_u8(int(fmt)))
        buf.extend(encoded)
        return bytes(buf)

    @staticmethod
    def _default_value(fmt: PropertyFormat) -> Any:
        match fmt:
            case PropertyFormat.STRING:
                return b''
            case PropertyFormat.BOOL:
                return False
            case PropertyFormat.INT | PropertyFormat.ENUM | PropertyFormat.BRICK_COLOR:
                return 0
            case PropertyFormat.FLOAT | PropertyFormat.DOUBLE:
                return 0.0
            case PropertyFormat.UDIM:
                return {'S': 0.0, 'O': 0}
            case PropertyFormat.UDIM2:
                return {'XS': 0.0, 'XO': 0, 'YS': 0.0, 'YO': 0}
            case PropertyFormat.RAY:
                return {
                    'origin': {'X': 0.0, 'Y': 0.0, 'Z': 0.0},
                    'direction': {'X': 0.0, 'Y': 0.0, 'Z': 0.0},
                }
            case PropertyFormat.FACES | PropertyFormat.AXES:
                return 0
            case PropertyFormat.COLOR3:
                return {'R': 0.0, 'G': 0.0, 'B': 0.0}
            case PropertyFormat.VECTOR2:
                return {'X': 0.0, 'Y': 0.0}
            case PropertyFormat.VECTOR3:
                return {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
            case PropertyFormat.VECTOR2INT16:
                return {'X': 0, 'Y': 0}
            case PropertyFormat.VECTOR3INT16:
                return {'X': 0, 'Y': 0, 'Z': 0}
            case PropertyFormat.CFRAME_MATRIX | PropertyFormat.CFRAME_QUAT:
                return {
                    'X': 0.0,
                    'Y': 0.0,
                    'Z': 0.0,
                    'R00': 1.0,
                    'R01': 0.0,
                    'R02': 0.0,
                    'R10': 0.0,
                    'R11': 1.0,
                    'R12': 0.0,
                    'R20': 0.0,
                    'R21': 0.0,
                    'R22': 1.0,
                }
            case PropertyFormat.OPTIONAL_CFRAME:
                return None
            case PropertyFormat.REF:
                return None
            case PropertyFormat.NUMBER_SEQUENCE:
                return []
            case PropertyFormat.COLOR_SEQUENCE:
                return []
            case PropertyFormat.NUMBER_RANGE:
                return {'Min': 0.0, 'Max': 1.0}
            case PropertyFormat.RECT2D:
                return {'min': {'X': 0.0, 'Y': 0.0}, 'max': {'X': 0.0, 'Y': 0.0}}
            case PropertyFormat.PHYSICAL_PROPERTIES:
                return None
            case PropertyFormat.COLOR3UINT8:
                return {'R': 0, 'G': 0, 'B': 0}
            case PropertyFormat.INT64:
                return 0
            case PropertyFormat.SHARED_STRING:
                return b''
            case PropertyFormat.BYTECODE:
                return b''
            case PropertyFormat.UNIQUE_ID:
                return {'Index': 0, 'Time': 0, 'Random': 0}
            case PropertyFormat.FONT:
                return {'Family': '', 'Weight': 400, 'Style': 0, 'CachedFaceId': ''}
            case PropertyFormat.SECURITY_CAPABILITIES:
                return 0
            case PropertyFormat.CONTENT:
                return None
            case _:
                return None

    def _encode_prop_values(self, fmt: PropertyFormat, values: list[Any]) -> bytes | None:
        
        match fmt:
            case PropertyFormat.STRING:
                return self._enc_strings(values)
            case PropertyFormat.BOOL:
                return bytes([1 if v else 0 for v in values])
            case PropertyFormat.INT:
                return interleave_i32([int(v) for v in values])
            case PropertyFormat.FLOAT:
                return interleave_f32([float(v) for v in values])
            case PropertyFormat.DOUBLE:
                return b''.join(write_f64(float(v)) for v in values)
            case PropertyFormat.UDIM:
                return interleave_f32([float(v['S']) for v in values]) + interleave_i32(
                    [int(v['O']) for v in values]
                )
            case PropertyFormat.UDIM2:
                return (
                    interleave_f32([float(v['XS']) for v in values])
                    + interleave_f32([float(v['YS']) for v in values])
                    + interleave_i32([int(v['XO']) for v in values])
                    + interleave_i32([int(v['YO']) for v in values])
                )
            case PropertyFormat.RAY:
                buf = bytearray()
                for v in values:
                    o, d = v['origin'], v['direction']
                    buf.extend(write_f32(o['X']))
                    buf.extend(write_f32(o['Y']))
                    buf.extend(write_f32(o['Z']))
                    buf.extend(write_f32(d['X']))
                    buf.extend(write_f32(d['Y']))
                    buf.extend(write_f32(d['Z']))
                return bytes(buf)
            case PropertyFormat.FACES | PropertyFormat.AXES:
                return bytes([int(v) for v in values])
            case PropertyFormat.BRICK_COLOR:
                return interleave_u32([int(v) for v in values])
            case PropertyFormat.COLOR3:
                return (
                    interleave_f32([float(v['R']) for v in values])
                    + interleave_f32([float(v['G']) for v in values])
                    + interleave_f32([float(v['B']) for v in values])
                )
            case PropertyFormat.VECTOR2:
                return interleave_f32([float(v['X']) for v in values]) + interleave_f32(
                    [float(v['Y']) for v in values]
                )
            case PropertyFormat.VECTOR3:
                return (
                    interleave_f32([float(v['X']) for v in values])
                    + interleave_f32([float(v['Y']) for v in values])
                    + interleave_f32([float(v['Z']) for v in values])
                )
            case PropertyFormat.VECTOR2INT16:
                return b''.join(struct.pack('<hh', int(v['X']), int(v['Y'])) for v in values)
            case PropertyFormat.VECTOR3INT16:
                return b''.join(
                    struct.pack('<hhh', int(v['X']), int(v['Y']), int(v['Z'])) for v in values
                )
            case PropertyFormat.CFRAME_MATRIX | PropertyFormat.CFRAME_QUAT:
                return self._enc_cframes(values)
            case PropertyFormat.OPTIONAL_CFRAME:
                return self._enc_optional_cframes(values)
            case PropertyFormat.ENUM:
                return interleave_u32([int(v) for v in values])
            case PropertyFormat.REF:
                return self._enc_refs(values)
            case PropertyFormat.NUMBER_SEQUENCE:
                return self._enc_number_sequences(values)
            case PropertyFormat.COLOR_SEQUENCE:
                return self._enc_color_sequences(values)
            case PropertyFormat.NUMBER_RANGE:
                buf = bytearray()
                for v in values:
                    buf.extend(write_f32(float(v['Min'])))
                    buf.extend(write_f32(float(v['Max'])))
                return bytes(buf)
            case PropertyFormat.RECT2D:
                return (
                    interleave_f32([float(v['min']['X']) for v in values])
                    + interleave_f32([float(v['min']['Y']) for v in values])
                    + interleave_f32([float(v['max']['X']) for v in values])
                    + interleave_f32([float(v['max']['Y']) for v in values])
                )
            case PropertyFormat.PHYSICAL_PROPERTIES:
                return self._enc_physical_properties(values)
            case PropertyFormat.COLOR3UINT8:
                return (
                    bytes([int(v['R']) for v in values])
                    + bytes([int(v['G']) for v in values])
                    + bytes([int(v['B']) for v in values])
                )
            case PropertyFormat.INT64:
                return interleave_i64([int(v) for v in values])
            case PropertyFormat.SHARED_STRING:
                return self._enc_shared_strings(values)
            case PropertyFormat.BYTECODE:
                return self._enc_bytecodes(values)
            case PropertyFormat.UNIQUE_ID:
                return self._enc_unique_ids(values)
            case PropertyFormat.FONT:
                return self._enc_fonts(values)
            case PropertyFormat.SECURITY_CAPABILITIES:
                return interleave_u64([int(v) for v in values])
            case PropertyFormat.CONTENT:
                return self._enc_contents(values)
            case _:
                return None

    @staticmethod
    def _enc_strings(values: list[Any]) -> bytes:
        buf = bytearray()
        for v in values:
            if isinstance(v, bytes):
                buf.extend(write_binary_string(v))
            else:
                raw = str(v).encode('utf-8')
                buf.extend(write_u32(len(raw)))
                buf.extend(raw)
        return bytes(buf)

    @staticmethod
    def _enc_cframes(values: list[Any]) -> bytes:
        
        buf = bytearray()
        xs, ys, zs = [], [], []
        for cf in values:
            buf.extend(write_u8(0))  
            buf.extend(write_f32(float(cf['R00'])))
            buf.extend(write_f32(float(cf['R01'])))
            buf.extend(write_f32(float(cf['R02'])))
            buf.extend(write_f32(float(cf['R10'])))
            buf.extend(write_f32(float(cf['R11'])))
            buf.extend(write_f32(float(cf['R12'])))
            buf.extend(write_f32(float(cf['R20'])))
            buf.extend(write_f32(float(cf['R21'])))
            buf.extend(write_f32(float(cf['R22'])))
            xs.append(float(cf['X']))
            ys.append(float(cf['Y']))
            zs.append(float(cf['Z']))
        buf.extend(interleave_f32(xs))
        buf.extend(interleave_f32(ys))
        buf.extend(interleave_f32(zs))
        return bytes(buf)

    @staticmethod
    def _enc_refs(values: list[Any]) -> bytes:
        
        ids = [(-1 if v is None else int(v)) for v in values]
        return encode_ids(ids)

    @staticmethod
    def _enc_number_sequences(values: list[Any]) -> bytes:
        buf = bytearray()
        for seq in values:
            buf.extend(write_u32(len(seq)))
            for key in seq:
                buf.extend(write_f32(float(key['Time'])))
                buf.extend(write_f32(float(key['Value'])))
                buf.extend(write_f32(float(key['Envelope'])))
        return bytes(buf)

    @staticmethod
    def _enc_color_sequences(values: list[Any]) -> bytes:
        buf = bytearray()
        for seq in values:
            buf.extend(write_u32(len(seq)))
            for key in seq:
                buf.extend(write_f32(float(key['Time'])))
                buf.extend(write_f32(float(key['R'])))
                buf.extend(write_f32(float(key['G'])))
                buf.extend(write_f32(float(key['B'])))
                buf.extend(write_f32(0.0))  
        return bytes(buf)

    @staticmethod
    def _enc_physical_properties(values: list[Any]) -> bytes:
        buf = bytearray()
        for v in values:
            if v is None:
                buf.extend(write_u8(0))
            elif not v.get('CustomPhysics', True):
                buf.extend(write_u8(2 if v.get('HasAcousticAbsorption') else 0))
            else:
                has_acoustic_absorption = 'AcousticAbsorption' in v
                buf.extend(write_u8(3 if has_acoustic_absorption else 1))
                buf.extend(write_f32(float(v['Density'])))
                buf.extend(write_f32(float(v['Friction'])))
                buf.extend(write_f32(float(v['Elasticity'])))
                buf.extend(write_f32(float(v['FrictionWeight'])))
                buf.extend(write_f32(float(v['ElasticityWeight'])))
                if has_acoustic_absorption:
                    buf.extend(write_f32(float(v['AcousticAbsorption'])))
        return bytes(buf)

    def _enc_shared_strings(self, values: list[Any]) -> bytes:
        
        indices = []
        for v in values:
            if isinstance(v, bytes) and v in self._shared_string_index:
                indices.append(self._shared_string_index[v])
            else:
                indices.append(0)
        return interleave_u32(indices)

    @staticmethod
    def _enc_bytecodes(values: list[Any]) -> bytes:
        buf = bytearray()
        for value in values:
            if isinstance(value, bytes):
                buf.extend(write_binary_string(value))
            else:
                buf.extend(write_binary_string(str(value).encode('utf-8')))
        return bytes(buf)

    @staticmethod
    def _enc_optional_cframes(values: list[Any]) -> bytes:
        default = RbxmSerializer._default_value(PropertyFormat.CFRAME_MATRIX)
        cframes = [default if value is None else value for value in values]
        present = [value is not None for value in values]
        return (
            write_u8(int(PropertyFormat.CFRAME_MATRIX))
            + RbxmSerializer._enc_cframes(cframes)
            + write_u8(int(PropertyFormat.BOOL))
            + bytes([1 if value else 0 for value in present])
        )

    @staticmethod
    def _enc_unique_ids(values: list[Any]) -> bytes:
        records: list[bytes] = []
        for value in values:
            if isinstance(value, bytes):
                records.append(value)
                continue
            records.append(
                struct.pack(
                    '>IIQ',
                    int(value.get('Index', 0)) & 0xFFFF_FFFF,
                    int(value.get('Time', 0)) & 0xFFFF_FFFF,
                    int(value.get('Random', 0)) & 0xFFFF_FFFF_FFFF_FFFF,
                )
            )
        return interleave_bytes(records, 16)

    @staticmethod
    def _enc_fonts(values: list[Any]) -> bytes:
        style_names = {'Normal': 0, 'Italic': 1}
        buf = bytearray()
        for value in values:
            family = str(value.get('Family', '')).encode('utf-8')
            cached_face_id = str(value.get('CachedFaceId', '')).encode('utf-8')
            style = value.get('Style', 0)
            if isinstance(style, str):
                style = style_names.get(style, 0)
            buf.extend(write_binary_string(family))
            buf.extend(write_u16(int(value.get('Weight', 400))))
            buf.extend(write_u8(int(style)))
            buf.extend(write_binary_string(cached_face_id))
        return bytes(buf)

    @staticmethod
    def _enc_contents(values: list[Any]) -> bytes:
        source_types: list[int] = []
        uris: list[str] = []
        object_refs: list[int] = []
        external_object_refs: list[int] = []

        for value in values:
            if value is None:
                source_types.append(0)
            elif isinstance(value, str):
                if value:
                    source_types.append(1)
                    uris.append(value)
                else:
                    source_types.append(0)
            elif value.get('SourceType') == 'Uri':
                source_types.append(1)
                uris.append(str(value.get('Uri', '')))
            elif value.get('SourceType') == 'Object':
                source_types.append(2)
                ref = -1 if value.get('Ref') is None else int(value['Ref'])
                if value.get('External'):
                    external_object_refs.append(ref)
                else:
                    object_refs.append(ref)
            else:
                source_types.append(int(value.get('SourceType', 0)))

        buf = bytearray()
        buf.extend(interleave_u32(source_types))
        buf.extend(write_u32(len(uris)))
        for uri in uris:
            buf.extend(write_binary_string(uri.encode('utf-8')))
        buf.extend(write_u32(len(object_refs)))
        buf.extend(encode_ids(object_refs))
        buf.extend(write_u32(len(external_object_refs)))
        buf.extend(encode_ids(external_object_refs))
        return bytes(buf)

    def _build_raw_props(self) -> list[bytes]:
        props: list[bytes] = []
        for raw in self._doc.raw_property_chunks:
            prop = self._build_raw_prop(raw)
            if prop is not None:
                props.append(prop)
        return props

    def _build_raw_prop(self, raw: RbxRawPropertyChunk) -> bytes | None:
        type_idx = self._type_index.get(raw.class_name)
        if type_idx is None:
            return None
        if len(self._type_instances[type_idx]) != raw.instance_count:
            return None

        buf = bytearray()
        buf.extend(write_u32(type_idx))
        buf.extend(write_string(raw.prop_name))
        buf.extend(write_u8(raw.fmt_byte))
        buf.extend(raw.value_data)
        return bytes(buf)

    def _build_prnt(self) -> bytes:
        
        child_to_parent: dict[int, int] = {}
        for inst in self._all_instances:
            for child in inst.children:
                child_to_parent[child.referent] = inst.referent

        child_ids: list[int] = []
        parent_ids: list[int] = []
        for inst in self._all_instances:
            child_ids.append(inst.referent)
            parent_ids.append(child_to_parent.get(inst.referent, -1))

        buf = bytearray()
        buf.extend(write_u8(0))  
        buf.extend(write_u32(len(child_ids)))
        buf.extend(encode_ids(child_ids))
        buf.extend(encode_ids(parent_ids))
        return bytes(buf)

import base64
import hashlib
import logging
from typing import Any
from xml.etree.ElementTree import Element, SubElement, indent, tostring
log = logging.getLogger(__name__)

_shared_string_registry: dict[str, str] = {}

def write_rbxmx(doc: RbxDocument) -> bytes:
    
    _shared_string_registry.clear()

    root = Element('roblox')
    root.set('xmlns:xmime', 'http://www.w3.org/2005/05/xmlmime')
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.set(
        'xsi:noNamespaceSchemaLocation',
        'http://www.roblox.com/roblox.xsd',
    )
    root.set('version', '4')

    ext1 = SubElement(root, 'External')
    ext1.text = 'null'
    ext2 = SubElement(root, 'External')
    ext2.text = 'nil'

    for key, value in doc.metadata.entries.items():
        meta_el = SubElement(root, 'Meta')
        meta_el.set('name', key)
        meta_el.text = value

    for inst in doc.roots:
        _write_instance(root, inst, doc)

    if _shared_string_registry:
        ss_section = SubElement(root, 'SharedStrings')
        for md5_hash, b64_content in _shared_string_registry.items():
            ss_el = SubElement(ss_section, 'SharedString')
            ss_el.set('md5', md5_hash)
            ss_el.text = b64_content

    indent(root, space='\t')
    xml_bytes = tostring(root, encoding='unicode', xml_declaration=False)
    header = '<?xml version="1.0" encoding="utf-8"?>\n'
    return (header + xml_bytes).encode('utf-8')

def _write_instance(
    parent_el: Element,
    inst: RbxInstance,
    doc: RbxDocument,
) -> None:
    
    item = SubElement(parent_el, 'Item')
    item.set('class', inst.class_name)
    item.set('referent', f'RBX{inst.referent:032X}')

    props_el = SubElement(item, 'Properties')

    for prop in sorted(inst.properties.values(), key=lambda p: p.name):
        _write_property(props_el, prop, doc)

    for child in inst.children:
        _write_instance(item, child, doc)

def _write_property(
    props_el: Element,
    prop: RbxProperty,
    doc: RbxDocument,  
) -> None:
    
    xml_tag = PROPERTY_FORMAT_TO_XML_TAG.get(prop.fmt, 'string')

    match prop.fmt:
        case PropertyFormat.STRING:
            _write_string_prop(props_el, xml_tag, prop)
        case PropertyFormat.BOOL:
            el = SubElement(props_el, xml_tag)
            el.set('name', prop.name)
            el.text = 'true' if prop.value else 'false'
        case PropertyFormat.INT | PropertyFormat.ENUM | PropertyFormat.BRICK_COLOR:
            el = SubElement(props_el, xml_tag)
            el.set('name', prop.name)
            el.text = str(prop.value)
        case PropertyFormat.FLOAT:
            el = SubElement(props_el, xml_tag)
            el.set('name', prop.name)
            el.text = _fmt_float(prop.value)
        case PropertyFormat.DOUBLE:
            el = SubElement(props_el, xml_tag)
            el.set('name', prop.name)
            el.text = _fmt_float(prop.value)
        case PropertyFormat.UDIM:
            _write_udim(props_el, prop)
        case PropertyFormat.UDIM2:
            _write_udim2(props_el, prop)
        case PropertyFormat.RAY:
            _write_ray(props_el, prop)
        case PropertyFormat.FACES:
            _write_faces(props_el, prop)
        case PropertyFormat.AXES:
            _write_axes(props_el, prop)
        case PropertyFormat.COLOR3:
            _write_color3(props_el, xml_tag, prop)
        case PropertyFormat.VECTOR2:
            _write_vector2(props_el, prop)
        case PropertyFormat.VECTOR3:
            _write_vector3(props_el, xml_tag, prop)
        case PropertyFormat.VECTOR2INT16:
            _write_vector_int(props_el, 'Vector2int16', prop, ('X', 'Y'))
        case PropertyFormat.VECTOR3INT16:
            _write_vector_int(props_el, 'Vector3int16', prop, ('X', 'Y', 'Z'))
        case PropertyFormat.CFRAME_MATRIX | PropertyFormat.CFRAME_QUAT:
            _write_cframe(props_el, prop)
        case PropertyFormat.OPTIONAL_CFRAME:
            _write_optional_cframe(props_el, prop)
        case PropertyFormat.REF:
            _write_ref(props_el, prop)
        case PropertyFormat.NUMBER_SEQUENCE:
            _write_number_sequence(props_el, prop)
        case PropertyFormat.COLOR_SEQUENCE:
            _write_color_sequence(props_el, prop)
        case PropertyFormat.NUMBER_RANGE:
            _write_number_range(props_el, prop)
        case PropertyFormat.RECT2D:
            _write_rect2d(props_el, prop)
        case PropertyFormat.PHYSICAL_PROPERTIES:
            _write_physical_properties(props_el, prop)
        case PropertyFormat.COLOR3UINT8:
            _write_color3uint8(props_el, prop)
        case PropertyFormat.INT64:
            el = SubElement(props_el, xml_tag)
            el.set('name', prop.name)
            el.text = str(prop.value)
        case PropertyFormat.BYTECODE:
            el = SubElement(props_el, xml_tag)
            el.set('name', prop.name)
            if isinstance(prop.value, bytes):
                el.text = base64.b64encode(prop.value).decode('ascii')
            else:
                el.text = base64.b64encode(str(prop.value).encode('utf-8')).decode('ascii')
        case PropertyFormat.UNIQUE_ID:
            _write_unique_id(props_el, prop)
        case PropertyFormat.FONT:
            _write_font(props_el, prop)
        case PropertyFormat.SECURITY_CAPABILITIES:
            el = SubElement(props_el, xml_tag)
            el.set('name', prop.name)
            el.text = str(prop.value)
        case PropertyFormat.CONTENT:
            _write_content(props_el, prop)
        case PropertyFormat.SHARED_STRING:
            _write_shared_string(props_el, prop)
        case _:
            log.warning('Skipping unhandled property format: %s', prop.fmt)

def _has_invalid_xml_chars(s: str) -> bool:
    
    for ch in s:
        codepoint = ord(ch)
        if codepoint < 0x20 and ch not in '\t\n\r':
            return True
        if 0xD800 <= codepoint <= 0xDFFF:
            return True
        if codepoint in (0xFFFE, 0xFFFF):
            return True
    return False

def _write_string_prop(parent: Element, tag: str, prop: RbxProperty) -> None:
    val = prop.value
    if isinstance(val, bytes):
        
        el = SubElement(parent, 'BinaryString')
        el.set('name', prop.name)
        el.text = base64.b64encode(val).decode('ascii')
        return

    if not isinstance(val, str):
        val = '' if val is None else str(val)

    if _has_invalid_xml_chars(val):
        
        el = SubElement(parent, 'BinaryString')
        el.set('name', prop.name)
        el.text = base64.b64encode(val.encode('utf-8', errors='surrogatepass')).decode('ascii')
        return

    if prop.name in {'Source', 'LinkedSource'}:
        el = SubElement(parent, 'ProtectedString')
        el.set('name', prop.name)
        el.text = val
    
    elif _is_content_url(val, prop.name):
        el = SubElement(parent, 'Content')
        el.set('name', prop.name)
        if val:
            url_el = SubElement(el, 'url')
            url_el.text = val
        else:
            SubElement(el, 'null')
    else:
        el = SubElement(parent, tag)
        el.set('name', prop.name)
        el.text = val

def _is_content_url(value: str, prop_name: str) -> bool:
    
    content_props = {
        'AssetId',
        'MeshId',
        'TextureId',
        'SoundId',
        'Texture',
        'LinkedSource',
        'Image',
        'Animation',
    }
    if prop_name in content_props:
        return True
    return value.startswith(('http://', 'https://', 'rbxassetid://', 'rbxasset://'))

def _write_udim(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'UDim')
    el.set('name', prop.name)
    SubElement(el, 'S').text = _fmt_float(prop.value['S'])
    SubElement(el, 'O').text = str(prop.value['O'])

def _write_udim2(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'UDim2')
    el.set('name', prop.name)
    SubElement(el, 'XS').text = _fmt_float(prop.value['XS'])
    SubElement(el, 'XO').text = str(prop.value['XO'])
    SubElement(el, 'YS').text = _fmt_float(prop.value['YS'])
    SubElement(el, 'YO').text = str(prop.value['YO'])

def _write_ray(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'Ray')
    el.set('name', prop.name)
    origin = SubElement(el, 'origin')
    SubElement(origin, 'X').text = _fmt_float(prop.value['origin']['X'])
    SubElement(origin, 'Y').text = _fmt_float(prop.value['origin']['Y'])
    SubElement(origin, 'Z').text = _fmt_float(prop.value['origin']['Z'])
    direction = SubElement(el, 'direction')
    SubElement(direction, 'X').text = _fmt_float(prop.value['direction']['X'])
    SubElement(direction, 'Y').text = _fmt_float(prop.value['direction']['Y'])
    SubElement(direction, 'Z').text = _fmt_float(prop.value['direction']['Z'])

def _write_faces(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'Faces')
    el.set('name', prop.name)
    mask = prop.value
    faces: list[str] = []
    face_names = ['Right', 'Top', 'Back', 'Left', 'Bottom', 'Front']
    for i, name in enumerate(face_names):
        if mask & (1 << i):
            faces.append(name)
    el.text = ', '.join(faces) if faces else ''

def _write_axes(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'Axes')
    el.set('name', prop.name)
    mask = prop.value
    axes: list[str] = []
    axis_names = ['X', 'Y', 'Z']
    for i, name in enumerate(axis_names):
        if mask & (1 << i):
            axes.append(name)
    el.text = ', '.join(axes) if axes else ''

def _write_color3(parent: Element, tag: str, prop: RbxProperty) -> None:
    el = SubElement(parent, tag)
    el.set('name', prop.name)
    SubElement(el, 'R').text = _fmt_float(prop.value['R'])
    SubElement(el, 'G').text = _fmt_float(prop.value['G'])
    SubElement(el, 'B').text = _fmt_float(prop.value['B'])

def _write_vector2(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'Vector2')
    el.set('name', prop.name)
    SubElement(el, 'X').text = _fmt_float(prop.value['X'])
    SubElement(el, 'Y').text = _fmt_float(prop.value['Y'])

def _write_vector3(parent: Element, tag: str, prop: RbxProperty) -> None:
    el = SubElement(parent, tag)
    el.set('name', prop.name)
    SubElement(el, 'X').text = _fmt_float(prop.value['X'])
    SubElement(el, 'Y').text = _fmt_float(prop.value['Y'])
    SubElement(el, 'Z').text = _fmt_float(prop.value['Z'])

def _write_vector_int(parent: Element, tag: str, prop: RbxProperty, axes: tuple[str, ...]) -> None:
    el = SubElement(parent, tag)
    el.set('name', prop.name)
    for axis in axes:
        SubElement(el, axis).text = str(prop.value[axis])

def _write_cframe(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'CoordinateFrame')
    el.set('name', prop.name)
    cf: dict[str, float] = prop.value
    SubElement(el, 'X').text = _fmt_float(cf['X'])
    SubElement(el, 'Y').text = _fmt_float(cf['Y'])
    SubElement(el, 'Z').text = _fmt_float(cf['Z'])
    for row in range(3):
        for col in range(3):
            key = f'R{row}{col}'
            SubElement(el, key).text = _fmt_float(cf[key])

def _write_cframe_fields(parent: Element, cf: dict[str, float]) -> None:
    SubElement(parent, 'X').text = _fmt_float(cf['X'])
    SubElement(parent, 'Y').text = _fmt_float(cf['Y'])
    SubElement(parent, 'Z').text = _fmt_float(cf['Z'])
    for row in range(3):
        for col in range(3):
            key = f'R{row}{col}'
            SubElement(parent, key).text = _fmt_float(cf[key])

def _write_optional_cframe(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'OptionalCoordinateFrame')
    el.set('name', prop.name)
    if prop.value is None:
        return
    cf_el = SubElement(el, 'CFrame')
    _write_cframe_fields(cf_el, prop.value)

def _write_ref(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'Ref')
    el.set('name', prop.name)
    if prop.value is None:
        el.text = 'null'
    else:
        el.text = f'RBX{prop.value:032X}'

def _write_number_sequence(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'NumberSequence')
    el.set('name', prop.name)
    parts: list[str] = [
        f'{_fmt_float(key["Time"])} {_fmt_float(key["Value"])} {_fmt_float(key["Envelope"])}'
        for key in prop.value
    ]
    el.text = ' '.join(parts)

def _write_color_sequence(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'ColorSequence')
    el.set('name', prop.name)
    parts: list[str] = [
        f'{_fmt_float(key["Time"])} {_fmt_float(key["R"])} '
        f'{_fmt_float(key["G"])} {_fmt_float(key["B"])} 0'
        for key in prop.value
    ]
    el.text = ' '.join(parts)

def _write_number_range(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'NumberRange')
    el.set('name', prop.name)
    el.text = f'{_fmt_float(prop.value["Min"])} {_fmt_float(prop.value["Max"])}'

def _write_rect2d(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'Rect2D')
    el.set('name', prop.name)
    mn: dict[str, Any] = prop.value['min']
    mx: dict[str, Any] = prop.value['max']
    min_el = SubElement(el, 'min')
    SubElement(min_el, 'X').text = _fmt_float(mn['X'])
    SubElement(min_el, 'Y').text = _fmt_float(mn['Y'])
    max_el = SubElement(el, 'max')
    SubElement(max_el, 'X').text = _fmt_float(mx['X'])
    SubElement(max_el, 'Y').text = _fmt_float(mx['Y'])

def _write_physical_properties(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'PhysicalProperties')
    el.set('name', prop.name)
    if prop.value is None or not prop.value.get('CustomPhysics', True):
        SubElement(el, 'CustomPhysics').text = 'false'
    else:
        SubElement(el, 'CustomPhysics').text = 'true'
        SubElement(el, 'Density').text = _fmt_float(prop.value['Density'])
        SubElement(el, 'Friction').text = _fmt_float(prop.value['Friction'])
        SubElement(el, 'Elasticity').text = _fmt_float(prop.value['Elasticity'])
        SubElement(el, 'FrictionWeight').text = _fmt_float(prop.value['FrictionWeight'])
        SubElement(el, 'ElasticityWeight').text = _fmt_float(prop.value['ElasticityWeight'])
        SubElement(el, 'AcousticAbsorption').text = _fmt_float(
            prop.value.get('AcousticAbsorption', 1.0)
        )

def _write_color3uint8(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'Color3uint8')
    el.set('name', prop.name)
    
    r = prop.value['R']
    g = prop.value['G']
    b = prop.value['B']
    packed = 0xFF000000 | (r << 16) | (g << 8) | b
    el.text = str(packed)

def _write_shared_string(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'SharedString')
    el.set('name', prop.name)
    if isinstance(prop.value, bytes):
        
        md5_b64 = base64.b64encode(hashlib.md5(prop.value).digest()).decode('ascii')  
        b64_content = base64.b64encode(prop.value).decode('ascii')
        
        _shared_string_registry[md5_b64] = b64_content
        
        el.text = md5_b64
    else:
        el.text = str(prop.value)

def _write_unique_id(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'UniqueId')
    el.set('name', prop.name)
    if isinstance(prop.value, bytes):
        el.text = prop.value.hex()
        return

    random_bits = int(prop.value.get('Random', 0)) & 0xFFFF_FFFF_FFFF_FFFF
    xml_random = ((random_bits << 1) & 0xFFFF_FFFF_FFFF_FFFF) | (random_bits >> 63)
    time = int(prop.value.get('Time', 0)) & 0xFFFF_FFFF
    index = int(prop.value.get('Index', 0)) & 0xFFFF_FFFF
    el.text = f'{xml_random:016x}{time:08x}{index:08x}'

def _write_font(parent: Element, prop: RbxProperty) -> None:
    style_names = {0: 'Normal', 1: 'Italic'}
    el = SubElement(parent, 'Font')
    el.set('name', prop.name)
    family = SubElement(el, 'Family')
    _write_content_value(family, prop.value.get('Family', ''))
    SubElement(el, 'Weight').text = str(prop.value.get('Weight', 400))
    style = prop.value.get('Style', 0)
    SubElement(el, 'Style').text = style_names.get(style, str(style))
    cached_face_id = prop.value.get('CachedFaceId', '')
    if cached_face_id:
        cached = SubElement(el, 'CachedFaceId')
        _write_content_value(cached, cached_face_id)

def _write_content(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'Content')
    el.set('name', prop.name)
    _write_content_value(el, prop.value)

def _write_content_value(parent: Element, value: Any) -> None:
    if value is None:
        SubElement(parent, 'null')
    elif isinstance(value, str):
        if value:
            uri = SubElement(parent, 'uri')
            uri.text = value
        else:
            SubElement(parent, 'null')
    elif value.get('SourceType') == 'Uri':
        uri = SubElement(parent, 'uri')
        uri.text = str(value.get('Uri', ''))
    elif value.get('SourceType') == 'Object':
        ref = SubElement(parent, 'Ref')
        ref_value = value.get('Ref')
        ref.text = 'null' if ref_value is None else f'RBX{int(ref_value):032X}'
    else:
        SubElement(parent, 'null')

def _fmt_float(value: Any) -> str:
    
    if isinstance(value, float):
        if value.is_integer() and abs(value) < 1e15:
            return str(int(value))
        return f'{value:.8g}'
    return str(value)

import logging
import struct
from typing import Any

import lz4.block  
log = logging.getLogger(__name__)

MAGIC_HEADER = b'<roblox!\x89\xff\x0d\x0a\x1a\x0a'
FILE_HEADER_SIZE = 32  
ZSTD_MAGIC = b'\x28\xb5\x2f\xfd'

def _decompress_chunk(raw: bytes, uncompressed_size: int) -> bytes:
    if raw.startswith(ZSTD_MAGIC):
        try:
            import zstandard  
        except ImportError as exc:
            msg = 'RBXM contains a ZSTD-compressed chunk; install zstandard to read it'
            raise RuntimeError(msg) from exc
        return zstandard.ZstdDecompressor().decompress(  
            raw, max_output_size=uncompressed_size
        )

    return lz4.block.decompress(  
        raw, uncompressed_size=uncompressed_size
    )

_ORIENTATION_MATRICES: dict[int, tuple[float, ...]] = {
    0: (1, 0, 0, 0, 1, 0, 0, 0, 1),
    1: (1, 0, 0, 0, 0, -1, 0, 1, 0),
    2: (1, 0, 0, 0, -1, 0, 0, 0, -1),
    3: (1, 0, 0, 0, 0, 1, 0, -1, 0),
    4: (0, 1, 0, 1, 0, 0, 0, 0, -1),
    5: (0, 0, 1, 1, 0, 0, 0, 1, 0),
    6: (0, -1, 0, 1, 0, 0, 0, 0, 1),
    7: (0, 0, -1, 1, 0, 0, 0, -1, 0),
    8: (0, 1, 0, 0, 0, 1, 1, 0, 0),
    9: (0, 0, -1, 0, 1, 0, 1, 0, 0),
    10: (0, -1, 0, 0, 0, -1, 1, 0, 0),
    11: (0, 0, 1, 0, -1, 0, 1, 0, 0),
    12: (-1, 0, 0, 0, 1, 0, 0, 0, -1),
    13: (-1, 0, 0, 0, 0, 1, 0, 1, 0),
    14: (-1, 0, 0, 0, -1, 0, 0, 0, 1),
    15: (-1, 0, 0, 0, 0, -1, 0, -1, 0),
    16: (0, 1, 0, -1, 0, 0, 0, 0, 1),
    17: (0, 0, -1, -1, 0, 0, 0, 1, 0),
    18: (0, -1, 0, -1, 0, 0, 0, 0, -1),
    19: (0, 0, 1, -1, 0, 0, 0, -1, 0),
    20: (0, 1, 0, 0, 0, -1, -1, 0, 0),
    21: (0, 0, 1, 0, 1, 0, -1, 0, 0),
    22: (0, -1, 0, 0, 0, 1, -1, 0, 0),
    23: (0, 0, -1, 0, -1, 0, -1, 0, 0),
}

class RbxmDeserializer:
    
    def __init__(self) -> None:
        self._type_infos: list[RbxTypeInfo] = []
        self._instances: dict[int, RbxInstance] = {}
        self._metadata = RbxMetadata()
        self._shared_strings: list[bytes] = []
        self._raw_property_chunks: list[RbxRawPropertyChunk] = []
        self._raw_chunks: list[RbxRawChunk] = []
        self._version: int = 0
        self._type_count: int = 0
        self._object_count: int = 0

    def deserialize(self, data: bytes) -> RbxDocument:
        
        offset = self._read_file_header(data)
        offset = self._read_chunks(data, offset)
        roots = self._build_tree()

        return RbxDocument(
            version=self._version,
            type_count=self._type_count,
            object_count=self._object_count,
            metadata=self._metadata,
            instances=self._instances,
            roots=roots,
            shared_strings=self._shared_strings,
            raw_property_chunks=self._raw_property_chunks,
            raw_chunks=self._raw_chunks,
        )

    def _read_file_header(self, data: bytes) -> int:
        magic = data[:14]
        if magic != MAGIC_HEADER:
            msg = f'Invalid RBXM header: {magic!r}'
            raise ValueError(msg)

        self._version = struct.unpack_from('<H', data, 14)[0]
        self._type_count = struct.unpack_from('<I', data, 16)[0]
        self._object_count = struct.unpack_from('<I', data, 20)[0]

        log.info(
            'RBXM v%d: %d types, %d objects',
            self._version,
            self._type_count,
            self._object_count,
        )
        return FILE_HEADER_SIZE

    def _read_chunks(self, data: bytes, offset: int) -> int:
        while offset < len(data):
            chunk_name = data[offset : offset + 4].decode('ascii')
            compressed_size = struct.unpack_from('<I', data, offset + 4)[0]
            uncompressed_size = struct.unpack_from('<I', data, offset + 8)[0]
            
            offset += 16

            chunk_data: bytes
            if compressed_size == 0:
                
                chunk_data = data[offset : offset + uncompressed_size]
                offset += uncompressed_size
            else:
                raw = data[offset : offset + compressed_size]
                chunk_data = _decompress_chunk(raw, uncompressed_size)
                offset += compressed_size

            self._process_chunk(chunk_name, chunk_data)

            if chunk_name == 'END\x00':
                break

        return offset

    def _process_chunk(self, name: str, data: bytes) -> None:
        handler = {
            'META': self._handle_meta,
            'SSTR': self._handle_sstr,
            'INST': self._handle_inst,
            'PROP': self._handle_prop,
            'PRNT': self._handle_prnt,
        }.get(name)

        if handler is not None:
            handler(data)
        elif name == 'END\x00':
            log.debug('END chunk reached')
        else:
            self._raw_chunks.append(RbxRawChunk(name=name, data=data))
            log.warning('Unknown chunk type: %r', name)

    def _handle_meta(self, data: bytes) -> None:
        offset = 0
        count, offset = read_u32(data, offset)
        for _ in range(count):
            key, offset = read_string(data, offset)
            value, offset = read_string(data, offset)
            self._metadata.entries[key] = value
            log.debug('META: %s = %s', key, value)

    def _handle_sstr(self, data: bytes) -> None:
        offset = 0
        _version, offset = read_u32(data, offset)
        count, offset = read_u32(data, offset)
        for _ in range(count):
            _md5, offset = read_bytes(data, offset, 16)
            blob, offset = read_binary_string(data, offset)
            self._shared_strings.append(blob)

    def _handle_inst(self, data: bytes) -> None:
        offset = 0
        type_index, offset = read_u32(data, offset)
        class_name, offset = read_string(data, offset)
        is_service_byte, offset = read_u8(data, offset)
        is_service = is_service_byte != 0
        id_count, offset = read_u32(data, offset)

        ids, offset = decode_ids(data, offset, id_count)

        service_flags: list[bool] = []
        if is_service:
            for _ in range(id_count):
                flag, offset = read_u8(data, offset)
                service_flags.append(flag != 0)

        info = RbxTypeInfo(
            type_index=type_index,
            class_name=class_name,
            is_service=is_service,
            instance_ids=ids,
        )

        while len(self._type_infos) <= type_index:
            self._type_infos.append(
                RbxTypeInfo(
                    type_index=len(self._type_infos),
                    class_name='',
                    is_service=False,
                    instance_ids=[],
                )
            )
        self._type_infos[type_index] = info

        for i, inst_id in enumerate(ids):
            inst = RbxInstance(
                class_name=class_name,
                referent=inst_id,
                is_service=is_service and i < len(service_flags) and service_flags[i],
            )
            self._instances[inst_id] = inst

        log.debug(
            'INST[%d]: %s x%d (service=%s)',
            type_index,
            class_name,
            id_count,
            is_service,
        )

    def _handle_prop(self, data: bytes) -> None:
        offset = 0
        type_index, offset = read_u32(data, offset)
        prop_name, offset = read_string(data, offset)
        fmt_byte, offset = read_u8(data, offset)

        try:
            fmt = PropertyFormat(fmt_byte)
        except ValueError:
            self._preserve_raw_property(type_index, prop_name, fmt_byte, data[offset:])
            return

        if type_index >= len(self._type_infos):
            log.warning('PROP references unknown type index %d', type_index)
            return

        info = self._type_infos[type_index]
        count = len(info.instance_ids)
        if fmt == PropertyFormat.UNKNOWN:
            self._preserve_raw_property(type_index, prop_name, fmt_byte, data[offset:])
            return

        values = self._read_property_values(fmt, data, offset, count)

        for i, inst_id in enumerate(info.instance_ids):
            if inst_id in self._instances and i < len(values):
                self._instances[inst_id].properties[prop_name] = RbxProperty(
                    name=prop_name,
                    fmt=fmt,
                    value=values[i],
                )

        log.debug(
            'PROP[%d].%s: fmt=%s, %d values',
            type_index,
            prop_name,
            fmt.name,
            len(values),
        )

    def _preserve_raw_property(
        self, type_index: int, prop_name: str, fmt_byte: int, value_data: bytes
    ) -> None:
        if type_index >= len(self._type_infos):
            log.warning('PROP references unknown type index %d', type_index)
            return
        info = self._type_infos[type_index]
        self._raw_property_chunks.append(
            RbxRawPropertyChunk(
                class_name=info.class_name,
                prop_name=prop_name,
                fmt_byte=fmt_byte,
                value_data=value_data,
                instance_count=len(info.instance_ids),
            )
        )
        log.warning(
            'Unknown property format %d for %s, preserving raw payload',
            fmt_byte,
            prop_name,
        )

    def _read_property_values(
        self,
        fmt: PropertyFormat,
        data: bytes,
        offset: int,
        count: int,
    ) -> list[Any]:
        
        match fmt:
            case PropertyFormat.STRING:
                return self._read_strings(data, offset, count)
            case PropertyFormat.BOOL:
                return self._read_bools(data, offset, count)
            case PropertyFormat.INT:
                return self._read_ints(data, offset, count)
            case PropertyFormat.FLOAT:
                return self._read_floats(data, offset, count)
            case PropertyFormat.DOUBLE:
                return self._read_doubles(data, offset, count)
            case PropertyFormat.UDIM:
                return self._read_udims(data, offset, count)
            case PropertyFormat.UDIM2:
                return self._read_udim2s(data, offset, count)
            case PropertyFormat.RAY:
                return self._read_rays(data, offset, count)
            case PropertyFormat.FACES:
                return self._read_faces(data, offset, count)
            case PropertyFormat.AXES:
                return self._read_axes(data, offset, count)
            case PropertyFormat.BRICK_COLOR:
                return self._read_brick_colors(data, offset, count)
            case PropertyFormat.COLOR3:
                return self._read_color3s(data, offset, count)
            case PropertyFormat.VECTOR2:
                return self._read_vector2s(data, offset, count)
            case PropertyFormat.VECTOR3:
                return self._read_vector3s(data, offset, count)
            case PropertyFormat.VECTOR2INT16:
                return self._read_vector2int16s(data, offset, count)
            case PropertyFormat.CFRAME_MATRIX | PropertyFormat.CFRAME_QUAT:
                return self._read_cframes(data, offset, count, fmt)
            case PropertyFormat.ENUM:
                return self._read_enums(data, offset, count)
            case PropertyFormat.REF:
                return self._read_refs(data, offset, count)
            case PropertyFormat.VECTOR3INT16:
                return self._read_vector3int16s(data, offset, count)
            case PropertyFormat.NUMBER_SEQUENCE:
                return self._read_number_sequences(data, offset, count)
            case PropertyFormat.COLOR_SEQUENCE:
                return self._read_color_sequences(data, offset, count)
            case PropertyFormat.NUMBER_RANGE:
                return self._read_number_ranges(data, offset, count)
            case PropertyFormat.RECT2D:
                return self._read_rect2ds(data, offset, count)
            case PropertyFormat.PHYSICAL_PROPERTIES:
                return self._read_physical_properties(data, offset, count)
            case PropertyFormat.COLOR3UINT8:
                return self._read_color3uint8s(data, offset, count)
            case PropertyFormat.INT64:
                return self._read_int64s(data, offset, count)
            case PropertyFormat.SHARED_STRING:
                return self._read_shared_strings(data, offset, count)
            case PropertyFormat.BYTECODE:
                return self._read_bytecodes(data, offset, count)
            case PropertyFormat.OPTIONAL_CFRAME:
                return self._read_optional_cframes(data, offset, count)
            case PropertyFormat.UNIQUE_ID:
                return self._read_unique_ids(data, offset, count)
            case PropertyFormat.FONT:
                return self._read_fonts(data, offset, count)
            case PropertyFormat.SECURITY_CAPABILITIES:
                return self._read_security_capabilities(data, offset, count)
            case PropertyFormat.CONTENT:
                return self._read_contents(data, offset, count)
            case _:
                log.warning('Unhandled property format: %s', fmt)
                return [None] * count

    def _read_strings(self, data: bytes, offset: int, count: int) -> list[str | bytes]:
        results: list[str | bytes] = []
        for _ in range(count):
            raw, offset = read_binary_string(data, offset)
            try:
                results.append(raw.decode('utf-8'))
            except UnicodeDecodeError:
                
                results.append(raw)
        return results

    def _read_bools(self, data: bytes, offset: int, count: int) -> list[bool]:
        return [data[offset + i] != 0 for i in range(count)]

    def _read_ints(self, data: bytes, offset: int, count: int) -> list[int]:
        return deinterleave_i32(data, offset, count)

    def _read_floats(self, data: bytes, offset: int, count: int) -> list[float]:
        return deinterleave_f32(data, offset, count)

    def _read_doubles(self, data: bytes, offset: int, count: int) -> list[float]:
        results: list[float] = []
        for i in range(count):
            val, _ = read_f64(data, offset + i * 8)
            results.append(val)
        return results

    def _read_udims(self, data: bytes, offset: int, count: int) -> list[dict[str, float | int]]:
        scales = deinterleave_f32(data, offset, count)
        offsets = deinterleave_i32(data, offset + count * 4, count)
        return [{'S': scales[i], 'O': offsets[i]} for i in range(count)]

    def _read_udim2s(self, data: bytes, offset: int, count: int) -> list[dict[str, float | int]]:
        xs = deinterleave_f32(data, offset, count)
        ys = deinterleave_f32(data, offset + count * 4, count)
        xo = deinterleave_i32(data, offset + count * 8, count)
        yo = deinterleave_i32(data, offset + count * 12, count)
        return [{'XS': xs[i], 'XO': xo[i], 'YS': ys[i], 'YO': yo[i]} for i in range(count)]

    def _read_rays(self, data: bytes, offset: int, count: int) -> list[dict[str, dict[str, float]]]:
        results: list[dict[str, dict[str, float]]] = []
        for _ in range(count):
            ox, offset = read_f32(data, offset)
            oy, offset = read_f32(data, offset)
            oz, offset = read_f32(data, offset)
            dx, offset = read_f32(data, offset)
            dy, offset = read_f32(data, offset)
            dz, offset = read_f32(data, offset)
            results.append(
                {
                    'origin': {'X': ox, 'Y': oy, 'Z': oz},
                    'direction': {'X': dx, 'Y': dy, 'Z': dz},
                }
            )
        return results

    def _read_faces(self, data: bytes, offset: int, count: int) -> list[int]:
        return [data[offset + i] for i in range(count)]

    def _read_axes(self, data: bytes, offset: int, count: int) -> list[int]:
        return [data[offset + i] for i in range(count)]

    def _read_brick_colors(self, data: bytes, offset: int, count: int) -> list[int]:
        return deinterleave_u32(data, offset, count)

    def _read_color3s(self, data: bytes, offset: int, count: int) -> list[dict[str, float]]:
        rs = deinterleave_f32(data, offset, count)
        gs = deinterleave_f32(data, offset + count * 4, count)
        bs = deinterleave_f32(data, offset + count * 8, count)
        return [{'R': rs[i], 'G': gs[i], 'B': bs[i]} for i in range(count)]

    def _read_vector2s(self, data: bytes, offset: int, count: int) -> list[dict[str, float]]:
        xs = deinterleave_f32(data, offset, count)
        ys = deinterleave_f32(data, offset + count * 4, count)
        return [{'X': xs[i], 'Y': ys[i]} for i in range(count)]

    def _read_vector3s(self, data: bytes, offset: int, count: int) -> list[dict[str, float]]:
        xs = deinterleave_f32(data, offset, count)
        ys = deinterleave_f32(data, offset + count * 4, count)
        zs = deinterleave_f32(data, offset + count * 8, count)
        return [{'X': xs[i], 'Y': ys[i], 'Z': zs[i]} for i in range(count)]

    def _read_vector2int16s(self, data: bytes, offset: int, count: int) -> list[dict[str, int]]:
        results: list[dict[str, int]] = []
        for _ in range(count):
            x = struct.unpack_from('<h', data, offset)[0]
            y = struct.unpack_from('<h', data, offset + 2)[0]
            offset += 4
            results.append({'X': x, 'Y': y})
        return results

    def _read_vector3int16s(self, data: bytes, offset: int, count: int) -> list[dict[str, int]]:
        results: list[dict[str, int]] = []
        for _ in range(count):
            x = struct.unpack_from('<h', data, offset)[0]
            y = struct.unpack_from('<h', data, offset + 2)[0]
            z = struct.unpack_from('<h', data, offset + 4)[0]
            offset += 6
            results.append({'X': x, 'Y': y, 'Z': z})
        return results

    def _read_cframes(
        self,
        data: bytes,
        offset: int,
        count: int,
        fmt: PropertyFormat,
    ) -> list[dict[str, float]]:
        
        results, _offset = self._read_cframes_with_offset(data, offset, count, fmt)
        return results

    def _read_cframes_with_offset(
        self,
        data: bytes,
        offset: int,
        count: int,
        fmt: PropertyFormat,
    ) -> tuple[list[dict[str, float]], int]:
        
        rotations: list[tuple[float, ...]] = []

        for _ in range(count):
            orient_id, offset = read_u8(data, offset)
            if orient_id != 0:

                mat_idx = orient_id - 2
                mat = _ORIENTATION_MATRICES.get(mat_idx, (1, 0, 0, 0, 1, 0, 0, 0, 1))
                rotations.append(mat)
            elif fmt == PropertyFormat.CFRAME_QUAT:
                
                qx, offset = read_f32(data, offset)
                qy, offset = read_f32(data, offset)
                qz, offset = read_f32(data, offset)
                qw, offset = read_f32(data, offset)
                
                rotations.append(_quat_to_matrix(qx, qy, qz, qw))
            else:
                
                vals: list[float] = []
                for _ in range(9):
                    v, offset = read_f32(data, offset)
                    vals.append(v)
                rotations.append(tuple(vals))

        xs = deinterleave_f32(data, offset, count)
        ys = deinterleave_f32(data, offset + count * 4, count)
        zs = deinterleave_f32(data, offset + count * 8, count)
        offset += count * 12

        results: list[dict[str, float]] = []
        for i in range(count):
            r = rotations[i]
            results.append(
                {
                    'X': xs[i],
                    'Y': ys[i],
                    'Z': zs[i],
                    'R00': r[0],
                    'R01': r[1],
                    'R02': r[2],
                    'R10': r[3],
                    'R11': r[4],
                    'R12': r[5],
                    'R20': r[6],
                    'R21': r[7],
                    'R22': r[8],
                }
            )
        return results, offset

    def _read_enums(self, data: bytes, offset: int, count: int) -> list[int]:
        return deinterleave_u32(data, offset, count)

    def _read_refs(self, data: bytes, offset: int, count: int) -> list[int | None]:
        ids, _ = decode_ids(data, offset, count)
        return [None if v == -1 else v for v in ids]

    def _read_number_sequences(
        self, data: bytes, offset: int, count: int
    ) -> list[list[dict[str, float]]]:
        results: list[list[dict[str, float]]] = []
        for _ in range(count):
            num_keys, offset = read_u32(data, offset)
            keys: list[dict[str, float]] = []
            for _ in range(num_keys):
                time, offset = read_f32(data, offset)
                value, offset = read_f32(data, offset)
                envelope, offset = read_f32(data, offset)
                keys.append({'Time': time, 'Value': value, 'Envelope': envelope})
            results.append(keys)
        return results

    def _read_color_sequences(
        self, data: bytes, offset: int, count: int
    ) -> list[list[dict[str, float]]]:
        results: list[list[dict[str, float]]] = []
        for _ in range(count):
            num_keys, offset = read_u32(data, offset)
            keys: list[dict[str, float]] = []
            for _ in range(num_keys):
                time, offset = read_f32(data, offset)
                r, offset = read_f32(data, offset)
                g, offset = read_f32(data, offset)
                b, offset = read_f32(data, offset)
                _envelope, offset = read_f32(data, offset)
                keys.append({'Time': time, 'R': r, 'G': g, 'B': b})
            results.append(keys)
        return results

    def _read_number_ranges(self, data: bytes, offset: int, count: int) -> list[dict[str, float]]:
        results: list[dict[str, float]] = []
        for _ in range(count):
            low, offset = read_f32(data, offset)
            high, offset = read_f32(data, offset)
            results.append({'Min': low, 'Max': high})
        return results

    def _read_rect2ds(
        self, data: bytes, offset: int, count: int
    ) -> list[dict[str, dict[str, float]]]:
        x0s = deinterleave_f32(data, offset, count)
        y0s = deinterleave_f32(data, offset + count * 4, count)
        x1s = deinterleave_f32(data, offset + count * 8, count)
        y1s = deinterleave_f32(data, offset + count * 12, count)
        return [
            {
                'min': {'X': x0s[i], 'Y': y0s[i]},
                'max': {'X': x1s[i], 'Y': y1s[i]},
            }
            for i in range(count)
        ]

    def _read_physical_properties(
        self, data: bytes, offset: int, count: int
    ) -> list[dict[str, Any] | None]:
        results: list[dict[str, Any] | None] = []
        for _ in range(count):
            flags, offset = read_u8(data, offset)
            custom = (flags & 0x01) != 0
            has_acoustic_absorption = (flags & 0x02) != 0
            if custom:
                density, offset = read_f32(data, offset)
                friction, offset = read_f32(data, offset)
                elasticity, offset = read_f32(data, offset)
                friction_weight, offset = read_f32(data, offset)
                elasticity_weight, offset = read_f32(data, offset)
                value: dict[str, Any] = {
                    'CustomPhysics': True,
                    'Density': density,
                    'Friction': friction,
                    'Elasticity': elasticity,
                    'FrictionWeight': friction_weight,
                    'ElasticityWeight': elasticity_weight,
                }
                if has_acoustic_absorption:
                    acoustic_absorption, offset = read_f32(data, offset)
                    value['AcousticAbsorption'] = acoustic_absorption
                results.append(value)
            elif has_acoustic_absorption:
                results.append(
                    {
                        'CustomPhysics': False,
                        'HasAcousticAbsorption': True,
                    }
                )
            else:
                results.append(None)
        return results

    def _read_color3uint8s(self, data: bytes, offset: int, count: int) -> list[dict[str, int]]:
        rs = data[offset : offset + count]
        gs = data[offset + count : offset + 2 * count]
        bs = data[offset + 2 * count : offset + 3 * count]
        return [{'R': rs[i], 'G': gs[i], 'B': bs[i]} for i in range(count)]

    def _read_int64s(self, data: bytes, offset: int, count: int) -> list[int]:
        return deinterleave_i64(data, offset, count)

    def _read_shared_strings(self, data: bytes, offset: int, count: int) -> list[bytes]:
        indices = deinterleave_u32(data, offset, count)
        return [
            self._shared_strings[idx] if idx < len(self._shared_strings) else b'' for idx in indices
        ]

    def _read_bytecodes(self, data: bytes, offset: int, count: int) -> list[bytes]:
        results: list[bytes] = []
        for _ in range(count):
            raw, offset = read_binary_string(data, offset)
            results.append(raw)
        return results

    def _read_optional_cframes(
        self, data: bytes, offset: int, count: int
    ) -> list[dict[str, float] | None]:
        cframe_fmt_byte, offset = read_u8(data, offset)
        if cframe_fmt_byte != int(PropertyFormat.CFRAME_MATRIX):
            log.warning(
                'OptionalCoordinateFrame contained unexpected value format %d',
                cframe_fmt_byte,
            )
        cframes, offset = self._read_cframes_with_offset(
            data, offset, count, PropertyFormat.CFRAME_MATRIX
        )
        bool_fmt_byte, offset = read_u8(data, offset)
        if bool_fmt_byte != int(PropertyFormat.BOOL):
            log.warning(
                'OptionalCoordinateFrame contained unexpected presence format %d',
                bool_fmt_byte,
            )
        present = self._read_bools(data, offset, count)
        return [cframes[i] if present[i] else None for i in range(count)]

    def _read_unique_ids(self, data: bytes, offset: int, count: int) -> list[dict[str, int]]:
        records = deinterleave_bytes(data, offset, count, 16)
        results: list[dict[str, int]] = []
        for record in records:
            index, time, random = struct.unpack('>IIQ', record)
            results.append({'Index': index, 'Time': time, 'Random': random})
        return results

    def _read_fonts(self, data: bytes, offset: int, count: int) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for _ in range(count):
            family_raw, offset = read_binary_string(data, offset)
            weight = struct.unpack_from('<H', data, offset)[0]
            offset += 2
            style, offset = read_u8(data, offset)
            cached_face_raw, offset = read_binary_string(data, offset)
            results.append(
                {
                    'Family': family_raw.decode('utf-8', errors='replace'),
                    'Weight': weight,
                    'Style': style,
                    'CachedFaceId': cached_face_raw.decode('utf-8', errors='replace'),
                }
            )
        return results

    def _read_security_capabilities(self, data: bytes, offset: int, count: int) -> list[int]:
        return deinterleave_u64(data, offset, count)

    def _read_contents(self, data: bytes, offset: int, count: int) -> list[dict[str, Any] | None]:
        source_types = deinterleave_u32(data, offset, count)
        offset += count * 4

        uri_count, offset = read_u32(data, offset)
        uris: list[str] = []
        for _ in range(uri_count):
            raw, offset = read_binary_string(data, offset)
            uris.append(raw.decode('utf-8', errors='replace'))

        object_count, offset = read_u32(data, offset)
        object_refs, offset = decode_ids(data, offset, object_count)

        external_object_count, offset = read_u32(data, offset)
        external_object_refs, offset = decode_ids(data, offset, external_object_count)

        uri_index = 0
        object_index = 0
        external_object_index = 0
        results: list[dict[str, Any] | None] = []
        for source_type in source_types:
            if source_type == 0:
                results.append(None)
            elif source_type == 1:
                uri = uris[uri_index] if uri_index < len(uris) else ''
                uri_index += 1
                results.append({'SourceType': 'Uri', 'Uri': uri})
            elif source_type == 2:
                if object_index < len(object_refs):
                    ref = object_refs[object_index]
                    object_index += 1
                    results.append({'SourceType': 'Object', 'Ref': ref})
                else:
                    ref = (
                        external_object_refs[external_object_index]
                        if external_object_index < len(external_object_refs)
                        else None
                    )
                    external_object_index += 1
                    results.append({'SourceType': 'Object', 'Ref': ref, 'External': True})
            else:
                results.append({'SourceType': source_type})
        return results

    def _handle_prnt(self, data: bytes) -> None:
        offset = 0
        _fmt, offset = read_u8(data, offset)
        link_count, offset = read_u32(data, offset)

        child_ids, offset = decode_ids(data, offset, link_count)
        parent_ids, offset = decode_ids(data, offset, link_count)

        for child_id, parent_id in zip(child_ids, parent_ids, strict=True):
            child = self._instances.get(child_id)
            parent = self._instances.get(parent_id)
            if child is not None and parent is not None:
                parent.children.append(child)

        log.debug('PRNT: %d links', link_count)

    def _build_tree(self) -> list[RbxInstance]:
        
        parented: set[int] = set()
        for inst in self._instances.values():
            for child in inst.children:
                parented.add(child.referent)

        return [inst for inst in self._instances.values() if inst.referent not in parented]

def _quat_to_matrix(x: float, y: float, z: float, w: float) -> tuple[float, ...]:
    
    xx, yy, zz = x * x, y * y, z * z
    xy, xz, yz = x * y, x * z, y * z
    wx, wy, wz = w * x, w * y, w * z

    return (
        1 - 2 * (yy + zz),
        2 * (xy - wz),
        2 * (xz + wy),
        2 * (xy + wz),
        1 - 2 * (xx + zz),
        2 * (yz - wx),
        2 * (xz - wy),
        2 * (yz + wx),
        1 - 2 * (xx + yy),
    )

import struct
import zlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import lz4.block

RBXM_MAGIC = b'<roblox!'
RBXM_SIGNATURE = bytes([0x89, 0xFF, 0x0D, 0x0A, 0x1A, 0x0A])

@dataclass
class RbxmInstance:
    
    class_name: str
    referent: int
    properties: Dict[str, Any] = field(default_factory=dict)
    children: List['RbxmInstance'] = field(default_factory=list)
    parent: Optional['RbxmInstance'] = None

def decode_interleaved_i32(data: bytes, count: int) -> List[int]:
    
    if len(data) < count * 4:
        return []

    result = []
    for i in range(count):
        
        b0 = data[i]
        b1 = data[count + i]
        b2 = data[count * 2 + i]
        b3 = data[count * 3 + i]

        value = (b0 << 24) | (b1 << 16) | (b2 << 8) | b3

        if value & 1:
            value = -((value >> 1) + 1)
        else:
            value = value >> 1

        result.append(value)

    return result

def decode_interleaved_f32(data: bytes, count: int) -> List[float]:
    
    if len(data) < count * 4:
        return []

    result = []
    for i in range(count):
        
        b0 = data[i]
        b1 = data[count + i]
        b2 = data[count * 2 + i]
        b3 = data[count * 3 + i]

        raw = (b0 << 24) | (b1 << 16) | (b2 << 8) | b3

        ieee = ((raw >> 1) | ((raw & 1) << 31)) & 0xFFFFFFFF

        result.append(struct.unpack('<f', struct.pack('<I', ieee))[0])

    return result

def read_string(data: bytes, offset: int) -> Tuple[str, int]:
    
    length = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    value = data[offset : offset + length].decode('utf-8', errors='replace')
    return value, offset + length

def decompress_chunk(data: bytes, compressed_size: int, uncompressed_size: int) -> bytes:
    
    if compressed_size == 0:
        return data[:uncompressed_size]

    try:
        return lz4.block.decompress(data[:compressed_size], uncompressed_size=uncompressed_size)
    except Exception:
        
        try:
            return lz4.block.decompress(data[:compressed_size])
        except Exception:
            
            return data[:compressed_size]

CFRAME_ROTATIONS = {
    0x02: [1, 0, 0, 0, 1, 0, 0, 0, 1],
    0x03: [1, 0, 0, 0, 0, -1, 0, 1, 0],
    0x04: [1, 0, 0, 0, -1, 0, 0, 0, -1],
    0x05: [1, 0, 0, 0, 0, 1, 0, -1, 0],
    0x06: [0, 1, 0, 1, 0, 0, 0, 0, -1],
    0x07: [0, 0, 1, 1, 0, 0, 0, 1, 0],
    0x08: [0, -1, 0, 1, 0, 0, 0, 0, 1],
    0x09: [0, 0, -1, 1, 0, 0, 0, -1, 0],
    0x0A: [0, 1, 0, 0, 0, 1, 1, 0, 0],
    0x0B: [0, 0, -1, 0, 1, 0, 1, 0, 0],
    0x0C: [0, -1, 0, 0, 0, -1, 1, 0, 0],
    0x0D: [0, 0, 1, 0, -1, 0, 1, 0, 0],
    0x0E: [-1, 0, 0, 0, 1, 0, 0, 0, -1],
    0x0F: [-1, 0, 0, 0, 0, 1, 0, 1, 0],
    0x10: [-1, 0, 0, 0, -1, 0, 0, 0, 1],
    0x11: [-1, 0, 0, 0, 0, -1, 0, -1, 0],
    0x12: [0, 1, 0, -1, 0, 0, 0, 0, 1],
    0x13: [0, 0, -1, -1, 0, 0, 0, 1, 0],
    0x14: [0, -1, 0, -1, 0, 0, 0, 0, -1],
    0x15: [0, 0, 1, -1, 0, 0, 0, -1, 0],
    0x16: [0, 1, 0, 0, 0, -1, -1, 0, 0],
    0x17: [0, 0, 1, 0, 1, 0, -1, 0, 0],
    0x18: [0, -1, 0, 0, 0, 1, -1, 0, 0],
    0x19: [0, 0, -1, 0, -1, 0, -1, 0, 0],
}

def parse_rbxm(data: bytes) -> Dict[int, RbxmInstance]:
    
    if len(data) < 32:
        raise ValueError('File too small to be valid RBXM')

    if not data.startswith(RBXM_MAGIC):
        raise ValueError('Invalid RBXM magic header')

    offset = 8
    signature = data[offset : offset + 6]
    offset += 6

    version = struct.unpack_from('<H', data, offset)[0]
    offset += 2

    class_count = struct.unpack_from('<i', data, offset)[0]
    offset += 4

    instance_count = struct.unpack_from('<i', data, offset)[0]
    offset += 4

    offset += 8

    class_info: Dict[int, Tuple[str, List[int]]] = {}  
    instances: Dict[int, RbxmInstance] = {}  
    parent_refs: Dict[int, int] = {}  

    while offset < len(data):
        if offset + 16 > len(data):
            break

        chunk_name = data[offset : offset + 4].decode('ascii', errors='replace').rstrip('\x00')
        offset += 4

        compressed_size = struct.unpack_from('<I', data, offset)[0]
        offset += 4

        uncompressed_size = struct.unpack_from('<I', data, offset)[0]
        offset += 4

        reserved = struct.unpack_from('<I', data, offset)[0]
        offset += 4

        if compressed_size == 0:
            chunk_data = data[offset : offset + uncompressed_size]
            offset += uncompressed_size
        else:
            chunk_data = decompress_chunk(data[offset:], compressed_size, uncompressed_size)
            offset += compressed_size

        if chunk_name == 'INST':
            _parse_inst_chunk(chunk_data, class_info, instances)
        elif chunk_name == 'PROP':
            _parse_prop_chunk(chunk_data, class_info, instances)
        elif chunk_name == 'PRNT':
            _parse_prnt_chunk(chunk_data, instances, parent_refs)
        elif chunk_name == 'END\x00' or chunk_name == 'END':
            break

    for child_ref, parent_ref in parent_refs.items():
        if child_ref in instances:
            child = instances[child_ref]
            if parent_ref >= 0 and parent_ref in instances:
                parent = instances[parent_ref]
                parent.children.append(child)
                child.parent = parent

    return instances

def _parse_inst_chunk(data: bytes, class_info: Dict, instances: Dict):
    
    offset = 0

    class_id = struct.unpack_from('<I', data, offset)[0]
    offset += 4

    class_name, offset = read_string(data, offset)

    object_format = data[offset]
    offset += 1

    instance_count = struct.unpack_from('<I', data, offset)[0]
    offset += 4

    referents_data = data[offset : offset + instance_count * 4]
    referent_deltas = decode_interleaved_i32(referents_data, instance_count)

    referents = []
    current = 0
    for delta in referent_deltas:
        current += delta
        referents.append(current)

    class_info[class_id] = (class_name, referents)

    for ref in referents:
        instances[ref] = RbxmInstance(class_name=class_name, referent=ref)

def _parse_prop_chunk(data: bytes, class_info: Dict, instances: Dict):
    
    offset = 0

    class_id = struct.unpack_from('<I', data, offset)[0]
    offset += 4

    prop_name, offset = read_string(data, offset)

    type_id = data[offset]
    offset += 1

    if class_id not in class_info:
        return

    class_name, referents = class_info[class_id]
    count = len(referents)

    if count == 0:
        return

    values = _parse_prop_values(data[offset:], type_id, count)

    for i, ref in enumerate(referents):
        if ref in instances and i < len(values):
            instances[ref].properties[prop_name] = values[i]

def _parse_prop_values(data: bytes, type_id: int, count: int) -> List[Any]:
    
    values = []

    if type_id == 0x01:  
        offset = 0
        for _ in range(count):
            if offset >= len(data):
                values.append('')
                continue
            string_value, offset = read_string(data, offset)
            values.append(string_value)

    elif type_id == 0x02:  
        for i in range(count):
            if i < len(data):
                values.append(bool(data[i]))
            else:
                values.append(False)

    elif type_id == 0x03:  
        values = decode_interleaved_i32(data, count)

    elif type_id == 0x04:  
        values = decode_interleaved_f32(data, count)

    elif type_id == 0x05:  
        for i in range(count):
            offset = i * 8
            if offset + 8 <= len(data):
                values.append(struct.unpack_from('<d', data, offset)[0])
            else:
                values.append(0.0)

    elif type_id == 0x10:  
        values = _parse_cframes(data, count)

    else:
        
        values = [None] * count

    return values

def _parse_cframes(data: bytes, count: int) -> List[Dict]:
    
    offset = 0
    cframes = []
    rotation_data = []

    for _ in range(count):
        if offset >= len(data):
            rotation_data.append((0x02, CFRAME_ROTATIONS[0x02]))
            continue

        rot_id = data[offset]
        offset += 1

        if rot_id == 0x00:
            
            if offset + 36 <= len(data):
                rot = list(struct.unpack_from('<9f', data, offset))
                offset += 36
            else:
                rot = [1, 0, 0, 0, 1, 0, 0, 0, 1]
            rotation_data.append((rot_id, rot))
        else:
            
            rot = CFRAME_ROTATIONS.get(rot_id, [1, 0, 0, 0, 1, 0, 0, 0, 1])
            rotation_data.append((rot_id, rot))

    positions_x = decode_interleaved_f32(data[offset:], count)
    offset += count * 4
    positions_y = decode_interleaved_f32(data[offset:], count)
    offset += count * 4
    positions_z = decode_interleaved_f32(data[offset:], count)

    for i in range(count):
        rot_id, rot = rotation_data[i] if i < len(rotation_data) else (0x02, CFRAME_ROTATIONS[0x02])
        x = positions_x[i] if i < len(positions_x) else 0.0
        y = positions_y[i] if i < len(positions_y) else 0.0
        z = positions_z[i] if i < len(positions_z) else 0.0

        cframes.append({'position': (x, y, z), 'rotation': rot})

    return cframes

def _parse_prnt_chunk(data: bytes, instances: Dict, parent_refs: Dict):
    
    offset = 0

    offset += 1

    count = struct.unpack_from('<I', data, offset)[0]
    offset += 4

    children = decode_interleaved_i32(data[offset:], count)
    offset += count * 4

    parents = decode_interleaved_i32(data[offset:], count)

    child_refs = []
    parent_ref_list = []

    child_current = 0
    parent_current = 0

    for i in range(min(len(children), len(parents))):
        child_current += children[i]
        parent_current += parents[i]
        child_refs.append(child_current)
        parent_ref_list.append(parent_current)

    for i in range(len(child_refs)):
        parent_refs[child_refs[i]] = parent_ref_list[i]

def get_root_instances(instances: Dict[int, RbxmInstance]) -> List[RbxmInstance]:
    
    return [inst for inst in instances.values() if inst.parent is None]

def find_by_class(instances: Dict[int, RbxmInstance], class_name: str) -> List[RbxmInstance]:
    
    return [inst for inst in instances.values() if inst.class_name == class_name]

class _EmbeddedLogBuffer:
    def __init__(self):
        self._lock = threading.Lock()
        self.buffer = []
    def log(self, tag, msg):
        try:
            with self._lock:
                self.buffer.append((tag, msg))
                if len(self.buffer) > 1000:
                    del self.buffer[:1000]
        except Exception:
            pass
    def clear(self):
        try:
            with self._lock:
                self.buffer.clear()
        except Exception:
            pass
log_buffer = _EmbeddedLogBuffer()

import gzip
import json
import struct

import numpy as np

try:
    import DracoPy

    DRACO_AVAILABLE = True
except ImportError:
    DRACO_AVAILABLE = False
    log_buffer.log('Mesh', 'DracoPy not installed. v6/v7 mesh conversion will not work.')

class Vertex:
    
    def __init__(self):
        
        self.px = self.py = self.pz = 0.0
        
        self.nx = self.ny = self.nz = 0.0
        
        self.tu = self.tv = self.tw = 0.0
        
        self.tx = self.ty = self.tz = self.ts = 0
        
        self.r = self.g = self.b = self.a = 255

class Face:
    
    def __init__(self, a=0, b=0, c=0):
        self.a, self.b, self.c = a, b, c

def fix_float(s: str) -> str:
    
    return s.replace(',', '.')

def read_vertices(data: bytes, offset: int, count: int, vsize: int) -> tuple[list[Vertex], int]:
    
    verts = []
    pos = offset
    for _ in range(count):
        v = Vertex()
        
        (v.px,) = struct.unpack_from('<f', data, pos)
        pos += 4
        (v.py,) = struct.unpack_from('<f', data, pos)
        pos += 4
        (v.pz,) = struct.unpack_from('<f', data, pos)
        pos += 4
        
        (v.nx,) = struct.unpack_from('<f', data, pos)
        pos += 4
        (v.ny,) = struct.unpack_from('<f', data, pos)
        pos += 4
        (v.nz,) = struct.unpack_from('<f', data, pos)
        pos += 4
        
        (v.tu,) = struct.unpack_from('<f', data, pos)
        pos += 4
        (tv,) = struct.unpack_from('<f', data, pos)
        pos += 4
        v.tv = 1.0 - tv  
        
        (v.tx,) = struct.unpack_from('<b', data, pos)
        pos += 1
        (v.ty,) = struct.unpack_from('<b', data, pos)
        pos += 1
        (v.tz,) = struct.unpack_from('<b', data, pos)
        pos += 1
        (v.ts,) = struct.unpack_from('<b', data, pos)
        pos += 1
        
        if vsize == 40:
            (v.r,) = struct.unpack_from('<B', data, pos)
            pos += 1
            (v.g,) = struct.unpack_from('<B', data, pos)
            pos += 1
            (v.b,) = struct.unpack_from('<B', data, pos)
            pos += 1
            (v.a,) = struct.unpack_from('<B', data, pos)
            pos += 1
        verts.append(v)
    return verts, pos

def write_obj_data(
    v_lines: list[str], n_lines: list[str], t_lines: list[str], f_lines: list[str]
) -> str:
    
    lines = ['# Converted from Roblox mesh format\n']
    lines.append(f'# Vertices: {len(v_lines)}, Faces: {len(f_lines)}\n\n')
    lines.extend(line + '\n' for line in v_lines)
    lines.append('\n')
    lines.extend(line + '\n' for line in n_lines)
    lines.append('\n')
    lines.extend(line + '\n' for line in t_lines)
    lines.append('\n')
    lines.extend(line + '\n' for line in f_lines)
    return ''.join(lines)

def process_v1(data: bytes) -> str:
    
    try:
        lines = data.decode('utf-8', errors='replace').splitlines()
        if len(lines) < 3:
            log_buffer.log('Mesh', 'Invalid v1 mesh: not enough lines')
            return None
        version = lines[0].strip()
        try:
            face_count = int(lines[1].strip())
        except ValueError as e:
            log_buffer.log('Mesh', f'Invalid v1 face count: {e}')
            return None
        
        try:
            
            content = json.loads('[' + lines[2].replace('][', '],[') + ']')
        except json.JSONDecodeError as e:
            log_buffer.log('Mesh', f'Failed to parse v1 JSON: {e}')
            return None
        
        groups = len(content) // 3
        if groups != face_count * 3:
            log_buffer.log('Mesh', f'Invalid v1 mesh: {groups} vertices for {face_count} faces')
            return None
        position_scale = 0.5 if version == 'version 1.00' else 1.0
        verts = []
        norms = []
        uvs = []
        faces = []
        for i in range(groups):
            v = content[i * 3]  
            n = content[i * 3 + 1]  
            uv = content[i * 3 + 2]  
            px = v[0] * position_scale
            py = v[1] * position_scale
            pz = v[2] * position_scale
            verts.append(f'v {fix_float(str(px))} {fix_float(str(py))} {fix_float(str(pz))}')
            norms.append(f'vn {fix_float(str(n[0]))} {fix_float(str(n[1]))} {fix_float(str(n[2]))}')
            uvs.append(
                f'vt {fix_float(str(uv[0]))} {fix_float(str(1 - uv[1]))} {fix_float(str(uv[2]))}'
            )
        
        for i in range(0, groups, 3):
            idx = i + 1  
            faces.append(
                f'f {idx}/{idx}/{idx} {idx + 1}/{idx + 1}/{idx + 1} {idx + 2}/{idx + 2}/{idx + 2}'
            )
        return write_obj_data(verts, norms, uvs, faces)
    except Exception as e:
        log_buffer.log('Mesh', f'Error processing v1 mesh: {e}')
        return None

def process_v2_to_v5(data: bytes, version_num: str) -> str:
    
    try:
        offset = 13  

        header_size = struct.unpack_from('<H', data, offset)[0]

        sizeof_vertex = 40  
        num_verts = 0
        num_faces = 0
        num_lod_offsets = 0
        num_bones = 0
        lod_type = 0

        if version_num in ('2.00',):

            sizeof_vertex = struct.unpack_from('<B', data, offset + 2)[0]
            
            num_verts = struct.unpack_from('<I', data, offset + 4)[0]
            num_faces = struct.unpack_from('<I', data, offset + 8)[0]
            num_lod_offsets = 0
            num_bones = 0
            lod_type = 0  

        elif version_num in ('3.00', '3.01'):

            sizeof_vertex = struct.unpack_from('<B', data, offset + 2)[0]

            num_lod_offsets = struct.unpack_from('<H', data, offset + 6)[0]
            num_verts = struct.unpack_from('<I', data, offset + 8)[0]
            num_faces = struct.unpack_from('<I', data, offset + 12)[0]
            num_bones = 0
            lod_type = 0  

        elif version_num in ('4.00', '4.01'):

            lod_type = struct.unpack_from('<H', data, offset + 2)[0]
            num_verts = struct.unpack_from('<I', data, offset + 4)[0]
            num_faces = struct.unpack_from('<I', data, offset + 8)[0]
            num_lod_offsets = struct.unpack_from('<H', data, offset + 12)[0]
            num_bones = struct.unpack_from('<H', data, offset + 14)[0]
            sizeof_vertex = 40  

        elif version_num in ('5.00',):
            
            lod_type = struct.unpack_from('<H', data, offset + 2)[0]
            num_verts = struct.unpack_from('<I', data, offset + 4)[0]
            num_faces = struct.unpack_from('<I', data, offset + 8)[0]
            num_lod_offsets = struct.unpack_from('<H', data, offset + 12)[0]
            num_bones = struct.unpack_from('<H', data, offset + 14)[0]
            sizeof_vertex = 40  

        else:
            log_buffer.log('Mesh', f'Unsupported version in v2-v5 path: {version_num}')
            return None

        log_buffer.log(
            'Mesh',
            f'v{version_num} header: {num_verts} verts, {num_faces} faces, '
            f'vertex_size={sizeof_vertex}, bones={num_bones}, lod_offsets={num_lod_offsets}',
        )

        offset = 13 + header_size

        verts, offset = read_vertices(data, offset, num_verts, sizeof_vertex)

        if version_num in ('4.00', '4.01', '5.00') and num_bones > 0:
            skinning_size = num_verts * 8  
            log_buffer.log(
                'Mesh',
                f'Skipping {skinning_size} bytes of skinning data ({num_verts} verts × 8 bytes)',
            )
            offset += skinning_size

        faces = []
        for _ in range(num_faces):
            a, b, c = struct.unpack_from('<III', data, offset)
            faces.append(Face(a + 1, b + 1, c + 1))  
            offset += 12

        if num_lod_offsets >= 2:
            try:
                lod_offsets = []
                for _ in range(num_lod_offsets):
                    lod_val = struct.unpack_from('<I', data, offset)[0]
                    lod_offsets.append(lod_val)
                    offset += 4

                if len(lod_offsets) >= 2 and lod_offsets[1] > 0 and lod_offsets[1] < len(faces):
                    original_count = len(faces)
                    faces = faces[: lod_offsets[1]]
                    log_buffer.log(
                        'Mesh',
                        f'Applied LOD: {original_count} → {len(faces)} faces '
                        f'(offsets: {lod_offsets})',
                    )
            except Exception as e:
                log_buffer.log('Mesh', f'LOD parsing failed: {e}')

        v_lines = [
            f'v {fix_float(f"{v.px:.6f}")} {fix_float(f"{v.py:.6f}")} {fix_float(f"{v.pz:.6f}")} '
            f'{fix_float(f"{v.r / 255.0:.6f}")} {fix_float(f"{v.g / 255.0:.6f}")} {fix_float(f"{v.b / 255.0:.6f}")}'
            for v in verts
        ]
        n_lines = [
            f'vn {fix_float(f"{v.nx:.6f}")} {fix_float(f"{v.ny:.6f}")} {fix_float(f"{v.nz:.6f}")}'
            for v in verts
        ]
        t_lines = [f'vt {fix_float(f"{v.tu:.6f}")} {fix_float(f"{v.tv:.6f}")} 0.0' for v in verts]
        f_lines = [f'f {f.a}/{f.a}/{f.a} {f.b}/{f.b}/{f.b} {f.c}/{f.c}/{f.c}' for f in faces]

        return write_obj_data(v_lines, n_lines, t_lines, f_lines)
    except Exception as e:
        log_buffer.log('Mesh', f'Error processing v{version_num} mesh: {e}')
        return None

def process_v6_v7(data: bytes) -> str:
    
    if not DRACO_AVAILABLE:
        log_buffer.log('Mesh', 'DracoPy not available - cannot process v6/v7 meshes')
        return None
    try:
        version = data[:12].decode('utf-8', errors='replace').strip()
        offset = 13  
        coremesh_data = None
        lod_data = None
        
        while offset < len(data):
            
            if offset + 16 > len(data):
                break
            chunk_type = data[offset : offset + 8].decode('utf-8', errors='ignore').rstrip('\0')
            offset += 8
            chunk_ver = struct.unpack_from('<I', data, offset)[0]
            offset += 4
            chunk_size = struct.unpack_from('<I', data, offset)[0]
            offset += 4
            
            if chunk_ver == 2:
                data_size = struct.unpack_from('<I', data, offset)[0]
                offset += 4
            else:
                data_size = chunk_size
            
            if offset + data_size > len(data):
                log_buffer.log('Mesh', f'Warning: Chunk {chunk_type} exceeds file size')
                break
            chunk_content = data[offset : offset + data_size]
            
            if chunk_type == 'COREMESH' and chunk_ver == 2:
                coremesh_data = chunk_content
            elif chunk_type == 'LODS':
                lod_data = chunk_content
            offset += data_size
        if not coremesh_data:
            log_buffer.log('Mesh', 'No COREMESH chunk found in v6/v7 mesh')
            return None
        
        try:
            mesh = DracoPy.decode(coremesh_data)
            if mesh is None or not hasattr(mesh, 'points'):
                log_buffer.log('Mesh', 'Draco decode failed: invalid mesh data')
                return None
            
            positions = np.array(mesh.points, dtype=np.float32)
            num_verts = len(positions)
            if num_verts == 0:
                log_buffer.log('Mesh', 'Draco mesh has no vertices')
                return None
            
            verts = [Vertex() for _ in range(num_verts)]
            for i in range(num_verts):
                verts[i].px, verts[i].py, verts[i].pz = positions[i]
            
            normals = None
            if hasattr(mesh, 'get_attribute_by_unique_id'):
                try:
                    
                    normal_attr = mesh.get_attribute_by_unique_id(1)
                    if normal_attr is not None and 'data' in normal_attr:
                        normals = np.array(normal_attr['data'], dtype=np.float32)
                        if normals.ndim == 1:
                            normals = normals.reshape(-1, 3)
                except Exception:
                    pass

            if normals is None and hasattr(mesh, 'normals') and mesh.normals is not None:
                normals = np.array(mesh.normals, dtype=np.float32)
                if normals.ndim == 1:
                    normals = normals.reshape(-1, 3)

            if normals is not None:
                if len(normals) == num_verts:
                    for i in range(num_verts):
                        verts[i].nx, verts[i].ny, verts[i].nz = normals[i]
                else:
                    log_buffer.log(
                        'Mesh',
                        f'Warning: Normal count mismatch ({len(normals)} vs {num_verts})',
                    )

            tex_coords = None
            if hasattr(mesh, 'get_attribute_by_unique_id'):
                try:
                    
                    uv_attr = mesh.get_attribute_by_unique_id(2)
                    if uv_attr is not None and 'data' in uv_attr:
                        tex_coords = np.array(uv_attr['data'], dtype=np.float32)
                        if tex_coords.ndim == 1:
                            tex_coords = tex_coords.reshape(-1, 2)
                except Exception:
                    pass
            
            colors = None
            if hasattr(mesh, 'get_attribute_by_unique_id'):
                try:
                    
                    color_attr = mesh.get_attribute_by_unique_id(4)
                    if color_attr is not None and 'data' in color_attr:
                        colors = np.array(color_attr['data'], dtype=np.uint8)
                        if colors.ndim == 1:
                            colors = colors.reshape(-1, 4)  
                except Exception:
                    pass

            if colors is not None:
                if len(colors) == num_verts:
                    for i in range(num_verts):
                        verts[i].r = colors[i][0]
                        verts[i].g = colors[i][1]
                        verts[i].b = colors[i][2]
                        verts[i].a = colors[i][3]
                else:
                    log_buffer.log(
                        'Mesh',
                        f'Warning: Color count mismatch ({len(colors)} vs {num_verts})',
                    )

            if tex_coords is None and hasattr(mesh, 'tex_coord') and mesh.tex_coord is not None:
                tex_coords = np.array(mesh.tex_coord, dtype=np.float32)
                if tex_coords.ndim == 1:
                    tex_coords = tex_coords.reshape(-1, 2)

            if tex_coords is not None:
                if len(tex_coords) == num_verts:
                    for i in range(num_verts):
                        u, v = tex_coords[i]
                        verts[i].tu = u
                        verts[i].tv = 1.0 - v  
                else:
                    log_buffer.log(
                        'Mesh',
                        f'Warning: UV count mismatch ({len(tex_coords)} vs {num_verts})',
                    )
            
            faces = []
            if hasattr(mesh, 'faces') and mesh.faces is not None:
                for tri in mesh.faces:
                    a, b, c = map(int, tri)
                    
                    faces.append(Face(a + 1, b + 1, c + 1))
            log_buffer.log(
                'Mesh',
                f'Draco mesh decoded: {num_verts:,} vertices, {len(faces):,} faces',
            )
            
            max_faces = len(faces)
            if lod_data and len(lod_data) > 7:
                try:
                    lod_pos = 0
                    
                    lod_pos += 2
                    
                    num_high_quality = lod_data[lod_pos]
                    lod_pos += 1
                    
                    num_offsets = struct.unpack_from('<I', lod_data, lod_pos)[0]
                    lod_pos += 4
                    if num_offsets >= 2:
                        
                        offset1 = struct.unpack_from('<I', lod_data, lod_pos)[0]
                        lod_pos += 4
                        offset2 = struct.unpack_from('<I', lod_data, lod_pos)[0]
                        
                        computed = offset2 - offset1
                        if computed > 0 and computed < len(faces):
                            max_faces = computed
                            log_buffer.log(
                                'Mesh',
                                f'Applying high-quality LOD: {len(faces):,} → {max_faces:,} faces',
                            )
                except Exception as e:
                    log_buffer.log('Mesh', f'LOD parsing failed: {e}')
            
            if max_faces < len(faces):
                faces = faces[:max_faces]
            
            v_lines = [
                f'v {fix_float(f"{v.px:.6f}")} {fix_float(f"{v.py:.6f}")} {fix_float(f"{v.pz:.6f}")} '
                f'{fix_float(f"{v.r / 255.0:.6f}")} {fix_float(f"{v.g / 255.0:.6f}")} {fix_float(f"{v.b / 255.0:.6f}")}'
                for v in verts
            ]
            n_lines = [
                f'vn {fix_float(f"{v.nx:.6f}")} {fix_float(f"{v.ny:.6f}")} {
                    fix_float(f"{v.nz:.6f}")
                }'
                for v in verts
            ]
            t_lines = [
                f'vt {fix_float(f"{v.tu:.6f}")} {fix_float(f"{v.tv:.6f}")} 0.0' for v in verts
            ]
            f_lines = [f'f {f.a}/{f.a}/{f.a} {f.b}/{f.b}/{f.b} {f.c}/{f.c}/{f.c}' for f in faces]
            return write_obj_data(v_lines, n_lines, t_lines, f_lines)
        except Exception as e:
            log_buffer.log('Mesh', f'DracoPy decoding error: {e}')
            import traceback

            traceback.print_exc()
            return None
    except Exception as e:
        log_buffer.log('Mesh', f'Error processing v6/v7 mesh: {e}')
        import traceback

        traceback.print_exc()
        return None

SUPPORTED_MESH_HEADERS = (
    'version 1.',
    'version 2.00',
    'version 3.00',
    'version 3.01',
    'version 4.00',
    'version 4.01',
    'version 5.00',
    'version 6.00',
    'version 7.00',
)

def _mesh_header(data: bytes) -> str:
    if data.startswith(b'\x1f\x8b'):
        try:
            data = gzip.decompress(data)
        except Exception:
            return ''
    return data[:12].decode('utf-8', errors='ignore').strip()

def is_mesh_data(data: bytes) -> bool:
    
    if not data or len(data) < 12:
        return False
    header = _mesh_header(data)
    return any(header.startswith(prefix) for prefix in SUPPORTED_MESH_HEADERS)

def convert(data: bytes, output_path: str = None) -> str:
    
    if not data or len(data) < 12:
        log_buffer.log('Mesh', 'Invalid mesh data: file too small')
        return None
    if data.startswith(b'\x1f\x8b'):
        try:
            data = gzip.decompress(data)
        except Exception as e:
            log_buffer.log('Mesh', f'Failed to decompress gzip mesh data: {e}')
            return None
    
    header = _mesh_header(data)
    log_buffer.log('Mesh', f'Detected mesh version: {header}')
    obj_content = None
    
    if header.startswith('version 1.'):
        obj_content = process_v1(data)
    elif header in [
        'version 2.00',
        'version 3.00',
        'version 3.01',
        'version 4.00',
        'version 4.01',
        'version 5.00',
    ]:
        version_num = header.split()[1]  
        obj_content = process_v2_to_v5(data, version_num)
    elif header in ['version 6.00', 'version 7.00']:
        obj_content = process_v6_v7(data)
    else:
        log_buffer.log('Mesh', f'Unsupported mesh version: {header}')
        return None
    
    if obj_content and output_path:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(obj_content)
            log_buffer.log('Mesh', f'OBJ file written to: {output_path}')
        except Exception as e:
            log_buffer.log('Mesh', f'Failed to write OBJ file: {e}')
    return obj_content

RBXM_MAGIC = b'<roblox!\x89\xff\x0d\x0a\x1a\x0a'

def decompress_if_needed(data: bytes) -> bytes:
    
    if data.startswith(b'\x1f\x8b'):
        return gzip.decompress(data)
    return data

def classify_roblox_document(data: bytes) -> str | None:
    
    try:
        data = decompress_if_needed(data)
    except Exception:
        return None

    if data.startswith(RBXM_MAGIC):
        return 'rbxl' if _binary_contains_class(data, 'DataModel') else 'rbxm'

    root = _parse_roblox_xml(data)
    if root is not None:
        if not _xml_contains_item(root):
            return None
        return 'rbxl' if _xml_contains_datamodel(root) else 'rbxmx'

    return None

def get_roblox_document_export_formats(data: bytes, asset_type: int | None = None) -> list[str]:
    
    kind = classify_roblox_document(data)
    if asset_type == 9 and kind in {'rbxl', 'rbxm', 'rbxmx'}:
        return ['converted_document_rbxl']
    if kind == 'rbxl':
        return ['converted_document_rbxl']
    if kind in {'rbxm', 'rbxmx'}:
        return ['converted_document_rbxm', 'converted_document_rbxmx']
    return []

def get_default_roblox_document_export_format(
    data: bytes, asset_type: int | None = None
) -> str | None:
    
    kind = classify_roblox_document(data)
    if asset_type == 9 and kind in {'rbxl', 'rbxm', 'rbxmx'}:
        return 'converted_document_rbxl'
    if kind == 'rbxl':
        return 'converted_document_rbxl'
    if kind == 'rbxmx':
        return 'converted_document_rbxmx'
    if kind == 'rbxm':
        return 'converted_document_rbxm'
    return None

def export_roblox_document(
    data: bytes,
    export_format: str,
    asset_type: int | None = None,
) -> tuple[bytes, str]:
    
    data = decompress_if_needed(data)
    kind = classify_roblox_document(data)
    if kind is None:
        raise ValueError('Data is not an RBXM/RBXMX/RBXL document')

    if export_format == 'converted_document_rbxl':
        if kind != 'rbxl' and asset_type != 9:
            raise ValueError('Only DataModel documents can be exported as RBXL')
        return _to_binary_document(data), '.rbxl'

    if export_format == 'converted_document_rbxm':
        if kind == 'rbxl' or asset_type == 9:
            raise ValueError('RBXL documents must be exported as RBXL')
        return _to_binary_document(data), '.rbxm'

    if export_format == 'converted_document_rbxmx':
        if kind == 'rbxl' or asset_type == 9:
            raise ValueError('RBXL documents must be exported as RBXL')
        if _parse_roblox_xml(data) is not None:
            return data, '.rbxmx'
        return write_rbxmx(RbxmDeserializer().deserialize(data)), '.rbxmx'

    raise ValueError(f'Unsupported Roblox document export format: {export_format}')

def _to_binary_document(data: bytes) -> bytes:
    if data.startswith(RBXM_MAGIC):
        return data
    return write_rbxm(_xml_to_document(data))

def _document_contains_datamodel(doc: RbxDocument) -> bool:
    return any(inst.class_name == 'DataModel' for inst in doc.instances.values())

def _binary_contains_class(data: bytes, class_name: str) -> bool:
    offset = 32
    target = class_name
    try:
        while offset + 16 <= len(data):
            chunk_name = data[offset : offset + 4].decode('ascii')
            compressed_size = struct.unpack_from('<I', data, offset + 4)[0]
            uncompressed_size = struct.unpack_from('<I', data, offset + 8)[0]
            offset += 16

            if chunk_name == 'END\x00':
                break

            if compressed_size == 0:
                chunk_start = offset
                offset += uncompressed_size
                if chunk_name != 'INST':
                    continue
                chunk_data = data[chunk_start:offset]
            else:
                raw = data[offset : offset + compressed_size]
                offset += compressed_size
                if chunk_name != 'INST':
                    continue
                chunk_data = _decompress_chunk(raw, uncompressed_size)

            if chunk_name == 'INST':
                found_class, _ = read_string(chunk_data, 4)
                if found_class == target:
                    return True
    except Exception:
        try:
            return _document_contains_datamodel(RbxmDeserializer().deserialize(data))
        except Exception:
            return False
    return False

def _xml_contains_datamodel(root: ET.Element) -> bool:
    return any(
        _tag_name(elem) == 'Item' and elem.get('class') == 'DataModel' for elem in root.iter()
    )

def _xml_contains_item(root: ET.Element) -> bool:
    return any(_tag_name(elem) == 'Item' for elem in root.iter())

def _parse_roblox_xml(data: bytes) -> ET.Element | None:
    stripped = data.lstrip()
    if stripped.startswith(b'\xef\xbb\xbf'):
        stripped = stripped[3:].lstrip()
    if not stripped.startswith(b'<'):
        return None
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return None
    if _tag_name(root) != 'roblox':
        return None
    return root

def _xml_to_document(data: bytes) -> RbxDocument:
    root = ET.fromstring(data)
    if _tag_name(root) != 'roblox':
        raise ValueError('XML root is not a Roblox document')

    shared_by_md5: dict[str, bytes] = {}
    shared_strings: list[bytes] = []
    ss_root = _find_child(root, 'SharedStrings')
    if ss_root is not None:
        for shared in _children_named(ss_root, 'SharedString'):
            text = (shared.text or '').strip()
            blob = b''
            if text:
                try:
                    blob = base64.b64decode(text)
                except Exception:
                    blob = text.encode('utf-8', errors='replace')
            md5 = shared.get('md5') or ''
            if md5:
                shared_by_md5[md5] = blob
            shared_strings.append(blob)

    ref_map: dict[str, int] = {}
    next_ref = 1

    def mapped_ref(ref: str) -> int:
        nonlocal next_ref
        if ref in ref_map:
            return ref_map[ref]
        try:
            value = int(ref)
        except ValueError:
            while next_ref in ref_map.values():
                next_ref += 1
            value = next_ref
            next_ref += 1
        ref_map[ref] = value
        return value

    instances: dict[int, RbxInstance] = {}

    def parse_item(item: ET.Element) -> RbxInstance:
        referent_text = item.get('referent') or ''
        referent = mapped_ref(referent_text)
        inst = RbxInstance(class_name=item.get('class') or 'Folder', referent=referent)
        instances[referent] = inst

        props_elem = _find_child(item, 'Properties')
        if props_elem is not None:
            for prop_elem in list(props_elem):
                prop_name = prop_elem.get('name') or ''
                if not prop_name:
                    continue
                type_name = _tag_name(prop_elem)
                fmt = _property_format_from_type_name(type_name)
                if fmt is None:
                    continue
                value = _xml_property_value(prop_elem, type_name, shared_by_md5)
                inst.properties[prop_name] = RbxProperty(
                    name=prop_name,
                    fmt=fmt,
                    value=_value_for_format(value, fmt, mapped_ref),
                )

        inst.children = [parse_item(child) for child in _children_named(item, 'Item')]
        return inst

    roots = [parse_item(item) for item in _children_named(root, 'Item')]
    metadata = {
        elem.get('name') or _tag_name(elem): (elem.text or '').strip()
        for elem in list(root)
        if _tag_name(elem) == 'Meta'
    }

    return RbxDocument(
        version=0,
        type_count=0,
        object_count=len(instances),
        metadata=RbxMetadata(entries=metadata),
        instances=instances,
        roots=roots,
        shared_strings=shared_strings,
    )

def _xml_property_value(
    elem: ET.Element,
    type_name: str,
    shared_by_md5: dict[str, bytes],
) -> Any:
    text = elem.text or ''
    if type_name == 'SharedString':
        return shared_by_md5.get(text.strip(), b'')
    if type_name == 'BinaryString':
        stripped = text.strip()
        if not stripped:
            return b''
        try:
            return base64.b64decode(stripped)
        except Exception:
            return stripped.encode('utf-8', errors='replace')
    if type_name == 'ProtectedString':
        return text
    if list(elem):
        return {_tag_name(child): (child.text or '').strip() for child in elem}
    return text.strip()

def _property_format_from_type_name(type_name: str) -> PropertyFormat | None:
    normalized = type_name.strip()
    if not normalized:
        return PropertyFormat.STRING
    upper = normalized.upper()
    if upper in PropertyFormat.__members__:
        return PropertyFormat[upper]

    tag_to_format = {tag.lower(): fmt for fmt, tag in PROPERTY_FORMAT_TO_XML_TAG.items()}
    aliases = {
        'class': None,
        'refid': None,
        'binarystring': PropertyFormat.STRING,
        'protectedstring': PropertyFormat.STRING,
        'content': PropertyFormat.CONTENT,
        'token': PropertyFormat.ENUM,
        'optionalcoordinateframe': PropertyFormat.OPTIONAL_CFRAME,
        'uniqueid': PropertyFormat.UNIQUE_ID,
        'securitycapabilities': PropertyFormat.SECURITY_CAPABILITIES,
    }
    key = normalized.lower()
    if key in aliases:
        return aliases[key]
    return tag_to_format.get(key, PropertyFormat.STRING)

def _value_for_format(value: Any, fmt: PropertyFormat, ref_mapper) -> Any:
    if fmt in {
        PropertyFormat.INT,
        PropertyFormat.ENUM,
        PropertyFormat.BRICK_COLOR,
        PropertyFormat.SECURITY_CAPABILITIES,
    }:
        return _safe_int(value)
    if fmt == PropertyFormat.INT64:
        return _safe_int(value)
    if fmt in {PropertyFormat.FLOAT, PropertyFormat.DOUBLE}:
        return _safe_float(value)
    if fmt == PropertyFormat.BOOL:
        return _safe_bool(value)
    if fmt == PropertyFormat.REF:
        if value is None:
            return None
        if isinstance(value, dict):
            value = value.get('Ref') or value.get('referent') or value.get('id')
        text = str(value or '').strip()
        if text in {'', 'None', '-1', 'null'}:
            return None
        if '->' in text:
            text = text.split('->', 1)[0].strip()
        return ref_mapper(text)
    if fmt == PropertyFormat.UNIQUE_ID:
        if isinstance(value, dict) or isinstance(value, bytes):
            return value
        text = str(value).strip().replace('-', '')
        if len(text) == 32:
            try:
                xml_random = int(text[:16], 16)
                random_bits = (xml_random >> 1) | ((xml_random & 1) << 63)
                return {
                    'Index': int(text[24:32], 16),
                    'Time': int(text[16:24], 16),
                    'Random': random_bits,
                }
            except ValueError:
                pass
        return {'Index': 0, 'Time': 0, 'Random': 0}
    if fmt == PropertyFormat.CONTENT:
        if isinstance(value, dict):
            uri = value.get('Uri') or value.get('uri') or value.get('url')
            if uri:
                return {'SourceType': 'Uri', 'Uri': str(uri)}
            ref = value.get('Ref')
            if ref is not None:
                return {'SourceType': 'Object', 'Ref': ref_mapper(str(ref))}
            if 'null' in value:
                return None
            return value
        if value is None:
            return value
        text = str(value)
        return {'SourceType': 'Uri', 'Uri': text} if text else None
    if fmt == PropertyFormat.UDIM:
        return _parse_udim_value(value)
    if fmt == PropertyFormat.UDIM2:
        return _parse_udim2_value(value)
    if fmt == PropertyFormat.RAY:
        return _parse_ray_value(value)
    if fmt == PropertyFormat.COLOR3:
        return _parse_vector_value(value, ('R', 'G', 'B'), float)
    if fmt == PropertyFormat.VECTOR2:
        return _parse_vector_value(value, ('X', 'Y'), float)
    if fmt == PropertyFormat.VECTOR3:
        return _parse_vector_value(value, ('X', 'Y', 'Z'), float)
    if fmt == PropertyFormat.VECTOR2INT16:
        return _parse_vector_value(value, ('X', 'Y'), int)
    if fmt == PropertyFormat.VECTOR3INT16:
        return _parse_vector_value(value, ('X', 'Y', 'Z'), int)
    if fmt in {
        PropertyFormat.CFRAME_MATRIX,
        PropertyFormat.CFRAME_QUAT,
        PropertyFormat.OPTIONAL_CFRAME,
    }:
        return _parse_cframe_value(value)
    if fmt == PropertyFormat.NUMBER_RANGE:
        return _parse_number_range_value(value)
    if fmt == PropertyFormat.RECT2D:
        return _parse_rect2d_value(value)
    if fmt == PropertyFormat.PHYSICAL_PROPERTIES:
        return _parse_physical_properties_value(value)
    if fmt == PropertyFormat.COLOR3UINT8:
        return _parse_vector_value(value, ('R', 'G', 'B'), int)
    if fmt == PropertyFormat.FONT:
        return _parse_font_value(value)
    return value

def _parse_udim_value(value: Any) -> dict[str, float | int]:
    pairs = (
        {str(k): v for k, v in value.items()}
        if isinstance(value, dict)
        else _parse_key_values(str(value))
    )
    if pairs:
        return {
            'S': _safe_float(pairs.get('S', 0.0)),
            'O': _safe_int(pairs.get('O', 0)),
        }
    numbers = _parse_numbers(str(value))
    return {
        'S': numbers[0] if len(numbers) > 0 else 0.0,
        'O': int(numbers[1]) if len(numbers) > 1 else 0,
    }

def _parse_udim2_value(value: Any) -> dict[str, float | int]:
    pairs = (
        {str(k): v for k, v in value.items()}
        if isinstance(value, dict)
        else _parse_key_values(str(value))
    )
    if pairs:
        return {
            'XS': _safe_float(pairs.get('XS', 0.0)),
            'XO': _safe_int(pairs.get('XO', 0)),
            'YS': _safe_float(pairs.get('YS', 0.0)),
            'YO': _safe_int(pairs.get('YO', 0)),
        }
    numbers = _parse_numbers(str(value))
    return {
        'XS': numbers[0] if len(numbers) > 0 else 0.0,
        'XO': int(numbers[1]) if len(numbers) > 1 else 0,
        'YS': numbers[2] if len(numbers) > 2 else 0.0,
        'YO': int(numbers[3]) if len(numbers) > 3 else 0,
    }

def _parse_vector_value(value: Any, keys: tuple[str, ...], caster) -> dict[str, Any]:
    pairs = (
        {str(k): v for k, v in value.items()}
        if isinstance(value, dict)
        else _parse_key_values(str(value))
    )
    if pairs:
        return {key: _cast_number(pairs.get(key, 0), caster) for key in keys}
    numbers = _parse_numbers(str(value))
    return {
        key: _cast_number(numbers[index] if index < len(numbers) else 0, caster)
        for index, key in enumerate(keys)
    }

def _parse_ray_value(value: Any) -> dict[str, dict[str, float]]:
    if isinstance(value, dict):
        return {
            'origin': _parse_vector_value(value.get('origin', {}), ('X', 'Y', 'Z'), float),
            'direction': _parse_vector_value(value.get('direction', {}), ('X', 'Y', 'Z'), float),
        }
    numbers = _parse_numbers(str(value))
    padded = numbers + [0.0] * max(0, 6 - len(numbers))
    return {
        'origin': {'X': padded[0], 'Y': padded[1], 'Z': padded[2]},
        'direction': {'X': padded[3], 'Y': padded[4], 'Z': padded[5]},
    }

def _parse_cframe_value(value: Any) -> dict[str, float] | None:
    text = str(value).strip()
    if value is None or text.lower() in {'', 'none', 'null'}:
        return None
    result = {
        'X': 0.0,
        'Y': 0.0,
        'Z': 0.0,
        'R00': 1.0,
        'R01': 0.0,
        'R02': 0.0,
        'R10': 0.0,
        'R11': 1.0,
        'R12': 0.0,
        'R20': 0.0,
        'R21': 0.0,
        'R22': 1.0,
    }
    if isinstance(value, dict):
        result.update({key: _safe_float(value.get(key, result[key])) for key in result})
        return result
    pairs = _parse_key_values(text)
    if pairs:
        for key in result:
            if key in pairs:
                result[key] = _safe_float(pairs[key])
        return result
    numbers = _parse_numbers(text)
    if len(numbers) >= 12:
        for key, number in zip(result, numbers[:12], strict=False):
            result[key] = number
    elif len(numbers) >= 3:
        result['X'], result['Y'], result['Z'] = numbers[:3]
    return result

def _parse_number_range_value(value: Any) -> dict[str, float]:
    if isinstance(value, dict):
        return {
            'Min': _safe_float(value.get('Min', 0.0)),
            'Max': _safe_float(value.get('Max', 0.0)),
        }
    pairs = _parse_key_values(str(value))
    if pairs:
        return {
            'Min': _safe_float(pairs.get('Min', 0.0)),
            'Max': _safe_float(pairs.get('Max', 0.0)),
        }
    numbers = _parse_numbers(str(value))
    return {
        'Min': numbers[0] if len(numbers) > 0 else 0.0,
        'Max': numbers[1] if len(numbers) > 1 else 0.0,
    }

def _parse_rect2d_value(value: Any) -> dict[str, dict[str, float]]:
    if isinstance(value, dict):
        return {
            'min': _parse_vector_value(value.get('min', {}), ('X', 'Y'), float),
            'max': _parse_vector_value(value.get('max', {}), ('X', 'Y'), float),
        }
    numbers = _parse_numbers(str(value))
    padded = numbers + [0.0] * max(0, 4 - len(numbers))
    return {
        'min': {'X': padded[0], 'Y': padded[1]},
        'max': {'X': padded[2], 'Y': padded[3]},
    }

def _parse_physical_properties_value(value: Any) -> dict[str, Any] | None:
    text = str(value).strip()
    if value is None or text.lower() in {'', 'none', 'null', 'default'}:
        return None
    if isinstance(value, dict):
        return {
            'CustomPhysics': _safe_bool(value.get('CustomPhysics', True)),
            'Density': _safe_float(value.get('Density', 0.0)),
            'Friction': _safe_float(value.get('Friction', 0.0)),
            'Elasticity': _safe_float(value.get('Elasticity', 0.0)),
            'FrictionWeight': _safe_float(value.get('FrictionWeight', 0.0)),
            'ElasticityWeight': _safe_float(value.get('ElasticityWeight', 0.0)),
            'AcousticAbsorption': _safe_float(value.get('AcousticAbsorption', 1.0)),
        }
    pairs = _parse_key_values(text)
    if pairs:
        return _parse_physical_properties_value(pairs)
    numbers = _parse_numbers(text)
    if len(numbers) < 5:
        return None
    result: dict[str, Any] = {
        'CustomPhysics': True,
        'Density': numbers[0],
        'Friction': numbers[1],
        'Elasticity': numbers[2],
        'FrictionWeight': numbers[3],
        'ElasticityWeight': numbers[4],
    }
    if len(numbers) > 5:
        result['AcousticAbsorption'] = numbers[5]
    return result

def _parse_font_value(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return {
            'Family': str(value.get('Family', '')),
            'Weight': _safe_int(value.get('Weight', 400)),
            'Style': _safe_int(value.get('Style', 0)),
            'CachedFaceId': str(value.get('CachedFaceId', '')),
        }
    pairs = _parse_key_values(str(value))
    if pairs:
        return _parse_font_value(pairs)
    parts = [part.strip() for part in str(value).split(',')]
    return {
        'Family': parts[0] if len(parts) > 0 else '',
        'Weight': _safe_int(parts[1] if len(parts) > 1 else 400),
        'Style': _safe_int(parts[2] if len(parts) > 2 else 0),
        'CachedFaceId': parts[3] if len(parts) > 3 else '',
    }

def _parse_key_values(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for part in re.split(r'[,;]\s*', text.strip().strip('[]{}()')):
        if '=' in part:
            key, raw_value = part.split('=', 1)
        elif ':' in part:
            key, raw_value = part.split(':', 1)
        else:
            continue
        key = key.strip().strip('"\'{}[]()')
        raw_value = raw_value.strip().strip('"\'{}[]()')
        if key:
            result[key] = raw_value
    return result

def _parse_numbers(text: str) -> list[float]:
    return [
        float(match.group(0))
        for match in re.finditer(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?', text)
    ]

def _cast_number(value: Any, caster):
    if caster is int:
        return int(round(float(value)))
    return caster(value)

def _safe_int(value: Any) -> int:
    try:
        return int(str(value).strip(), 0)
    except (TypeError, ValueError):
        return 0

def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

def _safe_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {'1', 'true', 'yes', 'on'}

def _find_child(parent: ET.Element, name: str) -> ET.Element | None:
    for child in list(parent):
        if _tag_name(child) == name:
            return child
    return None

def _children_named(parent: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in list(parent) if _tag_name(child) == name]

def _tag_name(elem: ET.Element) -> str:
    return elem.tag.rsplit('}', 1)[-1]

_decompress_document = decompress_if_needed
_classify_document = classify_roblox_document
_RbxmDeserializer = RbxmDeserializer
_write_rbxmx = write_rbxmx
_write_rbxm = write_rbxm

def apply_visual_polish(root: tk.Tk, theme: Optional[str] = "system",
                        palette: Optional[Dict[str, str]] = None):
    global _CURRENT_PALETTE
    try:
        root.tk.call("tk", "scaling", 1.25)
    except Exception:
        pass

    p = {
        "bg_dark": "#1e1e1e",
        "bg_medium": "#252526",
        "bg_light": "#333333",
        "bg_hover": "#3c3c3c",
        "fg": "#d4d4d4",
        "accent": "#007acc",
        "border": "#3c3c3c",
    }
    if palette:
        p.update(palette)

    style = ttk.Style(root)
    
    for t in ("clam", "alt", "default", "classic"):
        if t in style.theme_names():
            try:
                style.theme_use(t)
            except Exception:
                pass
            break

    try:
        tkfont.nametofont("TkDefaultFont").configure(family="Comic Sans MS", size=10)
        tkfont.nametofont("TkTextFont").configure(family="Consolas", size=10)
        tkfont.nametofont("TkFixedFont").configure(family="Consolas", size=10)
        tkfont.nametofont("TkMenuFont").configure(family="Comic Sans MS", size=10)
        tkfont.nametofont("TkHeadingFont").configure(family="Comic Sans MS", size=10, weight="bold")
    except Exception:
        pass

    _CURRENT_PALETTE = p
    bg_dark, bg_medium, bg_light = p["bg_dark"], p["bg_medium"], p["bg_light"]
    bg_hover, fg_white, accent, border = p["bg_hover"], p["fg"], p["accent"], p["border"]
    root.configure(bg=bg_dark)

    for opt, val in (
        ("*background", bg_dark),
        ("*foreground", fg_white),
        ("*activeBackground", bg_hover),
        ("*activeForeground", "#ffffff"),
        ("*insertBackground", "#ffffff"),
        ("*selectBackground", accent),
        ("*selectForeground", "#ffffff"),
        ("*troughColor", bg_medium),
        ("*highlightBackground", border),
        ("*highlightColor", accent),
    ):
        try:
            root.option_add(opt, val, priority=60)
        except Exception:
            pass

    for opt, val in (
        ("*Toplevel.background", bg_dark),
        ("*Dialog.background", bg_dark),
        ("*Message.background", bg_dark),
        ("*Message.foreground", fg_white),
        ("*Dialog.Entry.background", bg_medium),
        ("*Dialog.Entry.foreground", fg_white),
        ("*Dialog.Label.background", bg_dark),
        ("*Dialog.Label.foreground", fg_white),
        ("*Dialog.Button.background", bg_light),
        ("*Dialog.Button.foreground", fg_white),
        ("*Dialog.Button.activeBackground", bg_hover),
        ("*Dialog.Button.activeForeground", "#ffffff"),
    ):
        try:
            root.option_add(opt, val)
        except Exception:
            pass

    style.configure(".", background=bg_dark, foreground=fg_white, fieldbackground=bg_medium,
                    bordercolor=border, lightcolor=bg_medium, darkcolor=bg_medium, troughcolor=bg_medium,
                    activebackground=bg_hover, selectbackground=accent, selectforeground="#ffffff")

    style.configure("TFrame", background=bg_dark)
    style.configure("TLabel", background=bg_dark, foreground=fg_white, font=("Comic Sans MS", 10))
    style.configure("TLabelframe", background=bg_dark, foreground=fg_white, bordercolor=border)
    style.configure("TLabelframe.Label", background=bg_dark, foreground=fg_white, padding=(4, 0))

    style.configure("TButton", background=bg_light, foreground=fg_white, bordercolor=border,
                    focusthickness=0, padding=(12, 7), relief="flat", font=("Comic Sans MS", 9, "bold"))
    style.map("TButton",
              background=[("pressed", accent), ("active", bg_hover), ("disabled", bg_medium)],
              foreground=[("disabled", "#6f6f6f")],
              bordercolor=[("active", accent)])

    style.configure("TCheckbutton", background=bg_dark, foreground=fg_white)
    style.map("TCheckbutton", background=[("active", bg_dark)], foreground=[("active", fg_white)])
    style.configure("TRadiobutton", background=bg_dark, foreground=fg_white)
    style.map("TRadiobutton", background=[("active", bg_dark)], foreground=[("active", fg_white)])

    style.configure("TEntry", fieldbackground=bg_medium, foreground=fg_white,
                    insertcolor="#ffffff", bordercolor=border, padding=3)
    style.map("TEntry", fieldbackground=[("focus", bg_medium)], bordercolor=[("focus", accent)])
    style.configure("TCombobox", fieldbackground=bg_medium, background=bg_light, foreground=fg_white,
                    arrowcolor=fg_white, bordercolor=border, padding=3)
    style.map("TCombobox",
              fieldbackground=[("readonly", bg_medium)],
              background=[("readonly", bg_light)],
              foreground=[("readonly", fg_white)],
              selectbackground=[("readonly", accent)], selectforeground=[("readonly", "#ffffff")],
              bordercolor=[("focus", accent)])
    style.configure("TSpinbox", fieldbackground=bg_medium, background=bg_light, foreground=fg_white,
                    arrowcolor="#ffffff", bordercolor=border)
    style.map("TSpinbox", fieldbackground=[("focus", bg_medium)], bordercolor=[("focus", accent)])

    style.configure("Vertical.TScrollbar", background=bg_light, troughcolor=bg_dark,
                    arrowcolor=fg_white, bordercolor=border, relief="flat")
    style.configure("Horizontal.TScrollbar", background=bg_light, troughcolor=bg_dark,
                    arrowcolor=fg_white, bordercolor=border, relief="flat")
    style.configure("TProgressbar", background=accent, troughcolor=bg_medium)

    style.configure("TNotebook", background=bg_dark, borderwidth=0, tabmargins=(6, 4, 6, 0))
    style.configure("TNotebook.Tab", background=bg_medium, foreground=fg_white, padding=(12, 5), relief="flat")
    style.map("TNotebook.Tab",
              background=[("selected", accent)], foreground=[("selected", "#ffffff")],
              expand=[("selected", (2, 0, 2, 0))])

    style.configure("Treeview", rowheight=23, font=("Consolas", 9), background=bg_medium,
                    foreground=fg_white, fieldbackground=bg_medium, bordercolor=border)
    style.configure("Treeview.Heading", background=bg_light, foreground=fg_white,
                    font=("Segoe UI Semibold", 10), padding=(6, 4, 6, 4))
    style.map("Treeview", background=[("selected", accent)], foreground=[("selected", "#ffffff")])

    root._palette = p

    try:
        root.unbind_all("<Map>")
        root.bind_all("<Map>", _theme_on_map, add="+")
    except Exception:
        pass
    _theme_open_windows(root)

def darken_menus(menus: Iterable) -> None:
    
    p = _CURRENT_PALETTE
    bg_dark = p.get("bg_dark", "#1e1e1e")
    bg_light = p.get("bg_light", "#333333")
    fg_white = p.get("fg", "#d4d4d4")
    accent = p.get("accent", "#007acc")
    seen = set()

    def _apply(menu):
        if id(menu) in seen:
            return
        seen.add(id(menu))
        try:
            menu.configure(bg=bg_dark, fg=fg_white, activebackground=accent,
                           activeforeground="#ffffff", selectcolor="#ffffff",
                           bd=1, relief="flat", borderwidth=0, font=("Segoe UI", 10))
        except Exception:
            pass
        try:
            for index in (menu.index("end") or 0) + 1:
                try:
                    sub = menu.entrycget(index, "menu")
                except Exception:
                    sub = None
                if sub:
                    _apply(sub)
        except Exception:
            pass

    for m in menus:
        try:
            _apply(m)
        except Exception:
            pass

def _set_pane_minsize(paned: ttk.PanedWindow, pane, size: int) -> None:
    try:
        paned.paneconfigure(pane, minsize=size)
    except Exception:
        pass

def theme_toplevel(win) -> None:
    
    p = _CURRENT_PALETTE
    try:
        win.configure(bg=p["bg_dark"])
    except Exception:
        pass
    try:
        children = win.winfo_children()
    except Exception:
        children = []
    for c in children:
        try:
            klass = c.winfo_class()
            if klass in ("Frame", "Toplevel", "Panedwindow"):
                c.configure(bg=p["bg_dark"])
            elif klass == "Label":
                c.configure(bg=p["bg_dark"], fg=p["fg"])
            elif klass in ("Entry", "Spinbox"):
                c.configure(bg=p["bg_medium"], fg=p["fg"], insertbackground="#ffffff",
                            selectbackground=p["accent"], selectforeground="#ffffff")
            elif klass in ("Listbox", "Text"):
                c.configure(bg=p["bg_medium"], fg=p["fg"],
                            insertbackground="#ffffff", selectbackground=p["accent"],
                            selectforeground="#ffffff")
            elif klass == "Canvas":
                c.configure(bg=p["bg_dark"], highlightbackground=p["border"])
            elif klass == "Button":
                c.configure(bg=p["bg_light"], fg=p["fg"], activebackground=p["bg_hover"],
                            activeforeground="#ffffff", relief="flat", borderwidth=1)
            elif klass == "Scrollbar":
                c.configure(bg=p["bg_light"], troughcolor=p["bg_dark"], activebackground=p["bg_hover"])
            elif klass == "Menu":
                c.configure(bg=p["bg_dark"], fg=p["fg"], activebackground=p["accent"],
                            activeforeground="#ffffff")
        except Exception:
            pass
        theme_toplevel(c)

def _theme_on_map(event) -> None:
    
    try:
        widget = event.widget
        top = widget.winfo_toplevel()
        if top is not widget or isinstance(top, tk.Toplevel):
            theme_toplevel(top)
    except Exception:
        pass

def _theme_open_windows(root) -> None:
    
    try:
        for child in root.winfo_children():
            if isinstance(child, tk.Toplevel):
                theme_toplevel(child)
    except Exception:
        pass

def default_paths():
    local = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    db = os.path.join(local, "Roblox", "rbx-storage.db")
    shard_root = os.path.join(local, "Roblox", "rbx-storage")
    return db, shard_root

def human_size(n: int) -> str:
    n = max(0, int(n))
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.0f}{unit}" if unit == "B" else f"{n:.1f}{unit}"
        n /= 1024.0

def id_bytes_to_hex(b: bytes) -> str:
    return b.hex()

def shard_path(root: str, hash_hex: str) -> str:
    return os.path.join(root, hash_hex[:2], hash_hex)

def read_shard_bytes(root: str, hash_hex: str) -> Optional[bytes]:
    path = shard_path(root, hash_hex)
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception:
        return None

def now_hms() -> str:
    return datetime.now().strftime("%H:%M:%S")

def _sanitize_filename_for_windows(s: str) -> str:
    illegal = '<>:"/\\|?*'
    cleaned = "".join("_" if c in illegal else c for c in (s or ""))
    return cleaned.rstrip(" .")

def load_settings() -> Dict:
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_settings(data: Dict) -> None:
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


_BUNDLE_DIR = getattr(sys, "_MEIPASS", BASE_DIR)
ICON_PATH = os.path.join(_BUNDLE_DIR, "routils.ico")







FFLAG_VK_NAMES = {
    "SPACE": 0x20, "ENTER": 0x0D, "TAB": 0x09, "ESC": 0x1B, "ESCAPE": 0x1B,
    "BACKSPACE": 0x08, "DELETE": 0x2E, "INSERT": 0x2D,
    "HOME": 0x24, "END": 0x23, "PAGEUP": 0x21, "PAGEDOWN": 0x22,
    "LEFT": 0x25, "UP": 0x26, "RIGHT": 0x27, "DOWN": 0x28,
}
FFLAG_VK_NAMES.update({f"F{i}": 0x6F + i for i in range(1, 13)})
FFLAG_VK_NAMES.update({str(i): 0x30 + i for i in range(10)})
FFLAG_VK_NAMES.update({chr(ord("A") + i): 0x41 + i for i in range(26)})


def fflag_key_to_vk(key: str) -> int:
    key = str(key or "").strip().upper()
    if key in FFLAG_VK_NAMES:
        return FFLAG_VK_NAMES[key]
    if len(key) == 1 and sys.platform == "win32":
        try:
            vk = ctypes.windll.user32.VkKeyScanW(ord(key)) & 0xFF
            return int(vk)
        except Exception:
            pass
    return 0


RBXH_MAGIC = b"RBXH"

def _parse_header_lines(hdr_text: str) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    if not hdr_text:
        return headers
    for line in hdr_text.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        k, v = line.split(":", 1)
        headers[k.strip().lower()] = v.strip()
    return headers

def parse_rbxh(blob: bytes) -> Dict:
    res = {
        "wrapped": False,
        "url": None,
        "headers": {},
        "header_text": None,
        "body": blob,
        "full_payload": blob,
    }
    if not blob or blob[:4] != RBXH_MAGIC:
        return res

    res["wrapped"] = True
    data = blob[4:]
    res["full_payload"] = data

    if len(data) >= 8:
        ver, hlen = struct.unpack("<II", data[:8])
        if 0 <= hlen <= len(data) - 8 and 0 <= ver <= 16:
            hdr_bytes = data[8: 8 + hlen]
            body = data[8 + hlen:]
            header_text = hdr_bytes.decode("utf-8", "replace")
            res["header_text"] = header_text
            res["headers"] = _parse_header_lines(header_text)
            m = re.search(r"(https?://\S+)", header_text or "")
            if m:
                res["url"] = m.group(1).rstrip("')\",;]")
            res["body"] = body
            return res

    res["body"] = data
    return res

def _maybe_gunzip(b: bytes, headers: Dict[str, str]) -> bytes:
    enc = (headers.get("content-encoding") or headers.get("content_encoding") or "").lower()
    if "gzip" in enc:
        try:
            return gzip.decompress(b)
        except Exception:
            return b
    if len(b) >= 3 and b[:3] == b"\x1f\x8b\x08":
        try:
            return gzip.decompress(b)
        except Exception:
            return b
    return b

def _content_type(headers: Dict[str, str]) -> str:
    ct = (headers.get("content-type") or headers.get("content_type") or "").lower()
    return ct.split(";")[0].strip()

_ticket_url_re = re.compile(rb"https?://([A-Za-z0-9\.\-]+)\S+", re.IGNORECASE)

def detect_ticket(payload: bytes, url: Optional[str]) -> Tuple[bool, str]:
    if url and "rbxcdn.com" in url and any(k in url for k in ("__token_", "signature", "key-pair-id", "policy", "expires")):
        return True, "Ticket (signed URL)"
    n = len(payload)
    if 100 <= n <= 4096:
        if b"rbxcdn.com" in payload and any(k in payload.lower() for k in (b"key-pair-id", b"signature", b"policy", b"__token_", b"expires")):
            host = "rbxcdn"
            m = _ticket_url_re.search(payload)
            if m:
                try:
                    host = m.group(1).decode("ascii", "ignore")
                except Exception:
                    pass
            return True, f"Ticket ({host})"
    return False, ""

def find_embedded_image(body: bytes) -> Tuple[str, int]:
    scan = body[:131072]
    i = scan.find(b"RIFF")
    while i != -1 and i + 12 <= len(scan):
        if scan[i + 8: i + 12] == b"WEBP":
            return "WEBP", i
        i = scan.find(b"RIFF", i + 1)
    sigs = [
        (b"\x89PNG\r\n\x1a\n", "PNG"),
        (b"\xff\xd8\xff", "JPEG"),
        (b"GIF8", "GIF"),
        (b"DDS ", "DDS"),
        (b"BM", "BMP"),
    ]
    for sig, lbl in sigs:
        j = scan.find(sig)
        if j != -1:
            return lbl, j
    return "", -1

def _is_ogg_at(scan: bytes, j: int) -> bool:
    if j < 0 or j + 27 > len(scan):
        return False
    if scan[j: j + 4] != b"OggS":
        return False
    if scan[j + 4] != 0:
        return False
    tail = scan[j: j + 4096]
    return (b"vorbis" in tail) or (b"OpusHead" in tail)

_BITRATES = {
    (3, 3): [0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 0],
    (3, 2): [0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384, 0],
    (3, 1): [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0],
    (2, 3): [0, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256, 0],
    (2, 2): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0],
    (2, 1): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0],
    (0, 3): [0, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256, 0],
    (0, 2): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0],
    (0, 1): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0],
}
_SAMPLERATES = {
    3: [44100, 48000, 32000, 0],
    2: [22050, 24000, 16000, 0],
    0: [11025, 12000, 8000, 0],
}

def _read_u32_be(b: bytes, i: int) -> int:
    return (b[i] << 24) | (b[i + 1] << 16) | (b[i + 2] << 8) | (b[i + 3] << 0)

def _is_valid_mp3_header(h: int) -> Tuple[bool, dict]:
    if ((h >> 21) & 0x7FF) != 0x7FF:
        return False, {}
    ver = (h >> 19) & 0x3
    layer = (h >> 17) & 0x3
    br_ix = (h >> 12) & 0xF
    sr_ix = (h >> 10) & 0x3
    pad = (h >> 9) & 0x1
    if ver == 1 or layer == 0:
        return False, {}
    if sr_ix == 3 or br_ix == 0 or br_ix == 0xF:
        return False, {}
    sr = _SAMPLERATES.get(ver, [0, 0, 0, 0])[sr_ix]
    br = _BITRATES.get((ver, layer), [0] * 16)[br_ix] * 1000
    if sr == 0 or br == 0:
        return False, {}
    return True, {"ver": ver, "layer": layer, "sr": sr, "br": br, "pad": pad}

def _mp3_frame_size(info: dict) -> int:
    ver = info["ver"]
    layer = info["layer"]
    br = info["br"]
    sr = info["sr"]
    pad = info["pad"]
    if layer == 3:
        return int((12 * br / sr + pad) * 4)
    coef = 144 if ver == 3 else 72
    return int(coef * br / sr + pad)

def _find_mp3_two_frames(scan: bytes) -> int:
    n = min(len(scan), 131072)
    i = 0
    while i + 4 <= n:
        h = _read_u32_be(scan, i)
        ok, info = _is_valid_mp3_header(h)
        if not ok:
            i += 1
            continue
        sz = _mp3_frame_size(info)
        if sz < 24 or i + sz + 4 > n:
            i += 1
            continue
        j = i + sz
        h2 = _read_u32_be(scan, j)
        ok2, info2 = _is_valid_mp3_header(h2)
        if ok2 and info2["sr"] == info["sr"] and info2["layer"] == info["layer"]:
            return i
        i += 1
    return -1

def find_embedded_audio_robust(body: bytes) -> Tuple[str, int]:
    scan = body[:131072]
    i = scan.find(b"RIFF")
    while i != -1 and i + 12 <= len(scan):
        if scan[i + 8: i + 12] == b"WAVE":
            return "WAV", i
        i = scan.find(b"RIFF", i + 1)
    j = scan.find(b"OggS")
    if j != -1 and _is_ogg_at(scan, j):
        return "OGG", j
    off = _find_mp3_two_frames(scan)
    if off != -1:
        return "MP3", off
    return "", -1

KTX1_MAGIC = b"\xabKTX 11\xbb\r\n\x1a\n"
KTX2_MAGIC = b"\xabKTX 20\xbb\r\n\x1a\n"

def _label_ktx1(body: bytes, off: int) -> str:
    if off + 64 > len(body):
        return "KTX1"
    end = struct.unpack("<I", body[off + 12: off + 16])[0]
    gl_internal = struct.unpack("<I", body[off + 28: off + 32])[0] if end == 0x04030201 else 0
    dxt_vals = {0x83F0, 0x83F1, 0x83F2, 0x83F3, 0x86B0, 0x86B1}
    astc_min, astc_max = 0x93B0, 0x93FF
    if gl_internal in dxt_vals:
        return "KTX1 (BCn)"
    if astc_min <= gl_internal <= astc_max:
        return "KTX1 (ASTC)"
    return "KTX1"

def _label_ktx2(body: bytes, off: int) -> str:
    if off + 48 > len(body):
        return "KTX2"
    vkfmt = struct.unpack("<I", body[off + 12: off + 16])[0]
    bcn = {131, 132, 133, 134, 135, 137, 146}
    astc = set(range(166, 183))
    if vkfmt in bcn:
        return "KTX2 (BCn)"
    if vkfmt in astc:
        return "KTX2 (ASTC)"
    return "KTX2"

def detect_ktx_anywhere(body: bytes) -> Tuple[str, str]:
    scan = body[:131072]
    i1 = scan.find(KTX1_MAGIC)
    if i1 != -1:
        return "Texture", _label_ktx1(body, i1)
    i2 = scan.find(KTX2_MAGIC)
    if i2 != -1:
        return "Texture", _label_ktx2(body, i2)
    return "", ""

def detect_mesh_kind(payload: bytes) -> Tuple[str, str]:
    if payload.startswith(b"version "):
        try:
            first = payload.split(b"\n", 1)[0].decode("ascii", "ignore")
            m = re.search(r"version\s+(\d+)", first)
            if m:
                v = int(m.group(1))
                if 1 <= v <= 5:
                    return "Mesh", f"v{v} (ASCII)"
                if v >= 6:
                    return "Mesh", f"v{v}"
        except Exception:
            return "Mesh", "ASCII"
        return "Mesh", "ASCII"
    if b"DRACO" in payload[:4096] or b"MESH" in payload[:16]:
        return "Mesh", "v6/v7 (binary)"
    return "", ""

def detect_font_kind(body: bytes, ct: str) -> Tuple[str, str]:
    if ct.startswith("font/") or ct in (
        "application/font-sfnt",
        "application/font-woff",
        "application/font-woff2",
    ):
        if "woff2" in ct:
            return "Font", "WOFF2"
        if "woff" in ct:
            return "Font", "WOFF"
        if "otf" in ct:
            return "Font", "OTF"
        if "ttf" in ct:
            return "Font", "TTF"
    if body[:4] == b"OTTO":
        return "Font", "OTF"
    if body[:4] == b"ttcf":
        return "Font", "TTC"
    if body[:4] == b"wOFF":
        return "Font", "WOFF"
    if body[:4] == b"wOF2":
        return "Font", "WOFF2"
    if body[:4] == b"\x00\x01\x00\x00":
        return "Font", "TTF"
    return "", ""

def _find_json_head_slice(body: bytes, headers: Dict[str, str]) -> Optional[str]:
    scan = body[:262144]
    i = scan.find(b"{")
    if i != -1:
        try:
            return scan[i: i + 8192].decode("utf-8", "ignore")
        except Exception:
            pass
    body_unz = _maybe_gunzip(body, headers)
    if body_unz is not body:
        scan2 = body_unz[:262144]
        j = scan2.find(b"{")
        if j != -1:
            try:
                return scan2[j: j + 8192].decode("utf-8", "ignore")
            except Exception:
                pass
    return None

def is_translation_json_text(text: str) -> bool:
    t = text.lower()
    if "localizationtable" in t:
        return True
    hits = 0
    for key in ("translationmapping", '"entries"', '"translations"'):
        if key in t:
            hits += 1
    if hits >= 1 and ('"locale"' in t or "language" in t or "sourcelanguage" in t):
        return True
    return False

def detect_translation_json(body: bytes, headers: Dict[str, str]) -> Tuple[bool, str]:
    head = _find_json_head_slice(body, headers)
    if not head:
        return False, ""
    if head.lstrip().startswith("{") and is_translation_json_text(head):
        return True, "JSON"
    return False, ""

_RBXM_BIN_MAGIC = b"<roblox!"
_RBXM_SCAN_LIMIT = 8192

def detect_rbxm_binary(body: bytes) -> int:
    window = body[:_RBXM_SCAN_LIMIT]
    p = window.find(_RBXM_BIN_MAGIC)
    if p != -1 and p <= 64:
        return p
    return -1

def _instance_property_value(instance, name: str):
    
    try:
        value = instance.properties.get(name)
    except Exception:
        return None
    if hasattr(value, "value"):
        value = value.value
    return value

def _walk_instance_tree(instances) -> list:
    
    roots = list(instances.values()) if isinstance(instances, dict) else list(instances or [])
    out = []
    seen = set()

    def visit(node):
        key = id(node)
        if key in seen:
            return
        seen.add(key)
        out.append(node)
        for child in getattr(node, "children", ()) or ():
            visit(child)

    for node in roots:
        visit(node)
    return out

def _has_animation_structure(nodes) -> bool:
    
    classes = {getattr(node, "class_name", "") for node in nodes}
    if classes & {"KeyframeSequence", "CurveAnimation", "AnimationClip"}:
        return True
    
    for node in nodes:
        if getattr(node, "class_name", "") != "Keyframe":
            continue
        stack = list(getattr(node, "children", ()) or ())
        while stack:
            child = stack.pop()
            if getattr(child, "class_name", "") in {"Pose", "NumberPose"}:
                return True
            stack.extend(getattr(child, "children", ()) or ())
    return False

def _classify_rbxm_asset(body: bytes):
    
    _MODEL_CLASSES = {
        "Model", "Folder", "Tool", "Accessory", "Accoutrement", "Handle", "Part", "MeshPart",
        "WedgePart", "CornerWedgePart", "TrussPart", "CylinderPart", "UnionOperation",
        "PartOperation", "SpecialMesh", "FileMesh", "BasePart", "Humanoid", "Motor6D",
        "Texture", "Decal",
    }
    try:
        try:
            raw = _decompress_document(body)
        except Exception:
            raw = body
        if raw.lstrip().startswith(b"<roblox!"):
            
            insts = {}
            try:
                insts = parse_rbxm(raw)
            except Exception:
                insts = {}
            nodes = _walk_instance_tree(insts)
            class_names = {getattr(i, "class_name", "") for i in nodes}
            if _has_animation_structure(nodes):
                return "RBXM", "Animation"
            if _RbxmDeserializer is not None:
                try:
                    doc = _RbxmDeserializer().deserialize(raw)
                except Exception:
                    doc = None
                if doc is not None:
                    nodes = _walk_instance_tree(getattr(doc, "roots", None) or doc.instances)
                    class_names = {getattr(i, "class_name", "") for i in nodes}
                    if _has_animation_structure(nodes):
                        return "RBXM", "Animation"
                    if "DataModel" in class_names:
                        return "rbxl (place)", "RBXL (place)"
                    if class_names & _MODEL_CLASSES:
                        return "RBXM", "Model"
            
            if prop_names & _RIG_NAMES:
                return "Animation", "RBXM (bin)"
            return "RBXM", ""
        elif b"<roblox" in raw[:4096]:
            
            text = raw[:262144].decode("utf-8", "replace")
            low = text.lower()
            if re.search(r'class\s*=\s*"(Keyframe|CurveAnimation|KeyframeSequence|AnimationClip|Pose|NumberPose)"', text, re.I):
                return "Animation", "KeyframeSequence"
            if re.search(r'class\s*=\s*"DataModel"', text, re.I):
                return "rbxl (place)", "RBXL/XML"
            if re.search(r'class\s*=\s*"(Part|MeshPart|WedgePart|CylinderPart|SpecialMesh|BasePart|Tool|Model)"', text, re.I):
                return "Model", "RBXMX/XML"
            if b"<roblox" in low and not (b"properties" in low):
                return "Model", "RBXMX/XML"
    except Exception:
        return None, None
    return None, None

def _extract_rbxm_name(body: bytes) -> str:
    
    try:
        if body.lstrip().startswith(b"<roblox!"):
            
            instances = parse_rbxm(body)
            for node in instances.values():
                if node.class_name in ("AnimationClip", "CurveAnimation", "KeyframeSequence", "Model", "Folder", "Part"):
                    nm = node.properties.get("Name")
                    if isinstance(nm, str) and nm.strip():
                        return nm.strip()
            for node in instances.values():
                nm = node.properties.get("Name")
                if isinstance(nm, str) and nm.strip():
                    return nm.strip()
        elif b"<roblox" in body[:4096]:
            text = body[:262144].decode("utf-8", "ignore")
            m = re.search(r'<string name="Name">([^<]{1,120})</string>', text)
            if m and m.group(1).strip():
                return m.group(1).strip()
    except Exception:
        pass
    return ""

def _asset_name(body: bytes, url: Optional[str]) -> str:
    name = _extract_rbxm_name(body)
    if name:
        return name
    if url:
        tail = os.path.basename(urlparse(url).path).strip()
        if tail and "." not in tail and len(tail) < 120:
            return tail
    return ""

def sniff_kind(body: bytes, url: Optional[str], headers: Dict[str, str], full_payload: bytes) -> Tuple[str, str, bool]:
    
    is_t, ticket_label = detect_ticket(full_payload or body, url)
    if is_t:
        return "Ticket", ticket_label, True

    is_tr, tr_label = detect_translation_json(body, headers)
    if is_tr:
        return "Translations", tr_label, False

    def _is_decal_url(u: Optional[str]) -> bool:
        if not u:
            return False
        ul = u.lower()
        return ("tr.rbxcdn.com" in ul) or ("/image/" in ul) or ("/thumbnail/" in ul)

    k_cat, k_lbl = detect_ktx_anywhere(body)
    if k_cat:
        return k_cat, k_lbl, False

    if detect_rbxm_binary(body) != -1:
        try:
            kind = _classify_document(_decompress_document(body))
            rcat, rlbl = _classify_rbxm_asset(body)
            if rcat:
                return rcat, rlbl, False
            if kind and ("anim" in kind.lower() or "rbxl" not in kind.lower()):
                if any(k in body[:521].lower() for k in (b"keyframesequence", b"animationclip", b"curveanimation", b"pose")):
                    return "Animation", "RBXM (bin)", False
        except Exception:
            pass
        return "RBXM", "", False

    low = (body[:131072]).lower()
    if b"<roblox" in low:
        rcat, rlbl = _classify_rbxm_asset(body)
        if rcat:
            return rcat, rlbl, False
        if b"keyframesequence" in low or b"animationclip" in low:
            return "Animation", "KeyframeSequence", False
        return "Model", "RBXMX/XML", False

    m_cat, m_lbl = detect_mesh_kind(body)
    if m_cat:
        return m_cat, m_lbl, False

    ct = _content_type(headers)
    f_cat, f_lbl = detect_font_kind(body, ct)
    if f_cat:
        return f_cat, f_lbl, False

    if body[:8] == b"\x89PNG\r\n\x1a\n":
        return ("Decal" if _is_decal_url(url) else "Image"), "PNG", False
    if body[:3] == b"GIF":
        return ("Decal" if _is_decal_url(url) else "Image"), "GIF", False
    if body[:2] == b"\xff\xd8":
        return ("Decal" if _is_decal_url(url) else "Image"), "JPEG", False
    if len(body) >= 12 and body[:4] == b"RIFF" and body[8:12] == b"WEBP":
        return ("Decal" if _is_decal_url(url) else "Image"), "WEBP", False
    img_lbl, _ = find_embedded_image(body)
    if img_lbl:
        return ("Decal" if _is_decal_url(url) else "Image"), img_lbl, False

    if body[:4] == b"\x1a\x45\xdf\xa3":
        return "Video", "WebM", False
    if len(body) >= 12 and body[4:8] == b"ftyp":
        return "Video", "MP4", False
    text_head = (body[:8192]).decode("utf-8", "ignore").lstrip().lower()
    if text_head.startswith("#extm3u"):
        return "Video", "M3U", False

    if body[:3] == b"ID3":
        return "Sound", "MP3", False
    if len(body) >= 12 and body[:4] == b"RIFF" and body[8:12] == b"WAVE":
        return "Sound", "WAV", False
    if _is_ogg_at(body, 0):
        return "Sound", "OGG", False
    aud_lbl, _ = find_embedded_audio_robust(body)
    if aud_lbl:
        return "Sound", aud_lbl, False

    ct = _content_type(headers)
    if ct.startswith("image/"):
        return ("Decal" if _is_decal_url(url) else "Image"), ct.split("/", 1)[1].upper(), False
    if ct.startswith("audio/"):
        return "Sound", "MP3" if ct.endswith("mpeg") else ct.split("/", 1)[1].upper(), False
    if ct in ("application/ktx", "image/ktx", "image/ktx2"):
        return "Texture", "KTX2" if "ktx2" in ct else "KTX1", False
    if ct in ("application/json", "text/json", "application/ld+json"):
        if is_translation_json_text(text_head):
            return "Translations", "JSON", False
        return "Text", "JSON", False
    if ct in ("application/xml", "text/xml"):
        if text_head.startswith("<roblox"):
            rcat, rlbl = _classify_rbxm_asset(body)
            if rcat:
                return rcat, rlbl, False
            return "Model", "RBXMX/XML", False
        return "Text", "XML", False
    if ct.startswith("font/"):
        return "Font", ct.split("/", 1)[1].upper(), False

    if text_head.startswith("{") or text_head.startswith("["):
        if is_translation_json_text(text_head):
            return "Translations", "JSON", False
        return "Text", "JSON", False
    if text_head.startswith("<roblox"):
        rcat, rlbl = _classify_rbxm_asset(body)
        if rcat:
            return rcat, rlbl, False
        if "keyframesequence" in text_head or "animationclip" in text_head:
            return "Animation", "KeyframeSequence", False
        return "Model", "RBXMX/XML", False
    if text_head.startswith("<"):
        return "Text", "XML/HTML", False

    if url:
        u = urlparse(url)
        q = parse_qs(u.query or "")
        atype = (q.get("type") or q.get("assetType") or q.get("assettype") or [""])[0].lower()
        if atype == "animation":
            return "Animation", "Asset", False
        if atype == "mesh":
            return "Mesh", "Asset", False
        tail = (u.path or "").lower()
        if tail.endswith(".mesh"):
            return "Mesh", "Asset", False
        if any(tail.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".dds")):
            return ("Decal" if ("tr.rbxcdn.com" in u.netloc or "/image/" in tail or "/thumbnail/" in tail) else "Image"), tail.split(".")[-1].upper(), False
        if any(tail.endswith(ext) for ext in (".ogg", ".mp3", ".wav")):
            return "Sound", tail.split(".")[-1].upper(), False
        if tail.endswith(".ktx") or tail.endswith(".ktx2"):
            return "Texture", "KTX2" if tail.endswith("ktx2") else "KTX1", False
        if any(tail.endswith(ext) for ext in (".ttf", ".otf", ".ttc", ".woff", ".woff2")):
            return "Font", tail.split(".")[-1].upper(), False

    if body[:4] == b"\x28\xb5\x2f\xfd":
        return "Compressed", "ZSTD", False
    if body[:4] == b"\x04\x22\x4d\x18":
        return "Compressed", "LZ4F", False

    return "Unknown", "", False

def connect_ro(db_path: str) -> sqlite3.Connection:
    uri = f"file:{db_path}?mode=ro&cache=shared"
    return sqlite3.connect(uri, uri=True, timeout=0.5, isolation_level=None)

def connect_rw(db_path: str) -> sqlite3.Connection:
    uri = f"file:{db_path}?mode=rwc&cache=shared"
    return sqlite3.connect(uri, uri=True, timeout=5.0, isolation_level=None)

@dataclass
class ScanItem:
    time: str
    hash: str
    size: int
    kind: str
    src: str
    url: str
    wrapped: bool
    header_text: Optional[str]
    content_type: str
    is_ticket: bool
    name: str = ""
    id_bytes: bytes = field(repr=False, default=b"")

def scan_db_once(db_path: str, shard_root: str, seen: set, max_rows: Optional[int] = None) -> List[ScanItem]:
    out: List[ScanItem] = []
    try:
        conn = connect_ro(db_path)
    except Exception:
        return out

    try:
        cur = conn.cursor()
        cur.execute("SELECT id, content FROM files")
        cnt = 0
        for row in cur:
            cnt += 1
            if max_rows and cnt > max_rows:
                break

            id_b, content = row
            h = id_bytes_to_hex(id_b)
            if h in seen:
                continue

            blob = content if content is not None else read_shard_bytes(shard_root, h)
            if not blob:
                continue

            meta = parse_rbxh(blob)
            url = meta.get("url")
            body = meta.get("body") or b""
            headers = meta.get("headers") or {}
            full_payload = meta.get("full_payload") or body

            cat, lbl, is_ticket = sniff_kind(body, url, headers, full_payload)
            size = len(body)
            name = _asset_name(body, url)

            item = ScanItem(
                time=now_hms(),
                hash=h,
                size=size,
                kind=f"{cat}{' ('+lbl+')' if lbl else ''}",
                src=("inline" if content is not None else "shard"),
                url=url or "-",
                wrapped=bool(meta.get("wrapped", False)),
                header_text=meta.get("header_text"),
                content_type=_content_type(headers),
                is_ticket=is_ticket,
                name=name,
                id_bytes=id_b,
            )
            out.append(item)
            seen.add(h)
    except sqlite3.OperationalError:
        pass
    except Exception:
        pass
    finally:
        try:
            conn.close()
        except Exception:
            pass

    return out

@dataclass
class Keyframe:
    time: float
    pose_by_part_name: Dict[str, Dict]

def parse_xml_animation(anim_data: bytes) -> List[Keyframe]:
    try:
        anim_data = _decompress_document(anim_data)
        text = anim_data.decode('utf-8-sig', errors='replace')
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
        root = ET.fromstring(text)
    except Exception:
        return []

    keys: List[Keyframe] = []
    for item in root.iter('Item'):
        if item.attrib.get('class') != 'Keyframe':
            continue
        props = item.find('Properties')
        if props is None:
            continue
        t_elem = props.find("float[@name='Time']")
        t = float(t_elem.text if t_elem is not None and t_elem.text else '0')
        poses: Dict[str, Dict] = {}
        for pose_item in item.iter('Item'):
            if pose_item.attrib.get('class') != 'Pose':
                continue
            pprops = pose_item.find('Properties')
            if pprops is None:
                continue
            pname_elem = pprops.find("string[@name='Name']")
            cf_elem = pprops.find("CoordinateFrame[@name='CFrame']") or pprops.find("CFrame[@name='CFrame']")
            if pname_elem is None or cf_elem is None:
                continue
            pname = pname_elem.text or ""
            cf_d = {}
            for comp in cf_elem:
                cf_d[comp.tag] = comp.text
            pos = _cf_position(cf_d)
            poses[pname] = {"pos": pos, "cf": cf_d}
        keys.append(Keyframe(t, poses))

    keys.sort(key=lambda k: k.time)
    return keys

def _safe_number(value, default=0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

def parse_binary_animation(data: bytes) -> List[Keyframe]:
    data = _decompress_document(data)
    instances = {}
    try:
        instances = parse_rbxm(data)
    except Exception:
        instances = {}

    def _collect_poses(node, out):
        for child in node.children:
            if child.class_name in ("Pose", "NumberPose"):
                name = child.properties.get("Name")
                cf = child.properties.get("CFrame")
                pos = _cf_position(cf)
                if name:
                    out[name] = {"pos": pos, "cf": cf}
            _collect_poses(child, out)

    keyframes: List[Keyframe] = []
    for kf in sorted(
        (i for i in instances.values() if i.class_name == "Keyframe"),
        key=lambda i: _safe_number(i.properties.get("Time", 0.0)),
    ):
        poses: Dict[str, Dict] = {}
        _collect_poses(kf, poses)
        cf = kf.properties.get("CFrame")
        if not poses:
            poses["__frame__"] = {"pos": _cf_position(cf), "cf": cf}
        keyframes.append(Keyframe(_safe_number(kf.properties.get("Time", 0.0)), poses))

    if not keyframes and _RbxmDeserializer is not None:
        def _props(d: dict) -> dict:
            out = {}
            for k, v in d.items():
                nm = k.name if hasattr(k, "name") else str(k)
                out[nm] = v.value if hasattr(v, "value") else v
            return out

        def _collect(node, out: dict):
            for child in node.children:
                if child.class_name in ("Pose", "NumberPose"):
                    p = _props(child.properties)
                    name = p.get("Name")
                    if name:
                        out[name] = {"pos": _cf_position(p.get("CFrame")), "cf": p.get("CFrame")}
                _collect(child, out)

        try:
            doc = _RbxmDeserializer().deserialize(data)
        except Exception:
            doc = None
        if doc is not None:
            for kf in sorted(
                (i for i in doc.instances.values() if i.class_name == "Keyframe"),
                key=lambda i: _safe_number(_props(i.properties).get("Time", 0.0)),
            ):
                p = _props(kf.properties)
                poses: Dict[str, Dict] = {}
                _collect(kf, poses)
                if not poses:
                    poses["__frame__"] = {"pos": _cf_position(p.get("CFrame")), "cf": p.get("CFrame")}
                keyframes.append(Keyframe(_safe_number(p.get("Time", 0.0)), poses))
            keyframes.sort(key=lambda k: k.time)
    return keyframes

def parse_animation(data: bytes) -> List[Keyframe]:
    if not data:
        return []
    try:
        if b"CurveAnimation" in data:
            keys = parse_curve_animation(data)
            if keys:
                return keys
    except Exception:
        pass
    raw = data
    try:
        raw = _decompress_document(raw)
    except Exception:
        pass
    stripped = raw.lstrip(b"\xef\xbb\xbf \t\r\n")
    if stripped.startswith(b"<roblox!"):
        try:
            keys = parse_binary_animation(stripped)
            if keys:
                return keys
        except Exception:
            pass
        try:
            keys = parse_xml_animation(_normalize_roblox_document(stripped))
            if keys:
                return keys
        except Exception:
            pass
    return parse_xml_animation(stripped)

def parse_curve_animation(anim_data: bytes) -> List[Keyframe]:
    
    import base64 as _b64
    import struct as _struct

    TICKS = 14400.0
    bone_curves: Dict[str, dict] = {}

    def _empty_bc():
        return {"px": [], "py": [], "pz": [], "rx": [], "ry": [], "rz": []}

    def _vat(raw_b: bytes):
        if len(raw_b) < 8:
            return []
        _, n = _struct.unpack_from("<II", raw_b)
        if not n:
            return []
        off_t = 8 + n * 14
        if off_t + 8 + n * 4 > len(raw_b):
            return []
        _, sn = _struct.unpack_from("<II", raw_b, off_t)
        out = []
        for i in range(min(n, sn)):
            v = _struct.unpack_from("<f", raw_b, 8 + i * 14 + 2)[0]
            tk = _struct.unpack_from("<I", raw_b, off_t + 8 + i * 4)[0]
            out.append((tk / TICKS, v))
        return out

    def _lerp(tv, t):
        if not tv:
            return 0.0
        if t <= tv[0][0]:
            return tv[0][1]
        if t >= tv[-1][0]:
            return tv[-1][1]
        for i in range(len(tv) - 1):
            t0, v0 = tv[i]
            t1, v1 = tv[i + 1]
            if t0 <= t <= t1:
                f = (t - t0) / (t1 - t0) if t1 > t0 else 0.0
                return v0 + f * (v1 - v0)
        return tv[-1][1]

    if anim_data.lstrip().startswith(b"<roblox!"):
        try:
            if _RbxmDeserializer is None:
                return []
            tree = _RbxmDeserializer().deserialize(_decompress_document(anim_data))
        except Exception:
            return []

        def _prop(inst, key):
            for k, v in inst.properties.items():
                pk = k.name if hasattr(k, "name") else str(k)
                if pk == key:
                    return v.value if hasattr(v, "value") else v
            return None

        def _vat_rbxm(inst):
            for k, v in inst.properties.items():
                pk = k.name if hasattr(k, "name") else str(k)
                if pk == "ValuesAndTimes":
                    raw = v.value if hasattr(v, "value") else v
                    if raw:
                        rb = raw.encode("latin-1") if isinstance(raw, str) else bytes(raw)
                        return _vat(rb)
            return []

        def _walk_rbxm(inst):
            nonlocal bone_curves
            if inst.class_name == "Folder":
                name = _prop(inst, "Name") or ""
                if name:
                    bc = _empty_bc()
                    for child in inst.children:
                        ccls = child.class_name
                        if ccls == "Vector3Curve":
                            for fc in child.children:
                                if fc.class_name != "FloatCurve":
                                    continue
                                axis = (_prop(fc, "Name") or "").upper()
                                tv = _vat_rbxm(fc)
                                if axis == "X":
                                    bc["px"] = tv
                                elif axis == "Y":
                                    bc["py"] = tv
                                elif axis == "Z":
                                    bc["pz"] = tv
                        elif ccls == "EulerRotationCurve":
                            for fc in child.children:
                                if fc.class_name != "FloatCurve":
                                    continue
                                axis = (_prop(fc, "Name") or "").upper()
                                tv = _vat_rbxm(fc)
                                if axis == "X":
                                    bc["rx"] = tv
                                elif axis == "Y":
                                    bc["ry"] = tv
                                elif axis == "Z":
                                    bc["rz"] = tv
                        elif ccls == "Folder":
                            _walk_rbxm(child)
                    if any(bc[k] for k in bc):
                        bone_curves[name] = bc
            elif inst.class_name == "CurveAnimation":
                for child in inst.children:
                    _walk_rbxm(child)

        for root_inst in getattr(tree, "roots", []):
            _walk_rbxm(root_inst)

    else:
        try:
            text = anim_data.decode("utf-8-sig", errors="replace")
            text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
            root = ET.fromstring(text)
        except Exception:
            return []

        def _vat_xml(fc_item):
            for bs in fc_item.iter("BinaryString"):
                if bs.get("name") == "ValuesAndTimes" and bs.text:
                    try:
                        return _vat(_b64.b64decode(bs.text.strip()))
                    except Exception:
                        pass
            return []

        def _walk_xml(item):
            nonlocal bone_curves
            cls = item.get("class", "")
            if cls == "Folder":
                props = item.find("Properties")
                name = ""
                if props is not None:
                    ne = props.find("string[@name='Name']")
                    if ne is not None:
                        name = ne.text or ""
                if name:
                    bc = _empty_bc()
                    for child in item:
                        ccls = child.get("class", "")
                        if ccls == "Vector3Curve":
                            for fc in child:
                                if fc.get("class") != "FloatCurve":
                                    continue
                                fcp = fc.find("Properties")
                                if fcp is None:
                                    continue
                                ae = fcp.find("string[@name='Name']")
                                axis = (ae.text or "").upper() if ae is not None else ""
                                bc[("px" if axis == "X" else "py" if axis == "Y" else "pz" if axis == "Z" else axis.lower())] = _vat_xml(fc)
                        elif ccls == "EulerRotationCurve":
                            for fc in child:
                                if fc.get("class") != "FloatCurve":
                                    continue
                                fcp = fc.find("Properties")
                                if fcp is None:
                                    continue
                                ae = fcp.find("string[@name='Name']")
                                axis = (ae.text or "").upper() if ae is not None else ""
                                bc[("rx" if axis == "X" else "ry" if axis == "Y" else "rz" if axis == "Z" else axis.lower())] = _vat_xml(fc)
                        elif ccls == "Folder":
                            _walk_xml(child)
                    if any(bc[k] for k in bc):
                        bone_curves[name] = bc
            elif cls == "CurveAnimation":
                for child in item:
                    _walk_xml(child)

        for item in root.iter("Item"):
            if item.get("class") == "CurveAnimation":
                _walk_xml(item)
                break

    if not bone_curves:
        return []

    times_set: set = set()
    for bc in bone_curves.values():
        for tv in bc.values():
            for t, _ in tv:
                times_set.add(round(t, 6))
    if not times_set:
        return []
    all_times = sorted(times_set)

    keys: List[Keyframe] = []
    for t in all_times:
        poses: Dict[str, Dict] = {}
        for name, bc in bone_curves.items():
            poses[name] = {
                "pos": (_lerp(bc["px"], t), _lerp(bc["py"], t), _lerp(bc["pz"], t)),
                "rot": (_lerp(bc["rx"], t), _lerp(bc["ry"], t), _lerp(bc["rz"], t)),
            }
        keys.append(Keyframe(t, poses))
    return keys

def _cf_position(cf) -> Tuple[float, float, float]:
    
    if isinstance(cf, dict):
        if "position" in cf:
            p = cf["position"]
            if isinstance(p, (tuple, list)) and len(p) >= 3:
                try:
                    return (float(p[0]), float(p[1]), float(p[2]))
                except Exception:
                    pass
            return (0.0, 0.0, 0.0)
        if "X" in cf and "Y" in cf and "Z" in cf:
            try:
                return (float(cf["X"]), float(cf["Y"]), float(cf["Z"]))
            except Exception:
                return (0.0, 0.0, 0.0)
    if isinstance(cf, (tuple, list)) and len(cf) >= 3:
        try:
            return (float(cf[0]), float(cf[1]), float(cf[2]))
        except Exception:
            pass
    return (0.0, 0.0, 0.0)



def _extract_document_body(data: bytes) -> bytes:
    """Extract the actual Roblox document from raw bytes or an RBXH cache blob."""
    raw = data or b""
    if raw[:4] == RBXH_MAGIC:
        meta = parse_rbxh(raw)
        raw = meta.get("body") or b""
    pos = raw.find(RBXM_MAGIC)
    if pos >= 0:
        return raw[pos:]
    pos = raw.find(b"<roblox")
    if pos >= 0:
        return raw[pos:]
    return raw


def _identity_cframe(parent):
    c=ET.SubElement(parent,"CoordinateFrame",{"name":"CFrame"})
    for tag,val in (("X","0"),("Y","0"),("Z","0"),("R00","1"),("R01","0"),("R02","0"),("R10","0"),("R11","1"),("R12","0"),("R20","0"),("R21","0"),("R22","1")):
        ET.SubElement(c,tag).text=val
    return c

def _copy_pose_properties(src, dst):
    sp=src.find("Properties") if src is not None else None
    if sp is None: return
    for tag in ("token","float"):
        for el in sp.findall(tag):
            if el.get("name") in ("EasingDirection","EasingStyle","Weight"):
                ET.SubElement(dst,tag,{"name":el.get("name")}).text=el.text

def _pose_cf(src):
    if src is None: return None
    sp=src.find("Properties")
    if sp is None: return None
    return sp.find("CoordinateFrame[@name='CFrame']")

def _make_r15_pose(name: str, source_pose=None) -> ET.Element:
    item=ET.Element("Item",{"class":"Pose","referent":f"R15_{os.urandom(8).hex()}"})
    props=ET.SubElement(item,"Properties")
    ET.SubElement(props,"string",{"name":"Name"}).text=name
    src_cf=_pose_cf(source_pose)
    c=ET.SubElement(props,"CoordinateFrame",{"name":"CFrame"})
    if src_cf is not None:
        for ch in src_cf: ET.SubElement(c,ch.tag).text=ch.text
    else:
        for tag,val in (("X","0"),("Y","0"),("Z","0"),("R00","1"),("R01","0"),("R02","0"),("R10","0"),("R11","1"),("R12","0"),("R20","0"),("R21","0"),("R22","1")):
            ET.SubElement(c,tag).text=val
    _copy_pose_properties(source_pose,props)
    return item

def _r6_to_r15_keyframe(keyframe: ET.Element) -> int:
    """Convert an R6 Keyframe to a playable R15 hierarchy.

    The important part is not merely renaming Pose objects: Roblox evaluates
    Pose CFrames relative to their Motor6D/joint.  We therefore keep the R6
    transform on the corresponding R15 *upper* segment and explicitly create
    the intermediate R15 segments with identity transforms.  This preserves
    the R6 motion while producing the complete R15 Pose tree expected by the
    KeyframeSequence player.
    """
    poses={}
    def walk(parent):
        for child in list(parent):
            if child.get("class")=="Pose":
                props=child.find("Properties")
                n=props.find("string[@name='Name']") if props is not None else None
                if n is not None: poses[(n.text or "").strip()]=child
                walk(child)
    walk(keyframe)

    extras=[c for c in list(keyframe) if c.get("class")!="Pose"]
    for c in list(keyframe): keyframe.remove(c)

    def src(*names):
        for n in names:
            if n in poses: return poses[n]
        return None

    hrp=_make_r15_pose("HumanoidRootPart",src("HumanoidRootPart","RootJoint","Root"))
    lower=_make_r15_pose("LowerTorso",None)
    upper=_make_r15_pose("UpperTorso",src("Torso"))
    lower.append(upper)
    upper.append(_make_r15_pose("Head",src("Head")))

    for side in ("Left","Right"):
        arm=src(f"{side} Arm",f"{side}Arm")
        ua=_make_r15_pose(f"{side}UpperArm",arm)
        la=_make_r15_pose(f"{side}LowerArm",None)
        hand=_make_r15_pose(f"{side}Hand",None)
        la.append(hand); ua.append(la); upper.append(ua)

        leg=src(f"{side} Leg",f"{side}Leg")
        ul=_make_r15_pose(f"{side}UpperLeg",leg)
        ll=_make_r15_pose(f"{side}LowerLeg",None)
        foot=_make_r15_pose(f"{side}Foot",None)
        ll.append(foot); ul.append(ll); lower.append(ul)

    hrp.append(lower)
    keyframe.append(hrp)
    for c in extras: keyframe.append(c)
    return len(poses)

def _normalize_roblox_document(data: bytes) -> bytes:
    """Normalize XML, binary RBXM, or RBXH-wrapped Roblox documents."""
    raw=data or b""
    if raw[:4]==RBXH_MAGIC:
        raw=(parse_rbxh(raw).get("body") or b"")
    pos=raw.find(RBXM_MAGIC)
    if pos>=0:
        raw=raw[pos:]
    else:
        pos=raw.find(b"<roblox")
        if pos>=0: raw=raw[pos:]
    raw=raw.lstrip(b"\xef\xbb\xbf \t\r\n")
    if raw.startswith(RBXM_MAGIC):
        if _RbxmDeserializer is None: raise RuntimeError("RBXM deserializer is unavailable.")
        return write_rbxmx(_RbxmDeserializer().deserialize(raw))
    return raw


R6_TO_R15_POSE_MAP = {
    "Torso": "UpperTorso", "Left Arm": "LeftUpperArm", "Right Arm": "RightUpperArm",
    "Left Leg": "LeftUpperLeg", "Right Leg": "RightUpperLeg",
    "LeftArm": "LeftUpperArm", "RightArm": "RightUpperArm",
    "LeftLeg": "LeftUpperLeg", "RightLeg": "RightUpperLeg",
    "RootJoint": "Root", "Root": "Root", "HumanoidRootPart": "HumanoidRootPart", "Head": "Head",
}

def convert_r6_animation_to_r15(data: bytes) -> bytes:
    """Convert an R6 KeyframeSequence to a Roblox-valid R15 KeyframeSequence RBXMX.

    Important: the previous implementation inserted a custom <Meta> node at the
    root and treated the R6 CFrame as if it could simply be copied to an R15
    Pose.  Roblox's RBXMX schema does not accept that extra node, and the
    R6->R15 mapping needs to preserve the actual Pose hierarchy.
    """
    raw = _normalize_roblox_document(data)
    text = raw.decode("utf-8-sig", errors="replace")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    root = ET.fromstring(text)

    keyframes = [x for x in root.iter("Item") if x.get("class") == "Keyframe"]
    if not keyframes:
        raise ValueError("No Keyframe data found in the selected animation.")

    for m in list(root):
        if m.tag == "Meta" and m.get("name") == "RoutilsR6ToR15":
            root.remove(m)

    def get_name(pose):
        props = pose.find("Properties")
        e = props.find("string[@name='Name']") if props is not None else None
        return (e.text or "").strip() if e is not None else ""

    def get_cf(pose):
        props = pose.find("Properties")
        e = props.find("CoordinateFrame[@name='CFrame']") if props is not None else None
        if e is None:
            return [0.0,0.0,0.0, 1.0,0.0,0.0, 0.0,1.0,0.0, 0.0,0.0,1.0]
        vals = []
        for tag in ("X","Y","Z","R00","R01","R02","R10","R11","R12","R20","R21","R22"):
            q=e.find(tag)
            vals.append(float(q.text) if q is not None and q.text else (1.0 if tag in ("R00","R11","R22") else 0.0))
        return vals

    def easing(pose):
        props=pose.find("Properties")
        out=["0","0","1"]
        if props is not None:
            a=props.find("token[@name='EasingDirection']")
            b=props.find("token[@name='EasingStyle']")
            w=props.find("float[@name='Weight']")
            if a is not None: out[0]=a.text or "0"
            if b is not None: out[1]=b.text or "0"
            if w is not None: out[2]=w.text or "1"
        return tuple(out)

    def make_pose(name, cf, ease):
        item=ET.Element("Item", {"class":"Pose", "referent": "RBX"+uuid.uuid4().hex.upper()})
        props=ET.SubElement(item,"Properties")
        ET.SubElement(props,"string",{"name":"Name"}).text=name
        ce=ET.SubElement(props,"CoordinateFrame",{"name":"CFrame"})
        for tag,val in zip(("X","Y","Z","R00","R01","R02","R10","R11","R12","R20","R21","R22"),cf):
            ET.SubElement(ce,tag).text=f"{val:.8g}"
        ET.SubElement(props,"token",{"name":"EasingDirection"}).text=ease[0]
        ET.SubElement(props,"token",{"name":"EasingStyle"}).text=ease[1]
        ET.SubElement(props,"float",{"name":"Weight"}).text=ease[2]
        return item

    def collect(kf):
        found={}
        def walk(parent):
            for ch in parent.findall("Item"):
                if ch.get("class")=="Pose":
                    found[get_name(ch)]=(get_cf(ch),easing(ch))
                    walk(ch)
        walk(kf)
        return found

    def r6_position_to_r15(cf):
        return [cf[0], cf[2], cf[1]] + cf[3:]

    identity=[0.0,0.0,0.0, 1.0,0.0,0.0, 0.0,1.0,0.0, 0.0,0.0,1.0]

    for kf in keyframes:
        poses=collect(kf)
        extras=[c for c in list(kf) if c.get("class")!="Pose"]
        for c in list(kf):
            kf.remove(c)

        def p(name, source=None, transform_pos=False):
            if source and source in poses:
                cf,e=poses[source]
                if transform_pos:
                    cf=r6_position_to_r15(cf)
                return make_pose(name,cf,e)
            return make_pose(name,identity,("0","0","1"))

        hrp=p("HumanoidRootPart","HumanoidRootPart")
        lower=p("LowerTorso","Torso",True)
        upper=p("UpperTorso")
        hrp.append(lower)
        lower.append(upper)

        upper.append(p("Head","Head",True))

        for side in ("Left","Right"):
            ua=p(f"{side}UpperArm",f"{side} Arm",True)
            la=p(f"{side}LowerArm")
            hand=p(f"{side}Hand")
            la.append(hand); ua.append(la); upper.append(ua)

            ul=p(f"{side}UpperLeg",f"{side} Leg",True)
            ll=p(f"{side}LowerLeg")
            foot=p(f"{side}Foot")
            ll.append(foot); ul.append(ll); lower.append(ul)

        kf.append(hrp)
        for c in extras:
            kf.append(c)

    try:
        ET.indent(root, space="\t")
    except Exception:
        pass
    return b'<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(root, encoding="utf-8")


def parse_model_parts(data: bytes) -> Tuple[List[Dict], str]:
    
    parts: List[Dict] = []
    try:
        raw = _decompress_document(data)
    except Exception:
        raw = data

    def _dict_pos(d):
        if isinstance(d, dict):
            try:
                return (float(d.get("X", 0)), float(d.get("Y", 0)), float(d.get("Z", 0)))
            except Exception:
                pass
        if isinstance(d, (tuple, list)) and len(d) >= 3:
            try:
                return (float(d[0]), float(d[1]), float(d[2]))
            except Exception:
                pass
        return (1.0, 1.0, 1.0)

    def _cf_pos(cf):

        return _cf_position(cf)

    if raw.lstrip().startswith(b"<roblox!"):
        
        if _RbxmDeserializer is not None:
            try:
                doc = _RbxmDeserializer().deserialize(raw)
                for inst in doc.instances.values():
                    if inst.class_name not in ("Part", "MeshPart", "WedgePart", "CylinderPart", "CornerWedgePart", "TrussPart", "BasePart"):
                        continue
                    props = {}
                    for k, v in inst.properties.items():
                        props[k.name if hasattr(k, "name") else str(k)] = v.value if hasattr(v, "value") else v
                    cf = None
                    for key in ("CFrame", "Position"):
                        if key in props:
                            cf = props[key]
                            break
                    pos = _cf_pos(cf) if cf is not None else (0.0, 0.0, 0.0)
                    size = _dict_pos(props.get("Size", {"X": 1, "Y": 1, "Z": 1}))
                    color = "#58b6d6"
                    bc = props.get("Color", props.get("BrickColor"))
                    if isinstance(bc, dict):
                        if all(k in bc for k in ("R", "G", "B")):
                            try:
                                color = "#%02x%02x%02x" % (
                                    int(bc["R"] * 255), int(bc["G"] * 255), int(bc["B"] * 255))
                            except Exception:
                                pass
                    parts.append({
                        "name": props.get("Name") or inst.class_name,
                        "pos": pos,
                        "size": size,
                        "color": color,
                    })
            except Exception:
                parts = []
    else:
        
        try:
            text = raw.decode("utf-8-sig", errors="replace")
            text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
            root = ET.fromstring(text)
        except Exception:
            root = None
        if root is not None:
            part_classes = {"Part", "MeshPart", "WedgePart", "CylinderPart", "CornerWedgePart", "TrussPart", "BasePart"}
            for item in root.iter("Item"):
                if item.attrib.get("class") not in part_classes:
                    continue
                props = item.find("Properties")
                if props is None:
                    continue
                size = (1.0, 1.0, 1.0)
                se = props.find("Vector3[@name='Size']")
                if se is not None:
                    xe = se.find("X"); ye = se.find("Y"); ze = se.find("Z")
                    size = (
                        float(xe.text) if xe is not None and xe.text else 1.0,
                        float(ye.text) if ye is not None and ye.text else 1.0,
                        float(ze.text) if ze is not None and ze.text else 1.0,
                    )
                pos = (0.0, 0.0, 0.0)
                cfe = props.find("CoordinateFrame[@name='CFrame']")
                if cfe is not None:
                    xe = cfe.find("X"); ye = cfe.find("Y"); ze = cfe.find("Z")
                    pos = (
                        float(xe.text) if xe is not None and xe.text else 0.0,
                        float(ye.text) if ye is not None and ye.text else 0.0,
                        float(ze.text) if ze is not None and ze.text else 0.0,
                    )
                name = ""
                ne = props.find("string[@name='Name']")
                if ne is not None:
                    name = ne.text or ""
                parts.append({"name": name or item.attrib.get("class"), "pos": pos, "size": size, "color": "#58b6d6"})

    if not parts:
        return [], "Model present, but no parts found to render"
    return parts, f"Model: {len(parts)} parts"

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def quat_from_rot3(r: List[List[float]]) -> Tuple[float, float, float, float]:
    trace = r[0][0] + r[1][1] + r[2][2]
    if trace > 0.0:
        s = math.sqrt(trace + 1.0) * 2.0
        w = 0.25 * s
        x = (r[2][1] - r[1][2]) / s
        y = (r[0][2] - r[2][0]) / s
        z = (r[1][0] - r[0][1]) / s
    elif (r[0][0] > r[1][1]) and (r[0][0] > r[2][2]):
        s = math.sqrt(1.0 + r[0][0] - r[1][1] - r[2][2]) * 2.0
        w = (r[2][1] - r[1][2]) / s
        x = 0.25 * s
        y = (r[0][1] + r[1][0]) / s
        z = (r[0][2] + r[2][0]) / s
    elif r[1][1] > r[2][2]:
        s = math.sqrt(1.0 + r[1][1] - r[0][0] - r[2][2]) * 2.0
        w = (r[0][2] - r[2][0]) / s
        x = (r[0][1] + r[1][0]) / s
        y = 0.25 * s
        z = (r[1][2] + r[2][1]) / s
    else:
        s = math.sqrt(1.0 + r[2][2] - r[0][0] - r[1][1]) * 2.0
        w = (r[1][0] - r[0][1]) / s
        x = (r[0][2] + r[2][0]) / s
        y = (r[1][2] + r[2][1]) / s
        z = 0.25 * s
    n = math.sqrt(w * w + x * x + y * y + z * z) or 1.0
    return (w / n, x / n, y / n, z / n)

def rot3_from_quat(q: Tuple[float, float, float, float]) -> List[List[float]]:
    w, x, y, z = q
    xx, yy, zz = x * x, y * y, z * z
    xy, xz, yz = x * y, x * z, y * z
    wx, wy, wz = w * x, w * y, w * z
    return [
        [1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy)],
        [2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx)],
        [2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy)],
    ]

class Viewport3DPanel(ttk.Frame):
    
    def __init__(self, master, title="3D Viewport"):
        super().__init__(master)
        self.angle_x = 0.3
        self.angle_y = 0.5
        self.cam_distance = 7.0
        self.model_scale = 1.0

        self.is_playing = False
        self.anim_time = 0.0
        self.anim_job = None
        self.keyframes: List[Keyframe] = []
        self.mesh_vertices: List[Tuple[float, float, float]] = []
        self.mesh_faces: List[List[int]] = []
        self.mesh_info: str = ""
        self.model_parts: List[Dict] = []
        self.audio_path: Optional[str] = None
        self._last_mouse = (0, 0)
        self.show_wireframe = tk.BooleanVar(value=True)  
        self.reduce_polys = tk.BooleanVar(value=False)   
        self.is_own_host = False  
        self.pan_x = 0.0  
        self.pan_y = 0.0
        self.zoom = 1.0

        self.header = ttk.Frame(self)
        self.header.pack(fill="x", padx=4, pady=2)
        ttk.Label(self.header, text="Preview", font=("Segoe UI Semibold", 9)).pack(side="left")

        self.btn_close = ttk.Button(self.header, text="✕", width=3, command=self.hide)
        self.btn_close.pack(side="right")

        self.canvas = tk.Canvas(self, bg="#18181a", highlightthickness=0, height=220)
        self.canvas.pack(fill="both", expand=True, padx=4, pady=2)

        self.controls = ttk.Frame(self)
        self.controls.pack(fill="x", padx=4, pady=4)

        self.btn_play = ttk.Button(self.controls, text="▶ Play", width=7, command=self.toggle_play)
        self.btn_play.pack(side="left", padx=2)

        self.lbl_mode = ttk.Label(self.controls, text="Mode: Idle")
        self.lbl_mode.pack(side="left", padx=6)

        ttk.Checkbutton(self.controls, text="Wireframe lines", variable=self.show_wireframe, command=self.draw_frame).pack(side="left", padx=6)
        ttk.Checkbutton(self.controls, text="Reduce polys", variable=self.reduce_polys, command=self.draw_frame).pack(side="left", padx=6)

        self.canvas.bind("<Button-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind("<Button-4>", lambda e: self._zoom_by(1.15))
        self.canvas.bind("<Button-5>", lambda e: self._zoom_by(0.85))
        self.bind("<KeyPress>", self._on_key_press)
        self.bind("<KeyRelease>", self._on_key_release)
        self.canvas.bind("<KeyPress>", self._on_key_press)
        self.canvas.bind("<KeyRelease>", self._on_key_release)
        self._keys_held = set()

        self.pack_forget()

    def _zoom_by(self, factor: float) -> None:
        self.zoom = max(0.05, min(20.0, self.zoom * factor))
        self.draw_frame()

    def _on_mouse_wheel(self, event):
        try:
            step = -1 if event.delta > 0 else 1
            self._zoom_by(1.12 if step < 0 else 0.9)
        except Exception:
            pass

    def _on_key_press(self, event):
        self._keys_held.add(event.keysym.lower())
        self._move_with_keys()

    def _on_key_release(self, event):
        self._keys_held.discard(event.keysym.lower())

    def _move_with_keys(self):
        step = 8.0
        if "w" in self._keys_held:
            self.pan_y += step
        if "s" in self._keys_held:
            self.pan_y -= step
        if "a" in self._keys_held:
            self.pan_x += step
        if "d" in self._keys_held:
            self.pan_x -= step
        self.draw_frame()

    def set_asset_data_from_temp(self, temp_file_path: str, is_anim=False, is_mesh=False, is_model=False, is_audio=False):
        self.keyframes = []
        self.mesh_vertices = []
        self.mesh_faces = []
        self.mesh_info = ""
        self.model_parts = []
        self.audio_path = None
        try:
            with open(temp_file_path, "rb") as f:
                data = f.read()
        except Exception:
            data = b""
        try:
            data = _decompress_document(data)
        except Exception:
            pass
        if is_anim:
            self.keyframes = parse_animation(data)
            self.mesh_info = f"{len(self.keyframes)} keyframes"
        elif is_mesh:
            self._load_mesh(data)
        elif is_model:
            self._load_model(data)
        elif is_audio:
            self._load_audio(data)
        else:
            self.mesh_info = "No preview for this asset type"
        self.draw_frame()

    def _load_audio(self, data: bytes) -> None:
        
        ext = ""
        fmt, off = find_embedded_audio_robust(data)
        if fmt and off != -1:
            payload = data[off:]
            ext = {"WAV": "wav", "OGG": "ogg", "MP3": "mp3"}.get(fmt, "bin")
        elif data.startswith(b"ID3") or (len(data) > 2 and data[:3] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2")):
            fmt, payload, ext = "MP3", data, "mp3"
        elif data.startswith(b"OggS"):
            fmt, payload, ext = "OGG", data, "ogg"
        else:
            self.mesh_info = "Audio present, but no playable stream was found"
            return
        import tempfile as _tf

        self.audio_path = os.path.join(_tf.gettempdir(), f"rdbm_preview_{abs(hash(payload)):x}.{ext}")
        try:
            with open(self.audio_path, "wb") as f:
                f.write(payload)
        except Exception as e:
            self.audio_path = None
            self.mesh_info = f"Audio present, but could not write temp file ({e})"
            return
        try:
            from datetime import datetime

            stamp = datetime.now().strftime("%H:%M:%S")
        except Exception:
            stamp = ""
        self.mesh_info = f"Audio: {fmt} · {len(payload):,} bytes · {stamp} (▶ plays via system)"

    def _toggle_audio_play(self):
        if not self.audio_path or not os.path.isfile(self.audio_path):
            return
        try:
            os.startfile(self.audio_path)
        except Exception as e:
            messagebox.showerror("Audio", f"Could not open audio:\n{e}")

    def _load_model(self, data: bytes) -> None:
        self.model_parts, self.mesh_info = parse_model_parts(data)
        if not self.model_parts:
            try:
                xml = _normalize_roblox_document(data)
                self.model_parts, self.mesh_info = parse_model_parts(xml)
            except Exception:
                pass

    def _load_mesh(self, data: bytes) -> None:
        def _convert(b):
            try:
                return convert(b)
            except Exception:
                return None

        obj = _convert(data)
        if not obj and not data.lstrip().startswith(b"version "):
            idx = data.find(b"version ")
            if 0 < idx <= 512:
                obj = _convert(data[idx:])
        if not obj:
            self.mesh_info = "Mesh present, but this variant isn't supported by the converter"
            return
        verts: List[Tuple[float, float, float]] = []
        faces: List[List[int]] = []
        for line in obj.splitlines():
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "v":
                try:
                    verts.append((float(parts[1]), float(parts[2]), float(parts[3])))
                except (ValueError, IndexError):
                    pass
            elif parts[0] == "f":
                idx = []
                for p in parts[1:]:
                    try:
                        idx.append(int(p.split("/")[0]) - 1)
                    except (ValueError, IndexError):
                        pass
                if len(idx) >= 3:
                    faces.append(idx)
        self.mesh_vertices = verts
        self.mesh_faces = faces
        self.mesh_info = f"OBJ: {len(verts)} verts, {len(faces)} faces"

    def show(self, is_anim=True, mode_label="Mesh"):
        self.lbl_mode.config(text=f"Mode: {mode_label}")
        if self.is_own_host:
            self.pack(fill="both", expand=True)
        else:
            self.pack(fill="x", padx=8, pady=4)
        self.canvas.focus_set()
        self.is_playing = is_anim
        self.btn_play.config(state="normal" if (is_anim or self.audio_path) else "disabled")
        if is_anim and not self.anim_job:
            self._animate_loop()
        else:
            self.draw_frame()

    def hide(self):
        self.is_playing = False
        if self.anim_job:
            self.after_cancel(self.anim_job)
            self.anim_job = None
        self.pack_forget()

    def toggle_play(self):
        if self.audio_path and os.path.isfile(self.audio_path):
            self._toggle_audio_play()
            return
        self.is_playing = not self.is_playing
        self.btn_play.config(text="⏸ Pause" if self.is_playing else "▶ Play")
        if self.is_playing and not self.anim_job:
            self._animate_loop()

    def _on_mouse_down(self, event):
        self._last_mouse = (event.x, event.y)

    def _on_mouse_drag(self, event):
        dx = event.x - self._last_mouse[0]
        dy = event.y - self._last_mouse[1]
        self.angle_y += dx * 0.01
        self.angle_x += dy * 0.01
        self._last_mouse = (event.x, event.y)
        self.draw_frame()

    def _animate_loop(self):
        if not self.winfo_ismapped() or not self.is_playing:
            self.anim_job = None
            return
        self.anim_time += 0.03
        self.draw_frame()
        self.anim_job = self.after(33, self._animate_loop)

    def draw_frame(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 300
        h = self.canvas.winfo_height() or 220
        if self.mesh_vertices and self.mesh_faces:
            self._draw_mesh(w, h)
            if self.mesh_info:
                self.canvas.create_text(8, 8, text=self.mesh_info, anchor="nw", fill="#8ad0ff", font=("Consolas", 8))
            return
        if self.model_parts:
            self._draw_model(w, h)
            if self.mesh_info:
                self.canvas.create_text(8, 8, text=self.mesh_info, anchor="nw", fill="#8ad0ff", font=("Consolas", 8))
            return
        if self.keyframes:
            self._draw_skeleton(w, h)
        elif self.audio_path and self.mesh_info:
            self.canvas.create_text(w / 2, h / 2, text=self.mesh_info, fill="#8ad0ff", font=("Segoe UI", 10))
            self.canvas.create_text(w / 2, h / 2 + 26, text="Press ▶ to play via your system audio player", fill="#c8c8c8", font=("Segoe UI", 9))
        else:
            self.canvas.create_text(w / 2, h / 2, text="Animation: no keyframes to draw a skeleton (0 keyframe)", fill="#007acc", font=("Segoe UI", 10))

    BONES = [
        ("Head", "UpperTorso"), ("Head", "Torso"), ("UpperTorso", "LowerTorso"), ("Torso", "LowerTorso"),
        ("LowerTorso", "UpperTorso"), ("UpperTorso", "UpperArm"), ("UpperArm", "LowerArm"), ("LowerArm", "Hand"),
        ("UpperTorso", "LeftUpperArm"), ("LeftUpperArm", "LeftLowerArm"), ("LeftLowerArm", "LeftHand"),
        ("UpperTorso", "RightUpperArm"), ("RightUpperArm", "RightLowerArm"), ("RightLowerArm", "RightHand"),
        ("UpperArm", "LeftUpperArm"), ("UpperArm", "RightUpperArm"),
        ("LowerTorso", "UpperLeg"), ("UpperLeg", "LowerLeg"), ("LowerLeg", "Foot"),
        ("LowerTorso", "LeftUpperLeg"), ("LeftUpperLeg", "LeftLowerLeg"), ("LeftLowerLeg", "LeftFoot"),
        ("LowerTorso", "RightUpperLeg"), ("RightUpperLeg", "RightLowerLeg"), ("RightLowerLeg", "RightFoot"),
        ("UpperLeg", "LeftUpperLeg"), ("UpperLeg", "RightUpperLeg"),
    ]

    def _project_point(self, pos, cx, cy, scale, mirror_y=True):
        
        x, y, z = pos
        r = 0.0  
        x1 = x * math.cos(r) + z * math.sin(r)
        z1 = -x * math.sin(r) + z * math.cos(r)
        px = cx + x1 * scale
        py = cy - y * scale + z1 * scale * 0.35
        return (px, py)

    def _draw_model(self, w, h):
        
        if not self.model_parts:
            return
        ax, ay = self.angle_x, self.angle_y
        cx, cy = w / 2 + self.pan_x, h / 2 + self.pan_y
        base = max(40.0, min(w, h) / 3) * self.zoom

        all_pos = [p["pos"] for p in self.model_parts]
        mins = [min(v[i] for v in all_pos) for i in range(3)]
        maxs = [max(v[i] for v in all_pos) for i in range(3)]
        spans = [(float(maxs[i] - mins[i])) for i in range(3)]
        span_all = max(max(spans), 1e-6)
        scale = base / span_all
        mid = [(mins[i] + maxs[i]) / 2 for i in range(3)]

        cosx, sinx, cosy, siny = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay)

        def _proj(x, y, z):
            px, py, pz = x - mid[0], y - mid[1], z - mid[2]
            x1 = px * cosy + pz * siny
            z1 = -px * siny + pz * cosy
            y2 = py * cosx - z1 * sinx
            z2 = py * sinx + z1 * cosx
            return (cx + x1 * scale, cy - y2 * scale, z2)

        corners = [
            (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
        ]
        faces = [
            (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
            (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5),
        ]

        items = []
        for part in self.model_parts:
            pos = part["pos"]
            sx, sy, sz = part["size"]
            sx = sx or 1.0
            sy = sy or 1.0
            sz = sz or 1.0
            depth_pts = []
            poly_coords = []
            for face in faces:
                coords = []
                zd = 0.0
                for ci in face:
                    cx0, cy0, cz0 = corners[ci]
                    wx = pos[0] + cx0 * sx * 0.5
                    wy = pos[1] + cy0 * sy * 0.5
                    wz = pos[2] + cz0 * sz * 0.5
                    px2, py2, pz2 = _proj(wx, wy, wz)
                    coords.append((px2, py2))
                    zd += pz2
                depth_pts.append((zd / len(face), coords, part["color"]))
            items.extend(depth_pts)

        for depth, coords, color in sorted(items, key=lambda t: t[0], reverse=True):
            flat = [c for pt in coords for c in pt]
            if self.show_wireframe.get():
                self.canvas.create_polygon(flat, fill=color, outline="#9aa0a6", width=1)
            else:
                self.canvas.create_polygon(flat, fill=color, outline="")

        try:
            ymin = mins[1] - (maxs[1] - mins[1]) * 0.1
            shadow_pts = []
            for part in self.model_parts:
                pos = part["pos"]
                sx = (part["size"][0] or 1.0) * 0.5
                sz = (part["size"][2] or 1.0) * 0.5
                shadow_pts.append((pos[0] - sx, ymin, pos[2] - sz))
                shadow_pts.append((pos[0] + sx, ymin, pos[2] - sz))
                shadow_pts.append((pos[0] + sx, ymin, pos[2] + sz))
                shadow_pts.append((pos[0] - sx, ymin, pos[2] + sz))
            s_xy = [_proj(x, y, z)[:2] for x, y, z in shadow_pts]
            flat_s = [c for pt in s_xy for c in pt]
            self.canvas.create_polygon(flat_s, fill="#000000", outline="", stipple="gray12")
        except Exception:
            pass

    def _draw_skeleton(self, w, h):
        n = len(self.keyframes)
        idx = int(self.anim_time * 30.0) % n if self.is_playing and n else 0
        kf = self.keyframes[idx]
        t = kf.time

        cx, cy = w / 2 + self.pan_x, h / 2 + self.pan_y + 10
        scale = max(0.05, min(w, h) / 4.0) * self.zoom

        default_r6 = {
            "Head": (0, 3.1, 0), "Torso": (0, 1.8, 0),
            "Left Arm": (-1.5, 1.8, 0), "Right Arm": (1.5, 1.8, 0),
            "Left Leg": (-0.55, 0.0, 0), "Right Leg": (0.55, 0.0, 0),
        }
        default_r15 = {
            "Head": (0, 3.2, 0), "UpperTorso": (0, 2.25, 0), "LowerTorso": (0, 1.55, 0),
            "LeftUpperArm": (-0.8, 2.25, 0), "LeftLowerArm": (-1.35, 1.75, 0), "LeftHand": (-1.65, 1.35, 0),
            "RightUpperArm": (0.8, 2.25, 0), "RightLowerArm": (1.35, 1.75, 0), "RightHand": (1.65, 1.35, 0),
            "LeftUpperLeg": (-0.45, 0.9, 0), "LeftLowerLeg": (-0.45, 0.15, 0), "LeftFoot": (-0.45, -0.55, 0),
            "RightUpperLeg": (0.45, 0.9, 0), "RightLowerLeg": (0.45, 0.15, 0), "RightFoot": (0.45, -0.55, 0),
        }
        points = {}
        has_geo = False
        for name, pdata in kf.pose_by_part_name.items():
            pos = pdata.get("pos")
            if pos and any(abs(float(v)) > 1e-5 for v in pos):
                points[name] = self._project_point(pos, cx, cy, scale)
                has_geo = True
            else:
                fallback = default_r15.get(name) or default_r6.get(name)
                if fallback:
                    points[name] = self._project_point(fallback, cx, cy, scale)

        bone_pts = set()
        for a, b in self.BONES:
            if a in points and b in points:
                self.canvas.create_line(points[a][0], points[a][1], points[b][0], points[b][1],
                                        fill="#9aa0a6", width=3)
                bone_pts.add(a)
                bone_pts.add(b)

        for name, (px, py) in points.items():
            fill = "#ffd54f" if name in bone_pts else "#90a4ae"
            self.canvas.create_oval(px - 4, py - 4, px + 4, py + 4, fill=fill, outline="")
            self.canvas.create_text(px + 6, py - 6, text=name[:12], anchor="w", fill="#b0bec5", font=("Consolas", 7))

        info = f"Animation: {n} keyframes @ t={t:.2f}s | joints: {len(points)}"
        self.canvas.create_text(8, 8, text=info, anchor="nw", fill="#8ad0ff", font=("Consolas", 8))
        if not has_geo:
            self.canvas.create_text(w / 2, h / 2, text="No pose position data in skeleton (keyframe count shown above)", fill="#78909c", font=("Segoe UI", 9))

    def _draw_mesh(self, w, h):
        verts = self.mesh_vertices
        if not verts:
            return
        ax, ay = self.angle_x, self.angle_y
        cx, cy = w / 2 + self.pan_x, h / 2 + self.pan_y
        base = max(20.0, min(w, h) / 4) * self.zoom
        xs = [v[0] for v in verts]
        ys = [v[1] for v in verts]
        zs = [v[2] for v in verts]
        mx, my, mz = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, (max(zs) + min(zs)) / 2
        span = max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs), 1e-6)
        scale = base / span
        cosx, sinx, cosy, siny = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay)
        pts2d, pts3d = [], []
        for (x, y, z) in verts:
            px, py, pz = x - mx, y - my, z - mz
            x1 = px * cosy + pz * siny
            z1 = -px * siny + pz * cosy
            y2 = py * cosx - z1 * sinx
            z2 = py * sinx + z1 * cosx
            pts2d.append((cx + x1 * scale, cy - y2 * scale))
            pts3d.append(z2)
        
        shadow_poly = []
        for (x, y, z) in verts:
            px, py, pz = x - mx, 0.0 - my, z - mz
            x1 = px * cosy + pz * siny
            z1 = -px * siny + pz * cosy
            y2 = 0.0 * cosx - z1 * sinx
            shadow_poly.append((cx + x1 * scale, cy - y2 * scale))
        items = []
        faces = self.mesh_faces
        if self.reduce_polys.get() and len(faces) > 128:

            stride = max(1, (len(faces) + 127) // 128)
            faces = faces[::stride]
        for face in faces:
            coords = [c for i in face for c in pts2d[i % len(pts2d)]]
            depth = sum(pts3d[i % len(pts3d)] for i in face) / len(face)
            items.append((depth, coords))
        
        try:
            self.canvas.create_polygon(shadow_poly, fill="#000000", outline="", stipple="gray12")
        except Exception:
            pass
        for depth, coords in sorted(items, key=lambda t: t[0], reverse=True):
            if self.show_wireframe.get():
                self.canvas.create_polygon(coords, fill="#2a2d31", outline="#9aa0a6", width=1)
            else:
                
                shade = 90 - max(0, min(45, int((-depth) * 12)))
                shade = max(35, min(150, shade))
                fill = "#%02x%02x%02x" % (shade, shade + 8, shade + 18)
                self.canvas.create_polygon(coords, fill=fill, outline="")

class ReplacerPane(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.script_dir = DATA_DIR
        self.preinstalled_dir = os.path.join(self.script_dir, "caches", "preinstalled")
        self.own_dir = os.path.join(self.script_dir, "caches", "Own")
        self.hash_saves_dir = os.path.join(self.script_dir, "hashsaves")
        self.file_saves_dir = os.path.join(self.script_dir, "filesaves")

        for path in (self.preinstalled_dir, self.own_dir, self.hash_saves_dir, self.file_saves_dir):
            os.makedirs(path, exist_ok=True)

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=8, pady=(7, 6))

        self.top = ttk.Frame(self.container)
        self.top.pack(fill="x", pady=(0, 2))
        self.action_bar = ttk.Frame(self.top)
        self.action_bar.pack(side="left", padx=(4, 8))

        self.source_row = ttk.Frame(self.container)
        self.source_row.pack(fill="x", pady=(0, 6))

        ttk.Label(self.source_row, text="Source:").pack(side="left")
        self.source_var = tk.StringVar(value="Caches")
        for val in ("Caches", "HashSaves", "FileSaves"):
            ttk.Radiobutton(self.source_row, text=val, variable=self.source_var, value=val, command=self.refresh_view).pack(side="left", padx=5)

        self.search_row = ttk.Frame(self.container)
        self.search_row.pack(fill="x", pady=(0, 4))
        ttk.Label(self.search_row, text="Filter:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_row, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(4, 0))
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_view(True))

        self.btn_create = ttk.Button(self.action_bar, text="Create Cache", command=self.create_cache, width=13)
        self.btn_applycache = ttk.Button(self.action_bar, text="Apply", command=self.apply_caches, width=13)
        self.btn_savehash = ttk.Button(self.action_bar, text="Save Hash", command=self.save_hash, width=13)
        self.btn_savefile = ttk.Button(self.action_bar, text="Save File", command=self.save_file, width=13)

        self.list_frame = ttk.Frame(self.container, borderwidth=1, relief="solid")
        self.list_frame.pack(fill="both", expand=True)

        self.item_list = tk.Listbox(
            self.list_frame,
            selectbackground="#007acc",
            selectforeground="#ffffff",
            selectmode=tk.EXTENDED,
            exportselection=False,
            activestyle="none",
            bg="#252526",
            fg="#d4d4d4",
        )
        self.item_list.pack(side="left", fill="both", expand=True, pady=5, padx=5)
        scroll = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.item_list.yview)
        scroll.pack(side="right", fill="y")
        self.item_list.config(yscrollcommand=scroll.set)

        self.indent_px = tkfont.nametofont(self.item_list.cget("font")).measure("   ")
        self.view_index = []
        self.group_states = {}

        self.drag_start_x = None
        self.drag_start_y = None
        self.dragging = False
        self.drag_label = None

        self.hover_index = None
        self.item_list.bind("<Motion>", self._on_hover_move)
        self.item_list.bind("<Leave>", self._on_hover_leave)

        self.ctx_menu = tk.Menu(self, tearoff=0)
        darken_menus((self.ctx_menu,))
        self.item_list.bind("<Button-3>", self._on_context_request)
        self.item_list.bind("<Button-2>", self._on_context_request)

        self.item_list.bind("<Double-1>", self._on_double_click)
        self.item_list.bind("<Button-1>", self._on_press)
        self.item_list.bind("<B1-Motion>", self._on_drag_motion)
        self.item_list.bind("<ButtonRelease-1>", self._on_drag_release)

        for widget in (self, self.container, self.top, self.action_bar, self.source_row, self.list_frame):
            widget.bind("<Button-1>", self._clear_selection_bg, add="+")

        self.refresh_view()

    def _obj_key(self, obj):
        k = obj.get("kind")
        if k == "item":
            return ("item", obj["display"])
        if k == "group":
            return ("group", obj["path"])
        if k == "group_item":
            return ("group_item", obj["group_path"], obj["filename"])
        if k == "hash":
            return ("hash", obj["path"])
        return None

    def _get_selected_objs(self):
        return [self.view_index[i] for i in self.item_list.curselection()]

    def _snapshot_selection(self):
        return [self._obj_key(o) for o in self._get_selected_objs()]

    def _restore_selection(self, keys):
        if not keys:
            return
        to_select = []
        for i, o in enumerate(self.view_index):
            if self._obj_key(o) in keys:
                to_select.append(i)
        if to_select:
            for i in to_select:
                self.item_list.selection_set(i)
            self.item_list.activate(to_select[0])

    def _row_index_from_event(self, event):
        size = self.item_list.size()
        if size <= 0:
            return None
        idx = self.item_list.nearest(event.y)
        try:
            x0, y0, w, h = self.item_list.bbox(idx)
        except Exception:
            return None
        if event.y < y0 or event.y > y0 + h:
            return None
        return idx

    def _is_over_arrow(self, event, row) -> bool:
        indent = row.get("indent", 0)
        start = indent * self.indent_px
        return start <= event.x <= start + 20

    def _clear_hover(self):
        if self.hover_index is not None:
            try:
                self.item_list.itemconfig(self.hover_index, background="")
            except Exception:
                pass
            self.hover_index = None

    def _on_hover_move(self, event):
        idx = self._row_index_from_event(event)
        if idx == self.hover_index:
            return
        self._clear_hover()
        if idx is not None:
            try:
                self.item_list.itemconfig(idx, background="#333333")
                self.hover_index = idx
            except Exception:
                pass

    def _on_hover_leave(self, event):
        self._clear_hover()

    def _clear_selection_bg(self, event):
        self._clear_hover()
        if event.widget in (self, self.container, self.top, self.action_bar, self.list_frame):
            self.item_list.selection_clear(0, tk.END)
        self.drag_start_x = None
        self.drag_start_y = None
        self.dragging = False
        if self.drag_label:
            try:
                self.drag_label.destroy()
            except Exception:
                pass
            self.drag_label = None

    def _on_press(self, event):
        self.drag_start_x, self.drag_start_y = event.x, event.y
        self.dragging = False
        return self._on_left_click(event)

    def _on_left_click(self, event):
        idx = self._row_index_from_event(event)
        if idx is None:
            self.item_list.selection_clear(0, tk.END)
            return "break"
        row = self.view_index[idx]
        if row.get("kind") == "group" and self._is_over_arrow(event, row):
            sel_keys = self._snapshot_selection()
            path = row["path"]
            self.group_states[path] = not self.group_states.get(path, False)
            self.after_idle(lambda: self.refresh_view(True, sel_keys))
            return "break"

    def _on_drag_motion(self, event):
        if self.drag_start_x is None or self.drag_start_y is None:
            return "break"
        if not self.dragging:
            dx = abs(event.x - self.drag_start_x)
            dy = abs(event.y - self.drag_start_y)
            if dx > 4 or dy > 4:
                sel_objs = self._get_selected_objs()
                if not sel_objs:
                    return "break"
                text = sel_objs[0].get("display") or sel_objs[0].get("name")
                if len(sel_objs) > 1:
                    text += f" (+{len(sel_objs)-1})"
                self.drag_label = tk.Toplevel(self)
                self.drag_label.overrideredirect(True)
                theme_toplevel(self.drag_label)
                ttk.Label(self.drag_label, text=text, relief="solid", borderwidth=1).pack()
                self.dragging = True
        if self.dragging and self.drag_label:
            self.drag_label.geometry(f"+{event.x_root+15}+{event.y_root+15}")
        return "break"

    def _base_dir_for_view(self, view=None):
        v = view or self.source_var.get()
        if v == "HashSaves":
            return self.hash_saves_dir
        if v == "FileSaves":
            return self.file_saves_dir
        return self.own_dir

    def _move_selection_to(self, target_dir):
        objs = self._get_selected_objs()
        base_dir = self._base_dir_for_view()
        for o in objs:
            if o["kind"] == "group":
                src = o["path"]
                if target_dir and src.startswith(target_dir):
                    continue
                dest = target_dir or base_dir
                try:
                    shutil.move(src, os.path.join(dest, os.path.basename(src)))
                    expanded = self.group_states.pop(src, False)
                    new_path = os.path.join(dest, os.path.basename(src))
                    self.group_states[new_path] = expanded
                except Exception:
                    pass
            elif o["kind"] == "group_item":
                src = os.path.join(o["group_path"], o["filename"])
                dest = target_dir or base_dir
                try:
                    shutil.move(src, os.path.join(dest, os.path.basename(src)))
                except Exception:
                    try:
                        shutil.copy2(src, os.path.join(dest, os.path.basename(src)))
                        os.remove(src)
                    except Exception:
                        pass
            elif o["kind"] in ("hash",):
                src = o["path"]
                dest = target_dir or base_dir
                try:
                    shutil.move(src, os.path.join(dest, os.path.basename(src)))
                except Exception:
                    try:
                        shutil.copy2(src, os.path.join(dest, os.path.basename(src)))
                        os.remove(src)
                    except Exception:
                        pass
            elif o["kind"] == "item":
                src = None
                for folder in (self.own_dir, self.preinstalled_dir):
                    if not os.path.isdir(folder):
                        continue
                    for fname in os.listdir(folder):
                        if fname.endswith(f"- {o['display']}"):
                            src = os.path.join(folder, fname)
                            break
                    if src:
                        break
                if not src:
                    continue
                dest = target_dir or base_dir
                try:
                    shutil.move(src, os.path.join(dest, os.path.basename(src)))
                except Exception:
                    try:
                        shutil.copy2(src, os.path.join(dest, os.path.basename(src)))
                        if os.path.dirname(src) == self.own_dir:
                            os.remove(src)
                    except Exception:
                        pass

    def _on_drag_release(self, event):
        if self.drag_label:
            try:
                self.drag_label.destroy()
            except Exception:
                pass
            self.drag_label = None
        if not self.dragging:
            return "break"
        idx = self._row_index_from_event(event)
        target_dir = None
        if idx is not None:
            target_obj = self.view_index[idx]
            k = target_obj.get("kind")
            if k == "group":
                target_dir = target_obj["path"]
            elif k == "group_item":
                target_dir = target_obj["group_path"]
            elif k in ("hash",):
                target_dir = os.path.dirname(target_obj["path"])
        self._move_selection_to(target_dir)
        self.dragging = False
        self.refresh_view()
        return "break"

    def _on_double_click(self, event):
        idx = self._row_index_from_event(event)
        if idx is None:
            self.item_list.selection_clear(0, tk.END)
            return "break"
        row = self.view_index[idx]
        if row.get("kind") == "group" and self._is_over_arrow(event, row):
            sel_keys = self._snapshot_selection()
            path = row["path"]
            self.group_states[path] = not self.group_states.get(path, False)
            self.after_idle(lambda: self.refresh_view(True, sel_keys))
        return "break"

    def _on_context_request(self, event):
        idx = self._row_index_from_event(event)
        clicked_obj = None
        if idx is None:
            self.item_list.selection_clear(0, tk.END)
        else:
            sel = set(self.item_list.curselection())
            if idx not in sel:
                self.item_list.selection_clear(0, tk.END)
                self.item_list.selection_set(idx)
                self.item_list.activate(idx)
            clicked_obj = self.view_index[idx]

        selected_objs = self._get_selected_objs()

        self.ctx_menu.delete(0, "end")

        delete_state = "normal"
        if not selected_objs or (clicked_obj and clicked_obj.get("kind") == "group"):
            delete_state = "disabled"
        self.ctx_menu.add_command(label="Delete", command=self.delete_selected, state=delete_state)

        rename_state = "normal" if len(selected_objs) == 1 and selected_objs[0]["kind"] in ("item", "hash", "group_item", "group") else "disabled"
        self.ctx_menu.add_command(label="Rename", command=self.rename_selected, state=rename_state)

        self.ctx_menu.add_separator()
        self.ctx_menu.add_command(label="Create group", command=self.create_group_from_selection)

        if clicked_obj and clicked_obj.get("kind") == "group":
            self.ctx_menu.add_separator()
            self.ctx_menu.add_command(label="Delete group", command=self.delete_selected_groups)
            self.ctx_menu.add_command(label="Ungroup", command=self.ungroup_selected_groups)

        try:
            self.ctx_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.ctx_menu.grab_release()

    def _search_active(self) -> bool:
        return bool(self.search_var.get().strip())

    def _passes_search(self, s: str) -> bool:
        q = self.search_var.get().strip().lower()
        if not q:
            return True
        return q in s.lower()

    def _update_actions_panel(self):
        for btn in (self.btn_create, self.btn_applycache, self.btn_savehash, self.btn_savefile):
            try:
                btn.pack_forget()
            except Exception:
                pass
        view = self.source_var.get()
        if view == "HashSaves":
            self.btn_savehash.pack(side="left", padx=(0, 6), pady=0)
        elif view == "FileSaves":
            self.btn_savefile.pack(side="left", padx=(0, 6), pady=0)
        else:
            self.btn_create.pack(side="left", padx=(0, 6), pady=0)
            self.btn_applycache.pack(side="left", padx=(0, 6), pady=0)

    def _sanitize_filename(self, s: str) -> str:
        illegal = '<>:"/\\|?*'
        cleaned = "".join("_" if c in illegal else c for c in s)
        return cleaned.rstrip(" .")

    def _swap_hash_display(self, filename: str) -> str:
        parts = filename.split(" - ", 1)
        if len(parts) == 2:
            h, n = parts[0], parts[1]
            return f"{n} ({h})"
        return filename

    def _render_saves_tree(self, base_dir, display_fn, current_dir=None, indent=0):
        current = current_dir or base_dir
        try:
            entries = os.listdir(current)
        except Exception:
            entries = []
        dirs = []
        files = []
        for name in entries:
            p = os.path.join(current, name)
            if os.path.isdir(p):
                dirs.append(name)
            elif os.path.isfile(p):
                files.append(name)
        dirs.sort(key=lambda s: s.lower())
        files.sort(key=lambda s: display_fn(s).lower())

        indent_str = "   " * indent
        for d in dirs:
            path = os.path.join(current, d)
            expanded = self.group_states.get(path, False)
            arrow = "▼ " if expanded else "▶ "
            line = f"{indent_str}{arrow}{d}"
            if not self._passes_search(line):
                continue
            self.item_list.insert(tk.END, line)
            self.view_index.append({"kind": "group", "name": d, "path": path, "indent": indent})
            if expanded:
                self._render_saves_tree(base_dir, display_fn, path, indent + 1)

        for f in files:
            disp = display_fn(f)
            path = os.path.join(current, f)
            if not self._passes_search(disp):
                continue
            self.item_list.insert(tk.END, f"{indent_str}{disp}")
            if current == base_dir:
                self.view_index.append({"kind": "hash", "name": disp, "path": path, "realname": f, "indent": indent})
            else:
                self.view_index.append({"kind": "group_item", "display": disp, "group_path": current, "filename": f, "indent": indent})

    def _render_cache_tree(self, current_dir, indent=0):
        try:
            entries = os.listdir(current_dir)
        except Exception:
            entries = []
        dirs = []
        files = []
        for name in entries:
            p = os.path.join(current_dir, name)
            if os.path.isdir(p):
                dirs.append(name)
            elif os.path.isfile(p) and " - " in name:
                files.append(name)
        dirs.sort(key=lambda s: s.lower())
        files.sort(key=lambda s: s.lower())

        indent_str = "   " * indent
        for d in dirs:
            path = os.path.join(current_dir, d)
            expanded = self.group_states.get(path, False)
            arrow = "▼ " if expanded else "▶ "
            line = f"{indent_str}{arrow}{d}"
            if not self._passes_search(line):
                continue
            self.item_list.insert(tk.END, line)
            self.view_index.append({"kind": "group", "name": d, "path": path, "indent": indent})
            if expanded:
                self._render_cache_tree(path, indent + 1)

        for f in files:
            disp = f.split(" - ", 1)[1]
            if not self._passes_search(disp):
                continue
            self.item_list.insert(tk.END, f"{indent_str}{disp}")
            if indent == 0:
                self.view_index.append({"kind": "item", "display": disp, "indent": indent})
            else:
                self.view_index.append({"kind": "group_item", "display": disp, "group_path": current_dir, "filename": f, "indent": indent})
        if indent == 0:
            return {f.split(" - ", 1)[1] for f in files}

    def refresh_view(self, preserve_selection=False, selection_keys=None):
        if preserve_selection and selection_keys is None:
            selection_keys = self._snapshot_selection()
        self._clear_hover()
        self.item_list.delete(0, tk.END)
        self.view_index = []

        view = self.source_var.get()
        if view == "HashSaves":
            self._render_saves_tree(self.hash_saves_dir, self._swap_hash_display)
        elif view == "FileSaves":
            self._render_saves_tree(self.file_saves_dir, lambda s: s)
        else:
            shown = self._render_cache_tree(self.own_dir)
            seen = shown or set()
            if os.path.isdir(self.preinstalled_dir):
                for fname in os.listdir(self.preinstalled_dir):
                    p = os.path.join(self.preinstalled_dir, fname)
                    if os.path.isfile(p) and " - " in fname:
                        disp = fname.split(" - ", 1)[1]
                        if disp in seen:
                            continue
                        if not self._passes_search(disp):
                            continue
                        self.item_list.insert(tk.END, disp)
                        self.view_index.append({"kind": "item", "display": disp})

        if preserve_selection:
            self._restore_selection(selection_keys)
        self._update_actions_panel()

    def _scan_hash_saves(self) -> List[Tuple[str, str, str]]:
        out = []
        base = self.hash_saves_dir
        if not os.path.isdir(base):
            return out
        for root, _, files in os.walk(base):
            for f in files:
                if " - " not in f:
                    continue
                h, name = f.split(" - ", 1)
                out.append((name, h.strip(), os.path.join(root, f)))
        out.sort(key=lambda t: t[0].lower())
        return out

    def _scan_file_saves(self) -> List[Tuple[str, str]]:
        out = []
        base = self.file_saves_dir
        if not os.path.isdir(base):
            return out
        for root, _, files in os.walk(base):
            for f in files:
                out.append((f, os.path.join(root, f)))
        out.sort(key=lambda t: t[0].lower())
        return out

    def create_cache(self):
        dialog = tk.Toplevel(self)
        dialog.title("Create Cache")
        dialog.transient(self)
        dialog.grab_set()
        theme_toplevel(dialog)

        ttk.Label(dialog, text="Hash saves:").grid(row=0, column=0, sticky="w", padx=10, pady=(12, 4))
        hs = self._scan_hash_saves()
        hash_names = [name for (name, _h, _p) in hs]
        hash_combo = ttk.Combobox(dialog, values=hash_names, state="readonly", width=38)
        hash_combo.grid(row=0, column=1, sticky="we", padx=10, pady=(12, 4))
        if hash_names:
            hash_combo.current(0)

        chosen_hash = {"hex": None}

        def ask_custom_hash():
            ch = simpledialog.askstring("Custom Hash", "Enter custom hash value (hex):", parent=dialog)
            if ch and ch.strip():
                chosen_hash["hex"] = re.sub(r"[^0-9A-Fa-f]", "", ch.strip())
                messagebox.showinfo("Info", f"Using custom hash: {chosen_hash['hex']}", parent=dialog)
            elif ch is not None:
                chosen_hash["hex"] = None

        ttk.Button(dialog, text="Input Custom Hash", command=ask_custom_hash).grid(row=0, column=2, padx=10, pady=(12, 4))

        ttk.Label(dialog, text="File saves:").grid(row=1, column=0, sticky="w", padx=10, pady=4)
        fs = self._scan_file_saves()
        file_names = [name for (name, _p) in fs]
        file_combo = ttk.Combobox(dialog, values=file_names, state="readonly", width=38)
        file_combo.grid(row=1, column=1, sticky="we", padx=10, pady=4)
        if file_names:
            file_combo.current(0)

        chosen_file = {"path": None}

        def pick_custom_file():
            p = filedialog.askopenfilename(title="Choose source file")
            if p:
                chosen_file["path"] = p
                messagebox.showinfo("Info", f"Selected file:\n{p}", parent=dialog)

        ttk.Button(dialog, text="Input Custom File", command=pick_custom_file).grid(row=1, column=2, padx=10, pady=4)

        ttk.Label(dialog, text="Enter display name:").grid(row=2, column=0, sticky="w", padx=10, pady=(8, 4))
        entry_name = ttk.Entry(dialog, width=40)
        entry_name.grid(row=2, column=1, columnspan=2, sticky="we", padx=10, pady=(8, 4))

        btnf = ttk.Frame(dialog)
        btnf.grid(row=3, column=0, columnspan=3, pady=12)

        def on_ok():
            final_hash = chosen_hash["hex"]
            if not final_hash:
                sel = hash_combo.get()
                if sel:
                    for name, h, _p in hs:
                        if name == sel:
                            final_hash = h
                            break
            if not final_hash:
                messagebox.showerror("Create Cache", "Please choose a hash (or input a custom one).", parent=dialog)
                return
            final_hash = re.sub(r"[^0-9A-Fa-f]", "", final_hash)
            if len(final_hash) == 0:
                messagebox.showerror("Create Cache", "Invalid hash.", parent=dialog)
                return

            src_path = chosen_file["path"]
            if not src_path:
                selfn = file_combo.get()
                if selfn:
                    for name, p in fs:
                        if name == selfn:
                            src_path = p
                            break
            if not src_path:
                messagebox.showerror("Create Cache", "Please choose a file (or input a custom one).", parent=dialog)
                return
            if not os.path.isfile(src_path):
                messagebox.showerror("Create Cache", "Selected file is missing.", parent=dialog)
                return

            disp = entry_name.get().strip()
            if not disp:
                messagebox.showerror("Create Cache", "Display name is required.", parent=dialog)
                return

            safe_disp = self._sanitize_filename(disp)
            dest_name = f"{final_hash} - {safe_disp}"
            dest_path = os.path.join(self.own_dir, dest_name)
            if os.path.exists(dest_path):
                base = dest_name
                i = 1
                while True:
                    cand = f"{base} ({i})"
                    cand_path = os.path.join(self.own_dir, cand)
                    if not os.path.exists(cand_path):
                        dest_path = cand_path
                        break
                    i += 1
            try:
                shutil.copy2(src_path, dest_path)
            except Exception as e:
                messagebox.showerror("Create Cache", f"Failed to create cache:\n{e}", parent=dialog)
                return

            dialog.destroy()
            self.refresh_view()
            messagebox.showinfo("Success", f"Created cache:\n{os.path.basename(dest_path)}", parent=self)

        ttk.Button(btnf, text="OK", command=on_ok).pack(side="left", padx=6)
        ttk.Button(btnf, text="Cancel", command=dialog.destroy).pack(side="left", padx=6)

        dialog.columnconfigure(1, weight=1)
        entry_name.focus_set()
        dialog.wait_window()

    def save_hash(self):
        dialog = tk.Toplevel(self)
        dialog.title("Save Hash")
        dialog.transient(self)
        dialog.grab_set()
        theme_toplevel(dialog)
        ttk.Label(dialog, text="Hash:").grid(row=0, column=0, padx=10, pady=(12, 4), sticky="w")
        entry_hash = ttk.Entry(dialog, width=40)
        entry_hash.grid(row=0, column=1, padx=10, pady=(12, 4), sticky="we")
        ttk.Label(dialog, text="Name:").grid(row=1, column=0, padx=10, pady=4, sticky="w")
        entry_name = ttk.Entry(dialog, width=40)
        entry_name.grid(row=1, column=1, padx=10, pady=4, sticky="we")
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=12)
        dialog.columnconfigure(1, weight=1)

        def on_ok():
            hv = entry_hash.get().strip()
            nv = entry_name.get().strip()
            if not hv or not nv:
                messagebox.showerror("Error", "Both Hash and Name are required.", parent=dialog)
                return
            filename = " - ".join([re.sub(r"[^0-9A-Fa-f]", "", hv), nv])
            safe_filename = self._sanitize_filename(filename)
            if not safe_filename:
                messagebox.showerror("Error", "Resulting file name is empty after sanitization.", parent=dialog)
                return
            base_dir = self.hash_saves_dir
            dest = os.path.join(base_dir, safe_filename)
            if os.path.exists(dest):
                base = safe_filename
                i = 1
                while True:
                    cand = f"{base} ({i})"
                    dest2 = os.path.join(base_dir, cand)
                    if not os.path.exists(dest2):
                        dest = dest2
                        break
                    i += 1
            try:
                with open(dest, "x"):
                    pass
            except FileExistsError:
                with open(dest, "wb"):
                    pass
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {e}", parent=dialog)
                return
            dialog.destroy()
            self.refresh_view()
            messagebox.showinfo("Success", f"Saved '{os.path.basename(dest)}'.")

        ttk.Button(btn_frame, text="OK", command=on_ok).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=6)
        entry_hash.focus_set()
        dialog.wait_window()

    def save_file(self):
        dialog = tk.Toplevel(self)
        dialog.title("Save File")
        dialog.transient(self)
        dialog.grab_set()
        theme_toplevel(dialog)
        chosen = {"path": None}

        def pick_file():
            p = filedialog.askopenfilename(title="Choose file to save")
            if p:
                chosen["path"] = p
                lbl_file.config(text=p)

        ttk.Label(dialog, text="File:").grid(row=0, column=0, padx=10, pady=(12, 4), sticky="w")
        btn_pick = ttk.Button(dialog, text="Browse…", command=pick_file)
        btn_pick.grid(row=0, column=1, padx=10, pady=(12, 4), sticky="w")
        lbl_file = ttk.Label(dialog, text="No file selected")
        lbl_file.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 8), sticky="w")
        ttk.Label(dialog, text="Name:").grid(row=2, column=0, padx=10, pady=4, sticky="w")
        entry_name = ttk.Entry(dialog, width=40)
        entry_name.grid(row=2, column=1, padx=10, pady=4, sticky="we")
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=12)
        dialog.columnconfigure(1, weight=1)

        def on_ok():
            src = chosen["path"]
            name = entry_name.get().strip()
            if not src:
                messagebox.showerror("Error", "Please choose a file.", parent=dialog)
                return
            if not name:
                messagebox.showerror("Error", "Please enter a Name.", parent=dialog)
                return
            safe_name = self._sanitize_filename(name)
            if not safe_name:
                messagebox.showerror("Error", "Resulting file name is empty after sanitization.", parent=dialog)
                return
            is_roblox_model = os.path.splitext(src)[1].lower() in (".rbxm", ".rbxmx")
            if is_roblox_model:
                safe_name = os.path.splitext(safe_name)[0] + ".rbxh"
            dest = os.path.join(self.file_saves_dir, safe_name)
            if os.path.exists(dest):
                base = safe_name
                i = 1
                while True:
                    cand = f"{base} ({i})"
                    dest2 = os.path.join(self.file_saves_dir, cand)
                    if not os.path.exists(dest2):
                        dest = dest2
                        break
                    i += 1
            try:
                if is_roblox_model:
                    with open(src, "rb") as f:
                        source_bytes = f.read()
                    blob = self._wrap_rbxm_as_blob(source_bytes, "application/octet-stream")
                    with open(dest, "wb") as f:
                        f.write(blob)
                else:
                    shutil.copy2(src, dest)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}", parent=dialog)
                return
            dialog.destroy()
            self.refresh_view()
            msg = "RBXM/RBXMX converted to RBXH blob and saved" if is_roblox_model else "Saved"
            messagebox.showinfo("Success", f"{msg}: '{os.path.basename(dest)}'.")

        ttk.Button(btn_frame, text="OK", command=on_ok).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side="left", padx=6)
        entry_name.focus_set()
        dialog.wait_window()

    def _clean_hex(self, s: str) -> str:
        s = s.strip()
        if s.lower().startswith("0x"):
            s = s[2:]
        s = re.sub(r"[^0-9A-Fa-f]", "", s)
        if len(s) % 2 == 1:
            s = "0" + s
        return s

    def _resolve_cache_file_for_item(self, obj) -> Optional[Tuple[str, str, str]]:
        if obj.get("kind") == "group_item":
            fname = obj["filename"]
            full = os.path.join(obj["group_path"], fname)
            if os.path.isfile(full) and " - " in fname:
                h = fname.split(" - ", 1)[0].strip()
                return h, full, obj["display"]
            return None

        if obj.get("kind") == "item":
            disp = obj["display"]
            for folder in (self.own_dir, self.preinstalled_dir):
                if not os.path.isdir(folder):
                    continue
                for fname in os.listdir(folder):
                    if not os.path.isfile(os.path.join(folder, fname)):
                        continue
                    if fname.endswith(f"- {disp}") and " - " in fname:
                        h = fname.split(" - ", 1)[0].strip()
                        return h, os.path.join(folder, fname), disp
        return None

    def apply_caches(self):
        root = self.winfo_toplevel()
        db_path = getattr(root, "db_path", None)
        shard_root = getattr(root, "shard_root", None)
        if not db_path:
            messagebox.showerror("Apply", "No database path is set in the viewer.")
            return

        objs = self._get_selected_objs()
        if not objs:
            messagebox.showinfo("Apply", "Select one or more cache items.")
            return

        targets: List[Tuple[bytes, str, str, str]] = []
        for o in objs:
            info = self._resolve_cache_file_for_item(o)
            if not info:
                continue
            h_hex, full, display = info
            h_hex = self._clean_hex(h_hex)
            try:
                id_b = bytes.fromhex(h_hex)
            except Exception:
                continue
            targets.append((id_b, full, display, h_hex))

        if not targets:
            messagebox.showerror("Apply", "No valid cache items found to import.")
            return

        ok = 0
        try:
            conn = connect_rw(db_path)
            cur = conn.cursor()
            for id_b, full, _display, _h_hex in targets:
                try:
                    with open(full, "rb") as f:
                        blob = f.read()
                except Exception:
                    continue
                try:
                    cur.execute("BEGIN IMMEDIATE")
                    cur.execute("DELETE FROM files WHERE id=?", (id_b,))
                    conn.commit()
                except Exception:
                    try:
                        conn.rollback()
                    except Exception:
                        pass
                try:
                    if shard_root:
                        hex_id = id_b.hex()
                        sp = shard_path(shard_root, hex_id)
                        if os.path.isfile(sp):
                            os.remove(sp)
                except Exception:
                    pass
                try:
                    cur.execute("BEGIN IMMEDIATE")
                    cur.execute("INSERT INTO files(id, content) VALUES(?, ?)", (id_b, sqlite3.Binary(blob)))
                    conn.commit()
                    ok += 1
                except Exception:
                    try:
                        conn.rollback()
                    except Exception:
                        pass
            try:
                conn.close()
            except Exception:
                pass
        except Exception as e:
            messagebox.showerror("Apply", f"DB error:\n{e}")
            return

        if ok:
            root = self.winfo_toplevel()
            recorder = getattr(root, "_cc_record_applied_caches", None)
            if callable(recorder):
                applied = []
                for id_b, _full, display, h_hex in targets:
                    applied.append({"name": display, "hash": h_hex})
                recorder(applied)
        messagebox.showinfo("Apply", f"Imported {ok} of {len(targets)} blob(s).")

    def rename_selected(self):
        objs = self._get_selected_objs()
        if len(objs) != 1:
            return
        o = objs[0]
        kind = o.get("kind")
        current = o.get("display") or o.get("name")
        new_name = simpledialog.askstring("Rename", "Enter new name:", initialvalue=current)
        if not new_name:
            return
        new_name = self._sanitize_filename(new_name)
        try:
            if kind == "group":
                src = o["path"]
                dest = os.path.join(os.path.dirname(src), new_name)
                os.rename(src, dest)
                expanded = self.group_states.pop(src, False)
                self.group_states[dest] = expanded
            elif kind == "group_item":
                src = os.path.join(o["group_path"], o["filename"])
                h = o["filename"].split(" - ", 1)[0]
                dest = os.path.join(o["group_path"], f"{h} - {new_name}")
                os.rename(src, dest)
            elif kind == "hash":
                src = o["path"]
                h = o.get("realname", os.path.basename(src)).split(" - ", 1)[0]
                dest = os.path.join(os.path.dirname(src), f"{h} - {new_name}")
                os.rename(src, dest)
            elif kind == "item":
                src = None
                for folder in (self.own_dir, self.preinstalled_dir):
                    if not os.path.isdir(folder):
                        continue
                    for fname in os.listdir(folder):
                        if fname.endswith(f"- {o['display']}"):
                            src = os.path.join(folder, fname)
                            break
                    if src:
                        break
                if not src:
                    return
                h = os.path.basename(src).split(" - ", 1)[0]
                dest = os.path.join(os.path.dirname(src), f"{h} - {new_name}")
                os.rename(src, dest)
        except Exception as e:
            messagebox.showerror("Error", f"Rename failed: {e}")
            return
        self.refresh_view()

    def delete_selected(self):
        objs = self._get_selected_objs()
        if not objs:
            messagebox.showerror("Error", "No item selected.")
            return
        prompt = f"Are you sure you want to delete '{(objs[0].get('name') or objs[0].get('display'))}'?" if len(objs) == 1 else f"Are you sure you want to delete {len(objs)} items?"
        if not messagebox.askyesno("Confirm", prompt):
            return
        deleted_units = 0
        for o in objs:
            if o["kind"] == "group":
                try:
                    shutil.rmtree(o["path"])
                    deleted_units += 1
                    self.group_states.pop(o["path"], None)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete group: {e}")
                    return
            elif o["kind"] == "group_item":
                try:
                    os.remove(os.path.join(o["group_path"], o["filename"]))
                    deleted_units += 1
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete file: {e}")
                    return
            elif o["kind"] in ("item",):
                for folder in (self.preinstalled_dir, self.own_dir):
                    if not os.path.isdir(folder):
                        continue
                    for fname in list(os.listdir(folder)):
                        if fname.endswith(f"- {o['display']}"):
                            try:
                                os.remove(os.path.join(folder, fname))
                                deleted_units += 1
                            except Exception as e:
                                messagebox.showerror("Error", f"Failed to delete file: {e}")
                                return
            elif o["kind"] == "hash":
                try:
                    os.remove(o["path"])
                    deleted_units += 1
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete file: {e}")
                    return
        self.refresh_view()
        messagebox.showinfo("Success", f"Deleted {deleted_units} item(s).")

    def delete_selected_groups(self):
        objs = self._get_selected_objs()
        groups = [o for o in objs if o.get("kind") == "group"]
        if not groups:
            return
        prompt = f"Are you sure you want to delete group '{groups[0]['name']}'?" if len(groups) == 1 else f"Are you sure you want to delete {len(groups)} groups?"
        if not messagebox.askyesno("Confirm", prompt):
            return
        deleted = 0
        for g in groups:
            try:
                shutil.rmtree(g["path"])
                deleted += 1
                self.group_states.pop(g["path"], None)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete group: {e}")
                return
        self.refresh_view()
        messagebox.showinfo("Success", f"Deleted {deleted} group(s).")

    def ungroup_selected_groups(self):
        objs = self._get_selected_objs()
        groups = [o for o in objs if o.get("kind") == "group"]
        if not groups:
            return
        prompt = f"Remove group '{groups[0]['name']}' and move its files back?" if len(groups) == 1 else f"Remove {len(groups)} groups and move their files back?"
        if not messagebox.askyesno("Confirm", prompt):
            return
        moved_files = 0
        removed_groups = 0
        for g in groups:
            try:
                for f in os.listdir(g["path"]):
                    src = os.path.join(g["path"], f)
                    if not os.path.isfile(src):
                        continue
                    base = os.path.basename(src)
                    dst_dir = os.path.dirname(g["path"])
                    dst = os.path.join(dst_dir, base)
                    if os.path.exists(dst):
                        name, ext = os.path.splitext(base)
                        i = 1
                        while True:
                            alt = f"{name} ({i}){ext}"
                            alt_dst = os.path.join(dst_dir, alt)
                            if not os.path.exists(alt_dst):
                                dst = alt_dst
                                break
                            i += 1
                    try:
                        shutil.move(src, dst)
                    except Exception:
                        try:
                            shutil.copy2(src, dst)
                            os.remove(src)
                        except Exception:
                            pass
                    moved_files += 1
                shutil.rmtree(g["path"])
                removed_groups += 1
                self.group_states.pop(g["path"], None)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to ungroup: {e}")
                return
        self.refresh_view()
        messagebox.showinfo("Success", f"Ungrouped {removed_groups} group(s), restored {moved_files} file(s).")

    def create_group_from_selection(self):
        objs = self._get_selected_objs()
        view = self.source_var.get()

        if view == "Caches":
            allowed = {"item", "group_item"}
        else:
            allowed = {"hash", "group_item"}
        if any(o["kind"] not in allowed for o in objs):
            return

        def parent_dir(o):
            if o["kind"] == "group_item":
                return o["group_path"]
            if o["kind"] == "hash":
                return os.path.dirname(o["path"])
            if o["kind"] == "item":
                return self.own_dir
            return None

        base = self._base_dir_for_view()
        if objs:
            base = parent_dir(objs[0])
            if not base or any(parent_dir(o) != base for o in objs):
                messagebox.showerror("Error", "Items must share the same parent folder.")
                return

        name = simpledialog.askstring("Create group", "Group name:")
        if not name:
            return
        group_path = os.path.join(base, name)
        if os.path.exists(group_path):
            messagebox.showerror("Error", "A group with that name already exists.")
            return
        try:
            os.makedirs(group_path, exist_ok=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create group folder: {e}")
            return

        moved_count = 0
        for o in objs:
            if o["kind"] == "group_item":
                src_path = os.path.join(o["group_path"], o["filename"])
            elif o["kind"] == "hash":
                src_path = o["path"]
            else:
                src_path = None
                for folder in (self.own_dir, self.preinstalled_dir):
                    if not os.path.isdir(folder):
                        continue
                    for fname in os.listdir(folder):
                        if fname.endswith(f"- {o['display']}"):
                            src_path = os.path.join(folder, fname)
                            break
                    if src_path:
                        break
                if not src_path:
                    continue
            try:
                shutil.move(src_path, os.path.join(group_path, os.path.basename(src_path)))
                moved_count += 1
            except Exception:
                try:
                    shutil.copy2(src_path, os.path.join(group_path, os.path.basename(src_path)))
                    if o["kind"] in ("group_item", "item") and os.path.dirname(src_path) == self.own_dir:
                        try:
                            os.remove(src_path)
                        except Exception:
                            pass
                    moved_count += 1
                except Exception:
                    pass

        self.group_states[group_path] = True
        self.refresh_view()
        if objs:
            messagebox.showinfo("Success", f"Created group '{name}' with {moved_count} item(s).")
        else:
            messagebox.showinfo("Success", f"Created empty group '{name}'.")

TYPE_FILTERS = [
    ("All", lambda c: True),
    ("Mesh", lambda c: c == "Mesh"),
    ("Audio", lambda c: c == "Sound"),
    ("Animation", lambda c: c == "Animation"),
    ("Image", lambda c: c in ("Image", "Decal")),
    ("KTX Texture", lambda c: c == "KTX Texture"),
    ("Model/RBXM", lambda c: c in ("Model", "RBXM", "rbxl (place)")),
    ("Font", lambda c: c == "Font"),
    ("Text", lambda c: c in ("Text", "Translations", "Video", "Compressed", "Ticket")),
    ("Unknown", lambda c: c == "Unknown"),
]

FFLAG_PREFIXES = ["DFInt", "DFString", "DFFlag", "FInt", "FString", "FFlag",
                  "SFFlag", "SFInt", "SFString", "DFLog", "FLog"]
FFLAG_PATTERN = bytes.fromhex("48 83 EC 38 48 8B 0D 00 00 00 00 4C 8D 05")
FFLAG_MASK = "xxxxxxx????xxx"
FFLAG_MODULE_SIZE = 200 * 1024 * 1024

def fflag_strip_prefix(name: str) -> str:
    name = str(name).strip()
    for pfx in FFLAG_PREFIXES:
        if name.startswith(pfx):
            return name[len(pfx):]
    return name

def fflag_infer_type(value: str) -> str:
    v = str(value).strip().lower()
    if v in ("true", "false"):
        return "bool"
    try:
        int(v, 10)
        return "int"
    except ValueError:
        try:
            float(v)
            return "float"
        except ValueError:
            return "string"

class RobloxFFlagEngine:
    """Windows implementation matching the Velostrap singleton lookup/write path."""
    PROCESS_ALL_ACCESS = 0x1F0FFF
    TH32CS_SNAPMODULE = 0x00000008
    TH32CS_SNAPMODULE32 = 0x00000010
    MEM_COMMIT = 0x1000
    PAGE_NOACCESS = 0x01
    PAGE_GUARD = 0x100

    def __init__(self):
        self.handle = None
        self.pid = 0
        self.module_base = 0
        self.module_size = FFLAG_MODULE_SIZE
        self.cached_singleton = 0

    def close(self):
        if self.handle:
            try:
                ctypes.windll.kernel32.CloseHandle(self.handle)
            except Exception:
                pass
        self.handle = None
        self.pid = 0
        self.module_base = 0
        self.cached_singleton = 0

    def attach(self, pid: int) -> bool:
        self.close()
        if os.name != "nt":
            return False
        h = ctypes.windll.kernel32.OpenProcess(self.PROCESS_ALL_ACCESS, False, int(pid))
        if not h:
            return False
        self.handle = h
        self.pid = int(pid)
        self.module_base = self._get_module_base(pid, "RobloxPlayerBeta.exe")
        self.cached_singleton = 0
        if not self.module_base:
            self.close()
            return False
        return True

    def _get_module_base(self, pid: int, wanted: str) -> int:
        class MODULEENTRY32W(ctypes.Structure):
            _fields_ = [
                ("dwSize", ctypes.wintypes.DWORD), ("th32ModuleID", ctypes.wintypes.DWORD),
                ("th32ProcessID", ctypes.wintypes.DWORD), ("GlblcntUsage", ctypes.wintypes.DWORD),
                ("ProccntUsage", ctypes.wintypes.DWORD), ("modBaseAddr", ctypes.POINTER(ctypes.c_ubyte)),
                ("modBaseSize", ctypes.wintypes.DWORD), ("hModule", ctypes.c_void_p),
                ("szModule", ctypes.wintypes.WCHAR * 256), ("szExePath", ctypes.wintypes.WCHAR * 260)
            ]
        snap = ctypes.windll.kernel32.CreateToolhelp32Snapshot(
            self.TH32CS_SNAPMODULE | self.TH32CS_SNAPMODULE32, int(pid))
        if snap in (0, -1):
            return 0
        me = MODULEENTRY32W()
        me.dwSize = ctypes.sizeof(me)
        try:
            if ctypes.windll.kernel32.Module32FirstW(snap, ctypes.byref(me)):
                while True:
                    if me.szModule.lower() == wanted.lower():
                        self.module_size = int(me.modBaseSize) or FFLAG_MODULE_SIZE
                        return ctypes.cast(me.modBaseAddr, ctypes.c_void_p).value or 0
                    if not ctypes.windll.kernel32.Module32NextW(snap, ctypes.byref(me)):
                        break
        finally:
            ctypes.windll.kernel32.CloseHandle(snap)
        return 0

    def _read(self, address: int, size: int):
        if not self.handle or not address or size <= 0:
            return None
        buf = ctypes.create_string_buffer(size)
        got = ctypes.c_size_t()
        ok = ctypes.windll.kernel32.ReadProcessMemory(
            self.handle, ctypes.c_void_p(address), buf, size, ctypes.byref(got))
        return bytes(buf.raw[:got.value]) if ok and got.value == size else None

    def _read_u64(self, address: int) -> int:
        b = self._read(address, 8)
        return int.from_bytes(b, "little", signed=False) if b else 0

    def _read_i32(self, address: int) -> int:
        b = self._read(address, 4)
        return int.from_bytes(b, "little", signed=True) if b else 0

    def get_singleton(self) -> int:
        if self.cached_singleton:
            return self.cached_singleton
        if not self.handle or not self.module_base:
            return 0

        mbi = ctypes.create_string_buffer(48)
        addr = self.module_base
        stop = self.module_base + self.module_size
        while addr < stop:
            ret = ctypes.windll.kernel32.VirtualQueryEx(
                self.handle, ctypes.c_void_p(addr), mbi, ctypes.sizeof(mbi))
            if not ret:
                break
            vbase = int.from_bytes(mbi.raw[0:8], "little")
            vsize = int.from_bytes(mbi.raw[24:32], "little")
            state = int.from_bytes(mbi.raw[32:36], "little")
            protect = int.from_bytes(mbi.raw[44:48], "little")
            if state == self.MEM_COMMIT and not (protect & (self.PAGE_NOACCESS | self.PAGE_GUARD)) and vsize:
                data = self._read(vbase, vsize)
                if data:
                    idx = 0
                    prefix = FFLAG_PATTERN[:7]
                    suffix = FFLAG_PATTERN[11:]
                    while True:
                        idx = data.find(prefix, idx)
                        if idx < 0:
                            break
                        if idx + 14 > len(data) or data[idx + 11:idx + 14] != suffix:
                            idx += 1
                            continue
                        rel = int.from_bytes(data[idx + 7:idx + 11], "little", signed=True)
                        fa = vbase + idx
                        singleton = self._read_u64(fa + 11 + rel)
                        if singleton:
                            self.cached_singleton = singleton
                            return singleton
                        idx += 1
            addr = vbase + max(vsize, 0x1000)
        return 0

    @staticmethod
    def _fnv1a64(name: str) -> int:
        h = 0xcbf29ce484222325
        for ch in name:
            h ^= ord(ch)
            h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
        return h

    def set_flag(self, name: str, value: str) -> bool:
        singleton = self.get_singleton()
        if not singleton:
            return False
        h = self._fnv1a64(name)
        mask = self._read_u64(singleton + 48)
        mlist = self._read_u64(singleton + 24)
        mend = self._read_u64(singleton + 8)
        if not mask or not mlist:
            return False
        bucket = h & mask
        node = self._read_u64(mlist + bucket * 16 + 8)
        for _ in range(500):
            if not node or node == mend:
                break
            entry = self._read(node, 64)
            if not entry:
                break
            str_sz = int.from_bytes(entry[32:40], "little", signed=True)
            str_alc = int.from_bytes(entry[40:48], "little", signed=True)
            if str_alc > 15:
                ptr = int.from_bytes(entry[16:24], "little")
                ename_b = self._read(ptr, max(0, str_sz)) or b""
                ename = ename_b.decode("utf-8", errors="replace")
            else:
                ename = entry[16:16 + max(0, str_sz)].decode("utf-8", errors="replace")
            if ename == name:
                vpr = int.from_bytes(entry[48:56], "little")
                if not vpr:
                    return False
                vp = self._read_u64(vpr + 0xC0)
                if not vp:
                    return False
                v = str(value).strip().lower()
                try:
                    rv = 1 if v in ("true", "1") else 0 if v in ("false", "0") else int(value)
                except ValueError:
                    return False
                data = int(rv).to_bytes(4, "little", signed=True)
                written = ctypes.c_size_t()
                return bool(ctypes.windll.kernel32.WriteProcessMemory(
                    self.handle, ctypes.c_void_p(vp), data, 4, ctypes.byref(written)))
            node = int.from_bytes(entry[8:16], "little", signed=False)
        return False

    def get_flag_address(self, name: str) -> int:
        singleton = self.get_singleton()
        if not singleton:
            return 0
        h = self._fnv1a64(name)
        mask = self._read_u64(singleton + 48)
        mlist = self._read_u64(singleton + 24)
        mend = self._read_u64(singleton + 8)
        if not mask or not mlist:
            return 0
        bucket = h & mask
        node = self._read_u64(mlist + bucket * 16 + 8)
        for _ in range(500):
            if not node or node == mend:
                break
            entry = self._read(node, 64)
            if not entry:
                break
            str_sz = int.from_bytes(entry[32:40], "little", signed=True)
            str_alc = int.from_bytes(entry[40:48], "little", signed=True)
            if str_alc > 15:
                ptr = int.from_bytes(entry[16:24], "little")
                ename = (self._read(ptr, max(0, str_sz)) or b"").decode("utf-8", errors="replace")
            else:
                ename = entry[16:16 + max(0, str_sz)].decode("utf-8", errors="replace")
            if ename == name:
                vpr = int.from_bytes(entry[48:56], "little")
                if not vpr:
                    return 0
                return self._read_u64(vpr + 0xC0)
            node = int.from_bytes(entry[8:16], "little", signed=False)
        return 0

    def get_flag_address_with_prefixes(self, name: str) -> int:
        addr = self.get_flag_address(name)
        if addr:
            return addr
        for pfx in FFLAG_PREFIXES:
            addr = self.get_flag_address(pfx + name)
            if addr:
                return addr
        return 0

    def set_flag_with_prefixes(self, name: str, value: str) -> bool:
        if self.set_flag(name, value):
            return True
        for pfx in FFLAG_PREFIXES:
            if self.set_flag(pfx + name, value):
                return True
        return False

def _get_process_exe_path(pid):
    if not pid or sys.platform != "win32":
        return ""
    try:
        handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
        if not handle:
            return ""
        try:
            buf = ctypes.create_unicode_buffer(32768)
            size = ctypes.wintypes.DWORD(len(buf))
            if ctypes.windll.kernel32.QueryFullProcessImageNameW(handle, 0, buf, ctypes.byref(size)):
                return buf.value
        finally:
            ctypes.windll.kernel32.CloseHandle(handle)
    except Exception:
        pass
    return ""

def _fflag_find_pid() -> int:
    if os.name != "nt":
        return 0
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    try:
        class PROCESSENTRY32W(ctypes.Structure):
            _fields_ = [
                ("dwSize", ctypes.wintypes.DWORD), ("cntUsage", ctypes.wintypes.DWORD),
                ("th32ProcessID", ctypes.wintypes.DWORD), ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
                ("th32ModuleID", ctypes.wintypes.DWORD), ("cntThreads", ctypes.wintypes.DWORD),
                ("th32ParentProcessID", ctypes.wintypes.DWORD), ("pcPriClassBase", ctypes.c_long),
                ("dwFlags", ctypes.wintypes.DWORD), ("szExeFile", ctypes.wintypes.WCHAR * 260)
            ]
        snap = ctypes.windll.kernel32.CreateToolhelp32Snapshot(0x00000002, 0)
        if snap in (0, -1):
            return 0
        pe = PROCESSENTRY32W()
        pe.dwSize = ctypes.sizeof(pe)
        try:
            if ctypes.windll.kernel32.Process32FirstW(snap, ctypes.byref(pe)):
                while True:
                    if pe.szExeFile.lower() == "robloxplayerbeta.exe":
                        return int(pe.th32ProcessID)
                    if not ctypes.windll.kernel32.Process32NextW(snap, ctypes.byref(pe)):
                        break
        finally:
            ctypes.windll.kernel32.CloseHandle(snap)
    except Exception:
        pass
    return 0

_NATIVE_MESSAGEBOX = messagebox

class _MacNotification:
    """Small borderless dark macOS-like notification used for non-modal notices."""
    _active = []

    @classmethod
    def show(cls, title, message, parent=None, kind="info"):
        try:
            if parent is None:
                parent = tk._default_root
            if parent is None or not parent.winfo_exists():
                return
            win = tk.Toplevel(parent)
            win.overrideredirect(True)
            win.attributes("-topmost", True)
            win.configure(bg="#111111")
            outer = tk.Frame(win, bg="#111111", bd=0, highlightthickness=1, highlightbackground="#333333")
            outer.pack(fill="both", expand=True)
            bar = tk.Frame(outer, bg="#090909", height=30)
            bar.pack(fill="x")
            bar.pack_propagate(False)
            dots = tk.Canvas(bar, width=58, height=30, bg="#090909", bd=0, highlightthickness=0)
            dots.pack(side="left", padx=(7, 0))
            for i, c in enumerate(("#ff5f57", "#28c840", "#febc2e")):
                x = 8 + i * 14
                dots.create_oval(x, 10, x + 8, 18, fill=c, outline=c)
            tk.Label(bar, text=str(title), bg="#090909", fg="#eeeeee", font=("Comic Sans MS", 9, "bold")).pack(side="left", padx=4)
            body = tk.Frame(outer, bg="#111111", padx=14, pady=11)
            body.pack(fill="both", expand=True)
            tk.Label(body, text=str(message), bg="#111111", fg="#e5e5e5", justify="left", anchor="w",
                     wraplength=360, font=("Comic Sans MS", 9)).pack(fill="both", expand=True)
            def close():
                try:
                    if win in cls._active: cls._active.remove(win)
                    win.destroy()
                except Exception:
                    pass
            win.bind("<Button-1>", lambda _e: close())
            win.after(4200, close)
            win.update_idletasks()
            pw, ph = parent.winfo_width(), parent.winfo_height()
            px, py = parent.winfo_rootx(), parent.winfo_rooty()
            ww, wh = win.winfo_width(), win.winfo_height()
            x = px + max(10, pw - ww - 18)
            y = py + max(10, ph - wh - 18)
            win.geometry(f"{ww}x{wh}+{x}+{y}")
            cls._active.append(win)
        except Exception:
            pass

class _DarkMessageBox:
    @staticmethod
    def showinfo(title, message, parent=None, **kwargs):
        _MacNotification.show(title, message, parent, "info")
    @staticmethod
    def showwarning(title, message, parent=None, **kwargs):
        _MacNotification.show(title, message, parent, "warning")
    @staticmethod
    def showerror(title, message, parent=None, **kwargs):
        _MacNotification.show(title, message, parent, "error")
    @staticmethod
    def askyesno(title, message, parent=None, **kwargs):

        return _NATIVE_MESSAGEBOX.askyesno(title, message, parent=parent, **kwargs)


messagebox = _DarkMessageBox()

def _install_rounded_buttons():
    """Disabled: keep native ttk buttons for fast startup and stability."""
    return

class _ScrollableTab(ttk.Frame):
    """A normal-looking ttk tab whose contents can be vertically scrolled."""
    def __init__(self, master, padding=0, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(self, bg=_CURRENT_PALETTE["bg_dark"], highlightthickness=0, bd=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.inner = ttk.Frame(self, padding=padding)
        self.window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", self._update_region)
        self.canvas.bind("<Configure>", self._resize_inner)
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())
        self.canvas.bind("<MouseWheel>", self._wheel)
        self.inner.bind("<MouseWheel>", self._wheel)

    def _update_region(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_inner(self, event):
        self.canvas.itemconfigure(self.window, width=event.width)

    def _wheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(int(-event.delta / 120), "units")
        return "break"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()


        _saved_roblox = str(self.settings.get("roblox_path", "") or "").strip()
        if _saved_roblox and os.path.isdir(_saved_roblox):
            _candidate = os.path.join(_saved_roblox, "RobloxPlayerBeta.exe")
            if os.path.isfile(_candidate):
                self.settings["roblox_path"] = _candidate
        if not self.settings.get("roblox_path"):
            _pid = _fflag_find_pid()
            _exe = _get_process_exe_path(_pid)
            if _exe and os.path.basename(_exe).lower() == "robloxplayerbeta.exe":
                self.settings["roblox_path"] = _exe
                save_settings(self.settings)
        self.cconfigs_dir = os.path.join(DATA_DIR, "cconfigs")
        self.jsons_dir = os.path.join(DATA_DIR, "jsons")
        os.makedirs(self.cconfigs_dir, exist_ok=True)
        os.makedirs(self.jsons_dir, exist_ok=True)
        self.cc_applied_caches = []
        self._cc_load_applied_state()



        self._reset_version_file()
        self._history_last_game = None

        _t = self.settings.get("theme", DEFAULT_THEME)
        apply_visual_polish(self, theme=UI_THEME, palette=THEMES.get(_t, THEMES[DEFAULT_THEME]))
        self.title("RoUtils")
        self.geometry(STARTUP_GEOMETRY)
        self.minsize(700, 420)
        self.resizable(True, True)
        self._setup_custom_titlebar()



        self.bind("<Map>", lambda _e: self.after_idle(self._restore_windows_taskbar_presence), add="+")
        self.after_idle(self._restore_windows_taskbar_presence)
        try:
            self.iconbitmap(ICON_PATH)
        except Exception:
            pass
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._global_hotkey_q = queue.Queue()
        self._hotkey_stop = threading.Event()
        self.fflag_hotkeys = list(self.settings.get("fflag_hotkeys", []))
        self._hotkey_prev = {}
        self._hotkey_thread = None

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.tab_viewer = ttk.Frame(self.nb)
        self.nb.add(self.tab_viewer, text="Cache")

        self.hpaned = ttk.PanedWindow(self.tab_viewer, orient="horizontal")
        self.hpaned.pack(fill="both", expand=True)

        self.viewer_root = ttk.Frame(self.hpaned)
        self.hpaned.add(self.viewer_root, weight=3)
        _set_pane_minsize(self.hpaned, self.viewer_root, VIEWER_MIN_WIDTH)

        self.replacer = ReplacerPane(self.hpaned)
        self.hpaned.add(self.replacer, weight=2)
        _set_pane_minsize(self.hpaned, self.replacer, REPLACER_MIN_WIDTH)

        self.hpaned.bind("<B1-Motion>", lambda e: self._clamp_hsash())
        self.hpaned.bind("<ButtonRelease-1>", lambda e: self._clamp_hsash())

        self.viewer_collapsed = False
        self._restore_geom: Optional[Tuple[int, int, int, int]] = None
        self._saved_sash: Optional[int] = None
        self.collapse_btn = ttk.Button(self.replacer.top, text="\u25c0", width=2, command=self._toggle_viewer_pane)
        self.collapse_btn.pack(side="left", padx=(0, 4), before=self.replacer.action_bar)

        self.db_path, self.shard_root = default_paths()
        self.seen_hashes: set = set()
        self.items_by_iid: Dict[str, ScanItem] = {}
        self.items_by_hash: Dict[str, ScanItem] = {}
        self.new_items_q: "queue.Queue[List[ScanItem]]" = queue.Queue()
        self.watching = False
        self.stop_event = threading.Event()
        self.scan_thread: Optional[threading.Thread] = None
        self.autoscroll = tk.BooleanVar(value=self.settings.get("autoscroll", True))
        self.hide_tickets = tk.BooleanVar(value=self.settings.get("hide_tickets", True))
        self.stay_on_top = tk.BooleanVar(value=self.settings.get("stay_on_top", False))
        self.show_lines = tk.BooleanVar(value=self.settings.get("show_lines", True))

        def _trace(*_):
            self._save_settings()
        for v in (self.autoscroll, self.hide_tickets, self.stay_on_top, self.show_lines):
            v.trace_add("write", _trace)
        self.filter_text = tk.StringVar(value="")
        self.max_rows = tk.IntVar(value=0)
        self.type_filter = tk.StringVar(value=self.settings.get("type_filter", "All"))
        self.autostart_watch = tk.BooleanVar(value=self.settings.get("autostart_watch", False))
        self.autostart_watch.trace_add("write", lambda *_: self._save_settings())


        try:
            saved_fps = int(self.settings.get("fps_limit", 0))
        except Exception:
            saved_fps = 0
        self.fps_limit = tk.IntVar(value=max(0, min(800, saved_fps)))
        self._hidden_fps_flag_name = "DFIntTaskSchedulerTargetFps"
        self._hidden_fps_flag_value = None
        self.after(30000, self._fps_apply_tick)

        self._hover_preview_job: Optional[str] = None
        self._hover_preview_iid: Optional[str] = None
        self._hover_preview_xy: Tuple[int, int] = (0, 0)
        self._img_preview_win: Optional[tk.Toplevel] = None
        self._img_preview_label: Optional[ttk.Label] = None
        self._img_preview_photo = None
        self._img_preview_fade_job: Optional[str] = None
        self._tree_hover_iid: Optional[str] = None

        self._build_viewer_widgets()
        self.fflag_engine = RobloxFFlagEngine()
        self.fflag_flags = []
        self.fflag_offsets = {}
        self.fflag_presets = []
        self.fflag_pid = 0
        self.fflag_original_values = {}
        self.fflag_auto_apply = tk.BooleanVar(value=self.settings.get("fflag_auto_apply", False))
        self.launch_on_startup = tk.BooleanVar(value=self.settings.get("launch_on_startup", False))
        self._load_fflag_flags()
        self._sync_fps_flag_to_manager()
        self._build_home_tab()
        self._build_themes_tab()
        self._build_settings_tab()
        self._build_fflag_tab()
        self._build_utils_tab()
        self._build_cconfigs_tab()
        self._build_subplace_joiner_tab()
        self._build_history_tab()
        self._history_resolve_existing_names()
        self._build_client_tab()
        self._reorder_tabs()


        self.after_idle(self._install_global_scroll_support)
        self._start_history_watcher()
        self._detect_roblox_profile()
        self._start_profile_detection()
        self._start_version_check()
        self._install_startup_shortcut()
        self._start_global_hotkeys()
        self.after(50, self._process_global_hotkeys)
        self.update_idletasks()
        self._apply_startup_layouts()
        if self.settings.get("viewer_collapsed"):
            self._toggle_viewer_pane()
        self._update_status()
        self.after(150, self._drain_queue)
        self.after(200, self._save_settings)
        self.after(6000, self._fflag_auto_apply_tick)


    def _start_global_hotkeys(self):
        if self._hotkey_thread and self._hotkey_thread.is_alive():
            return
        if sys.platform != "win32":
            return

        def worker():
            user32 = ctypes.windll.user32
            while not self._hotkey_stop.is_set():
                try:
                    bindings = list(self.fflag_hotkeys)
                    seen = set()
                    for binding in bindings:
                        key = str(binding.get("key", "")).upper()
                        vk = fflag_key_to_vk(key)
                        if not vk or vk in seen:
                            continue
                        seen.add(vk)
                        down = bool(user32.GetAsyncKeyState(vk) & 0x8000)
                        was_down = self._hotkey_prev.get(vk, False)
                        self._hotkey_prev[vk] = down
                        if down and not was_down:
                            self._global_hotkey_q.put(binding.copy())
                except Exception:
                    pass
                time.sleep(0.025)

        self._hotkey_thread = threading.Thread(target=worker, name="RoUtilsGlobalHotkeys", daemon=True)
        self._hotkey_thread.start()

    def _process_global_hotkeys(self):
        try:
            while True:
                binding = self._global_hotkey_q.get_nowait()
                self._handle_fflag_hotkey(binding)
        except queue.Empty:
            pass
        except Exception:
            pass
        if not self._hotkey_stop.is_set():
            self.after(50, self._process_global_hotkeys)

    def _handle_fflag_hotkey(self, binding):
        flag_name = fflag_strip_prefix(str(binding.get("flag", "")).strip())
        if not flag_name:
            return

        actual = None
        for item in self.fflag_hotkeys:
            if (
                str(item.get("key", "")).upper() == str(binding.get("key", "")).upper()
                and fflag_strip_prefix(str(item.get("flag", ""))) == flag_name
            ):
                actual = item
                break
        if actual is None:
            return

        value1 = str(actual.get("value1", "true"))
        value2 = str(actual.get("value2", "false"))
        state = bool(actual.get("state", False))
        new_value = value2 if state else value1
        actual["state"] = not state

        found = None
        for flag in self.fflag_flags:
            if fflag_strip_prefix(flag.get("name", "")) == flag_name:
                found = flag
                break
        if found is None:
            found = {"name": flag_name, "value": new_value, "type": fflag_infer_type(new_value)}
            self.fflag_flags.append(found)
        else:
            found["value"] = new_value
            found["type"] = fflag_infer_type(new_value)

        self._save_fflag_flags()
        self._save_settings()
        self._refresh_fflag_list()

        if self.fflag_pid and self.fflag_engine.handle:
            try:
                self.fflag_engine.get_singleton()
                self.fflag_engine.set_flag_with_prefixes(flag_name, new_value)
                self.fflag_status.config(
                    text=f"{flag_name} = {new_value}",
                    foreground="#65d98b"
                )
            except Exception:
                pass


    def _fflag_hotkeys_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("FFlag Hotkeys")
        dlg.geometry("900x500")
        dlg.transient(self)
        theme_toplevel(dlg)

        outer = ttk.Frame(dlg, padding=12)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(1, weight=1)

        ttk.Label(
            outer,
            text="Global FFlag Hotkeys",
            font=("Segoe UI Semibold", 13)
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        cols = ("key", "flag", "mode", "value1", "value2")
        tree = ttk.Treeview(outer, columns=cols, show="headings", selectmode="browse")
        headers = {
            "key": "KEY", "flag": "FFLAG", "mode": "MODE",
            "value1": "TOGGLE 1", "value2": "TOGGLE 2"
        }
        widths = {"key": 100, "flag": 320, "mode": 100, "value1": 140, "value2": 140}
        for col in cols:
            tree.heading(col, text=headers[col])
            tree.column(col, width=widths[col], anchor="w")
        tree.grid(row=1, column=0, sticky="nsew")

        def refresh():
            tree.delete(*tree.get_children())
            for i, item in enumerate(self.fflag_hotkeys):
                tree.insert(
                    "", "end", iid=str(i),
                    values=(
                        item.get("key", ""),
                        item.get("flag", ""),
                        item.get("mode", "Toggle"),
                        item.get("value1", "true"),
                        item.get("value2", "false"),
                    )
                )

        def edit():
            sel = tree.selection()
            if not sel:
                return
            idx = int(sel[0])
            self._fflag_hotkey_editor(idx, dlg, refresh)

        btns = ttk.Frame(outer)
        btns.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        ttk.Button(btns, text="+ Add Hotkey", command=lambda: self._fflag_hotkey_editor(None, dlg, refresh)).pack(side="left")
        ttk.Button(btns, text="Edit", command=edit).pack(side="left", padx=5)
        ttk.Button(btns, text="Remove", command=lambda: self._remove_fflag_hotkey(tree, refresh)).pack(side="left")
        ttk.Button(btns, text="Close", command=dlg.destroy).pack(side="right")
        refresh()

    def _remove_fflag_hotkey(self, tree, refresh):
        sel = tree.selection()
        if not sel:
            return
        del self.fflag_hotkeys[int(sel[0])]
        self._save_settings()
        refresh()

    def _fflag_hotkey_editor(self, index, parent, refresh):
        dlg = tk.Toplevel(parent)
        dlg.title("FFlag Hotkey")
        dlg.transient(parent)
        dlg.grab_set()
        theme_toplevel(dlg)

        existing = self.fflag_hotkeys[index] if index is not None else {}
        key_var = tk.StringVar(value=str(existing.get("key", "")))
        flag_var = tk.StringVar(value=str(existing.get("flag", "")))
        mode_var = tk.StringVar(value=str(existing.get("mode", "Toggle")))
        v1_var = tk.StringVar(value=str(existing.get("value1", "true")))
        v2_var = tk.StringVar(value=str(existing.get("value2", "false")))

        ttk.Label(dlg, text="Key:").grid(row=0, column=0, padx=10, pady=(12, 4), sticky="w")
        key_entry = ttk.Entry(dlg, textvariable=key_var, width=20)
        key_entry.grid(row=1, column=0, padx=10, sticky="ew")

        ttk.Label(dlg, text="FFlag:").grid(row=2, column=0, padx=10, pady=(8, 4), sticky="w")
        flag_combo = ttk.Combobox(
            dlg, textvariable=flag_var,
            values=[x.get("name", "") for x in self.fflag_flags],
            width=48
        )
        flag_combo.grid(row=3, column=0, padx=10, sticky="ew")

        ttk.Label(dlg, text="Action:").grid(row=4, column=0, padx=10, pady=(8, 4), sticky="w")
        mode_combo = ttk.Combobox(dlg, textvariable=mode_var, values=["Toggle"], state="readonly", width=20)
        mode_combo.grid(row=5, column=0, padx=10, sticky="w")

        ttk.Label(dlg, text="Toggle 1 value:").grid(row=6, column=0, padx=10, pady=(8, 4), sticky="w")
        ttk.Entry(dlg, textvariable=v1_var, width=30).grid(row=7, column=0, padx=10, sticky="ew")

        ttk.Label(dlg, text="Toggle 2 value:").grid(row=8, column=0, padx=10, pady=(8, 4), sticky="w")
        ttk.Entry(dlg, textvariable=v2_var, width=30).grid(row=9, column=0, padx=10, sticky="ew")

        ttk.Label(
            dlg,
            text="Example: K + DebugDrawBroadPhaseAABBs + true/false toggles the value globally.",
            foreground="#9aa0a6"
        ).grid(row=10, column=0, padx=10, pady=(8, 4), sticky="w")

        def capture_key(event):
            if event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R"):
                return "break"
            key = event.keysym.upper()
            if key == "ESCAPE":
                key = "ESC"
            key_var.set(key)
            return "break"

        key_entry.bind("<KeyPress>", capture_key)

        def save():
            key = key_var.get().strip().upper()
            flag = fflag_strip_prefix(flag_var.get().strip())
            if not key or not fflag_key_to_vk(key):
                messagebox.showerror("FFlag Hotkeys", "Enter a supported keyboard key.", parent=dlg)
                return
            if not flag:
                messagebox.showerror("FFlag Hotkeys", "Enter an FFlag name.", parent=dlg)
                return
            item = {
                "key": key,
                "flag": flag,
                "mode": "Toggle",
                "value1": v1_var.get(),
                "value2": v2_var.get(),
                "state": bool(existing.get("state", False)),
            }
            if index is None:
                self.fflag_hotkeys.append(item)
            else:
                self.fflag_hotkeys[index] = item
            self._save_settings()
            refresh()
            dlg.destroy()

        btns = ttk.Frame(dlg)
        btns.grid(row=11, column=0, pady=12)
        ttk.Button(btns, text="Save", command=save).pack(side="left", padx=4)
        ttk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="left", padx=4)
        dlg.columnconfigure(0, weight=1)
        key_entry.focus_set()




    def _restore_windows_taskbar_presence(self):
        """Keep this exact Tk root as a normal Windows taskbar/Alt+Tab app.
        Never withdraw/deiconify here: doing that can create a ghost/second taskbar
        entry and can make a frameless Tk window disappear from Alt+Tab.
        """
        if sys.platform != "win32" or not self.winfo_exists():
            return
        try:
            hwnd = int(self.winfo_id())
            user32 = ctypes.windll.user32
            GWL_EXSTYLE = -20
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_TOOLWINDOW = 0x00000080
            SWP_NOSIZE = 0x0001
            SWP_NOMOVE = 0x0002
            SWP_NOZORDER = 0x0004
            SWP_NOACTIVATE = 0x0010
            SWP_FRAMECHANGED = 0x0020
            get_ex = getattr(user32, "GetWindowLongPtrW", user32.GetWindowLongW)
            set_ex = getattr(user32, "SetWindowLongPtrW", user32.SetWindowLongW)
            ex = int(get_ex(hwnd, GWL_EXSTYLE))
            ex = (ex | WS_EX_APPWINDOW) & ~WS_EX_TOOLWINDOW
            set_ex(hwnd, GWL_EXSTYLE, ex)
            user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0,
                                SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER |
                                SWP_NOACTIVATE | SWP_FRAMECHANGED)

            if os.path.isfile(ICON_PATH):
                IMAGE_ICON = 1
                LR_LOADFROMFILE = 0x00000010
                LR_DEFAULTSIZE = 0x00000040
                hicon = user32.LoadImageW(None, ICON_PATH, IMAGE_ICON, 32, 32,
                                          LR_LOADFROMFILE | LR_DEFAULTSIZE)
                if hicon:
                    WM_SETICON = 0x0080
                    ICON_SMALL = 0
                    ICON_BIG = 1
                    user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)
                    user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
        except Exception:
            pass

    def _make_native_borderless_window(self):
        if sys.platform != "win32":
            return
        try:
            hwnd = int(self.winfo_id())
            user32 = ctypes.windll.user32
            GWL_STYLE = -16
            GWL_EXSTYLE = -20
            WS_CAPTION = 0x00C00000
            WS_THICKFRAME = 0x00040000
            WS_MINIMIZEBOX = 0x00020000
            WS_MAXIMIZEBOX = 0x00010000
            WS_SYSMENU = 0x00080000
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_TOOLWINDOW = 0x00000080
            SWP_NOSIZE = 0x0001
            SWP_NOMOVE = 0x0002
            SWP_NOZORDER = 0x0004
            SWP_NOACTIVATE = 0x0010
            SWP_FRAMECHANGED = 0x0020

            get_style = getattr(user32, "GetWindowLongPtrW", user32.GetWindowLongW)
            set_style = getattr(user32, "SetWindowLongPtrW", user32.SetWindowLongW)
            style = int(get_style(hwnd, GWL_STYLE))
            style &= ~WS_CAPTION
            style |= WS_SYSMENU | WS_MINIMIZEBOX | WS_MAXIMIZEBOX
            style &= ~WS_THICKFRAME
            set_style(hwnd, GWL_STYLE, style)

            ex = int(get_style(hwnd, GWL_EXSTYLE))
            ex = (ex | WS_EX_APPWINDOW) & ~WS_EX_TOOLWINDOW
            set_style(hwnd, GWL_EXSTYLE, ex)

            user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0,
                                SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER |
                                SWP_NOACTIVATE | SWP_FRAMECHANGED)
        except Exception:
            pass

    def _setup_custom_titlebar(self):



        self._make_native_borderless_window()
        self._window_maximized = False
        self._restore_geometry = None
        palette = _CURRENT_PALETTE
        self._titlebar = tk.Frame(self, bg=palette["bg_dark"], height=42, bd=0, highlightthickness=0)
        self._titlebar.pack(fill="x", side="top")
        self._titlebar.pack_propagate(False)


        controls = tk.Frame(self._titlebar, bg=palette["bg_dark"], bd=0, highlightthickness=0)
        controls.pack(side="right", padx=(0, 14))
        self._titlebar_controls = controls

        def dot(parent, fill, command, symbol=""):
            c = tk.Canvas(parent, width=16, height=16, bg=palette["bg_dark"], bd=0,
                          highlightthickness=0, cursor="hand2")
            c.pack(side="left", padx=4)
            c.create_oval(2, 2, 14, 14, fill=fill, outline=fill)
            if symbol:
                c.create_text(8, 8, text=symbol, fill="#202020", font=("Arial", 7, "bold"))
            c.bind("<Button-1>", lambda _e: command())
            return c

        self._close_dot = dot(controls, "#ff5f57", self._titlebar_close, "×")
        self._minimize_dot = dot(controls, "#28c840", self._titlebar_minimize, "−")
        self._resize_dot = dot(controls, "#febc2e", self._titlebar_toggle_maximize, "↕")

        self._titlebar_title = tk.Label(self._titlebar, text="RoUtils", bg=palette["bg_dark"],
                                        fg=palette["fg"], font=("Comic Sans MS", 13, "bold"))
        self._titlebar_title.place(relx=0.5, rely=0.5, anchor="center")
        self._titlebar.bind("<ButtonPress-1>", self._titlebar_press)
        self._titlebar.bind("<B1-Motion>", self._titlebar_drag)
        self._titlebar.bind("<Double-Button-1>", lambda _e: self._titlebar_toggle_maximize())
        self._titlebar_title.bind("<ButtonPress-1>", self._titlebar_press)
        self._titlebar_title.bind("<B1-Motion>", self._titlebar_drag)
        self._titlebar_title.bind("<Double-Button-1>", lambda _e: self._titlebar_toggle_maximize())

    def _titlebar_press(self, event):
        self._drag_x = event.x_root - self.winfo_x()
        self._drag_y = event.y_root - self.winfo_y()

    def _titlebar_drag(self, event):
        if getattr(self, "_window_maximized", False):
            return
        x = event.x_root - getattr(self, "_drag_x", 0)
        y = event.y_root - getattr(self, "_drag_y", 0)
        self.geometry(f"+{x}+{y}")

    def _titlebar_close(self):
        self._on_close()

    def _titlebar_minimize(self):
        """Minimize the one real root window; never withdraw it."""
        try:
            self.iconify()
        except Exception:
            try:
                self.state("iconic")
            except Exception:
                pass

    def _titlebar_toggle_maximize(self):
        try:
            if not self._window_maximized:
                self._restore_geometry = self.geometry()
                self.state("zoomed")
                self._window_maximized = True
            else:
                self.state("normal")
                self.after_idle(self._restore_windows_taskbar_presence)
                if self._restore_geometry:
                    self.geometry(self._restore_geometry)
                self._window_maximized = False
        except Exception:
            try:
                if self._window_maximized and self._restore_geometry:
                    self.geometry(self._restore_geometry)
                    self._window_maximized = False
                else:
                    self._restore_geometry = self.geometry()
                    self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
                    self._window_maximized = True
            except Exception:
                pass

    def _install_global_scroll_support(self):


        def wheel(event):
            try:
                x, y = event.x_root, event.y_root
                target = None

                w = self.winfo_containing(x, y)
                while w is not None:
                    if isinstance(w, _ScrollableTab):
                        target = w.canvas
                        break
                    try:
                        parent = w.nametowidget(w.winfo_parent())
                        if parent is w:
                            break
                        w = parent
                    except Exception:
                        break

                if target is None:
                    for child in self.nb.winfo_children() if hasattr(self, 'nb') else ():
                        if isinstance(child, _ScrollableTab):
                            cx, cy = child.canvas.winfo_rootx(), child.canvas.winfo_rooty()
                            cw, ch = child.canvas.winfo_width(), child.canvas.winfo_height()
                            if cx <= x <= cx + cw and cy <= y <= cy + ch:
                                target = child.canvas
                                break
                if target is None:
                    return
                if getattr(event, 'delta', 0):
                    steps = int(-event.delta / 120)
                    if steps == 0:
                        steps = -1 if event.delta > 0 else 1
                else:
                    steps = -1 if getattr(event, 'num', None) == 4 else 1
                target.yview_scroll(steps, 'units')
                return 'break'
            except Exception:
                return None

        self.bind_all('<MouseWheel>', wheel, add='+')
        self.bind_all('<Button-4>', wheel, add='+')
        self.bind_all('<Button-5>', wheel, add='+')

    def _apply_titlebar_theme(self):
        if not hasattr(self, "_titlebar"):
            return
        p = _CURRENT_PALETTE
        try:
            self._titlebar.configure(bg=p["bg_dark"])
            self._titlebar_title.configure(bg=p["bg_dark"], fg=p["fg"])
            self._titlebar_controls.configure(bg=p["bg_dark"])
            for dot in (self._close_dot, self._minimize_dot, self._resize_dot):
                dot.configure(bg=p["bg_dark"])
        except Exception:
            pass

    def _build_themes_tab(self):
        tab = ttk.Frame(self.nb, padding=0)
        self.nb.add(tab, text="Themes")
        ttk.Label(tab, text="Themes", font=("Segoe UI Semibold", 15)).pack(anchor="w")
        ttk.Label(tab, text="Choose a complete UI palette or create your own.", foreground="#9aa0a6").pack(anchor="w", pady=(0,10))
        outer=ttk.Frame(tab); outer.pack(fill="both",expand=True)
        left=ttk.Frame(outer); left.pack(side="left",fill="both",expand=True)
        right=ttk.LabelFrame(outer,text="Custom Theme",padding=12); right.pack(side="right",fill="y",padx=(14,0))
        self.theme_var=tk.StringVar(value=self.settings.get("theme",DEFAULT_THEME))
        lb=tk.Listbox(left,bg=_CURRENT_PALETTE["bg_medium"],fg=_CURRENT_PALETTE["fg"],selectbackground=_CURRENT_PALETTE["accent"],relief="flat",bd=0)
        lb.pack(fill="both",expand=True)
        for name in THEME_NAMES: lb.insert("end",name)
        try: lb.selection_set(THEME_NAMES.index(self.theme_var.get()))
        except Exception: pass
        lb.bind("<<ListboxSelect>>",lambda _e:self._theme_list_apply(lb))
        self.custom_theme_vars={}
        custom=self.settings.get("custom_theme",{})
        for key in ("bg_dark","bg_medium","bg_light","bg_hover","fg","accent","border"):
            row=ttk.Frame(right); row.pack(fill="x",pady=3)
            ttk.Label(row,text=key,width=10).pack(side="left")
            v=tk.StringVar(value=custom.get(key,THEMES[DEFAULT_THEME][key])); self.custom_theme_vars[key]=v
            ttk.Entry(row,textvariable=v,width=12).pack(side="left")
        ttk.Button(right,text="Apply Custom",command=self._apply_custom_theme).pack(fill="x",pady=(10,4))
        ttk.Button(right,text="Save Custom",command=self._save_custom_theme).pack(fill="x")
    def _theme_list_apply(self,lb):
        sel=lb.curselection()
        if not sel:return
        self.theme_var.set(lb.get(sel[0])); self._apply_theme()
    def _apply_custom_theme(self):
        palette={k:v.get().strip() for k,v in self.custom_theme_vars.items()}
        self.settings["theme"]="Custom"; self.settings["custom_theme"]=palette
        apply_visual_polish(self,theme=UI_THEME,palette=palette); darken_menus(self._collect_menus()); self._save_settings()
    def _save_custom_theme(self):
        self._apply_custom_theme()
        messagebox.showinfo("Themes","Custom theme saved.",parent=self)

    def _apply_theme(self):
        name = self.theme_var.get()
        self.settings["theme"] = name
        palette = self.settings.get("custom_theme", THEMES[DEFAULT_THEME]) if name == "Custom" else THEMES.get(name, THEMES[DEFAULT_THEME])
        try:
            apply_visual_polish(self, theme=UI_THEME, palette=palette)
        except Exception:
            pass
        darken_menus(self._collect_menus())
        for w in (self._ctx, self._colmenu, getattr(self.replacer, "ctx_menu", None)):
            if w is not None:
                try:
                    w.configure(bg=palette["bg_dark"], fg=palette["fg"],
                                activebackground=palette["accent"], activeforeground="#ffffff")
                except Exception:
                    pass
        if hasattr(self, "_titlebar"):
            try:
                self._titlebar.configure(bg=_CURRENT_PALETTE["bg_dark"])
                for child in self._titlebar.winfo_children():
                    if isinstance(child, tk.Label): child.configure(bg=_CURRENT_PALETTE["bg_dark"], fg=_CURRENT_PALETTE["fg"])
            except Exception:
                pass
        if self.viewport_3d.winfo_ismapped():
            self.viewport_3d.draw_frame()
        self._save_settings()

    def _collect_menus(self):
        out = []
        try:
            m = self.nametowidget(self.cget("menu"))
            if m:
                out.append(m)
                for i in range(m.index("end") + 1 if m.index("end") is not None else 0):
                    try:
                        sub = m.entrycget(i, "menu")
                        if sub:
                            out.append(sub)
                    except Exception:
                        pass
        except Exception:
            pass
        return out

    def _fflag_path(self):
        return os.path.join(DATA_DIR, "routils_fflags.json")

    def _load_fflag_flags(self):
        try:
            with open(self._fflag_path(), "r", encoding="utf-8") as f:
                data = json.load(f)
            self.fflag_flags = data if isinstance(data, list) else []
        except Exception:
            self.fflag_flags = []

    def _save_fflag_flags(self):
        try:
            with open(self._fflag_path(), "w", encoding="utf-8") as f:
                json.dump(self.fflag_flags, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("FFlags", f"Failed to save flags:\n{e}", parent=self)

    def _wrap_rbxm_as_blob(self, data: bytes, content_type: str = "application/octet-stream") -> bytes:
        """Create an RBXH v2 blob using the real Roblox cache-style framing."""
        if data[:4]==RBXH_MAGIC: return data
        raw=data or b""
        kind=classify_roblox_document(raw)
        if kind=="rbxmx":
            if _RbxmDeserializer is None: raise RuntimeError("RBXM serializer is unavailable.")
            raw=write_rbxm(_RbxmDeserializer().deserialize(raw))
        elif kind!="rbxm" and not raw.startswith(RBXM_MAGIC):
            raise ValueError("The selected file is not a valid RBXM/RBXMX document.")
        prefix=bytearray(b"\x00\xc8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb8\x08\x00\x00\xdc\xc0\xe5\x18\x03\x00\x00\x00")
        struct.pack_into("<I",prefix,13,len(raw))
        url=("https://c4.rbxcdn.com/"+hashlib.md5(raw).hexdigest()).encode("ascii")
        return RBXH_MAGIC+struct.pack("<II",2,len(url))+url+bytes(prefix)+raw

    def _utils_rbxm_to_blob(self):
        src = filedialog.askopenfilename(
            parent=self, title="RBXM to Blob",
            filetypes=[("Roblox Model", "*.rbxm *.rbxmx"), ("RBXM", "*.rbxm"), ("RBXMX", "*.rbxmx"), ("All files", "*.*")]
        )
        if not src:
            return
        try:
            with open(src, "rb") as f:
                data = f.read()
            blob = self._wrap_rbxm_as_blob(data, "application/octet-stream")
            base = os.path.splitext(os.path.basename(src))[0] + ".rbxh"
            dest = filedialog.asksaveasfilename(
                parent=self, title="Save RBXH Blob", initialfile=base,
                defaultextension=".rbxh", filetypes=[("RBXH Blob", "*.rbxh"), ("All files", "*.*")]
            )
            if not dest:
                return
            with open(dest, "wb") as f:
                f.write(blob)
            messagebox.showinfo("RBXM to Blob", f"Blob created successfully.\n\n{dest}\nSize: {human_size(len(blob))}", parent=self)
        except Exception as e:
            messagebox.showerror("RBXM to Blob", f"Failed to create blob:\n{e}", parent=self)

    def _utils_r6_to_r15(self):
        src = filedialog.askopenfilename(
            parent=self, title="R6 Animation → R15",
            filetypes=[("Roblox Animation", "*.rbxm *.rbxmx"), ("All files", "*.*")]
        )
        if not src:
            return
        try:
            with open(src, "rb") as f:
                data = f.read()
            out = convert_r6_animation_to_r15(data)
            base = os.path.splitext(os.path.basename(src))[0] + "_R15.rbxmx"
            dest = filedialog.asksaveasfilename(
                parent=self, title="Save R15 Animation", initialfile=base,
                defaultextension=".rbxmx", filetypes=[("RBXMX Animation", "*.rbxmx"), ("All files", "*.*")]
            )
            if not dest:
                return
            with open(dest, "wb") as f:
                f.write(out)
            messagebox.showinfo("R6 → R15", f"R6 animation retargeted to R15.\n\n{dest}", parent=self)
        except Exception as e:
            messagebox.showerror("R6 → R15", f"Could not convert animation:\n{e}", parent=self)

    def _cc_state_path(self):
        return os.path.join(DATA_DIR, "routils_cconfigs_state.json")

    def _cc_load_applied_state(self):
        try:
            with open(self._cc_state_path(), "r", encoding="utf-8") as f:
                data = json.load(f)
            self.cc_applied_caches = data if isinstance(data, list) else []
        except Exception:
            self.cc_applied_caches = []

    def _cc_save_applied_state(self):
        try:
            with open(self._cc_state_path(), "w", encoding="utf-8") as f:
                json.dump(self.cc_applied_caches, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _cc_record_applied_caches(self, caches):
        """Remember the cache items successfully applied to the current DB."""
        if not caches:
            return
        now = datetime.now().isoformat(timespec="seconds")
        by_hash = {}
        for item in self.cc_applied_caches:
            if isinstance(item, dict):
                h = str(item.get("hash", "")).lower()
                if h:
                    by_hash[h] = item
        for item in caches:
            if not isinstance(item, dict):
                continue
            h = re.sub(r"[^0-9A-Fa-f]", "", str(item.get("hash", ""))).lower()
            if not h:
                continue
            by_hash[h] = {
                "hash": h,
                "name": str(item.get("name", "")),
                "applied_at": str(item.get("applied_at") or now),
            }
        self.cc_applied_caches = list(by_hash.values())
        self._cc_save_applied_state()
        if hasattr(self, "cc_cache_count_label"):
            self.cc_cache_count_label.config(
                text=f"Current applied caches: {len(self.cc_applied_caches)}"
            )

    def _cc_safe_name(self, name):
        name = re.sub(r'[<>:"/\\\\|?*]', "_", str(name)).strip().rstrip(".")
        return name or "Config"

    def _cc_unique_path(self, directory, filename):
        base, ext = os.path.splitext(filename)
        path = os.path.join(directory, filename)
        i = 1
        while os.path.exists(path):
            path = os.path.join(directory, f"{base} ({i}){ext}")
            i += 1
        return path

    def _cc_snapshot_database(self, src_db, dst_db):
        """Make a consistent SQLite snapshot when possible, with a file-copy fallback."""
        if not os.path.isfile(src_db):
            raise FileNotFoundError(f"Database not found:\n{src_db}")
        os.makedirs(os.path.dirname(dst_db), exist_ok=True)
        try:
            src_conn = sqlite3.connect(src_db, timeout=3)
            dst_conn = sqlite3.connect(dst_db)
            with dst_conn:
                src_conn.backup(dst_conn)
            dst_conn.close()
            src_conn.close()
        except Exception:
            try:
                if os.path.exists(dst_db):
                    os.remove(dst_db)
            except Exception:
                pass
            shutil.copy2(src_db, dst_db)

    def _cc_make_package(self, destination, name):
        """Create a portable CConfigs DB package containing the DB and applied-cache metadata."""
        src_db = getattr(self, "db_path", None)
        if not src_db or not os.path.isfile(src_db):
            raise FileNotFoundError("The current rbx-storage.db does not exist.")
        with tempfile.TemporaryDirectory(prefix="routils_cc_") as td:
            snap = os.path.join(td, "rbx-storage.db")
            self._cc_snapshot_database(src_db, snap)
            metadata = {
                "format": "RoUtils CConfigs",
                "version": 1,
                "name": name,
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "source_db": os.path.abspath(src_db),
                "applied_caches": list(self.cc_applied_caches),
            }
            with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as z:
                z.write(snap, "rbx-storage.db")
                z.writestr(
                    "config.json",
                    json.dumps(metadata, ensure_ascii=False, indent=2),
                )

    def _cc_read_package_info(self, path):
        if path.lower().endswith(".db"):
            conn = sqlite3.connect(path, timeout=3)
            try:
                conn.execute("PRAGMA schema_version").fetchone()
            finally:
                conn.close()
            return {
                "name": os.path.splitext(os.path.basename(path))[0],
                "created_at": "",
                "applied_caches": [],
                "raw_db": True,
            }
        with zipfile.ZipFile(path, "r") as z:
            if "config.json" not in z.namelist():
                raise ValueError("This is not a valid CConfigs package.")
            info = json.loads(z.read("config.json").decode("utf-8"))
            if "rbx-storage.db" not in z.namelist():
                raise ValueError("CConfigs package is missing rbx-storage.db.")
            info["raw_db"] = False
            return info

    def _cc_scan_packages(self):
        out = []
        try:
            names = os.listdir(self.cconfigs_dir)
        except Exception:
            names = []
        for fname in names:
            if not fname.lower().endswith((".ccdb", ".db")):
                continue
            path = os.path.join(self.cconfigs_dir, fname)
            try:
                info = self._cc_read_package_info(path)
            except Exception:
                info = {
                    "name": os.path.splitext(fname)[0],
                    "created_at": "",
                    "applied_caches": [],
                }
            info["_path"] = path
            info["_file"] = fname
            out.append(info)
        out.sort(key=lambda x: str(x.get("name", "")).lower())
        return out

    def _cc_refresh_list(self, select_path=None):
        if not hasattr(self, "cc_tree"):
            return
        self.cc_tree.delete(*self.cc_tree.get_children())
        packages = self._cc_scan_packages()
        wanted = os.path.abspath(select_path) if select_path else None
        selected_iid = None
        for i, info in enumerate(packages):
            iid = str(i)
            caches = info.get("applied_caches") or []
            self.cc_tree.insert(
                "", "end", iid=iid,
                values=(
                    info.get("name", os.path.splitext(info.get("_file", ""))[0]),
                    info.get("created_at", ""),
                    len(caches),
                    info.get("_file", ""),
                ),
            )
            if wanted and os.path.abspath(info.get("_path", "")) == wanted:
                selected_iid = iid
        if selected_iid is not None:
            self.cc_tree.selection_set(selected_iid)
            self.cc_tree.focus(selected_iid)
        self._cc_show_selected()

    def _cc_selected_info(self):
        sel = self.cc_tree.selection() if hasattr(self, "cc_tree") else ()
        if not sel:
            return None
        try:
            idx = int(sel[0])
        except Exception:
            return None
        packages = self._cc_scan_packages()
        return packages[idx] if 0 <= idx < len(packages) else None

    def _cc_show_selected(self, _event=None):
        if not hasattr(self, "cc_details"):
            return
        info = self._cc_selected_info()
        self.cc_details.configure(state="normal")
        self.cc_details.delete("1.0", tk.END)
        if not info:
            self.cc_details.insert(tk.END, "Select a saved DB to view its details.")
        else:
            caches = info.get("applied_caches") or []
            lines = [
                f"Config: {info.get('name', '')}",
                f"Created: {info.get('created_at', '')}",
                f"File: {info.get('_file', '')}",
                "",
                f"Applied caches: {len(caches)}",
                "",
            ]
            if caches:
                for i, cache in enumerate(caches, 1):
                    name = cache.get("name", "(unnamed)")
                    h = cache.get("hash", "")
                    at = cache.get("applied_at", "")
                    lines.append(f"{i}. {name}")
                    lines.append(f"   Hash: {h}")
                    if at:
                        lines.append(f"   Applied: {at}")
            else:
                lines.append("No cache applications were recorded for this config.")
            self.cc_details.insert(tk.END, "\n".join(lines))
        self.cc_details.configure(state="disabled")

    def _cc_save_db(self):
        name = simpledialog.askstring(
            "Save DB", "Enter a name for this CConfigs DB:",
            parent=self
        )
        if not name:
            return
        name = self._cc_safe_name(name)
        path = self._cc_unique_path(self.cconfigs_dir, name + ".ccdb")
        try:
            self._cc_make_package(path, name)
        except Exception as e:
            messagebox.showerror("CConfigs", f"Failed to save DB:\n{e}", parent=self)
            return
        self._cc_refresh_list(select_path=path)
        messagebox.showinfo(
            "CConfigs",
            f"DB saved as '{os.path.basename(path)}'.\n\n"
            f"Recorded applied caches: {len(self.cc_applied_caches)}",
            parent=self,
        )

    def _cc_upload_db(self):
        path = filedialog.askopenfilename(
            parent=self,
            title="Upload DB",
            filetypes=[("Database files", "*.db *.ccdb"), ("SQLite DB", "*.db"), ("CConfigs DB", "*.ccdb"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            info = self._cc_read_package_info(path)
            if path.lower().endswith(".db"):
                name = self._cc_safe_name(os.path.splitext(os.path.basename(path))[0] or "rbx-storage")
                dest = self._cc_unique_path(self.cconfigs_dir, name + ".db")
            else:
                name = self._cc_safe_name(info.get("name") or os.path.splitext(os.path.basename(path))[0])
                dest = self._cc_unique_path(self.cconfigs_dir, name + ".ccdb")
            shutil.copy2(path, dest)
        except Exception as e:
            messagebox.showerror("CConfigs", f"Failed to upload DB:\n{e}", parent=self)
            return
        self._cc_refresh_list(select_path=dest)
        messagebox.showinfo("CConfigs", f"Uploaded '{os.path.basename(dest)}'.", parent=self)

    def _cc_apply_db(self):
        info = self._cc_selected_info()
        if not info:
            messagebox.showinfo("CConfigs", "Select a saved DB first.", parent=self)
            return
        if not messagebox.askyesno(
            "Apply DB",
            f"Apply '{info.get('name', '')}' to Roblox?\n\n"
            "This will delete rbx-storage.db, rbx-storage.db-shm, rbx-storage.db-wal and rbx-storage.id, then install only rbx-storage.db.",
            parent=self,
        ):
            return

        was_watching = self.watching
        if was_watching:
            self._stop_watching()
        temp_source = None
        try:
            with tempfile.NamedTemporaryFile(prefix="routils_cc_apply_", suffix=".db", delete=False) as tf:
                temp_source = tf.name

            if info.get("raw_db") or info.get("_file", "").lower().endswith(".db"):
                shutil.copy2(info["_path"], temp_source)
            else:
                with tempfile.TemporaryDirectory(prefix="routils_apply_cc_") as td:
                    with zipfile.ZipFile(info["_path"], "r") as z:
                        z.extract("rbx-storage.db", td)
                    shutil.copy2(os.path.join(td, "rbx-storage.db"), temp_source)

            conn = sqlite3.connect(temp_source, timeout=3)
            conn.execute("PRAGMA schema_version").fetchone()
            conn.close()

            self._install_selected_db(temp_source)
            self.cc_applied_caches = list(info.get("applied_caches") or [])
            self._cc_save_applied_state()
            self._update_status()
            if was_watching:
                self._start_watching()
        except Exception as e:
            messagebox.showerror(
                "CConfigs",
                "Failed to apply DB.\n\n"
                f"{e}\n\nClose Roblox and try again. No force-delete was used.",
                parent=self,
            )
            if was_watching:
                self._start_watching()
            return
        finally:
            if temp_source:
                try:
                    os.remove(temp_source)
                except Exception:
                    pass

        if hasattr(self, "cc_cache_count_label"):
            self.cc_cache_count_label.config(
                text=f"Current applied caches: {len(self.cc_applied_caches)}"
            )
        messagebox.showinfo(
            "CConfigs",
            f"Applied '{info.get('name', '')}'.\n"
            f"Recorded caches: {len(self.cc_applied_caches)}\n\n"
            "Installed only rbx-storage.db.",
            parent=self,
        )

    def _cc_export_db(self):
        info = self._cc_selected_info()
        if not info:
            messagebox.showinfo("CConfigs", "Select a saved DB first.", parent=self)
            return
        base = self._cc_safe_name(info.get("name") or "config") + ".db"
        path = filedialog.asksaveasfilename(
            parent=self,
            title="Export DB as normal .db",
            initialfile=base,
            defaultextension=".db",
            filetypes=[("SQLite DB", "*.db"), ("All files", "*.*")],
        )
        if not path:
            return
        temp_source = None
        try:
            with tempfile.NamedTemporaryFile(prefix="routils_cc_export_", suffix=".db", delete=False) as tf:
                temp_source = tf.name
            if info.get("raw_db") or info.get("_file", "").lower().endswith(".db"):
                shutil.copy2(info["_path"], temp_source)
            else:
                with zipfile.ZipFile(info["_path"], "r") as z:
                    with z.open("rbx-storage.db") as src, open(temp_source, "wb") as dst:
                        shutil.copyfileobj(src, dst)
            conn = sqlite3.connect(temp_source, timeout=3)
            conn.execute("PRAGMA schema_version").fetchone()
            conn.close()
            shutil.copy2(temp_source, path)
        except Exception as e:
            messagebox.showerror("CConfigs", f"Failed to export DB:\n{e}", parent=self)
            return
        finally:
            if temp_source:
                try:
                    os.remove(temp_source)
                except Exception:
                    pass
        messagebox.showinfo("CConfigs", f"Normal .db exported:\n{path}", parent=self)

    def _cc_delete_db(self):
        info = self._cc_selected_info()
        if not info:
            return
        if not messagebox.askyesno(
            "Delete DB",
            f"Delete saved DB '{info.get('name', '')}'?",
            parent=self,
        ):
            return
        try:
            os.remove(info["_path"])
        except Exception as e:
            messagebox.showerror("CConfigs", f"Failed to delete DB:\n{e}", parent=self)
            return
        self._cc_refresh_list()

    def _build_cconfigs_tab(self):
        tab = ttk.Frame(self.nb, padding=0)
        self.nb.add(tab, text="CConfigs")
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)

        head = ttk.Frame(tab)
        head.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(head, text="CConfigs", font=("Segoe UI Semibold", 15)).pack(side="left")
        self.cc_cache_count_label = ttk.Label(
            head,
            text=f"Current applied caches: {len(self.cc_applied_caches)}",
            foreground="#9aa0a6",
        )
        self.cc_cache_count_label.pack(side="right")

        bar = ttk.Frame(tab)
        bar.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        for label, command in (
            ("Save DB", self._cc_save_db),
            ("Upload DB", self._cc_upload_db),
            ("Apply DB", self._cc_apply_db),
            ("Export DB", self._cc_export_db),
            ("Delete DB", self._cc_delete_db),
            ("Refresh", lambda: self._cc_refresh_list()),
        ):
            ttk.Button(bar, text=label, command=command).pack(side="left", padx=(0, 6))

        paned = ttk.PanedWindow(tab, orient="vertical")
        paned.grid(row=2, column=0, sticky="nsew")
        top = ttk.Frame(paned)
        bottom = ttk.Frame(paned)
        paned.add(top, weight=3)
        paned.add(bottom, weight=2)

        columns = ("name", "created", "caches", "file")
        self.cc_tree = ttk.Treeview(top, columns=columns, show="headings", selectmode="browse")
        self.cc_tree.heading("name", text="CONFIG")
        self.cc_tree.heading("created", text="CREATED")
        self.cc_tree.heading("caches", text="APPLIED")
        self.cc_tree.heading("file", text="FILE")
        self.cc_tree.column("name", width=240, anchor="w")
        self.cc_tree.column("created", width=160, anchor="w")
        self.cc_tree.column("caches", width=80, anchor="center")
        self.cc_tree.column("file", width=280, anchor="w")
        self.cc_tree.pack(side="left", fill="both", expand=True)
        cc_scroll = ttk.Scrollbar(top, orient="vertical", command=self.cc_tree.yview)
        cc_scroll.pack(side="right", fill="y")
        self.cc_tree.configure(yscrollcommand=cc_scroll.set)
        self.cc_tree.bind("<<TreeviewSelect>>", self._cc_show_selected)
        self.cc_tree.bind("<Double-1>", lambda _e: self._cc_apply_db())

        ttk.Label(bottom, text="Saved DB details", font=("Segoe UI Semibold", 10)).pack(anchor="w", pady=(4, 4))
        self.cc_details = tk.Text(
            bottom, wrap="word", height=8, font=("Consolas", 9),
            bg="#252526", fg="#d4d4d4", insertbackground="#ffffff",
            selectbackground="#007acc", selectforeground="#ffffff",
            relief="flat", bd=0,
        )
        self.cc_details.pack(fill="both", expand=True)
        self.cc_details.configure(state="disabled")
        self._cc_refresh_list()

    def _open_selected_roblox(self):
        path = self.settings.get("roblox_path", "") if hasattr(self, "settings") else ""
        if not path:
            try:
                path = self.roblox_path_var.get()
            except Exception:
                path = ""
        if os.path.isdir(path):
            candidate = os.path.join(path, "RobloxPlayerBeta.exe")
            if os.path.isfile(candidate):
                path = candidate
        if not path or os.path.basename(path).lower() != "robloxplayerbeta.exe" or not os.path.isfile(path):
            try:
                messagebox.showwarning("RoUtils", "Please select a valid RobloxPlayerBeta.exe first.")
            except Exception:
                pass
            return
        try:
            subprocess.Popen([path], shell=False)
        except Exception as e:
            try:
                messagebox.showerror("RoUtils", f"Could not open Roblox:\n{e}")
            except Exception:
                pass

    def _enable_beta_classic_theme(self):
        path = self.settings.get("roblox_path", "") if hasattr(self, "settings") else ""
        if not path:
            try:
                path = self.roblox_path_var.get()
            except Exception:
                path = ""
        if os.path.isdir(path):
            candidate = os.path.join(path, "RobloxPlayerBeta.exe")
            if os.path.isfile(candidate):
                path = candidate
        if not path or os.path.basename(path).lower() != "robloxplayerbeta.exe" or not os.path.isfile(path):
            try:
                messagebox.showwarning("RoUtils", "Please select a valid RobloxPlayerBeta.exe first.")
            except Exception:
                pass
            return
        try:
            import winshell
            from win32com.client import Dispatch
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "Roblox (Classic).lnk")
            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = path
            shortcut.Arguments = '-channel "zrobloxplustheme"'
            shortcut.WorkingDirectory = os.path.dirname(path)
            shortcut.IconLocation = path + ",0"
            shortcut.save()
            messagebox.showinfo("RoUtils", "Classic Roblox Shortcut added to Desktop")
        except Exception:

            try:
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                shortcut_path = os.path.join(desktop, "Roblox (Classic).lnk")
                shell = __import__("win32com.client", fromlist=["Dispatch"]).Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = path
                shortcut.Arguments = '-channel "zrobloxplustheme"'
                shortcut.WorkingDirectory = os.path.dirname(path)
                shortcut.IconLocation = path + ",0"
                shortcut.save()
                messagebox.showinfo("RoUtils", "Classic Roblox Shortcut added to Desktop")
            except Exception as e:
                messagebox.showerror("RoUtils", f"Could not create shortcut:\n{e}")

    def _build_utils_tab(self):
        tab_outer = _ScrollableTab(self.nb, padding=0)
        tab = tab_outer.inner
        self.nb.insert(2, tab_outer, text="Modifications")
        tab.columnconfigure(0, weight=1)
        ttk.Label(tab, text="Modifications", font=("Segoe UI Semibold", 15)).grid(row=0, column=0, sticky="w")
        ttk.Label(tab, text="Roblox Modifications", foreground="#9aa0a6").grid(row=1, column=0, sticky="w", pady=(0, 14))
        anim = ttk.LabelFrame(tab, text="Converters", padding=14); anim.grid(row=2,column=0,sticky="ew",pady=(0,10))
        ttk.Button(anim, text="R6 Animation → R15", command=self._utils_r6_to_r15).pack(anchor="w", pady=(0,6))
        ttk.Button(anim, text="Roblox File Converter (.rbxm / .rbxh / .rbxmx)", command=self._utils_roblox_file_convert).pack(anchor="w")
        mesh = ttk.LabelFrame(tab, text="Default Mesh Changer", padding=14); mesh.grid(row=3,column=0,sticky="ew",pady=(0,10))
        ttk.Label(mesh, text="It allows you to change the default R6 Meshes.").grid(row=0,column=0,columnspan=3,sticky="w",pady=(0,8))
        pathrow=ttk.Frame(mesh); pathrow.grid(row=1,column=0,columnspan=3,sticky="ew",pady=(0,10)); pathrow.columnconfigure(0,weight=1)
        self.roblox_path_var=tk.StringVar(value=self.settings.get("roblox_path",""))
        ttk.Entry(pathrow,textvariable=self.roblox_path_var,state="readonly").grid(row=0,column=0,sticky="ew")
        ttk.Button(pathrow,text="Choose",command=self._choose_roblox_path).grid(row=0,column=1,padx=(6,0))
        ttk.Button(pathrow,text="Open Selected Roblox",command=self._open_selected_roblox).grid(row=0,column=2,padx=(6,0))
        self.mesh_rows={}
        for i,name in enumerate(("Head.mesh","leftarm.mesh","leftleg.mesh","rightarm.mesh","rightleg.mesh","torso.mesh"),start=2):
            ttk.Label(mesh,text=name).grid(row=i,column=0,sticky="w",pady=3)
            ttk.Button(mesh,text="Delete",command=lambda n=name:self._delete_default_mesh(n)).grid(row=i,column=1,padx=5)
            ttk.Button(mesh,text="Choose",command=lambda n=name:self._choose_default_mesh(n)).grid(row=i,column=2)
        mesh.columnconfigure(0,weight=1)
        classic = ttk.LabelFrame(tab, text="Classic Theme", padding=14)
        classic.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(classic, text="Create a Roblox (Classic) desktop shortcut using the selected RobloxPlayerBeta.exe.").pack(anchor="w", pady=(0, 8))
        ttk.Button(classic, text="Enable Beta Classic Theme", command=self._enable_beta_classic_theme).pack(anchor="w")
        conv=ttk.LabelFrame(tab,text="Mesh to OBJ",padding=14); conv.grid(row=5,column=0,sticky="ew")
        ttk.Label(conv,text="Convert a Roblox .mesh file to .obj.").pack(anchor="w",pady=(0,8))
        ttk.Button(conv,text="Mesh to OBJ",command=self._utils_mesh_to_obj).pack(anchor="w")
        fps_box=ttk.LabelFrame(tab,text="FPS",padding=(10,8)); fps_box.grid(row=6,column=0,sticky="ew",pady=(12,0))
        self.fps_value_label=ttk.Label(fps_box,font=("Segoe UI Semibold",10)); self.fps_value_label.pack(anchor="w")
        self.fps_pid_label=ttk.Label(fps_box,text="PID: Waiting for Roblox...",foreground="#9aa0a6"); self.fps_pid_label.pack(anchor="w",pady=(0,4))
        def _fps_ui(value=None):


            fps = int(round(float(self.fps_limit.get() if value is None else value)))
            fps = max(0, min(240, fps))
            if self.fps_limit.get() != fps:
                self.fps_limit.set(fps)
            self.fps_value_label.config(text="FPS: Unlocked" if fps == 0 else f"FPS: {fps}")

        def _fps_slider_released(_event=None):


            if getattr(self, "_fps_release_job", None):
                try:
                    self.after_cancel(self._fps_release_job)
                except Exception:
                    pass
            self._fps_release_job = self.after(80, self._apply_fps_after_slider)

        ttk.Scale(fps_box, from_=0, to=240, orient="horizontal", variable=self.fps_limit, command=_fps_ui).pack(fill="x")
        self._fps_scale_widget = fps_box.winfo_children()[-1]
        self._fps_scale_widget.bind("<ButtonRelease-1>", _fps_slider_released, add="+")
        ttk.Label(fps_box, text="FPS Changer", font=("Segoe UI",8), foreground="#9aa0a6").pack(anchor="w")
        _fps_ui()

    def _version_path(self):
        return os.path.join(DATA_DIR, "version.txt")

    def _reset_version_file(self):
        try:
            vp = self._version_path()
            if os.path.exists(vp):
                try:
                    os.remove(vp)
                except Exception:
                    pass
            with open(vp, "w", encoding="utf-8") as f:
                f.write(APP_VERSION)
        except Exception:
            pass

    def _local_version(self):
        try:
            if not os.path.exists(self._version_path()):
                with open(self._version_path(), "w", encoding="utf-8") as f:
                    f.write(APP_VERSION)
            with open(self._version_path(), encoding="utf-8") as f:
                return f.read().strip() or APP_VERSION
        except Exception:
            return APP_VERSION

    def _build_home_tab(self):
        tab = ttk.Frame(self.nb, padding=0)
        self.nb.insert(0, tab, text="Home")
        ttk.Label(tab, text="RoUtils", font=("Segoe UI Semibold", 20)).pack(anchor="w")
        ttk.Label(tab, text=f"Welcome Dear, {platform.node() or os.environ.get('COMPUTERNAME', 'System')}", font=("Segoe UI Semibold", 14)).pack(anchor="w", pady=(14, 14))

        links = ttk.Frame(tab)
        links.pack(anchor="w", fill="x")
        github = tk.Label(links, text="Official Github Link: https://github.com/offp001/routils",
                          fg="#4da6ff", bg=_CURRENT_PALETTE["bg_dark"], cursor="hand2")
        github.pack(anchor="w", pady=2)
        github.bind("<Button-1>", lambda _e: webbrowser.open("https://github.com/offp001/routils"))
        github.bind("<Enter>", lambda _e: github.config(font=("Segoe UI", 9, "underline")))
        github.bind("<Leave>", lambda _e: github.config(font=("Segoe UI", 9)))

        discord = tk.Label(links, text="Official Discord Invite: https://discord.gg/849VtrYhm2 (Join to Support me)",
                           fg="#4da6ff", bg=_CURRENT_PALETTE["bg_dark"], cursor="hand2")
        discord.pack(anchor="w", pady=2)
        discord.bind("<Button-1>", lambda _e: webbrowser.open("https://discord.gg/849VtrYhm2"))
        discord.bind("<Enter>", lambda _e: discord.config(font=("Segoe UI", 9, "underline")))
        discord.bind("<Leave>", lambda _e: discord.config(font=("Segoe UI", 9)))

        ttk.Separator(tab).pack(fill="x", pady=18)
        version_row = ttk.Frame(tab)
        version_row.pack(anchor="w")
        ttk.Label(version_row, text="Version: ", font=("Comic Sans MS", 10, "bold")).pack(side="left")
        self.home_version_value = ttk.Label(version_row, text=self._local_version(), font=("Comic Sans MS", 10, "bold"))
        self.home_version_value.pack(side="left")
        self.home_version_state = ttk.Label(version_row, text="Checking", font=("Comic Sans MS", 10, "bold"))
        self.home_version_state.pack(side="left", padx=(6, 0))
        self.home_version_var = tk.StringVar(value=f'Version: {self._local_version()} (Checking)')

    def _extract_profile_from_cookies(self):
        path=os.path.join(os.environ.get("LOCALAPPDATA", ""),"Roblox","LocalStorage","RobloxCookies.dat")
        if not os.path.isfile(path): return None, None
        try:
            raw=open(path,"rb").read()
            text=raw.decode("utf-8",errors="ignore")

            uid=None; username=None
            for pat in (r'"userId"\s*[:=]\s*"?(\d+)',r'"UserId"\s*[:=]\s*"?(\d+)',r'userid[^0-9]{0,30}(\d+)'):
                m=re.search(pat,text,re.I)
                if m: uid=m.group(1); break
            for pat in (r'"username"\s*[:=]\s*"([^"\\]+)',r'"name"\s*[:=]\s*"([^"\\]+)'):
                m=re.search(pat,text,re.I)
                if m: username=m.group(1); break

            if not uid:
                for token in re.findall(r'[A-Za-z0-9+/=]{24,}',text):
                    try:
                        t=base64.b64decode(token).decode("utf-8",errors="ignore")
                        m=re.search(r'"(?:userId|UserId)"\s*:\s*"?(\d+)',t)
                        if m: uid=m.group(1)
                        m2=re.search(r'"(?:username|name)"\s*:\s*"([^"\\]+)',t,re.I)
                        if m2: username=m2.group(1)
                        if uid: break
                    except Exception: pass
            return username, uid
        except Exception: return None, None

    def _detect_roblox_profile(self):
        username, uid = self._extract_profile_from_cookies()
        if username:
            self.settings["roblox_username"] = username
        if uid:
            self.settings["roblox_user_id"] = uid
        save_settings(self.settings)

    def _start_profile_detection(self):
        def worker():
            self._detect_roblox_profile()
        threading.Thread(target=worker,daemon=True).start()


    def _start_version_check(self):
        def worker():
            current=self._local_version()
            self.after(0,lambda:(self.home_version_value.config(text=current), self.home_version_state.config(text="Checking", foreground="#f2c94c"), self.home_version_var.set(f"Version: {current} (Checking)")))
            latest=current
            try:

                req=urllib.request.Request("https://github.com/offp001/routils/releases/latest",method="HEAD")
                with urllib.request.urlopen(req,timeout=8) as r:
                    m=re.search(r'/tag/([^/]+)$',r.geturl()); latest=m.group(1) if m else current
            except Exception: pass
            def done():
                state="Latest" if latest==current else "Outdated"
                color="#65d98b" if state == "Latest" else "#ff5f57"
                self.home_version_value.config(text=current)
                self.home_version_state.config(text=state, foreground=color)
                self.home_version_var.set(f"Version: {current} ({state})")
            self.after(0,done)
        threading.Thread(target=worker,daemon=True).start()


    def _reorder_tabs(self):
        order=["Home","Cache","FFlags","Modifications","CConfigs","Subplace Joiner","History","Client","Themes","Settings"]
        for i,name in enumerate(order):
            for tab_id in self.nb.tabs():
                if self.nb.tab(tab_id,"text")==name:
                    self.nb.insert(i,tab_id)
                    break

    def _fflag_json_editor(self):
        dlg=tk.Toplevel(self); dlg.title("JSON Editor"); dlg.geometry("620x460"); theme_toplevel(dlg)
        txt=tk.Text(dlg,wrap="none",font=("Consolas",10),bg=_CURRENT_PALETTE["bg_medium"],fg=_CURRENT_PALETTE["fg"],insertbackground="#fff"); txt.pack(fill="both",expand=True,padx=10,pady=10)
        ttk.Button(dlg,text="Add",command=lambda:self._add_json_editor_value(txt,dlg)).pack(pady=(0,10))
    def _add_json_editor_value(self,txt,dlg):
        try: data=json.loads(txt.get("1.0","end")); assert isinstance(data,(dict,list))
        except Exception as e: messagebox.showerror("JSON Editor",f"Invalid JSON:\n{e}",parent=dlg); return
        if isinstance(data,dict):
            for n,v in data.items(): self.fflag_flags.append({"name":fflag_strip_prefix(str(n)),"value":str(v).lower() if isinstance(v,bool) else str(v),"type":fflag_infer_type(v)})
        else:
            for x in data:
                if isinstance(x,dict) and x.get("name") is not None: self.fflag_flags.append({"name":fflag_strip_prefix(str(x["name"])),"value":str(x.get("value","")),"type":x.get("type") or fflag_infer_type(x.get("value",""))})
        self._save_fflag_flags(); self._refresh_fflag_list(); dlg.destroy()
    def _refresh_json_list(self):
        if not hasattr(self,"json_tree"): return
        self.json_tree.delete(0,"end")
        for n in sorted(os.listdir(self.jsons_dir)) if os.path.isdir(self.jsons_dir) else []:
            if n.lower().endswith(".json"): self.json_tree.insert("end",n)
    def _apply_selected_json(self):
        if not hasattr(self,"json_tree"): return
        sel=self.json_tree.curselection()
        if not sel: return
        path=os.path.join(self.jsons_dir,self.json_tree.get(sel[0]))
        try:
            with open(path,"r",encoding="utf-8") as f:data=json.load(f)
            flags=[]
            if isinstance(data,dict):
                flags=[{"name":fflag_strip_prefix(str(k)),"value":str(v).lower() if isinstance(v,bool) else str(v),"type":fflag_infer_type(v)} for k,v in data.items()]
            elif isinstance(data,list):
                flags=[{"name":fflag_strip_prefix(str(x["name"])),"value":str(x.get("value","")),"type":x.get("type") or fflag_infer_type(x.get("value",""))} for x in data if isinstance(x,dict) and x.get("name") is not None]
            else: raise ValueError("JSON must be an object or array.")
            self.fflag_flags=flags; self._save_fflag_flags(); self._refresh_fflag_list(); messagebox.showinfo("FFlags",f"Applied {len(flags)} flags from {os.path.basename(path)}.",parent=self)
        except Exception as e: messagebox.showerror("FFlags",f"Failed to apply JSON:\n{e}",parent=self)
    def _choose_roblox_path(self):
        path=filedialog.askopenfilename(parent=self,title="Select RobloxPlayerBeta.exe",filetypes=[("Roblox Player","RobloxPlayerBeta.exe"),("Executable","*.exe")])
        if path and os.path.basename(path).lower()=="robloxplayerbeta.exe": self.roblox_path_var.set(path); self.settings["roblox_path"]=path; self._save_settings()
    def _default_mesh_path(self,name):
        root=self.roblox_path_var.get().strip();
        if not root or os.path.basename(root).lower() != "robloxplayerbeta.exe": return None
        root=os.path.dirname(root)
        folder="heads" if name.lower()=="head.mesh" else "meshes"
        return os.path.join(root,"content","avatar",folder,name)
    def _choose_default_mesh(self,name):
        target=self._default_mesh_path(name)
        if not target: messagebox.showwarning("Default Mesh Changer","Choose RobloxPlayerBeta.exe first.",parent=self); return
        src=filedialog.askopenfilename(parent=self,title=f"Choose replacement for {name}",filetypes=[("Mesh files","*.mesh"),("All files","*.*")])
        if not src:return
        try:
            os.makedirs(os.path.dirname(target),exist_ok=True)
            if os.path.abspath(src).lower()==os.path.abspath(target).lower(): return
            if os.path.exists(target): os.remove(target)
            shutil.copy2(src,target)
        except Exception as e: messagebox.showerror("Default Mesh Changer",f"Failed:\n{e}",parent=self)
    def _delete_default_mesh(self,name):
        target=self._default_mesh_path(name)
        if not target:return
        try:
            if os.path.exists(target): os.remove(target)
        except Exception as e: messagebox.showerror("Default Mesh Changer",f"Failed:\n{e}",parent=self)
    def _utils_mesh_to_obj(self):
        src=filedialog.askopenfilename(parent=self,title="Select Roblox Mesh",filetypes=[("Roblox Mesh","*.mesh"),("All files","*.*")])
        if not src:return
        out=os.path.splitext(src)[0]+".obj"
        try:
            with open(src,"rb") as f:data=f.read()
            ver=_mesh_header(data).replace("version ","") or "unknown"
            print(f'Selected Mesh Version "{ver}"')
            print("Converting")
            convert(data,out)
            print(f"Converted: {out}")
            
        except Exception as e: messagebox.showerror("Mesh to OBJ",f"Conversion failed:\n{e}",parent=self)
    def _utils_roblox_file_convert(self):
        src = filedialog.askopenfilename(
            parent=self,
            title="Select Roblox File",
            filetypes=[
                ("Roblox Files", "*.rbxm *.rbxh *.rbxmx"),
                ("RBXM", "*.rbxm"),
                ("RBXH", "*.rbxh"),
                ("RBXMX", "*.rbxmx"),
                ("All files", "*.*"),
            ],
        )
        if not src:
            return
        try:
            with open(src, "rb") as f:
                content = f.read()
            filename, ext = os.path.splitext(os.path.basename(src))
            ext = ext.lower()
            if ext not in (".rbxm", ".rbxh", ".rbxmx"):
                messagebox.showwarning("Roblox File Converter", "Please select an .rbxm, .rbxh or .rbxmx file.", parent=self)
                return

            is_xml = b"<roblox" in content[:100]

            if ext == ".rbxm":
                new_ext = ".rbxh"
                output_data = content
            elif ext == ".rbxh":
                new_ext = ".rbxm"
                binary_start = content.find(b"<roblox!")
                xml_start = content.find(b"<roblox")
                if binary_start != -1:
                    output_data = content[binary_start:]
                elif xml_start != -1:
                    output_data = content[xml_start:]
                else:
                    output_data = content
            else:
                new_ext = ".rbxh"
                output_data = content

            output_path = os.path.join(os.path.dirname(src), f"{filename}_converted{new_ext}")
            with open(output_path, "wb") as f:
                f.write(output_data)
            messagebox.showinfo(
                "Roblox File Converter",
                f"Converted successfully.\\n\\n{os.path.basename(output_path)}",
                parent=self,
            )
        except Exception as e:
            messagebox.showerror("Roblox File Converter", f"Conversion failed:\\n{e}", parent=self)




    def _history_load(self):
        try:
            if not os.path.exists(HISTORY_PATH):
                return []
            with open(HISTORY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _history_save(self, data):
        try:
            tmp = HISTORY_PATH + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp, HISTORY_PATH)
        except Exception:
            pass

    def _resolve_history_game_name(self, place_id):
        place_id = str(place_id or "").strip()
        if not place_id.isdigit():
            return None

        for url in (
            f"https://games.roblox.com/v1/games/multiget-place-details?placeIds={place_id}",
            f"https://develop.roblox.com/v1/places/{place_id}",
        ):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "RoUtils/3.3"})
                with urllib.request.urlopen(req, timeout=8) as r:
                    data = json.load(r)
                if isinstance(data, list):
                    data = data[0] if data else {}
                name = str(data.get("name") or data.get("universeName") or "").strip()
                if name and not name.isdigit():
                    return name
            except Exception:
                pass

        try:
            req = urllib.request.Request(
                f"https://apis.roblox.com/universes/v1/places/{place_id}/universe",
                headers={"User-Agent": "RoUtils/3.3"},
            )
            with urllib.request.urlopen(req, timeout=8) as r:
                universe_id = json.load(r).get("universeId")
            if universe_id:
                req = urllib.request.Request(
                    f"https://games.roblox.com/v1/games?universeIds={universe_id}",
                    headers={"User-Agent": "RoUtils/3.3"},
                )
                with urllib.request.urlopen(req, timeout=8) as r:
                    data = json.load(r)
                rows = data.get("data", []) if isinstance(data, dict) else []
                if rows:
                    name = str(rows[0].get("name") or "").strip()
                    if name and not name.isdigit():
                        return name
        except Exception:
            pass
        return None

    def _history_resolve_existing_names(self):
        history = self._history_load()
        if not history:
            return
        pending = []
        for entry in history:
            pid = str(entry.get("place_id") or "").strip()
            old = str(entry.get("game_name") or "").strip()
            if pid.isdigit() and (
                not old
                or old == pid
                or old.lower().startswith("place ")
                or old.lower() in ("unknown game", "unknown", "game")
            ):
                pending.append((pid, entry))
        if not pending:
            return
        def worker():
            changed = False
            for pid, entry in pending:
                name = self._resolve_history_game_name(pid)
                if name:
                    entry["game_name"] = name
                    changed = True
            if changed:
                self._history_save(history)
                try:
                    self.after(0, self._history_refresh)
                except Exception:
                    pass
        threading.Thread(target=worker, daemon=True).start()

    def _history_add(self, place_id, job_id):
        place_id = str(place_id or "").strip()
        job_id = str(job_id or "").strip()
        if not place_id or not job_id:
            return
        key = (place_id, job_id.lower())
        if self._history_last_game == key:
            return
        self._history_last_game = key

        def worker():
            name = self._resolve_history_game_name(place_id) or place_id

            now = datetime.now()
            entry = {
                "game_name": name,
                "place_id": place_id,
                "job_id": job_id,
                "deeplink": f"roblox://experiences/start?placeId={place_id}&gameInstanceId={job_id}",
                "date": now.strftime("%d.%m.%Y"),
                "time": now.strftime("%H:%M:%S"),
                "timestamp": now.isoformat(timespec="seconds"),
            }
            history = self._history_load()
            history = [x for x in history if not (
                str(x.get("place_id")) == place_id and
                str(x.get("job_id", "")).lower() == job_id.lower()
            )]
            history.insert(0, entry)
            self._history_save(history)
            try:
                self.after(0, self._history_refresh)
            except Exception:
                pass

        threading.Thread(target=worker, daemon=True).start()

    def _detect_current_game(self, silent=True):
        logs_dir = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Roblox", "logs")
        uuid_re = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
        join_re = re.compile(rf"!\s*Joining\s+game\s+[\"']?({uuid_re})[\"']?\s+place\s+(\d+)", re.IGNORECASE)
        try:
            log_files = sorted([os.path.join(logs_dir, f) for f in os.listdir(logs_dir) if f.lower().endswith(".log")], key=lambda x: os.path.getmtime(x), reverse=True)[:30]
        except Exception:
            return None, None
        for log_path in log_files:
            try:
                with open(log_path, "r", encoding="utf-8", errors="ignore") as f: text=f.read()
            except Exception: continue
            matches=list(join_re.finditer(text))
            if matches:
                m=matches[-1]; return m.group(2), m.group(1)
        place_id=job_id=None
        for log_path in log_files:
            try:
                with open(log_path, "r", encoding="utf-8", errors="ignore") as f: text=f.read()
            except Exception: continue
            if not place_id:
                m=re.findall(r"\bplaceid\s*[:=]\s*(\d+)",text,re.IGNORECASE)
                if m: place_id=m[-1]
            if not job_id:
                m=re.findall(rf"\bjobId\s*[:=]\s*[\"']?({uuid_re})",text,re.IGNORECASE)
                if m: job_id=m[-1]
            if place_id and job_id: return place_id,job_id
        return None,None

    def _start_history_watcher(self):
        def worker():
            while True:
                try:
                    place_id, job_id = self._detect_current_game()
                    if place_id and job_id:
                        self.after(0, lambda p=place_id, j=job_id: self._history_add(p, j))
                except Exception:
                    pass
                time.sleep(1.5)
        threading.Thread(target=worker, daemon=True).start()

    def _build_history_tab(self):
        tab = ttk.Frame(self.nb, padding=0)
        self.nb.add(tab, text="History")
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)

        head = ttk.Frame(tab)
        head.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(head, text="Game History", font=("Segoe UI Semibold", 15)).pack(side="left")
        ttk.Button(head, text="Refresh", command=self._history_refresh).pack(side="right", padx=(6, 0))
        ttk.Button(head, text="Clear History", command=self._history_clear).pack(side="right")
        ttk.Label(tab, text="Game History.", foreground="#9aa0a6").grid(row=1, column=0, sticky="w", pady=(0, 8))

        outer = ttk.Frame(tab)
        outer.grid(row=2, column=0, sticky="nsew")
        outer.columnconfigure(0, weight=1); outer.rowconfigure(0, weight=1)
        self.history_canvas = tk.Canvas(outer, bg=_CURRENT_PALETTE["bg_dark"], highlightthickness=0, borderwidth=0)
        scroll = ttk.Scrollbar(outer, orient="vertical", command=self.history_canvas.yview)
        self.history_canvas.configure(yscrollcommand=scroll.set)
        self.history_canvas.grid(row=0, column=0, sticky="nsew"); scroll.grid(row=0, column=1, sticky="ns")
        self.history_inner = ttk.Frame(self.history_canvas)
        self.history_window = self.history_canvas.create_window((0, 0), window=self.history_inner, anchor="nw")
        self.history_inner.bind("<Configure>", lambda _e: self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all")))
        self.history_canvas.bind("<Configure>", lambda e: self.history_canvas.itemconfigure(self.history_window, width=e.width))
        self._history_refresh()

    def _history_refresh(self):
        if not hasattr(self, "history_inner"):
            return
        for child in self.history_inner.winfo_children():
            child.destroy()
        history = self._history_load()
        if not history:
            ttk.Label(self.history_inner, text="No games recorded yet.", foreground="#9aa0a6").pack(anchor="w", padx=12, pady=18)
            return
        header = ttk.Frame(self.history_inner); header.pack(fill="x", padx=6, pady=(0, 4))
        for col, weight in enumerate((3, 2, 3, 2, 0, 0)): header.columnconfigure(col, weight=weight)
        for col, label in enumerate(("GAME", "ID", "JOB ID", "DATE / TIME", "", "")):
            ttk.Label(header, text=label, foreground="#9aa0a6").grid(row=0, column=col, sticky="w", padx=6)
        for entry in history:
            row = ttk.Frame(self.history_inner); row.pack(fill="x", padx=6, pady=2)
            for col, weight in enumerate((3, 2, 3, 2, 0, 0)): row.columnconfigure(col, weight=weight)
            game=str(entry.get("game_name") or entry.get("place_id") or "Unknown Game")
            pid=str(entry.get("place_id") or ""); jid=str(entry.get("job_id") or "")
            dt=f"{entry.get('date','')} {entry.get('time','')}".strip()
            link=str(entry.get("deeplink") or f"roblox://experiences/start?placeId={pid}&gameInstanceId={jid}")
            ttk.Label(row, text=game, font=("Comic Sans MS", 10, "bold")).grid(row=0,column=0,sticky="w",padx=6,pady=5)
            ttk.Label(row, text=pid).grid(row=0,column=1,sticky="w",padx=6)
            ttk.Label(row, text=jid).grid(row=0,column=2,sticky="w",padx=6)
            ttk.Label(row, text=dt).grid(row=0,column=3,sticky="w",padx=6)
            ttk.Button(row,text="Copy Deeplink",command=lambda l=link:self._history_copy(l)).grid(row=0,column=4,padx=4)
            ttk.Button(row,text="Join",command=lambda l=link:self._history_join(l)).grid(row=0,column=5,padx=(2,6))

    def _history_copy(self, link):
        try:
            self.clipboard_clear(); self.clipboard_append(link); self.update_idletasks()
        except Exception as e:
            messagebox.showerror("History", f"Could not copy deeplink:\
{e}", parent=self)

    def _history_join(self, link):
        try:
            os.startfile(link)
        except Exception as e:
            messagebox.showerror("History", f"Could not launch Roblox:\
{e}", parent=self)

    def _history_clear(self):
        if not messagebox.askyesno("History", "Clear all saved game history?", parent=self): return
        self._history_save([]); self._history_last_game=None; self._history_refresh()




    def _build_client_tab(self):
        tab=ttk.Frame(self.nb,padding=0); self.nb.add(tab,text="Client"); tab.columnconfigure(0,weight=1)
        ttk.Label(tab,text="Roblox Client",font=("Segoe UI Semibold",15)).grid(row=0,column=0,sticky="w")
        ttk.Label(tab,text="Live Roblox client information and current game details.",foreground="#9aa0a6").grid(row=1,column=0,sticky="w",pady=(0,14))
        info=ttk.LabelFrame(tab,text="Client Information",padding=14); info.grid(row=2,column=0,sticky="ew",pady=(0,10)); info.columnconfigure(1,weight=1)
        self.client_status_var=tk.StringVar(value="Checking..."); self.client_pid_var=tk.StringVar(value="—"); self.client_path_var=tk.StringVar(value="—")
        self.client_version_var=tk.StringVar(value="—"); self.client_game_var=tk.StringVar(value="Detecting..."); self.client_place_var=tk.StringVar(value="—"); self.client_job_var=tk.StringVar(value="—")
        self.client_cpu_var=tk.StringVar(value="—"); self.client_ram_var=tk.StringVar(value="—")
        rows=(("Status",self.client_status_var),("PID",self.client_pid_var),("Path",self.client_path_var),("File Version",self.client_version_var),
              ("Game",self.client_game_var),("Place ID",self.client_place_var),("Job ID",self.client_job_var),("CPU Usage",self.client_cpu_var),("RAM Usage",self.client_ram_var))
        for i,(label,var) in enumerate(rows):
            ttk.Label(info,text=label).grid(row=i,column=0,sticky="w",padx=(0,14),pady=5); ttk.Label(info,textvariable=var).grid(row=i,column=1,sticky="w",pady=5)
        actions=ttk.Frame(tab); actions.grid(row=3,column=0,sticky="w",pady=(4,0))
        ttk.Button(actions,text="Refresh",command=self._client_refresh).pack(side="left",padx=(0,6)); ttk.Button(actions,text="Open Roblox",command=self._open_selected_roblox).pack(side="left")
        self._client_cpu_prev=None; self._client_system_prev=None; self._client_refresh(); self.after(1000,self._client_live_update)

    def _client_roblox_pids(self):
        """Return the Roblox Game Client process tree members.
        Task Manager can show Roblox as a grouped parent with one or more
        child processes, so looking only for one PID misses the real usage.
        """
        if os.name != "nt":
            return []
        try:
            import ctypes
            class PROCESSENTRY32W(ctypes.Structure):
                _fields_ = [
                    ("dwSize", ctypes.wintypes.DWORD),
                    ("cntUsage", ctypes.wintypes.DWORD),
                    ("th32ProcessID", ctypes.wintypes.DWORD),
                    ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
                    ("th32ModuleID", ctypes.wintypes.DWORD),
                    ("cntThreads", ctypes.wintypes.DWORD),
                    ("th32ParentProcessID", ctypes.wintypes.DWORD),
                    ("pcPriClassBase", ctypes.c_long),
                    ("dwFlags", ctypes.wintypes.DWORD),
                    ("szExeFile", ctypes.wintypes.WCHAR * 260),
                ]
            snap = ctypes.windll.kernel32.CreateToolhelp32Snapshot(0x00000002, 0)
            if snap in (0, -1):
                return []
            procs = []
            pe = PROCESSENTRY32W()
            pe.dwSize = ctypes.sizeof(pe)
            try:
                ok = ctypes.windll.kernel32.Process32FirstW(snap, ctypes.byref(pe))
                while ok:
                    name = pe.szExeFile.lower()


                    if name in ("robloxplayerbeta.exe", "roblox.exe"):
                        procs.append((int(pe.th32ProcessID), int(pe.th32ParentProcessID), name))
                    ok = ctypes.windll.kernel32.Process32NextW(snap, ctypes.byref(pe))
            finally:
                ctypes.windll.kernel32.CloseHandle(snap)

            if not procs:
                return []



            pids = {pid for pid, _, _ in procs}
            changed = True
            while changed:
                changed = False
                for pid, ppid, _ in procs:
                    if ppid in pids and pid not in pids:
                        pids.add(pid)
                        changed = True
            return list(pids)
        except Exception:
            return []

    def _client_process_stats(self, pids):
        """Aggregate CPU time and working-set RAM for all Roblox client PIDs."""
        if not pids:
            return None, None
        try:
            import ctypes, ctypes.wintypes as wt
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            PROCESS_VM_READ = 0x0010

            class PMC(ctypes.Structure):
                _fields_ = [
                    ("cb", wt.DWORD),
                    ("PageFaultCount", wt.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t),
                    ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t),
                    ("PeakPagefileUsage", ctypes.c_size_t),
                ]

            total_cpu = 0
            total_ram = 0
            any_cpu = False
            any_ram = False

            for pid in pids:
                h = ctypes.windll.kernel32.OpenProcess(
                    PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_VM_READ,
                    False, int(pid)
                )
                if not h:

                    h = ctypes.windll.kernel32.OpenProcess(
                        PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid)
                    )
                if not h:
                    continue
                try:
                    pm = PMC()
                    pm.cb = ctypes.sizeof(pm)
                    if ctypes.windll.psapi.GetProcessMemoryInfo(
                        h, ctypes.byref(pm), pm.cb
                    ):
                        total_ram += int(pm.WorkingSetSize)
                        any_ram = True

                    c = wt.FILETIME()
                    e = wt.FILETIME()
                    k = wt.FILETIME()
                    u = wt.FILETIME()
                    if ctypes.windll.kernel32.GetProcessTimes(
                        h, ctypes.byref(c), ctypes.byref(e),
                        ctypes.byref(k), ctypes.byref(u)
                    ):
                        total_cpu += (
                            ((k.dwHighDateTime << 32) | k.dwLowDateTime) +
                            ((u.dwHighDateTime << 32) | u.dwLowDateTime)
                        )
                        any_cpu = True
                finally:
                    ctypes.windll.kernel32.CloseHandle(h)



            if not any_cpu and not any_ram:
                return None, None

            st = wt.FILETIME()
            kt = wt.FILETIME()
            ut = wt.FILETIME()
            if ctypes.windll.kernel32.GetSystemTimes(
                ctypes.byref(st), ctypes.byref(kt), ctypes.byref(ut)
            ):
                system_time = (
                    ((kt.dwHighDateTime << 32) | kt.dwLowDateTime) +
                    ((ut.dwHighDateTime << 32) | ut.dwLowDateTime)
                )
                idle_time = ((st.dwHighDateTime << 32) | st.dwLowDateTime)
                cpu_data = (total_cpu, (system_time, idle_time))
            else:
                cpu_data = total_cpu

            return cpu_data, (total_ram if any_ram else None)
        except Exception:
            return None, None

    def _client_game_refresh(self, place_id, job_id):
        place_id = str(place_id or "").strip()
        self.client_place_var.set(place_id or "—")
        self.client_job_var.set(str(job_id or "—"))
        if not place_id:
            self.client_game_var.set("Not in a game")
            return

        self.client_game_var.set("Resolving game name...")

        def worker():
            name = None
            try:


                name = self._resolve_history_game_name(place_id)
            except Exception:
                pass
            if not name:
                name = f"Place {place_id}"
            try:
                def update():
                    self.client_game_var.set(name)


                    self.client_place_var.set(f"{place_id} — {name}")
                self.after(0, update)
            except Exception:
                pass
        threading.Thread(target=worker, daemon=True).start()

    def _client_live_update(self):
        try:
            pids = self._client_roblox_pids()
            if pids:
                stats, ram = self._client_process_stats(pids)
                if isinstance(stats, tuple) and len(stats) == 2 and isinstance(stats[1], tuple):
                    proc, system = stats
                    if self._client_cpu_prev and self._client_system_prev:
                        dp = proc - self._client_cpu_prev
                        ds_total = system[0] - self._client_system_prev[0]
                        prev_busy = (
                            self._client_system_prev[0] -
                            self._client_system_prev[1]
                        )
                        curr_busy = system[0] - system[1]
                        busy = curr_busy - prev_busy



                        if ds_total > 0:
                            cpu_pct = (dp / ds_total) * 100.0
                            self.client_cpu_var.set(
                                f"{max(0.0, min(100.0, cpu_pct)):.1f}%"
                            )
                    self._client_cpu_prev = proc
                    self._client_system_prev = system
                elif isinstance(stats, (int, float)):
                    if self._client_cpu_prev is not None:

                        dp = stats - self._client_cpu_prev
                        if dp >= 0:
                            self.client_cpu_var.set(f"{dp / 10_000_000 * 100:.1f}%")
                    self._client_cpu_prev = stats

                if ram is not None:
                    self.client_ram_var.set(f"{ram / 1024 / 1024:.1f} MB")
            else:
                self._client_cpu_prev = None
                self._client_system_prev = None
                self.client_cpu_var.set("—")
                self.client_ram_var.set("—")
        except Exception:
            pass
        try:
            self.after(1000, self._client_live_update)
        except Exception:
            pass

    def _client_refresh(self):
        pids = self._client_roblox_pids()
        pid = pids[0] if pids else _fflag_find_pid()
        path = _get_process_exe_path(pid) if pid else ""

        if not path:
            saved = str(self.settings.get("roblox_path", "") or "")
            if saved and os.path.isfile(saved):
                path = saved

        self.client_pid_var.set(
            ", ".join(str(x) for x in sorted(pids)) if pids
            else ("Not running" if not pid else str(pid))
        )
        self.client_status_var.set("Running" if pids or pid else "Not running")
        self.client_path_var.set(path or "Roblox Game Client not found")

        version = "—"
        if path and os.path.isfile(path):
            try:
                import win32api
                info = win32api.GetFileVersionInfo(path, "\\")
                ms = info["FileVersionMS"]
                ls = info["FileVersionLS"]
                version = f"{ms >> 16}.{ms & 0xffff}.{ls >> 16}.{ls & 0xffff}"
            except Exception:
                pass
        self.client_version_var.set(version)

        place_id, job_id = self._detect_current_game(silent=True) if (pids or pid) else (None, None)
        self._client_game_refresh(place_id, job_id)


        self._client_cpu_prev = None
        self._client_system_prev = None

    def _build_subplace_joiner_tab(self):
        tab=ttk.Frame(self.nb,padding=0); self.nb.add(tab,text="Subplace Joiner"); tab.columnconfigure(0,weight=1); tab.rowconfigure(2,weight=1)
        ttk.Label(tab,text="Subplace Joiner",font=("Segoe UI Semibold",15)).grid(row=0,column=0,sticky="w")
        row=ttk.Frame(tab); row.grid(row=1,column=0,sticky="ew",pady=8); row.columnconfigure(0,weight=1)
        self.subplace_id=tk.StringVar(); ttk.Entry(row,textvariable=self.subplace_id).grid(row=0,column=0,sticky="ew"); ttk.Button(row,text="Search",command=self._subplace_search).grid(row=0,column=1,padx=6)
        self.subplace_tree=ttk.Treeview(tab,columns=("id","name"),show="headings"); self.subplace_tree.heading("id",text="PLACE ID"); self.subplace_tree.heading("name",text="NAME"); self.subplace_tree.column("id",width=160); self.subplace_tree.column("name",width=400); self.subplace_tree.grid(row=2,column=0,sticky="nsew")
        buttons=ttk.Frame(tab); buttons.grid(row=3,column=0,sticky="e",pady=8)
        ttk.Button(buttons,text="Join Selected",command=self._subplace_join).pack(side="left",padx=(0,6))
        ttk.Button(buttons,text="Copy Deeplink",command=self._subplace_copy_deeplink).pack(side="left")
    def _subplace_search(self):
        pid=self.subplace_id.get().strip()
        if not pid.isdigit(): return
        try:
            req=urllib.request.Request(f"https://apis.roblox.com/universes/v1/places/{pid}/universe")
            with urllib.request.urlopen(req,timeout=10) as r: universe_id=json.load(r).get("universeId")
            if not universe_id: raise ValueError("Universe not found for this Place ID.")
            req=urllib.request.Request(f"https://develop.roblox.com/v1/universes/{universe_id}/places?limit=100&sortOrder=Asc")
            with urllib.request.urlopen(req,timeout=10) as r:data=json.load(r)
            self.subplace_tree.delete(*self.subplace_tree.get_children())
            for x in data.get("data",[]): self.subplace_tree.insert("","end",values=(x.get("id",""),x.get("name",x.get("id",""))))
        except Exception as e: messagebox.showerror("Subplace Joiner",f"Search failed:\n{e}",parent=self)
    def _subplace_copy_deeplink(self):

        place_id = None
        game_instance_id = None
        logs_dir = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Roblox", "logs")
        uuid_re = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
        try:
            log_files = sorted(
                [os.path.join(logs_dir, f) for f in os.listdir(logs_dir) if f.lower().endswith(".log")],
                key=lambda x: os.path.getmtime(x), reverse=True
            )[:30]
            join_re = re.compile(rf"!\s*Joining\s+game\s+[\"']?({uuid_re})[\"']?\s+place\s+(\d+)", re.IGNORECASE)
            for log_path in log_files:
                try:
                    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                except Exception:
                    continue
                matches = list(join_re.finditer(text))
                if matches:
                    m = matches[-1]
                    game_instance_id, place_id = m.group(1), m.group(2)
                    break
            if not place_id or not game_instance_id:
                for log_path in log_files:
                    try:
                        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                            text = f.read()
                    except Exception:
                        continue
                    if not place_id:
                        m = re.findall(r"\bplaceid\s*[:=]\s*(\d+)", text, re.IGNORECASE)
                        if m: place_id = m[-1]
                    if not game_instance_id:
                        m = re.findall(rf"\bjobId\s*[:=]\s*[\"']?({uuid_re})", text, re.IGNORECASE)
                        if m: game_instance_id = m[-1]
                    if place_id and game_instance_id: break
        except Exception as e:
            messagebox.showerror("Subplace Joiner", f"Could not read Roblox logs:\n{e}", parent=self)
            return
        if not place_id or not game_instance_id:
            messagebox.showwarning("Subplace Joiner", "Could not detect the current Roblox server. Make sure you are inside a game, then try again.", parent=self)
            return
        link = f"roblox://experiences/start?placeId={place_id}&gameInstanceId={game_instance_id}"
        self._history_add(place_id, game_instance_id)
        try:
            self.clipboard_clear()
            self.clipboard_append(link)
            self.update_idletasks()
            messagebox.showinfo("Subplace Joiner", "Current game's deeplink copied to clipboard.", parent=self)
        except Exception as e:
            messagebox.showerror("Subplace Joiner", f"Could not copy deeplink:\n{e}", parent=self)

    def _subplace_join(self):
        sel=self.subplace_tree.selection()
        if not sel:return
        pid=self.subplace_tree.item(sel[0],"values")[0]
        try: os.startfile(f"roblox://placeId={pid}")
        except Exception as e: messagebox.showerror("Subplace Joiner",f"Could not launch Roblox:\n{e}",parent=self)

    def _build_fflag_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.insert(1, tab, text="FFlags")
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)

        head = ttk.Frame(tab)
        head.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(head, text="FFlags", font=("Segoe UI Semibold", 15)).pack(side="left")
        self.fflag_status = ttk.Label(head, text="Waiting for Roblox...", foreground="#9aa0a6")
        self.fflag_status.pack(side="right", padx=(8, 0))

        bar = ttk.Frame(tab)
        bar.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        buttons = [
            ("+ Add", self._fflag_add_dialog), ("Remove", self._fflag_remove),
            ("Remove All", self._fflag_remove_all), ("Presets", self._fflag_presets_dialog),
            ("Import", self._fflag_import), ("Export", self._fflag_export),
            ("Hotkeys", self._fflag_hotkeys_dialog), ("JSON Editor", self._fflag_json_editor),
        ]
        for text, cmd in buttons:
            ttk.Button(bar, text=text, command=cmd).pack(side="left", padx=(0, 5))
        ttk.Checkbutton(bar, text="Auto Apply", variable=self.fflag_auto_apply, command=self._toggle_fflag_auto_apply).pack(side="left", padx=(8, 0))
        ttk.Button(bar, text="Apply Selected Json", command=self._apply_selected_json).pack(side="right")

        frame = ttk.PanedWindow(tab, orient="horizontal")
        frame.grid(row=2, column=0, sticky="nsew")
        left = ttk.Frame(frame)
        right = ttk.Frame(frame)
        frame.add(left, weight=4)
        frame.add(right, weight=1)
        left.columnconfigure(0, weight=1)
        left.rowconfigure(1, weight=1)
        search_row = ttk.Frame(left)
        search_row.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        ttk.Label(search_row, text="Search:").pack(side="left")
        self.fflag_search = tk.StringVar()
        ent = ttk.Entry(search_row, textvariable=self.fflag_search)
        ent.pack(side="left", fill="x", expand=True, padx=6)
        self.fflag_search.trace_add("write", lambda *_: self._refresh_fflag_list())

        cols = ("name", "type", "value")
        self.fflag_tree = ttk.Treeview(left, columns=cols, show="headings", selectmode="browse")
        self.fflag_tree.heading("name", text="NAME")
        self.fflag_tree.heading("type", text="TYPE")
        self.fflag_tree.heading("value", text="VALUE")
        self.fflag_tree.column("name", width=460, anchor="w")
        self.fflag_tree.column("type", width=90, anchor="center")
        self.fflag_tree.column("value", width=220, anchor="w")
        self.fflag_tree.grid(row=1, column=0, sticky="nsew")
        self.fflag_tree.bind("<Double-1>", self._fflag_inline_edit)

        ttk.Label(right, text="Saved JSONs", font=("Segoe UI Semibold", 10)).pack(anchor="w", padx=8, pady=(4, 6))
        self.json_tree = tk.Listbox(right, bg=_CURRENT_PALETTE["bg_medium"], fg=_CURRENT_PALETTE["fg"], relief="flat", bd=0, highlightthickness=0)
        self.json_tree.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.json_tree.bind("<Double-1>", lambda _e: self._apply_selected_json())
        ttk.Button(right, text="Refresh", command=self._refresh_json_list).pack(fill="x", padx=8, pady=(0, 8))
        self._refresh_json_list()

        bottom = ttk.Frame(tab)
        bottom.grid(row=3, column=0, sticky="ew", pady=(8, 0))
        ttk.Button(bottom, text="Apply to Roblox", command=self._fflag_apply).pack(side="right", padx=(5, 0))
        ttk.Button(bottom, text="Save Flags", command=self._save_fflag_flags).pack(side="right")
        ttk.Button(bottom, text="Refresh", command=self._fflag_refresh_process).pack(side="left")
        self._refresh_fflag_list()
        self.after(1000, self._fflag_refresh_process)

    def _refresh_fflag_list(self):
        if not hasattr(self, "fflag_tree"):
            return
        self.fflag_tree.delete(*self.fflag_tree.get_children())
        filt = self.fflag_search.get().strip().lower() if hasattr(self, "fflag_search") else ""
        for i, flag in enumerate(self.fflag_flags):
            if filt and filt not in flag.get("name", "").lower():
                continue
            self.fflag_tree.insert("", "end", iid=str(i), values=(flag.get("name", ""), flag.get("type", ""), flag.get("value", "")))

    def _fflag_add_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("Add FFlag")
        dlg.transient(self)
        dlg.grab_set()
        theme_toplevel(dlg)
        ttk.Label(dlg, text="FFlag name").grid(row=0, column=0, padx=10, pady=(10, 4), sticky="w")
        name = ttk.Entry(dlg, width=48)
        name.grid(row=1, column=0, padx=10, sticky="ew")
        ttk.Label(dlg, text="Value:").grid(row=2, column=0, padx=10, pady=(8, 4), sticky="w")
        value = ttk.Entry(dlg, width=48)
        value.grid(row=3, column=0, padx=10, sticky="ew")
        def add():
            n, v = name.get().strip(), value.get().strip()
            if not n or not v:
                return
            bare = fflag_strip_prefix(n)
            self.fflag_flags.append({"name": bare, "value": v, "type": fflag_infer_type(v)})
            self._save_fflag_flags(); self._refresh_fflag_list(); dlg.destroy()
        btns = ttk.Frame(dlg); btns.grid(row=4, column=0, pady=10)
        ttk.Button(btns, text="Add Flag", command=add).pack(side="left", padx=4)
        ttk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="left", padx=4)
        dlg.columnconfigure(0, weight=1)
        name.focus_set()

    def _fflag_inline_edit(self,event):
        tree=self.fflag_tree; row=tree.identify_row(event.y); col=tree.identify_column(event.x)
        if not row or col not in ("#1","#3"): return
        idx=int(row); column="name" if col=="#1" else "value"; bbox=tree.bbox(row,col)
        if not bbox: return
        x,y,w,h=bbox; entry=ttk.Entry(tree); entry.place(x=x,y=y,width=w,height=h); entry.insert(0,str(self.fflag_flags[idx].get(column,""))); entry.focus_set(); entry.selection_range(0,"end")
        def save(_=None):
            value=entry.get().strip()
            if value:
                self.fflag_flags[idx][column]=fflag_strip_prefix(value) if column=="name" else value; self.fflag_flags[idx]["type"]=fflag_infer_type(self.fflag_flags[idx].get("value","")); self._save_fflag_flags(); self._refresh_fflag_list()
            entry.destroy()
        entry.bind("<Return>",save); entry.bind("<FocusOut>",save); entry.bind("<Escape>",lambda _e: entry.destroy())

    def _fflag_edit_selected(self, _event=None):
        sel = self.fflag_tree.selection()
        if not sel:
            return
        idx = int(sel[0]); flag = self.fflag_flags[idx]
        dlg = tk.Toplevel(self); dlg.title("Edit FFlag"); dlg.transient(self); dlg.grab_set(); theme_toplevel(dlg)
        ttk.Label(dlg, text="Flag name:").grid(row=0, column=0, padx=10, pady=(10, 4), sticky="w")
        name = ttk.Entry(dlg, width=48); name.insert(0, flag.get("name", "")); name.grid(row=1, column=0, padx=10)
        ttk.Label(dlg, text="Value:").grid(row=2, column=0, padx=10, pady=(8, 4), sticky="w")
        value = ttk.Entry(dlg, width=48); value.insert(0, flag.get("value", "")); value.grid(row=3, column=0, padx=10)
        def save():
            n, v = name.get().strip(), value.get().strip()
            if n and v:
                self.fflag_flags[idx] = {"name": fflag_strip_prefix(n), "value": v, "type": fflag_infer_type(v)}
                self._save_fflag_flags(); self._refresh_fflag_list(); dlg.destroy()
        b = ttk.Frame(dlg); b.grid(row=4, column=0, pady=10)
        ttk.Button(b, text="Save", command=save).pack(side="left", padx=4); ttk.Button(b, text="Cancel", command=dlg.destroy).pack(side="left", padx=4)

    def _fflag_remove(self):
        sel = self.fflag_tree.selection()
        if not sel: return
        del self.fflag_flags[int(sel[0])]
        self._save_fflag_flags(); self._refresh_fflag_list()

    def _fflag_remove_all(self):
        if not self.fflag_flags or not messagebox.askyesno("FFlags", "Remove all flags?", parent=self): return
        self.fflag_flags.clear(); self._save_fflag_flags(); self._refresh_fflag_list()

    def _fflag_presets_dialog(self):
        dlg = tk.Toplevel(self); dlg.title("FFlag Presets"); dlg.geometry("620x520"); dlg.transient(self); theme_toplevel(dlg)
        ttk.Label(dlg, text="Add Flag from Presets", font=("Segoe UI Semibold", 12)).pack(anchor="w", padx=12, pady=(10, 6))
        search = tk.StringVar(); ttk.Entry(dlg, textvariable=search).pack(fill="x", padx=12, pady=(0, 6))
        tree = ttk.Treeview(dlg, columns=("name",), show="headings", selectmode="browse"); tree.heading("name", text="FLAG NAME"); tree.column("name", width=580); tree.pack(fill="both", expand=True, padx=12, pady=6)
        val = tk.StringVar(value="true"); row = ttk.Frame(dlg); row.pack(fill="x", padx=12, pady=6)
        ttk.Label(row, text="Value:").pack(side="left"); ttk.Entry(row, textvariable=val, width=25).pack(side="left", padx=6)
        def refresh(*_):
            tree.delete(*tree.get_children()); f=search.get().lower().strip()
            for n in self.fflag_presets:
                if not f or f in n.lower(): tree.insert("", "end", values=(n,))
        def add():
            sel=tree.selection()
            if not sel: return
            n=tree.item(sel[0], "values")[0]
            self.fflag_flags.append({"name":fflag_strip_prefix(n),"value":val.get(),"type":fflag_infer_type(val.get())})
            self._save_fflag_flags(); self._refresh_fflag_list(); dlg.destroy()
        search.trace_add("write", refresh); refresh()
        ttk.Button(dlg, text="Add Selected", command=add).pack(pady=(0, 10))

    def _fflag_import(self):
        path = filedialog.askopenfilename(parent=self, title="Import FFlags", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if not path: return
        try:
            with open(path, "r", encoding="utf-8") as f: data=json.load(f)
            count=0
            if isinstance(data, dict):
                for n,v in data.items():
                    bare=fflag_strip_prefix(n); found=next((x for x in self.fflag_flags if x.get("name")==bare), None)
                    item={"name":bare,"value":str(v).lower() if isinstance(v,bool) else str(v),"type":fflag_infer_type(v)}
                    if found: found.update(item)
                    else: self.fflag_flags.append(item)
                    count+=1
            elif isinstance(data, list):
                for x in data:
                    if isinstance(x, dict) and x.get("name") is not None:
                        item={"name":fflag_strip_prefix(x["name"]),"value":str(x.get("value", "")),"type":x.get("type") or fflag_infer_type(x.get("value", ""))}
                        self.fflag_flags.append(item); count+=1
            self._save_fflag_flags(); self._refresh_fflag_list(); messagebox.showinfo("FFlags", f"Imported {count} flag(s).", parent=self)
        except Exception as e:
            messagebox.showerror("FFlags", f"Import failed:\n{e}", parent=self)

    def _fflag_export(self):
        if not self.fflag_flags:
            return
        path=filedialog.asksaveasfilename(parent=self,title="Export FFlags",defaultextension=".json",filetypes=[("JSON files","*.json")])
        if not path:return
        data={x["name"]:x["value"] for x in self.fflag_flags}
        with open(path,"w",encoding="utf-8") as f: json.dump(data,f,ensure_ascii=False,indent=4)

    def _fflag_refresh_process(self):
        pid = _fflag_find_pid()
        if pid and pid != self.fflag_pid:

            self.fflag_original_values.clear()
            self.fflag_pid = pid
            exe_path = _get_process_exe_path(pid)
            if exe_path and os.path.basename(exe_path).lower() == "robloxplayerbeta.exe":
                self.settings["roblox_path"] = exe_path
                self._save_settings()
                if hasattr(self, "roblox_path_var"):
                    self.roblox_path_var.set(exe_path)
            if self.fflag_engine.attach(pid):
                self.fflag_status.config(text=f"Roblox attached  PID {pid}", foreground="#65d98b")
                if hasattr(self, "fps_pid_label"):
                    self.fps_pid_label.config(text=f"PID: {pid} selected", foreground="#65d98b")
                if self.fflag_auto_apply.get(): self.after(6000, self._fflag_apply)
            else:
                self.fflag_status.config(text="Roblox found, attach failed", foreground="#ff6b6b")
        elif not pid:
            if self.fflag_pid:
                self.fflag_engine.close()
            self.fflag_original_values.clear()
            self.fflag_pid=0; self.fflag_status.config(text="Waiting for Roblox...", foreground="#9aa0a6")
            if hasattr(self, "fps_pid_label"):
                self.fps_pid_label.config(text="PID: Waiting for Roblox...", foreground="#9aa0a6")
        self.after(1000, self._fflag_refresh_process)

    def _fps_flag_value(self):
        fps = max(0, min(800, int(self.fps_limit.get())))
        return "9999999999999999" if fps == 0 else str(fps)

    def _sync_fps_flag_to_manager(self):



        full_name = "TaskSchedulerTargetFps"
        normalized_name = fflag_strip_prefix(full_name)
        value = self._fps_flag_value()

        fps_entry = None
        cleaned_flags = []

        for flag in self.fflag_flags:
            flag_name = str(flag.get("name", "")).strip()
            if fflag_strip_prefix(flag_name) == normalized_name:
                if fps_entry is None:

                    flag["name"] = full_name
                    flag["value"] = value
                    flag["type"] = "int"
                    fps_entry = flag
                    cleaned_flags.append(flag)

                continue
            cleaned_flags.append(flag)

        if fps_entry is None:
            fps_entry = {"name": full_name, "value": value, "type": "int"}
            cleaned_flags.append(fps_entry)

        self.fflag_flags = cleaned_flags
        self._save_fflag_flags()

        if hasattr(self, "fflag_tree"):
            self._refresh_fflag_list()

    def _apply_fps_flag(self, silent=True):
        self._sync_fps_flag_to_manager()
        if not self.fflag_pid or not self.fflag_engine.handle:
            return False
        if not self.fflag_engine.get_singleton():
            return False
        value = self._fps_flag_value()
        return bool(self.fflag_engine.set_flag_with_prefixes("DFIntTaskSchedulerTargetFps", value))

    def _on_fps_limit_changed(self, *_):


        return

    def _apply_fps_after_slider(self):
        self._fps_release_job = None
        try:
            self._sync_fps_flag_to_manager()
            self._fflag_apply(silent=True)
            self._save_settings()
        except Exception:
            pass

    def _fps_apply_tick(self):
        self._apply_fps_flag(silent=True)
        self.after(30000, self._fps_apply_tick)

    def _fflag_apply(self, silent=False):
        if not self.fflag_pid or not self.fflag_engine.handle:
            if not silent:
                messagebox.showwarning("FFlags", "Roblox is not attached.", parent=self)
            return
        if not self.fflag_engine.get_singleton():
            self.fflag_status.config(text="Singleton not found", foreground="#ff6b6b")
            return
        ok=0
        for flag in self.fflag_flags:
            name = fflag_strip_prefix(str(flag.get("name", "")))
            if not name:
                continue
            address = self.fflag_engine.get_flag_address_with_prefixes(name)
            if address and address not in self.fflag_original_values:
                original = self.fflag_engine._read(address, 4)
                if original is not None:
                    self.fflag_original_values[address] = original
            if self.fflag_engine.set_flag_with_prefixes(name, str(flag.get("value", ""))):
                ok += 1
        self._apply_fps_flag(silent=True)
        self.fflag_status.config(text=f"Applied {ok}/{len(self.fflag_flags)} flags", foreground="#65d98b")

    def _fflag_unapply(self):


        self.fflag_auto_apply.set(False)
        if not self.fflag_pid or not self.fflag_engine.handle:
            self.fflag_original_values.clear()
            messagebox.showwarning("FFlags", "Roblox is not attached.", parent=self)
            return
        restored = 0
        failed = 0
        snapshots = list(self.fflag_original_values.items())
        for address, original in snapshots:
            try:
                written = ctypes.c_size_t()
                ok = ctypes.windll.kernel32.WriteProcessMemory(
                    self.fflag_engine.handle, ctypes.c_void_p(address),
                    original, len(original), ctypes.byref(written)
                )
                if ok and written.value == len(original):
                    restored += 1
                else:
                    failed += 1
            except Exception:
                failed += 1
        self.fflag_original_values.clear()
        self.fflag_status.config(
            text=f"Unapplied {restored} flag(s)" + (f", {failed} failed" if failed else ""),
            foreground="#65d98b" if not failed else "#ff6b6b"
        )

    def _toggle_fflag_auto_apply(self):

        if self.fflag_auto_apply.get() and self.fflag_pid and self.fflag_engine.handle:
            self._fflag_apply(silent=True)

    def _fflag_auto_apply_tick(self):

        if self.fflag_auto_apply.get() and self.fflag_pid and self.fflag_engine.handle:
            self._fflag_apply(silent=True)
            self.after(6000, self._fflag_auto_apply_tick)

    def _build_settings_tab(self):
        tab = ttk.Frame(self.nb, padding=0)
        self.nb.add(tab, text="Settings")
        ttk.Label(tab, text="Settings & Options", font=("Segoe UI Semibold", 12)).pack(anchor="w")
        ttk.Label(tab, text="General options.",
                  foreground="#9aa0a6").pack(anchor="w", pady=(0, 10))

        box = ttk.LabelFrame(tab, text="Cache Viewer")
        box.pack(fill="x", pady=6)
        ttk.Checkbutton(box, text="Start watching for new assets on launch", variable=self.autostart_watch, command=self._save_settings).pack(anchor="w", padx=8, pady=2)
        ttk.Checkbutton(box, text="Auto-scroll to newest row", variable=self.autoscroll, command=self._save_settings).pack(anchor="w", padx=8, pady=2)
        ttk.Checkbutton(box, text="Hide ticket assets", variable=self.hide_tickets, command=self._apply_filter).pack(anchor="w", padx=8, pady=2)
        ttk.Label(box, text="Show lines (wireframe) for the Preview", foreground="#c8c8c8").pack(anchor="w", padx=8, pady=(6, 0))
        ttk.Checkbutton(box, text="Wireframe lines on", variable=self.show_lines, command=self._apply_show_lines).pack(anchor="w", padx=8, pady=2)

        startup = ttk.LabelFrame(tab, text="Startup")
        startup.pack(fill="x", pady=6)
        ttk.Checkbutton(startup, text="Launch on Startup", variable=self.launch_on_startup, command=self._startup_setting_changed).pack(anchor="w", padx=8, pady=2)

        db = ttk.LabelFrame(tab, text="Database")
        db.pack(fill="x", pady=6)
        ttk.Button(db, text="Choose DB File…", command=self._choose_db).pack(anchor="w", padx=8, pady=4)
        ttk.Button(db, text="Choose Shard Root…", command=self._choose_shard_root).pack(anchor="w", padx=8, pady=4)


    def _build_viewer_widgets(self):
        top = ttk.Frame(self.viewer_root, padding=(8, 6))
        top.pack(fill="x")

        ttk.Checkbutton(top, text="Auto-scroll", variable=self.autoscroll).grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(top, text="Hide tickets", variable=self.hide_tickets, command=self._apply_filter).grid(row=0, column=1, sticky="w", padx=(4, 0))
        ttk.Checkbutton(top, text="Stay on top", variable=self.stay_on_top, command=self._apply_stay_on_top).grid(row=0, column=2, sticky="w", padx=(4, 0))
        ttk.Checkbutton(top, text="Show lines", variable=self.show_lines, command=self._apply_show_lines).grid(row=0, column=3, sticky="w", padx=(4, 0))

        self.btn_clear = ttk.Button(top, text="Clear rbx-storage", command=self._clear_storage_now)
        self.btn_clear.grid(row=0, column=5, sticky="e", padx=(0, 6))
        self.btn_delete_type = ttk.Button(top, text="Delete Cache Type", command=self._open_delete_cache_type)
        self.btn_delete_type.grid(row=0, column=6, sticky="e", padx=(0, 6))
        self.toggle_btn = ttk.Button(top, text="Start Watching", command=self._toggle_watch)
        self.toggle_btn.grid(row=0, column=7, sticky="e", padx=(0, 6))
        self.btn_dump = ttk.Button(top, text="Dump Caches", command=self._dump_all_caches)
        self.btn_dump.grid(row=0, column=8, sticky="e")

        ttk.Label(top, text="DB:").grid(row=1, column=0, sticky="w", pady=(4, 0))
        self.db_label = ttk.Label(top, text=self.db_path, width=50)
        self.db_label.grid(row=1, column=1, columnspan=6, sticky="ew", padx=(4, 12), pady=(4, 0))

        ttk.Label(top, text="Type:").grid(row=2, column=0, sticky="w", pady=(4, 0))
        type_combo = ttk.Combobox(top, textvariable=self.type_filter, values=[t[0] for t in TYPE_FILTERS], state="readonly", width=14)
        type_combo.grid(row=2, column=1, sticky="w", padx=(8, 0), pady=(4, 0))
        type_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_filter())

        ttk.Label(top, text="Filter:").grid(row=3, column=0, sticky="w", pady=(4, 0))
        f_entry = ttk.Entry(top, textvariable=self.filter_text)
        f_entry.grid(row=3, column=1, columnspan=6, sticky="ew", pady=(4, 0))
        f_entry.bind("<KeyRelease>", lambda e: self._apply_filter())

        for c in (3, 4):
            top.columnconfigure(c, weight=1)
        for c in (5, 6, 7, 8):
            top.columnconfigure(c, weight=0)

        self.vpaned = ttk.PanedWindow(self.viewer_root, orient="vertical")
        self.vpaned.pack(fill="both", expand=True, padx=8, pady=(0, 6))

        self.table_frame = ttk.Frame(self.vpaned)
        self.vpaned.add(self.table_frame, weight=3)
        _set_pane_minsize(self.vpaned, self.table_frame, 200)

        columns = ("time", "name", "hash", "size", "kind", "src")
        self.columns = columns
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", selectmode="extended")
        self.tree.heading("time", text="TIME", command=lambda: self._sort_by("time"))
        self.tree.heading("name", text="NAME", command=lambda: self._sort_by("name"))
        self.tree.heading("hash", text="HASH", command=lambda: self._sort_by("hash"))
        self.tree.heading("size", text="SIZE", command=lambda: self._sort_by("size", numeric=True))
        self.tree.heading("kind", text="TYPE", command=lambda: self._sort_by("kind"))
        self.tree.heading("src", text="SOURCE", command=lambda: self._sort_by("src"))

        self.tree.column("time", width=70, minwidth=60, anchor="w", stretch=True)
        self.tree.column("name", width=140, minwidth=80, anchor="w", stretch=True)
        self.tree.column("hash", width=200, minwidth=200, anchor="w", stretch=True)
        self.tree.column("size", width=70, minwidth=60, anchor="w", stretch=True)
        self.tree.column("kind", width=150, minwidth=120, anchor="w", stretch=True)
        self.tree.column("src", width=80, minwidth=60, anchor="w", stretch=True)

        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.columnconfigure(0, weight=1)

        self.tree.tag_configure("hover", background="#333333")
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree.bind("<Delete>", lambda e: self._action_delete_blob())
        self.tree.bind("<F2>", lambda e: self._action_change_hash())

        self._ctx = tk.Menu(self, tearoff=0)
        self._ctx.add_command(label="Export ▸ Full Blob…", command=self._export_selected_full)
        self._ctx.add_command(label="Export ▸ RBXM…", command=self._export_selected_rbxm)
        self._ctx_rbxm_index = self._ctx.index("end")
        self._ctx.add_command(label="Export ▸ Image…", command=self._export_selected_image)
        self._ctx_img_index = self._ctx.index("end")
        self._ctx.add_separator()
        for lbl, cmd in [
            ("Change Hash…", self._action_change_hash),
            ("Delete Blob", self._action_delete_blob),
        ]:
            self._ctx.add_command(label=lbl, command=cmd)
        self._ctx.add_separator()
        self._ctx.add_command(label="Copy Hash", command=lambda: self._copy_selected_hash())
        self._ctx.add_separator()
        self._ctx.add_command(label="Save Hash…", command=self._action_save_hash_to_saves)
        self._ctx.add_command(label="Save Blob…", command=self._action_save_blob_to_saves)
        darken_menus((self._ctx,))

        self._col_vars = {}
        self._colmenu = tk.Menu(self, tearoff=0)
        col_defs = {
            "time": ("TIME", True),
            "name": ("NAME", True),
            "hash": ("HASH", True),
            "size": ("SIZE", True),
            "kind": ("TYPE", True),
            "src": ("SOURCE", False),
        }
        for col in self.columns:
            label, default = col_defs[col]
            var = tk.BooleanVar(value=self.settings.get("columns", {}).get(col, default))
            self._col_vars[col] = var
            self._colmenu.add_checkbutton(label=label, variable=var, command=self._update_displaycolumns)
        self._update_displaycolumns(save=False)
        darken_menus((self._colmenu,))

        self.tree.bind("<Button-3>", self._on_tree_right_click)
        self.tree.bind("<Control-Button-1>", self._on_tree_right_click)
        self.tree.bind("<Motion>", self._on_tree_motion)
        self.tree.bind("<Leave>", self._on_tree_leave)

        self.details = ttk.Frame(self.vpaned)
        self.vpaned.add(self.details, weight=2)
        _set_pane_minsize(self.vpaned, self.details, 100)

        self.detail_pane = ttk.PanedWindow(self.details, orient="vertical")
        self.detail_pane.pack(fill="both", expand=True)

        self.viewport_host = ttk.Frame(self.detail_pane)
        self.detail_pane.add(self.viewport_host, weight=3)
        self.viewport_3d = Viewport3DPanel(self.viewport_host)
        self.viewport_3d.is_own_host = True

        self.text_host = ttk.Frame(self.detail_pane)
        self.detail_pane.add(self.text_host, weight=1)

        self.details_text = tk.Text(self.text_host, wrap="word", height=6, font=("Consolas", 10),
                                bg="#252526", fg="#d4d4d4", insertbackground="#ffffff",
                                selectbackground="#007acc", selectforeground="#ffffff",
                                relief="flat", bd=0)
        d_vsb = ttk.Scrollbar(self.text_host, orient="vertical", command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=d_vsb.set)
        self.details_text.grid(row=0, column=0, sticky="nsew")
        d_vsb.grid(row=0, column=1, sticky="ns")
        self.text_host.rowconfigure(0, weight=1)
        self.text_host.columnconfigure(0, weight=1)

        self.after(50, self._ensure_pane_order)

        status = ttk.Frame(self.viewer_root, padding=(8, 6, 8, 8))
        status.pack(fill="x")
        self.status_label = ttk.Label(status, text="")
        self.status_label.pack(side="left")

    def _ensure_pane_order(self):
        try:
            panes = self.vpaned.panes()
            tf = str(self.table_frame)
            df = str(self.details)
            if not panes or panes[0] != tf:
                self.vpaned.forget(self.table_frame)
                self.vpaned.forget(self.details)
                self.vpaned.add(self.table_frame, weight=3)
                _set_pane_minsize(self.vpaned, self.table_frame, 200)
                self.vpaned.add(self.details, weight=2)
                _set_pane_minsize(self.vpaned, self.details, 100)
        except Exception:
            pass

    def _clamp_hsash(self):
        try:
            panes = self.hpaned.panes()
            if len(panes) < 2:
                return
            total = self.hpaned.winfo_width()
            pos = self.hpaned.sashpos(0)
            min_left = VIEWER_MIN_WIDTH
            min_right = REPLACER_MIN_WIDTH
            self.hpaned.sashpos(0, max(min_left, min(pos, total - min_right)))
        except Exception:
            pass

    def _toggle_viewer_pane(self):
        if self.viewer_collapsed:
            try:
                if self._restore_geom:
                    w, h, _, _ = self._restore_geom
                    cur_w = self.winfo_width()
                    cur_x = self.winfo_x()
                    cur_y = self.winfo_y()
                    right = cur_x + cur_w
                    new_x = right - w
                    self.geometry(f"{w}x{h}+{new_x}+{cur_y}")
                self.hpaned.insert(0, self.viewer_root, weight=3)
                _set_pane_minsize(self.hpaned, self.viewer_root, VIEWER_MIN_WIDTH)
                self.hpaned.paneconfigure(self.replacer, weight=2)
                _set_pane_minsize(self.hpaned, self.replacer, REPLACER_MIN_WIDTH)
                self.update_idletasks()
                total = self.hpaned.winfo_width()
                if total > 0:
                    pos = self._saved_sash if self._saved_sash is not None else int(total * HPANED_LEFT_FRACTION)
                    self.hpaned.sashpos(0, pos)
                    self._clamp_hsash()
            except Exception:
                pass
            self.viewer_collapsed = False
            self.collapse_btn.config(text="\u25c0")
            self._save_settings()
        else:
            try:
                self.update_idletasks()
                self._restore_geom = (self.winfo_width(), self.winfo_height(), self.winfo_x(), self.winfo_y())
                self._saved_sash = None
                try:
                    self._saved_sash = self.hpaned.sashpos(0)
                except Exception:
                    pass
                viewer_w = self.viewer_root.winfo_width()
                self.hpaned.forget(self.viewer_root)
                min_w, _ = self.wm_minsize()
                orig_w, h, x, y = self._restore_geom
                new_w = max(orig_w - viewer_w, min_w)
                orig_right = x + orig_w
                new_x = orig_right - new_w
                self.geometry(f"{new_w}x{h}+{new_x}+{y}")
            except Exception:
                pass
            self.viewer_collapsed = True
            self.collapse_btn.config(text="\u25b6")
            self._save_settings()

    def _save_settings(self):
        data = {
            "autoscroll": self.autoscroll.get(),
            "hide_tickets": self.hide_tickets.get(),
            "stay_on_top": self.stay_on_top.get(),
            "show_lines": self.show_lines.get(),
            "fps_limit": self.fps_limit.get() if hasattr(self, "fps_limit") else self.settings.get("fps_limit", 0),
            "type_filter": self.type_filter.get(),
            "columns": {c: var.get() for c, var in getattr(self, "_col_vars", {}).items()},
            "viewer_collapsed": self.viewer_collapsed,
            "theme": self.theme_var.get() if hasattr(self, "theme_var") else self.settings.get("theme", DEFAULT_THEME),
            "fflag_hotkeys": self.fflag_hotkeys,
            "fflag_auto_apply": self.fflag_auto_apply.get() if hasattr(self,"fflag_auto_apply") else self.settings.get("fflag_auto_apply",False),
            "roblox_path": self.settings.get("roblox_path",""),
            "roblox_username": self.settings.get("roblox_username",""),
            "roblox_user_id": self.settings.get("roblox_user_id",""),
            "fps_limit": self.fps_limit.get() if hasattr(self, "fps_limit") else self.settings.get("fps_limit", 0),
        }
        save_settings(data)
        self.settings = data

    def _apply_startup_layouts(self):
        try:
            total = self.vpaned.winfo_height()
            if total > 0:
                self.vpaned.sashpos(0, int(total * PANED_TOP_FRACTION))
        except Exception:
            pass
        try:
            total = self.hpaned.winfo_width()
            if total > 0:
                self.hpaned.sashpos(0, int(total * HPANED_LEFT_FRACTION))
                self._clamp_hsash()
        except Exception:
            pass
        self._autosize_columns_once()

    def _autosize_columns_once(self, padding=24):
        cols = self.tree["columns"]
        for c in cols:
            try:
                w = tkfont.Font().measure(self.tree.heading(c)["text"])
            except Exception:
                w = 80
            for i, iid in enumerate(self.tree.get_children("")):
                if i > 500:
                    break
                text = str(self.tree.set(iid, c))
                w = max(w, tkfont.Font().measure(text))
            measured = min(max(w + padding, 80), 520)
            current = int(self.tree.column(c, "width"))
            self.tree.column(c, width=max(current, measured))

    def _cache_type_matches(self, it, selected):
        """Return True when a scanned cache item belongs to a delete category."""
        cat = str(it.kind or "").split(" ", 1)[0].strip().lower()
        selected = str(selected).strip().lower()
        if selected == "mesh":
            return cat == "mesh"
        if selected == "model/rbxm":
            return cat in {"model", "rbxm", "rbxl", "rbxl (place)"}
        if selected == "animation":
            return cat == "animation"
        if selected == "image":
            return cat in {"image", "decal", "texture"}
        if selected == "audio":
            return cat in {"sound", "audio"}
        if selected == "font":
            return cat == "font"
        if selected == "text":
            return cat in {"text", "translations", "translation"}
        if selected == "unknown":
            return cat == "unknown"
        return False

    def _open_delete_cache_type(self):
        dlg = tk.Toplevel(self)
        dlg.title("Delete Cache Type")
        dlg.resizable(False, False)
        dlg.transient(self)
        theme_toplevel(dlg)

        outer = ttk.Frame(dlg, padding=12)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="Delete all caches of this type:").pack(anchor="w", pady=(0, 7))

        type_var = tk.StringVar(value="Mesh")
        combo = ttk.Combobox(
            outer,
            textvariable=type_var,
            values=("Mesh", "Model/RBXM", "Animation", "Image", "Audio", "Font", "Text", "Unknown"),
            state="readonly",
            width=18,
        )
        combo.pack(fill="x")

        def do_delete():
            selected = type_var.get()
            dlg.destroy()
            self._delete_cache_type(selected)

        btns = ttk.Frame(outer)
        btns.pack(fill="x", pady=(10, 0))
        ttk.Button(btns, text="Delete", command=do_delete).pack(side="left")
        ttk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="right")
        combo.focus_set()

    def _delete_cache_type(self, selected):
        """Find and delete one cache category without blocking/crashing Tk."""
        if getattr(self, "_cache_type_busy", False):
            return
        self._cache_type_busy = True
        try:
            self.btn_delete_type.config(state="disabled")
        except Exception:
            pass

        was_running = bool(self.watching)
        if was_running:
            self._stop_watching()

        def scan_worker():
            try:
                if not os.path.isfile(self.db_path):
                    result = ("error", "rbx-storage.db was not found.")
                else:
                    items = scan_db_once(self.db_path, self.shard_root, set(), None)
                    targets = [it for it in items if self._cache_type_matches(it, selected)]
                    result = ("found", targets)
            except Exception as e:
                result = ("error", str(e))
            self.after(0, lambda r=result: self._delete_cache_type_scan_done(selected, r, was_running))

        threading.Thread(target=scan_worker, daemon=True, name="RoUtils-DeleteTypeScan").start()

    def _delete_cache_type_scan_done(self, selected, result, was_running):
        if result[0] == "error":
            self._finish_delete_cache_type(("error", result[1]), was_running)
            return
        targets = result[1]
        if not targets:
            self._finish_delete_cache_type(("none", None), was_running)
            return
        try:
            ok = messagebox.askyesno(
                "Delete Cache Type",
                f"Delete all {len(targets)} {selected} cache(s)?\n\nThis cannot be undone.",
                parent=self,
            )
        except Exception as e:
            self._finish_delete_cache_type(("error", str(e)), was_running)
            return
        if not ok:
            self._finish_delete_cache_type(("cancel", None), was_running)
            return

        def delete_worker():
            deleted_ids = []
            failed = 0
            try:
                conn = connect_rw(self.db_path)
                try:
                    cur = conn.cursor()
                    cur.execute("BEGIN IMMEDIATE")
                    for it in targets:
                        try:
                            cur.execute("DELETE FROM files WHERE id=?", (it.id_bytes,))
                            if cur.rowcount:
                                deleted_ids.append(it)
                        except Exception:
                            failed += 1
                    conn.commit()
                finally:
                    conn.close()

                for it in deleted_ids:
                    try:
                        spath = shard_path(self.shard_root, it.hash)
                        if os.path.isfile(spath):
                            os.remove(spath)
                    except Exception:
                        failed += 1
                self.after(0, lambda: self._finish_delete_cache_type(("ok", len(deleted_ids), failed, deleted_ids, selected), was_running))
            except Exception as e:
                self.after(0, lambda e=e: self._finish_delete_cache_type(("error", str(e)), was_running))

        threading.Thread(target=delete_worker, daemon=True, name="RoUtils-DeleteTypeDelete").start()

    def _finish_delete_cache_type(self, result, was_running):
        try:
            kind = result[0]
            if kind == "none":
                messagebox.showinfo("Delete Cache Type", "No caches of the selected type were found.", parent=self)
            elif kind == "cancel":
                pass
            elif kind == "ok":
                _, deleted, failed, targets, selected = result
                for it in targets:
                    self.seen_hashes.discard(it.hash)
                    self.items_by_iid.pop(it.hash, None)
                    self.items_by_hash.pop(it.hash, None)

                    for iid in self.tree.get_children(""):
                        try:
                            vals = self.tree.item(iid, "values")
                            if len(vals) > 2 and str(vals[2]) == str(it.hash):
                                self.tree.delete(iid)
                                break
                        except Exception:
                            pass
                self._update_status()
                msg = f"Deleted {deleted} {selected} cache(s)."
                if failed:
                    msg += f"\nFailed: {failed}"
                messagebox.showinfo("Delete Cache Type", msg, parent=self)
            else:
                messagebox.showerror("Delete Cache Type", str(result[1]), parent=self)
        except Exception as e:
            try:
                messagebox.showerror("Delete Cache Type", str(e), parent=self)
            except Exception:
                pass
        finally:
            self._cache_type_busy = False
            try:
                self.btn_delete_type.config(state="normal")
            except Exception:
                pass
            if was_running and not self.watching:
                self._start_watching()

    def _cache_type_label(self, result):

        return "selected type"

    def _dump_blob_body(self, blob):
        """Return the decompressed cache body and RBXH metadata."""
        meta = parse_rbxh(blob)
        body = meta.get("body") or b""
        if not body:
            return b"", meta
        try:
            body = _maybe_gunzip(body, meta.get("headers") or {})
        except Exception:
            pass
        try:
            body = decompress_if_needed(body)
        except Exception:
            pass
        return body, meta

    def _dump_image_payload(self, body):
        """Extract an embedded image and return (bytes, extension)."""
        try:
            label, off = find_embedded_image(body)
            if off > 0:
                body = body[off:]
            img = Image.open(io.BytesIO(body))
            out = io.BytesIO()
            fmt = (img.format or "PNG").upper()
            if fmt == "JPEG":
                ext = ".jpg"
                img.save(out, format="JPEG")
            elif fmt == "WEBP":
                ext = ".webp"
                img.save(out, format="WEBP")
            elif fmt == "GIF":
                ext = ".gif"
                img.save(out, format="GIF")
            else:
                ext = ".png"
                if img.mode not in ("RGB", "RGBA", "L", "LA", "P"):
                    img = img.convert("RGBA")
                img.save(out, format="PNG")
            return out.getvalue(), ext
        except Exception:
            return None, None

    def _dump_one_cache(self, it, dump_root):
        blob = self._fetch_full_blob(it)
        if not blob:
            return False
        body, meta = self._dump_blob_body(blob)
        if not body:
            return False

        cat = str(it.kind or "Unknown").split(" ", 1)[0].strip()
        cat_low = cat.lower()
        folder = "Unknown"
        payload = body
        ext = ".bin"

        if cat_low == "mesh":
            folder, ext = "Meshes", ".obj"
            try:
                obj = convert(body)
            except Exception:
                obj = None
            if not obj:
                return False
            payload = obj.encode("utf-8")
        elif cat_low in {"model", "rbxm", "rbxl", "rbxl (place)"}:
            folder = "Model-RBXM"
            out = self._rbxm_body(it)
            if out:
                payload, is_binary = out
                ext = ".rbxm" if is_binary else ".rbxmx"
            else:
                ext = ".rbxh"
                payload = blob
        elif cat_low == "animation":
            folder = "Animations"
            out = self._rbxm_body(it)
            if out:
                payload, is_binary = out
                ext = ".rbxm" if is_binary else ".rbxmx"
            else:
                ext = ".bin"
        elif cat_low in {"image", "decal", "texture"}:
            folder = "Images"
            img_payload, img_ext = self._dump_image_payload(body)
            if img_payload:
                payload, ext = img_payload, img_ext
            else:

                ext = ".ktx2" if b"KTX 20" in body[:64] else (".ktx" if b"KTX 11" in body[:64] else ".bin")
        elif cat_low in {"sound", "audio"}:
            folder = "Audios"
            lbl = str(it.kind).lower()
            if "ogg" in lbl or body.startswith(b"OggS"):
                ext = ".ogg"
            elif "wav" in lbl or (len(body) >= 12 and body[:4] == b"RIFF" and body[8:12] == b"WAVE"):
                ext = ".wav"
            elif body.startswith(b"ID3"):
                ext = ".mp3"
            else:
                ext = ".bin"
        elif cat_low == "font":
            folder, ext = "Fonts", ".ttf"
            if b"OTTO" in body[:4]:
                ext = ".otf"
        elif cat_low in {"translations", "translation"}:
            folder, ext = "Translations", ".json"
        elif cat_low == "text":
            folder, ext = "Text", ".txt"
        elif cat_low == "video":
            folder = "Videos"
            ext = ".webm" if body[:4] == b"\x1a\x45\xdf\xa3" else ".mp4"
        elif cat_low == "compressed":
            folder, ext = "Compressed", ".bin"

        out_dir = os.path.join(dump_root, folder)
        os.makedirs(out_dir, exist_ok=True)
        name = _sanitize_filename_for_windows(it.name or it.hash) or it.hash
        path = os.path.join(out_dir, f"{name}_{it.hash}{ext}")
        with open(path, "wb") as f:
            f.write(payload)
        return True

    def _dump_all_caches(self):
        """Launch a real console process for dumping; keep the GUI untouched."""
        try:
            if getattr(sys, "frozen", False):
                command = [sys.executable, "--dump-caches"]
            else:


                pyexe = sys.executable
                base = os.path.basename(pyexe).lower()
                if base == "pythonw.exe":
                    candidate = os.path.join(os.path.dirname(pyexe), "python.exe")
                    if os.path.isfile(candidate):
                        pyexe = candidate
                command = [pyexe, os.path.abspath(__file__), "--dump-caches"]

            subprocess.Popen(
                ["cmd.exe", "/k"] + command,
                creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0),
                close_fds=True,
            )
        except Exception as e:
            messagebox.showerror("Dump Caches", f"Could not open dump CMD:\n{e}", parent=self)

    def _run_dump_caches_cli(self):
        """Dump caches from a console-only helper; no Tk GUI is required."""
        if os.name == "nt":
            try:
                ctypes.windll.kernel32.AllocConsole()
            except Exception:
                pass

        dump_root = os.path.join(DATA_DIR, "Dump")
        os.makedirs(dump_root, exist_ok=True)
        db_path, shard_root = default_paths()
        if not os.path.isfile(db_path):
            print("ERROR: rbx-storage.db was not found.", flush=True)
            return 1

        print("RoUtils - Dump Caches", flush=True)
        print(f"Database: {db_path}", flush=True)
        print(f"Dump folder: {dump_root}", flush=True)
        print("Scanning cache...", flush=True)




        helper = object.__new__(App)
        helper.db_path = db_path
        helper.shard_root = shard_root

        try:
            items = scan_db_once(db_path, shard_root, set(), None)
        except Exception as e:
            print(f"ERROR while scanning: {e}", flush=True)
            return 1

        dumped = 0
        failed = 0
        total = len(items)
        print(f"Found {total} cache(s).", flush=True)
        print()

        for index, it in enumerate(items, 1):
            try:
                if App._dump_one_cache(helper, it, dump_root):
                    dumped += 1
                else:
                    failed += 1
            except Exception as e:
                failed += 1
                print(f"Failed {it.hash}: {e}", flush=True)
            if index % 10 == 0 or index == total:
                print(f"Processed {index}/{total} | dumped={dumped} failed={failed}", flush=True)

        print()
        print(f"Finished. Dumped: {dumped} | Failed: {failed}", flush=True)
        print(f"Output: {dump_root}", flush=True)
        return 0

    def _clear_storage_now(self):
        was = self.watching
        if was:
            self._stop_watching()

        deleted_db = False
        try:
            if os.path.isfile(self.db_path):
                os.remove(self.db_path)
                deleted_db = True
        except Exception:
            pass

        deleted_shards = 0
        try:
            if os.path.isdir(self.shard_root):
                for a in os.listdir(self.shard_root):
                    ap = os.path.join(self.shard_root, a)
                    if os.path.isdir(ap) and len(a) == 2:
                        for f in os.listdir(ap):
                            fp = os.path.join(ap, f)
                            try:
                                if os.path.isfile(fp):
                                    os.remove(fp)
                                    deleted_shards += 1
                            except Exception:
                                pass
        except Exception:
            pass

        self.seen_hashes.clear()
        self.items_by_iid.clear()
        self.items_by_hash.clear()
        self.tree.delete(*self.tree.get_children())
        self._update_status()

        messagebox.showinfo("Clear rbx-storage", f"Deleted shards: {deleted_shards}\nDeleted DB: {'yes' if deleted_db else 'no'}")

        if was:
            self._start_watching()

    def _install_selected_db(self, source_db):
        """Replace Roblox storage with exactly one DB file.

        Removes db, -shm, -wal and .id, then installs only rbx-storage.db.
        No force-delete is used; locked files cause the operation to abort.
        """
        local = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
        roblox_dir = os.path.join(local, "Roblox")
        target = os.path.join(roblox_dir, "rbx-storage.db")
        sidecars = [
            target,
            target + "-shm",
            target + "-wal",
            os.path.join(roblox_dir, "rbx-storage.id"),
        ]
        os.makedirs(roblox_dir, exist_ok=True)

        source_db = os.path.abspath(source_db)
        if not os.path.isfile(source_db):
            raise FileNotFoundError(f"DB file not found: {source_db}")

        with tempfile.NamedTemporaryFile(prefix="routils_db_install_", suffix=".db", delete=False) as tf:
            temp_source = tf.name
        try:
            shutil.copy2(source_db, temp_source)
            conn = sqlite3.connect(temp_source, timeout=3)
            conn.execute("PRAGMA schema_version").fetchone()
            conn.close()

            backup_dir = tempfile.mkdtemp(prefix="routils_db_backup_")
            backups = {}
            try:
                for idx, path in enumerate(sidecars):
                    if os.path.isfile(path):
                        bp = os.path.join(backup_dir, f"{idx}.bak")
                        shutil.copy2(path, bp)
                        backups[path] = bp

                deleted = []
                try:
                    for path in sidecars:
                        if os.path.exists(path):
                            try:
                                os.remove(path)
                            except PermissionError as e:
                                raise PermissionError(
                                    f"Cannot delete '{os.path.basename(path)}'. Roblox or another program may be using it."
                                ) from e
                            except OSError as e:
                                raise OSError(
                                    f"Cannot delete '{os.path.basename(path)}': {e}"
                                ) from e
                            deleted.append(path)

                    shutil.copy2(temp_source, target)
                except Exception:
                    try:
                        if os.path.isfile(target) and target not in backups:
                            os.remove(target)
                    except Exception:
                        pass
                    for path, bp in backups.items():
                        try:
                            if os.path.exists(path):
                                os.remove(path)
                            shutil.copy2(bp, path)
                        except Exception:
                            pass
                    raise
            finally:
                shutil.rmtree(backup_dir, ignore_errors=True)
        finally:
            try:
                os.remove(temp_source)
            except Exception:
                pass

        self.db_path = target
        self.shard_root = os.path.join(roblox_dir, "rbx-storage")
        self.db_label.config(text=self.db_path)
        self._reset_seen(clear_list=True)
        return target

    def _choose_db(self):
        path = filedialog.askopenfilename(
            title="Select rbx-storage.db",
            filetypes=[("SQLite DB", "*.db"), ("All Files", "*.*")],
        )
        if not path:
            return
        was_watching = self.watching
        if was_watching:
            self._stop_watching()
        try:
            self._install_selected_db(path)
        except Exception as e:
            messagebox.showerror(
                "Choose DB File",
                "Could not replace Roblox storage files.\n\n"
                f"{e}\n\nClose Roblox and try again. No force-delete was used.",
            )
            if was_watching:
                self._start_watching()
            return
        if was_watching:
            self._start_watching()
        messagebox.showinfo(
            "Choose DB File",
            "Installed selected DB successfully.\n\n"
            "Deleted: rbx-storage.db, rbx-storage.db-shm, rbx-storage.db-wal, rbx-storage.id\n"
            "Installed: rbx-storage.db only.",
        )

    def _choose_shard_root(self):
        d = filedialog.askdirectory(title="Select shard root folder (rbx-storage)")
        if not d:
            return
        self.shard_root = d
        self._reset_seen(clear_list=False)

    def _toggle_watch(self):
        if self.watching:
            self._stop_watching()
        else:
            self._start_watching()

    def _start_watching(self):
        if not os.path.isfile(self.db_path):
            self._update_status()
            return
        self.stop_event.clear()
        self.watching = True
        self.toggle_btn.config(text="Stop Watching")
        self._update_status()
        self._launch_scan_loop()

    def _stop_watching(self):
        self.stop_event.set()
        self.watching = False
        self.toggle_btn.config(text="Start Watching")
        self._update_status()

    def _launch_scan_loop(self):
        if self.scan_thread and self.scan_thread.is_alive():
            return
        self.scan_thread = threading.Thread(target=self._scan_loop, daemon=True)
        self.scan_thread.start()

    def _scan_loop(self):
        while not self.stop_event.is_set():
            items = scan_db_once(self.db_path, self.shard_root, self.seen_hashes, None if self.max_rows.get() <= 0 else self.max_rows.get())
            if items:
                self.new_items_q.put(items)
            self.stop_event.wait(WATCH_INTERVAL_SEC)

    def _drain_queue(self):
        try:
            while True:
                items = self.new_items_q.get_nowait()
                self._insert_items(items)
        except queue.Empty:
            pass
        finally:
            self.after(150, self._drain_queue)

    def _should_display(self, it: ScanItem, filt: str) -> bool:
        if self.hide_tickets.get() and it.is_ticket:
            return False
        cat = it.kind.split(" ", 1)[0]
        tf = self.type_filter.get()
        if tf != "All":
            for (label, matcher) in TYPE_FILTERS:
                if label == tf:
                    if not matcher(cat):
                        return False
                    break
        row = (it.time, it.name, it.hash, human_size(it.size), it.kind, it.src)
        row_join = " ".join(map(str, row)).lower()
        if filt and filt not in row_join:
            return False
        return True

    def _insert_items(self, items: List[ScanItem]):
        filt = self.filter_text.get().lower().strip()
        for it in items:
            self.items_by_hash[it.hash] = it
            if not self._should_display(it, filt):
                continue
            iid = it.hash
            self.tree.insert("", "end", iid=iid, values=(it.time, it.name, it.hash, human_size(it.size), it.kind, it.src))
            self.items_by_iid[iid] = it
        if self.autoscroll.get():
            try:
                last = self.tree.get_children()[-1]
                self.tree.see(last)
            except IndexError:
                pass
        self._update_status()

    def _apply_filter(self):
        self.tree.delete(*self.tree.get_children())
        filt = self.filter_text.get().lower().strip()
        for _, it in self.items_by_hash.items():
            if not self._should_display(it, filt):
                continue
            self.tree.insert("", "end", iid=it.hash, values=(it.time, it.name, it.hash, human_size(it.size), it.kind, it.src))
        if self.autoscroll.get():
            try:
                last = self.tree.get_children()[-1]
                self.tree.see(last)
            except IndexError:
                pass
        self._update_status()

    def _apply_stay_on_top(self):
        self.wm_attributes("-topmost", self.stay_on_top.get())

    def _apply_show_lines(self):
        self.viewport_3d.show_wireframe.set(self.show_lines.get())
        if hasattr(self, "_titlebar"):
            try:
                self._titlebar.configure(bg=_CURRENT_PALETTE["bg_dark"])
                for child in self._titlebar.winfo_children():
                    if isinstance(child, tk.Label): child.configure(bg=_CURRENT_PALETTE["bg_dark"], fg=_CURRENT_PALETTE["fg"])
            except Exception:
                pass
        if self.viewport_3d.winfo_ismapped():
            self.viewport_3d.draw_frame()

    def _show_details(self):
        self._cancel_image_preview()
        sel = self.tree.selection()
        if not sel:
            return
        multi = len(sel)
        iid = sel[0]
        it = self.items_by_iid.get(iid) or self.items_by_hash.get(iid)
        if not it:
            return
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", "end")
        lines = [
            f"Hash:    {it.hash}",
            f"Name:    {it.name}",
            f"Time:    {it.time}",
            f"Source:  {it.src}",
            f"Wrapped: {it.wrapped}",
            f"Size:    {human_size(it.size)}",
            f"Type:    {it.kind}",
        ]
        if multi > 1:
            lines.append(f"Selection: {multi} rows (actions apply to all selected)")
        if it.content_type:
            lines.append(f"Content-Type: {it.content_type}")
        lines.append(f"URL:     {it.url}")
        lines.append("")
        if it.header_text:
            lines.append("RBXH headers (best-effort):")
            lines.append(it.header_text.strip())
            lines.append("")
        if it.is_ticket:
            lines.append("Note: This is a signed-URL ticket cached by the client before fetching the real asset.")
        self.details_text.insert("1.0", "\n".join(lines))
        self.details_text.configure(state="disabled")

    def _update_preview(self):
        
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        it = self.items_by_iid.get(iid) or self.items_by_hash.get(iid)
        if not it:
            return
        blob = self._fetch_full_blob(it)
        if not blob:
            self.viewport_3d.hide()
            return
        meta = parse_rbxh(blob)
        body = meta.get("body") or b""
        cat = it.kind.split(" ", 1)[0]

        is_mesh = cat == "Mesh"
        is_anim = cat == "Animation"
        is_audio = cat == "Sound"
        is_model = cat in ("Model", "RBXM", "rbxl (place)")
        if not (is_mesh or is_anim or is_audio or is_model):
            self.viewport_3d.hide()
            return

        temp_pkg_path = os.path.join(TEMP_EMU_DIR, f"preview_{it.hash}.bin")
        try:
            with open(temp_pkg_path, "wb") as f:
                f.write(body)
        except Exception:
            pass

        self.viewport_3d.set_asset_data_from_temp(
            temp_pkg_path, is_anim=is_anim, is_mesh=is_mesh, is_model=is_model, is_audio=is_audio
        )
        if is_anim:
            self.viewport_3d.show(is_anim=True, mode_label="Animation View")
        elif is_mesh:
            self.viewport_3d.show(is_anim=False, mode_label="Mesh View")
        elif is_model:
            self.viewport_3d.show(is_anim=False, mode_label="Model View")
        else:
            self.viewport_3d.show(is_anim=False, mode_label="Audio View")

    def _update_displaycolumns(self, save: bool = True):
        cols = [c for c in self.columns if self._col_vars[c].get()]
        if not cols:
            first = self.columns[0]
            self._col_vars[first].set(True)
            cols = [first]
        self.tree.config(displaycolumns=cols)
        for c in cols:
            w = self.tree.column(c, width=None)
            self.tree.column(c, width=w)
        self.tree.update_idletasks()
        if save:
            self._save_settings()

    def _on_tree_select(self, event):
        self._clear_tree_hover()
        self._show_details()
        self._update_preview()
    def _clear_tree_hover(self):
        if self._tree_hover_iid:
            tags = list(self.tree.item(self._tree_hover_iid, "tags"))
            if "hover" in tags:
                tags.remove("hover")
                self.tree.item(self._tree_hover_iid, tags=tags)
            self._tree_hover_iid = None

    def _on_tree_leave(self, event):
        self._cancel_image_preview()
        self._clear_tree_hover()

    def _on_tree_right_click(self, event):
        self._cancel_image_preview()
        region = self.tree.identify_region(event.x, event.y)
        if region == "heading":
            try:
                self._colmenu.tk_popup(event.x_root, event.y_root)
            finally:
                self._colmenu.grab_release()
            return
        row = self.tree.identify_row(event.y)
        if row:
            sel = self.tree.selection()
            
            if row not in sel:
                self.tree.selection_set(row)
            items = self._get_selected_items()
            if not items:
                return
            any_model = any((i.kind.split(" ", 1)[0] in ("RBXM", "Model")) for i in items)
            any_img = any((i.kind.split(" ", 1)[0] in ("Image", "Decal", "Texture")) for i in items)
            self._ctx.entryconfigure(self._ctx_rbxm_index, state=tk.NORMAL if any_model else tk.DISABLED)
            self._ctx.entryconfigure(self._ctx_img_index, state=tk.NORMAL if any_img else tk.DISABLED)
            try:
                self._ctx.tk_popup(event.x_root, event.y_root)
            finally:
                self._ctx.grab_release()

    def _copy_selected_hash(self):
        items = self._get_selected_items()
        if not items:
            return
        joined = "\n".join(it.hash for it in items)
        self.clipboard_clear()
        self.clipboard_append(joined)
        self.update_idletasks()
        messagebox.showinfo("Copied", f"Copied {len(items)} hash(es) to clipboard.")

    def _on_tree_motion(self, event):
        row = self.tree.identify_row(event.y)
        self._hover_preview_xy = (event.x_root, event.y_root)
        if row != self._tree_hover_iid:
            self._clear_tree_hover()
            if row:
                tags = list(self.tree.item(row, "tags"))
                if "hover" not in tags:
                    tags.append("hover")
                    self.tree.item(row, tags=tags)
                self._tree_hover_iid = row
        if row == self._hover_preview_iid:
            return
        self._cancel_image_preview()
        if not row:
            return
        it = self.items_by_iid.get(row) or self.items_by_hash.get(row)
        if not it:
            return
        cat = it.kind.split(" ", 1)[0]
        if cat in ("Image", "Decal", "Texture"):
            self._hover_preview_iid = row
            self._hover_preview_job = self.after(1200, self._show_image_preview)

    def _cancel_image_preview(self):
        if self._hover_preview_job:
            try:
                self.after_cancel(self._hover_preview_job)
            except Exception:
                pass
            self._hover_preview_job = None
        self._hover_preview_iid = None
        if self._img_preview_fade_job:
            try:
                self.after_cancel(self._img_preview_fade_job)
            except Exception:
                pass
            self._img_preview_fade_job = None
        if self._img_preview_win and self._img_preview_win.winfo_exists():
            self._fade_preview(0.0)

    def _show_image_preview(self):
        self._hover_preview_job = None
        iid = self._hover_preview_iid
        if not iid:
            return
        it = self.items_by_iid.get(iid) or self.items_by_hash.get(iid)
        if not it:
            return
        blob = self._fetch_full_blob(it)
        if not blob:
            return
        meta = parse_rbxh(blob)
        body = meta.get("body") or b""
        _, off = find_embedded_image(body)
        if off > 0:
            body = body[off:]
        try:
            img = Image.open(io.BytesIO(body))
            img.thumbnail((256, 256))
            photo = ImageTk.PhotoImage(img)
        except Exception:
            return
        if not self._img_preview_win or not self._img_preview_win.winfo_exists():
            self._img_preview_win = tk.Toplevel(self)
            self._img_preview_win.wm_overrideredirect(True)
            theme_toplevel(self._img_preview_win)
            self._img_preview_label = ttk.Label(self._img_preview_win)
            self._img_preview_label.pack()
        if self._img_preview_fade_job:
            try:
                self.after_cancel(self._img_preview_fade_job)
            except Exception:
                pass
            self._img_preview_fade_job = None
        self._img_preview_photo = photo
        self._img_preview_label.configure(image=photo)
        x, y = self._hover_preview_xy
        self._img_preview_win.geometry(f"+{x+16}+{y+16}")
        try:
            self._img_preview_win.attributes("-alpha", 0.0)
        except Exception:
            pass
        self._img_preview_win.deiconify()
        self._img_preview_win.lift()
        self._fade_preview(1.0)

    def _fade_preview(self, target: float, step: float = 0.12):
        if not self._img_preview_win or not self._img_preview_win.winfo_exists():
            return
        try:
            cur = float(self._img_preview_win.attributes("-alpha"))
        except Exception:
            self._img_preview_win.attributes("-alpha", target)
            if target == 0.0:
                self._img_preview_win.withdraw()
            return
        if (target > cur and cur >= target - step) or (target < cur and cur <= target + step):
            self._img_preview_win.attributes("-alpha", target)
            if target == 0.0:
                self._img_preview_win.withdraw()
            self._img_preview_fade_job = None
            return
        cur += step if target > cur else -step
        self._img_preview_win.attributes("-alpha", cur)
        self._img_preview_fade_job = self.after(25, self._fade_preview, target, step)

    def _fetch_full_blob(self, it: ScanItem) -> Optional[bytes]:
        try:
            conn = connect_ro(self.db_path)
            cur = conn.cursor()
            cur.execute("SELECT content FROM files WHERE id=?", (it.id_bytes,))
            row = cur.fetchone()
        except Exception:
            row = None
        finally:
            try:
                conn.close()
            except Exception:
                pass

        if row is None:
            return read_shard_bytes(self.shard_root, it.hash)
        content = row[0]
        if content is not None:
            return content
        return read_shard_bytes(self.shard_root, it.hash)

    def _export_selected_full(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo("Export Blob", "Select a row first.")
            return
        if len(items) == 1:
            self._export_one_full(items[0])
            return
        directory = filedialog.askdirectory(title="Export Full Blobs to folder")
        if not directory:
            return
        saved = 0
        for it in items:
            blob = self._fetch_full_blob(it)
            if not blob:
                continue
            ext = ".rbxh" if blob[:4] == RBXH_MAGIC else ".bin"
            path = os.path.join(directory, f"{it.hash}{ext}")
            try:
                with open(path, "wb") as f:
                    f.write(blob)
                saved += 1
            except Exception:
                pass
        messagebox.showinfo("Export Blob", f"Exported {saved} of {len(items)} blobs to:\n{directory}")

    def _export_one_full(self, it):
        blob = self._fetch_full_blob(it)
        if not blob:
            messagebox.showerror("Export Blob", "Unable to read blob (DB/shard).")
            return

        ext = ".rbxh" if blob[:4] == RBXH_MAGIC else ".bin"
        default_name = f"{it.hash}{ext}"
        path = filedialog.asksaveasfilename(
            title="Export Full Blob",
            defaultextension=ext,
            initialfile=default_name,
            filetypes=[("RBXH blob", "*.rbxh"), ("Binary", "*.bin"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "wb") as f:
                f.write(blob)
            messagebox.showinfo("Export Blob", f"Saved full blob:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Blob", f"Failed to save file:\n{e}")

    def _export_selected_rbxm(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo("Export RBXM", "Select a row first.")
            return
        if len(items) > 1:
            directory = filedialog.askdirectory(title="Export RBXM models to folder")
            if not directory:
                return
            saved = 0
            for it in items:
                out = self._rbxm_body(it)
                if not out:
                    continue
                ext = ".rbxm" if out[1] else ".rbxmx"
                path = os.path.join(directory, f"{it.hash}{ext}")
                try:
                    with open(path, "wb") as f:
                        f.write(out[0])
                    saved += 1
                except Exception:
                    pass
            messagebox.showinfo("Export RBXM", f"Exported {saved} of {len(items)} models to:\n{directory}")
            return
        it = items[0]
        out = self._rbxm_body(it)
        if not out:
            return
        body, is_binary = out
        ext = ".rbxm" if is_binary else ".rbxmx"
        default_name = f"{it.hash}{ext}"
        path = filedialog.asksaveasfilename(
            title="Export RBXM",
            defaultextension=ext,
            initialfile=default_name,
            filetypes=[("Roblox model", f"*{ext}"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "wb") as f:
                f.write(body)
            messagebox.showinfo("Export RBXM", f"Saved model:\n{path}")
        except Exception as e:
            messagebox.showerror("Export RBXM", f"Failed to save file:\n{e}")

    def _rbxm_body(self, it):
        
        try:
            blob = self._fetch_full_blob(it)
            if not blob:
                return None
            meta = parse_rbxh(blob)
            body = meta.get("body") or b""
            if not body:
                return None
            body = _maybe_gunzip(body, meta.get("headers") or {})
            body = decompress_if_needed(body)

            magic = body.find(b"<roblox!")
            if magic == -1:
                magic = body.find(b"<roblox")
            if magic > 0:
                body = body[magic:]
            stripped = body.lstrip()
            if stripped.startswith(b"\xef\xbb\xbf"):
                stripped = stripped[3:].lstrip()
            if stripped.startswith(b"<roblox!"):
                return body, True

            if b"<roblox" in body[:4096]:
                if _write_rbxm is not None:
                    try:
                        return write_rbxm(_xml_to_document(body)), True
                    except Exception:
                        return body, False
                return body, False
        except Exception:
            return None
        return None

    def _export_selected_image(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo("Export Image", "Select a row first.")
            return
        if len(items) > 1:
            directory = filedialog.askdirectory(title="Export images to folder")
            if not directory:
                return
            saved = 0
            for it in items:
                img = self._image_from_item(it)
                if not img:
                    continue
                fmt = (img.format or "PNG").upper()
                ext = f".{fmt.lower()}"
                path = os.path.join(directory, f"{it.hash}{ext}")
                try:
                    img.save(path)
                    saved += 1
                except Exception:
                    pass
            messagebox.showinfo("Export Image", f"Exported {saved} of {len(items)} images to:\n{directory}")
            return
        it = items[0]
        img = self._image_from_item(it)
        if not img:
            messagebox.showerror("Export Image", "Blob does not contain a valid image.")
            return
        fmt = (img.format or "PNG").upper()
        ext = f".{fmt.lower()}"
        default_name = f"{it.hash}{ext}"
        path = filedialog.asksaveasfilename(
            title="Export Image",
            defaultextension=ext,
            initialfile=default_name,
            filetypes=[(f"{fmt} image", f"*{ext}"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            img.save(path)
            messagebox.showinfo("Export Image", f"Saved image:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Image", f"Failed to save file:\n{e}")

    def _image_from_item(self, it) -> Optional[Image.Image]:
        blob = self._fetch_full_blob(it)
        if not blob:
            return None
        meta = parse_rbxh(blob)
        body = meta.get("body") or b""
        _, off = find_embedded_image(body)
        if off > 0:
            body = body[off:]
        try:
            return Image.open(io.BytesIO(body))
        except Exception:
            return None

    def _get_selected_item(self) -> Optional[ScanItem]:
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("No Selection", "Select a row first.")
            return None
        it = self.items_by_iid.get(sel[0]) or self.items_by_hash.get(sel[0])
        if not it:
            messagebox.showerror("Selection Error", "Selected row is no longer available.")
            return None
        return it

    def _get_selected_items(self) -> List[ScanItem]:
        
        out: List[ScanItem] = []
        for s in self.tree.selection():
            it = self.items_by_iid.get(s) or self.items_by_hash.get(s)
            if it:
                out.append(it)
        return out

    def _pause_scanner(self):
        was = self.watching
        if was:
            self._stop_watching()
        return was

    def _resume_scanner(self, was_running: bool):
        if was_running:
            self._start_watching()

    def _parse_new_hash(self, s: str, expected_nibbles: int) -> bytes:
        if not s:
            raise ValueError("Empty input.")
        s = s.strip()
        if s.lower().startswith("0x"):
            s = s[2:]
        s = re.sub(r"[^0-9A-Fa-f]", "", s)
        if len(s) != expected_nibbles:
            raise ValueError(f"Hash must be {expected_nibbles} hex characters (got {len(s)}).")
        try:
            return bytes.fromhex(s)
        except Exception:
            raise ValueError("Invalid hex characters.")

    def _action_change_hash(self):
        it = self._get_selected_item()
        if not it:
            return
        expected_nibbles = len(it.id_bytes) * 2
        new_hash = simpledialog.askstring(
            "Change Hash", f"Enter new {expected_nibbles}-hex hash for this blob:", initialvalue=it.hash
        )
        if not new_hash:
            return
        try:
            new_id_b = self._parse_new_hash(new_hash, expected_nibbles)
            new_hash_hex = new_id_b.hex()
        except Exception as e:
            messagebox.showerror("Invalid Hash", str(e))
            return

        if not messagebox.askyesno("Confirm Change Hash", f"Update DB id and rename shard?\n\nOld: {it.hash}\nNew: {new_hash_hex}"):
            return

        was_running = self._pause_scanner()
        try:
            conn = connect_rw(self.db_path)
            try:
                cur = conn.cursor()
                cur.execute("BEGIN IMMEDIATE")
                cur.execute("UPDATE files SET id=? WHERE id=?", (new_id_b, it.id_bytes))
                conn.commit()
            finally:
                conn.close()

            old_path = shard_path(self.shard_root, it.hash)
            if os.path.isfile(old_path):
                new_dir = os.path.join(self.shard_root, new_hash_hex[:2])
                os.makedirs(new_dir, exist_ok=True)
                new_path = os.path.join(new_dir, new_hash_hex)
                try:
                    if os.path.isfile(new_path):
                        os.remove(new_path)
                    os.replace(old_path, new_path)
                except Exception as e:
                    messagebox.showwarning("Shard Rename", f"DB updated, but shard rename failed:\n{e}")

            old_hash = it.hash
            self.seen_hashes.discard(old_hash)
            self.items_by_iid.pop(old_hash, None)
            self.items_by_hash.pop(old_hash, None)
            try:
                self.tree.delete(old_hash)
            except Exception:
                pass

            it.hash, it.id_bytes = new_hash_hex, new_id_b
            self.seen_hashes.add(new_hash_hex)
            self.items_by_hash[new_hash_hex] = it

            self.tree.insert("", "end", iid=new_hash_hex, values=(it.time, it.name, it.hash, human_size(it.size), it.kind, it.src))
            self.tree.selection_set(new_hash_hex)
            self._update_status()
            messagebox.showinfo("Change Hash", "Hash updated successfully.")
        except Exception as e:
            messagebox.showerror("Change Hash", f"Failed to change hash:\n{e}")
        finally:
            self._resume_scanner(was_running)

    def _action_delete_blob(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo("Delete Blob", "Select a row first.")
            return
        names = ", ".join(it.hash for it in items[:12]) + ("…" if len(items) > 12 else "")
        if not messagebox.askyesno("Confirm Delete", f"Delete {len(items)} blob(s) from DB and remove shard files?\n\n{names}"):
            return

        was_running = self._pause_scanner()
        deleted = 0
        try:
            for it in items:
                try:
                    conn = connect_rw(self.db_path)
                    cur = conn.cursor()
                    cur.execute("BEGIN IMMEDIATE")
                    cur.execute("DELETE FROM files WHERE id=?", (it.id_bytes,))
                    conn.commit()
                    conn.close()
                except Exception:
                    pass

                spath = shard_path(self.shard_root, it.hash)
                if os.path.isfile(spath):
                    try:
                        os.remove(spath)
                    except Exception:
                        pass

                self.seen_hashes.discard(it.hash)
                self.items_by_iid.pop(it.hash, None)
                self.items_by_hash.pop(it.hash, None)
                try:
                    self.tree.delete(it.hash)
                except Exception:
                    pass
                deleted += 1
            self._update_status()
            messagebox.showinfo("Delete Blob", f"Deleted {deleted} blob(s).")
        except Exception as e:
            messagebox.showerror("Delete Blob", f"Failed to delete blob:\n{e}")
        finally:
            self._resume_scanner(was_running)

    def _action_save_hash_to_saves(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo("Save Hash", "Select a row first.")
            return

        name = simpledialog.askstring("Save Hash", "Name to show in Hash saves:")
        if not name:
            return

        safe_name = _sanitize_filename_for_windows(name.strip())
        if not safe_name:
            messagebox.showerror("Save Hash", "Name cannot be empty.")
            return

        base_dir = getattr(self.replacer, "hash_saves_dir", None)
        if not base_dir:
            messagebox.showerror("Save Hash", "Hash saves folder not available.")
            return
        os.makedirs(base_dir, exist_ok=True)

        saved = 0
        for idx, it in enumerate(items):
            label = safe_name if len(items) == 1 else f"{safe_name}_{idx+1}"
            filename = f"{it.hash} - {label}"
            dest = os.path.join(base_dir, filename)

            if os.path.exists(dest):
                base = filename
                i = 1
                while True:
                    cand = f"{base} ({i})"
                    cand_path = os.path.join(base_dir, cand)
                    if not os.path.exists(cand_path):
                        dest = cand_path
                        break
                    i += 1

            try:
                with open(dest, "x"):
                    pass
            except FileExistsError:
                with open(dest, "wb"):
                    pass
            except Exception as e:
                messagebox.showerror("Save Hash", f"Failed to save: {e}")
                return
            saved += 1

        try:
            if self.replacer.source_var.get() == "HashSaves":
                self.replacer.refresh_view()
        except Exception:
            pass

        messagebox.showinfo("Save Hash", f"Saved {saved} hash(es).")

    def _action_save_blob_to_saves(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo("Save Blob", "Select a row first.")
            return

        name = simpledialog.askstring("Save Blob", "File name to save in File saves:")
        if not name:
            return

        safe_name = _sanitize_filename_for_windows(name.strip())
        if not safe_name:
            messagebox.showerror("Save Blob", "Name cannot be empty.")
            return

        base_dir = getattr(self.replacer, "file_saves_dir", None)
        if not base_dir:
            messagebox.showerror("Save Blob", "File saves folder not available.")
            return
        os.makedirs(base_dir, exist_ok=True)

        saved = 0
        for idx, it in enumerate(items):
            blob = self._fetch_full_blob(it)
            if not blob:
                continue
            fname = safe_name if len(items) == 1 else f"{safe_name}_{idx+1}"
            dest = os.path.join(base_dir, fname)

            if os.path.exists(dest):
                b = fname
                i = 1
                while True:
                    cand = f"{b} ({i})"
                    cand_path = os.path.join(base_dir, cand)
                    if not os.path.exists(cand_path):
                        dest = cand_path
                        break
                    i += 1

            try:
                with open(dest, "wb") as f:
                    f.write(blob)
            except Exception as e:
                messagebox.showerror("Save Blob", f"Failed to save blob: {e}")
                return
            saved += 1

        try:
            if self.replacer.source_var.get() == "FileSaves":
                self.replacer.refresh_view()
        except Exception:
            pass

        messagebox.showinfo("Save Blob", f"Saved {saved} blob(s).")

    def _clear_list(self):
        self.tree.delete(*self.tree.get_children())
        self.items_by_iid.clear()
        self._update_status()

    def _reset_seen(self, clear_list: bool):
        self.seen_hashes.clear()
        if clear_list:
            self.tree.delete(*self.tree.get_children())
            self.items_by_iid.clear()
            self.items_by_hash.clear()
        self._update_status()

    def _sort_by(self, col_key: str, numeric: bool = False):
        def parse_size(s: str) -> float:
            s = s.strip().upper()
            try:
                if s.endswith("KB"):
                    return float(s[:-2]) * 1024
                if s.endswith("MB"):
                    return float(s[:-2]) * 1024**2
                if s.endswith("GB"):
                    return float(s[:-2]) * 1024**3
                if s.endswith("TB"):
                    return float(s[:-2]) * 1024**4
                if s.endswith("B"):
                    return float(s[:-1])
                return float(s)
            except Exception:
                return 0.0

        items = [(self.tree.set(k, col_key), k) for k in self.tree.get_children("")]
        if col_key == "size":
            items.sort(key=lambda t: parse_size(t[0]))
        else:
            items.sort(key=lambda t: t[0])
        if getattr(self, "_last_sort", None) == (col_key, "asc"):
            items.reverse()
            self._last_sort = (col_key, "desc")
        else:
            self._last_sort = (col_key, "asc")
        for idx, (_, k) in enumerate(items):
            self.tree.move(k, "", idx)

    def _update_status(self):
        total = len(self.items_by_hash)
        vis = len(self.tree.get_children())
        stat = "Watching" if self.watching else "Idle"
        self.status_label.config(text=f"Status: {stat}   Visible: {vis}   Total seen: {total}   Interval: {WATCH_INTERVAL_SEC:.1f}s")

    def _startup_setting_changed(self):
        self._save_settings(); self._install_startup_shortcut()

    def _install_startup_shortcut(self):
        if os.name!="nt": return
        startup=os.path.join(os.environ.get("APPDATA",""),"Microsoft","Windows","Start Menu","Programs","Startup")
        link=os.path.join(startup,"RoUtils.lnk")
        if not self.launch_on_startup.get():
            try: os.remove(link)
            except OSError: pass
            return
        try:
            target=sys.executable if getattr(sys,"frozen",False) else sys.executable
            args=""
            ps="& { $w=New-Object -ComObject WScript.Shell; $s=$w.CreateShortcut($env:LINK); $s.TargetPath=$env:TARGET; $s.Arguments=$env:ARGS; $s.WorkingDirectory=$env:WORK; $s.Save() }"
            env=os.environ.copy(); env.update({"LINK":link,"TARGET":target,"ARGS":args,"WORK":BASE_DIR})
            subprocess.run(["powershell","-NoProfile","-WindowStyle","Hidden","-Command",ps],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0),timeout=10)
        except Exception: pass

    def _on_close(self):
        self.watching = False; self.stop_event.set(); self._hotkey_stop.set(); self._save_settings()
        try: self.fflag_engine.close()
        except Exception: pass
        self.destroy()

def main():
    if "--dump-caches" in sys.argv:

        try:
            helper = object.__new__(App)
            code = App._run_dump_caches_cli(helper)
        except Exception as e:
            print(f"ERROR: {e}", flush=True)
            code = 1
        input("\nPress Enter to close...")
        raise SystemExit(code)

    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
