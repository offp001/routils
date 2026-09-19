import gzip
import hashlib
import html
import io
import math
import os
import queue
import re
import shlex
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
import traceback
import importlib.util
import winreg
import threading
import time
UI_HOTKEY_INTERVAL_MS = 75
UI_QUICK_PANEL_INTERVAL_MS = 200
UI_QUEUE_INTERVAL_MS = 200
UI_CLIENT_INTERVAL_MS = 1500
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
try:
    import sv_ttk
except Exception:
    sv_ttk = None
from urllib.parse import parse_qs, urlparse, urljoin
UI_THEME = 'clam'
THEMES = {'Midnight': {'bg_dark': '#1b1b1c', 'bg_medium': '#252526', 'bg_light': '#3a3a3c', 'bg_hover': '#464648', 'fg': '#dcdcdc', 'accent': '#7f8cff', 'border': '#444446'}, 'Ocean': {'bg_dark': '#0f2436', 'bg_medium': '#153248', 'bg_light': '#1f425e', 'bg_hover': '#2a5474', 'fg': '#d7e6f0', 'accent': '#3aa0ff', 'border': '#28506e'}, 'Hacker': {'bg_dark': '#0a0f0a', 'bg_medium': '#0f180f', 'bg_light': '#1a2a1a', 'bg_hover': '#223522', 'fg': '#b8ffb0', 'accent': '#2fff2f', 'border': '#2a4a2a'}, 'Amethyst': {'bg_dark': '#1a1423', 'bg_medium': '#241b31', 'bg_light': '#35284a', 'bg_hover': '#453665', 'fg': '#e0d6f0', 'accent': '#b06bff', 'border': '#4a3a63'}, 'Onyx': {'bg_dark': '#101010', 'bg_medium': '#171717', 'bg_light': '#262626', 'bg_hover': '#303030', 'fg': '#cfcfcf', 'accent': '#c0c0c0', 'border': '#333333'}}
THEMES.update({'Nord': {'bg_dark': '#1e2430', 'bg_medium': '#252d3a', 'bg_light': '#303a4a', 'bg_hover': '#3a4658', 'fg': '#d8dee9', 'accent': '#88c0d0', 'border': '#414b5d'}, 'Dracula': {'bg_dark': '#282a36', 'bg_medium': '#303241', 'bg_light': '#44475a', 'bg_hover': '#565a70', 'fg': '#f8f8f2', 'accent': '#bd93f9', 'border': '#44475a'}, 'Monokai': {'bg_dark': '#272822', 'bg_medium': '#2e2f2a', 'bg_light': '#3e3d32', 'bg_hover': '#49483e', 'fg': '#f8f8f2', 'accent': '#a6e22e', 'border': '#49483e'}, 'Solarized': {'bg_dark': '#002b36', 'bg_medium': '#073642', 'bg_light': '#586e75', 'bg_hover': '#657b83', 'fg': '#eee8d5', 'accent': '#2aa198', 'border': '#586e75'}, 'Rose Pine': {'bg_dark': '#191724', 'bg_medium': '#1f1d2e', 'bg_light': '#26233a', 'bg_hover': '#403d52', 'fg': '#e0def4', 'accent': '#ebbcba', 'border': '#403d52'}, 'Catppuccin': {'bg_dark': '#1e1e2e', 'bg_medium': '#313244', 'bg_light': '#45475a', 'bg_hover': '#585b70', 'fg': '#cdd6f4', 'accent': '#cba6f7', 'border': '#45475a'}, 'Gruvbox': {'bg_dark': '#282828', 'bg_medium': '#3c3836', 'bg_light': '#504945', 'bg_hover': '#665c54', 'fg': '#ebdbb2', 'accent': '#fabd2f', 'border': '#504945'}, 'Tokyo Night': {'bg_dark': '#16161e', 'bg_medium': '#1f2335', 'bg_light': '#292e42', 'bg_hover': '#3b4261', 'fg': '#c0caf5', 'accent': '#7aa2f7', 'border': '#3b4261'}, 'Synthwave': {'bg_dark': '#241b2f', 'bg_medium': '#30233d', 'bg_light': '#45304f', 'bg_hover': '#5a3e64', 'fg': '#f5d7fe', 'accent': '#ff7edb', 'border': '#5a3e64'}, 'Forest': {'bg_dark': '#102018', 'bg_medium': '#183025', 'bg_light': '#254638', 'bg_hover': '#315a48', 'fg': '#d8f3dc', 'accent': '#74c69d', 'border': '#315a48'}, 'Ruby': {'bg_dark': '#241417', 'bg_medium': '#351b20', 'bg_light': '#4a252d', 'bg_hover': '#63323d', 'fg': '#f7dfe3', 'accent': '#ff6b81', 'border': '#63323d'}, 'Amber': {'bg_dark': '#211a0e', 'bg_medium': '#33270f', 'bg_light': '#4a3815', 'bg_hover': '#61491d', 'fg': '#fff0c2', 'accent': '#ffb84d', 'border': '#61491d'}, 'Arctic': {'bg_dark': '#17212b', 'bg_medium': '#21303d', 'bg_light': '#304554', 'bg_hover': '#405b6d', 'fg': '#e7f5ff', 'accent': '#66c7ff', 'border': '#405b6d'}, 'Lavender': {'bg_dark': '#211d2b', 'bg_medium': '#2d263b', 'bg_light': '#3c3350', 'bg_hover': '#514466', 'fg': '#eee7ff', 'accent': '#c4a7ff', 'border': '#514466'}, 'Coffee': {'bg_dark': '#211915', 'bg_medium': '#30231d', 'bg_light': '#45332a', 'bg_hover': '#5b4437', 'fg': '#f1dfd0', 'accent': '#d69e78', 'border': '#5b4437'}, 'Slate': {'bg_dark': '#181c20', 'bg_medium': '#232a30', 'bg_light': '#313a42', 'bg_hover': '#414c56', 'fg': '#d9e1e8', 'accent': '#8ab4c7', 'border': '#414c56'}, 'Cyber': {'bg_dark': '#080b12', 'bg_medium': '#101522', 'bg_light': '#182033', 'bg_hover': '#26334d', 'fg': '#d9f7ff', 'accent': '#00e5ff', 'border': '#26334d'}, 'Sunset': {'bg_dark': '#241516', 'bg_medium': '#35201e', 'bg_light': '#4a2b27', 'bg_hover': '#633b35', 'fg': '#ffe4d6', 'accent': '#ff8a65', 'border': '#633b35'}, 'Mint': {'bg_dark': '#10211e', 'bg_medium': '#17312c', 'bg_light': '#24473f', 'bg_hover': '#315d52', 'fg': '#dcfff5', 'accent': '#62e6c8', 'border': '#315d52'}, 'Deep Blue': {'bg_dark': '#0b1424', 'bg_medium': '#10213a', 'bg_light': '#193153', 'bg_hover': '#24446f', 'fg': '#dcecff', 'accent': '#5ca9ff', 'border': '#24446f'}, 'Obsidian': {'bg_dark': '#111318', 'bg_medium': '#1a1d24', 'bg_light': '#292e38', 'bg_hover': '#363d49', 'fg': '#e6e9ef', 'accent': '#8ab4f8', 'border': '#3b4351'}, 'Aurora': {'bg_dark': '#101820', 'bg_medium': '#172633', 'bg_light': '#234353', 'bg_hover': '#2d5c6d', 'fg': '#e4fbff', 'accent': '#66e3d4', 'border': '#376878'}, 'Plasma': {'bg_dark': '#160d24', 'bg_medium': '#24143b', 'bg_light': '#38215b', 'bg_hover': '#4d2b79', 'fg': '#f4eaff', 'accent': '#e38cff', 'border': '#5d3d83'}, 'Ember': {'bg_dark': '#20110d', 'bg_medium': '#321a14', 'bg_light': '#4a2820', 'bg_hover': '#63362a', 'fg': '#ffede5', 'accent': '#ff9d5c', 'border': '#714334'}, 'Meadow': {'bg_dark': '#0d1b16', 'bg_medium': '#142a20', 'bg_light': '#204433', 'bg_hover': '#2c5c43', 'fg': '#e4ffef', 'accent': '#8be28b', 'border': '#38694e'}})
THEME_NAMES = list(THEMES.keys())
DEFAULT_THEME = 'Midnight'
_CURRENT_PALETTE = dict(THEMES[DEFAULT_THEME])
STARTUP_GEOMETRY = '1400x800'
PANED_TOP_FRACTION = 0.45
HPANED_LEFT_FRACTION = 0.55
VIEWER_MIN_WIDTH = 480
REPLACER_MIN_WIDTH = 320
WATCH_INTERVAL_SEC = 0.5
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_LOCAL_APPDATA = os.environ.get('LOCALAPPDATA') or os.path.expanduser('~')
DATA_DIR = os.path.join(_LOCAL_APPDATA, 'RoUtils')
os.makedirs(DATA_DIR, exist_ok=True)
APP_VERSION = '4.2'
HISTORY_PATH = os.path.join(DATA_DIR, 'history.json')
SETTINGS_PATH = os.path.join(DATA_DIR, 'routils_settings.json')
ERROR_REPORT_DIR = os.path.join(DATA_DIR, 'errors')
_ACTIVE_APP = None
_ERROR_REPORTING = False

def _report_rotools_error(exc_type, exc_value, exc_tb, app=None):
    global _ERROR_REPORTING
    if _ERROR_REPORTING:
        return
    _ERROR_REPORTING = True
    try:
        detail = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        os.makedirs(ERROR_REPORT_DIR, exist_ok=True)
        stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = os.path.join(ERROR_REPORT_DIR, f'error_{stamp}.txt')
        with open(path, 'w', encoding='utf-8') as f:
            f.write('RoUtils Error Report\n')
            f.write(f'Version: {APP_VERSION}\n')
            f.write(f'Time: {datetime.now().isoformat()}\n\n')
            f.write(detail)
        short = str(exc_value).strip().splitlines()[0] if str(exc_value).strip() else exc_type.__name__
        target = app or _ACTIVE_APP
        if target is not None:
            try:
                target._console_log(f'RoUtils encountered an error: {short} (details: {path})')
            except Exception:
                pass
        message = f'RoUtils encountered an error.\n\nError: {short}\n\nDetailed report saved to:\n{path}\n\nCheck Console for more details.'
        try:
            if target is not None and target.winfo_exists():
                target.after(0, lambda: messagebox.showerror('RoUtils Error', message, parent=target))
            else:
                messagebox.showerror('RoUtils Error', message)
        except Exception:
            pass
    finally:
        _ERROR_REPORTING = False

def _install_error_hooks():

    def hook(exc_type, exc_value, exc_tb):
        _report_rotools_error(exc_type, exc_value, exc_tb)
    sys.excepthook = hook
    if hasattr(threading, 'excepthook'):
        threading.excepthook = lambda args: _report_rotools_error(args.exc_type, args.exc_value, args.exc_traceback)
CONSOLE_HISTORY_PATH = os.path.join(DATA_DIR, 'console_history.json')
TEMP_EMU_DIR = os.path.join(tempfile.gettempdir(), 'RobloxStudio_TempView')
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
PROPERTY_FORMAT_TO_XML_TAG: dict[PropertyFormat, str] = {PropertyFormat.STRING: 'string', PropertyFormat.BOOL: 'bool', PropertyFormat.INT: 'int', PropertyFormat.FLOAT: 'float', PropertyFormat.DOUBLE: 'double', PropertyFormat.UDIM: 'UDim', PropertyFormat.UDIM2: 'UDim2', PropertyFormat.RAY: 'Ray', PropertyFormat.FACES: 'Faces', PropertyFormat.AXES: 'Axes', PropertyFormat.BRICK_COLOR: 'BrickColor', PropertyFormat.COLOR3: 'Color3', PropertyFormat.VECTOR2: 'Vector2', PropertyFormat.VECTOR3: 'Vector3', PropertyFormat.VECTOR2INT16: 'Vector2int16', PropertyFormat.CFRAME_MATRIX: 'CoordinateFrame', PropertyFormat.CFRAME_QUAT: 'CoordinateFrame', PropertyFormat.ENUM: 'token', PropertyFormat.REF: 'Ref', PropertyFormat.VECTOR3INT16: 'Vector3int16', PropertyFormat.NUMBER_SEQUENCE: 'NumberSequence', PropertyFormat.COLOR_SEQUENCE: 'ColorSequence', PropertyFormat.NUMBER_RANGE: 'NumberRange', PropertyFormat.RECT2D: 'Rect2D', PropertyFormat.PHYSICAL_PROPERTIES: 'PhysicalProperties', PropertyFormat.COLOR3UINT8: 'Color3uint8', PropertyFormat.INT64: 'int64', PropertyFormat.SHARED_STRING: 'SharedString', PropertyFormat.BYTECODE: 'BinaryString', PropertyFormat.OPTIONAL_CFRAME: 'OptionalCoordinateFrame', PropertyFormat.UNIQUE_ID: 'UniqueId', PropertyFormat.FONT: 'Font', PropertyFormat.SECURITY_CAPABILITIES: 'SecurityCapabilities', PropertyFormat.CONTENT: 'Content'}

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
    raw_property_chunks: list[RbxRawPropertyChunk] = field(default_factory=list[RbxRawPropertyChunk])
    raw_chunks: list[RbxRawChunk] = field(default_factory=list[RbxRawChunk])
import struct
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass

def read_u8(data: bytes, offset: int) -> tuple[int, int]:
    return (data[offset], offset + 1)

def read_u32(data: bytes, offset: int) -> tuple[int, int]:
    val = struct.unpack_from('<I', data, offset)[0]
    return (val, offset + 4)

def read_f32(data: bytes, offset: int) -> tuple[float, int]:
    val = struct.unpack_from('<f', data, offset)[0]
    return (val, offset + 4)

def read_f64(data: bytes, offset: int) -> tuple[float, int]:
    val = struct.unpack_from('<d', data, offset)[0]
    return (val, offset + 8)

def read_bytes(data: bytes, offset: int, length: int) -> tuple[bytes, int]:
    return (data[offset:offset + length], offset + length)

def read_string(data: bytes, offset: int) -> tuple[str, int]:
    length, offset = read_u32(data, offset)
    raw, offset = read_bytes(data, offset, length)
    return (raw.decode('utf-8', errors='replace'), offset)

def read_binary_string(data: bytes, offset: int) -> tuple[bytes, int]:
    length, offset = read_u32(data, offset)
    raw, offset = read_bytes(data, offset, length)
    return (raw, offset)

def decode_zigzag(value: int) -> int:
    return value >> 1 ^ -(value & 1)

def deinterleave_u32(data: bytes, offset: int, count: int) -> list[int]:
    values: list[int] = []
    total = count * 4
    block = data[offset:offset + total]
    for i in range(count):
        b0 = block[i]
        b1 = block[count + i]
        b2 = block[2 * count + i]
        b3 = block[3 * count + i]
        values.append(b0 << 24 | b1 << 16 | b2 << 8 | b3)
    return values

def deinterleave_i32(data: bytes, offset: int, count: int) -> list[int]:
    raw = deinterleave_u32(data, offset, count)
    return [decode_zigzag(v) for v in raw]

def deinterleave_f32(data: bytes, offset: int, count: int) -> list[float]:
    raw = deinterleave_u32(data, offset, count)
    result: list[float] = []
    for v in raw:
        bits = v >> 1 | (v & 1) << 31
        result.append(struct.unpack('<f', struct.pack('<I', bits))[0])
    return result

def deinterleave_i64(data: bytes, offset: int, count: int) -> list[int]:
    values: list[int] = []
    total = count * 8
    block = data[offset:offset + total]
    for i in range(count):
        val = 0
        for byte_idx in range(8):
            val = val << 8 | block[byte_idx * count + i]
        values.append(val >> 1 ^ -(val & 1))
    return values

def deinterleave_u64(data: bytes, offset: int, count: int) -> list[int]:
    values: list[int] = []
    total = count * 8
    block = data[offset:offset + total]
    for i in range(count):
        val = 0
        for byte_idx in range(8):
            val = val << 8 | block[byte_idx * count + i]
        values.append(val)
    return values

def deinterleave_bytes(data: bytes, offset: int, count: int, width: int) -> list[bytes]:
    block = data[offset:offset + count * width]
    return [bytes((block[byte_idx * count + i] for byte_idx in range(width))) for i in range(count)]

def decode_ids(data: bytes, offset: int, count: int) -> tuple[list[int], int]:
    deltas = deinterleave_i32(data, offset, count)
    ids: list[int] = []
    acc = 0
    for d in deltas:
        acc += d
        ids.append(acc)
    return (ids, offset + count * 4)
import struct

def write_u8(value: int) -> bytes:
    return bytes([value & 255])

def write_u16(value: int) -> bytes:
    return struct.pack('<H', value)

def write_u32(value: int) -> bytes:
    return struct.pack('<I', value)

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
    return (value << 1 ^ value >> 31) & 4294967295

def encode_zigzag64(value: int) -> int:
    return (value << 1 ^ value >> 63) & 18446744073709551615

def interleave_u32(values: list[int]) -> bytes:
    count = len(values)
    out = bytearray(count * 4)
    for i, v in enumerate(values):
        out[i] = v >> 24 & 255
        out[count + i] = v >> 16 & 255
        out[2 * count + i] = v >> 8 & 255
        out[3 * count + i] = v & 255
    return bytes(out)

def interleave_i32(values: list[int]) -> bytes:
    return interleave_u32([encode_zigzag32(v) for v in values])

def interleave_f32(values: list[float]) -> bytes:
    raw_ints: list[int] = []
    for v in values:
        bits = struct.unpack('<I', struct.pack('<f', v))[0]
        rotated = ((bits & 2147483647) << 1 | bits >> 31) & 4294967295
        raw_ints.append(rotated)
    return interleave_u32(raw_ints)

def interleave_i64(values: list[int]) -> bytes:
    count = len(values)
    out = bytearray(count * 8)
    for i, v in enumerate(values):
        zz = encode_zigzag64(v)
        for byte_idx in range(8):
            out[byte_idx * count + i] = zz >> 56 - byte_idx * 8 & 255
    return bytes(out)

def interleave_u64(values: list[int]) -> bytes:
    count = len(values)
    out = bytearray(count * 8)
    for i, v in enumerate(values):
        v &= 18446744073709551615
        for byte_idx in range(8):
            out[byte_idx * count + i] = v >> 56 - byte_idx * 8 & 255
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
MAGIC_HEADER = b'<roblox!\x89\xff\r\n\x1a\n'
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
        header = MAGIC_HEADER + struct.pack('<H', FILE_VERSION) + struct.pack('<I', type_count) + struct.pack('<I', object_count) + b'\x00' * 8
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
        is_service = any((inst.is_service for inst in instances))
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

    def _build_prop(self, type_idx: int, prop_name: str, instances: list[RbxInstance]) -> bytes | None:
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
                return {'origin': {'X': 0.0, 'Y': 0.0, 'Z': 0.0}, 'direction': {'X': 0.0, 'Y': 0.0, 'Z': 0.0}}
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
                return {'X': 0.0, 'Y': 0.0, 'Z': 0.0, 'R00': 1.0, 'R01': 0.0, 'R02': 0.0, 'R10': 0.0, 'R11': 1.0, 'R12': 0.0, 'R20': 0.0, 'R21': 0.0, 'R22': 1.0}
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
                return b''.join((write_f64(float(v)) for v in values))
            case PropertyFormat.UDIM:
                return interleave_f32([float(v['S']) for v in values]) + interleave_i32([int(v['O']) for v in values])
            case PropertyFormat.UDIM2:
                return interleave_f32([float(v['XS']) for v in values]) + interleave_f32([float(v['YS']) for v in values]) + interleave_i32([int(v['XO']) for v in values]) + interleave_i32([int(v['YO']) for v in values])
            case PropertyFormat.RAY:
                buf = bytearray()
                for v in values:
                    o, d = (v['origin'], v['direction'])
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
                return interleave_f32([float(v['R']) for v in values]) + interleave_f32([float(v['G']) for v in values]) + interleave_f32([float(v['B']) for v in values])
            case PropertyFormat.VECTOR2:
                return interleave_f32([float(v['X']) for v in values]) + interleave_f32([float(v['Y']) for v in values])
            case PropertyFormat.VECTOR3:
                return interleave_f32([float(v['X']) for v in values]) + interleave_f32([float(v['Y']) for v in values]) + interleave_f32([float(v['Z']) for v in values])
            case PropertyFormat.VECTOR2INT16:
                return b''.join((struct.pack('<hh', int(v['X']), int(v['Y'])) for v in values))
            case PropertyFormat.VECTOR3INT16:
                return b''.join((struct.pack('<hhh', int(v['X']), int(v['Y']), int(v['Z'])) for v in values))
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
                return interleave_f32([float(v['min']['X']) for v in values]) + interleave_f32([float(v['min']['Y']) for v in values]) + interleave_f32([float(v['max']['X']) for v in values]) + interleave_f32([float(v['max']['Y']) for v in values])
            case PropertyFormat.PHYSICAL_PROPERTIES:
                return self._enc_physical_properties(values)
            case PropertyFormat.COLOR3UINT8:
                return bytes([int(v['R']) for v in values]) + bytes([int(v['G']) for v in values]) + bytes([int(v['B']) for v in values])
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
        xs, ys, zs = ([], [], [])
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
        ids = [-1 if v is None else int(v) for v in values]
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
        return write_u8(int(PropertyFormat.CFRAME_MATRIX)) + RbxmSerializer._enc_cframes(cframes) + write_u8(int(PropertyFormat.BOOL)) + bytes([1 if value else 0 for value in present])

    @staticmethod
    def _enc_unique_ids(values: list[Any]) -> bytes:
        records: list[bytes] = []
        for value in values:
            if isinstance(value, bytes):
                records.append(value)
                continue
            records.append(struct.pack('>IIQ', int(value.get('Index', 0)) & 4294967295, int(value.get('Time', 0)) & 4294967295, int(value.get('Random', 0)) & 18446744073709551615))
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
    root.set('xsi:noNamespaceSchemaLocation', 'http://www.roblox.com/roblox.xsd')
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

def _write_instance(parent_el: Element, inst: RbxInstance, doc: RbxDocument) -> None:
    item = SubElement(parent_el, 'Item')
    item.set('class', inst.class_name)
    item.set('referent', f'RBX{inst.referent:032X}')
    props_el = SubElement(item, 'Properties')
    for prop in sorted(inst.properties.values(), key=lambda p: p.name):
        _write_property(props_el, prop, doc)
    for child in inst.children:
        _write_instance(item, child, doc)

def _write_property(props_el: Element, prop: RbxProperty, doc: RbxDocument) -> None:
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
        if codepoint < 32 and ch not in '\t\n\r':
            return True
        if 55296 <= codepoint <= 57343:
            return True
        if codepoint in (65534, 65535):
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
    content_props = {'AssetId', 'MeshId', 'TextureId', 'SoundId', 'Texture', 'LinkedSource', 'Image', 'Animation'}
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
        if mask & 1 << i:
            faces.append(name)
    el.text = ', '.join(faces) if faces else ''

def _write_axes(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'Axes')
    el.set('name', prop.name)
    mask = prop.value
    axes: list[str] = []
    axis_names = ['X', 'Y', 'Z']
    for i, name in enumerate(axis_names):
        if mask & 1 << i:
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
    parts: list[str] = [f"{_fmt_float(key['Time'])} {_fmt_float(key['Value'])} {_fmt_float(key['Envelope'])}" for key in prop.value]
    el.text = ' '.join(parts)

def _write_color_sequence(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'ColorSequence')
    el.set('name', prop.name)
    parts: list[str] = [f"{_fmt_float(key['Time'])} {_fmt_float(key['R'])} {_fmt_float(key['G'])} {_fmt_float(key['B'])} 0" for key in prop.value]
    el.text = ' '.join(parts)

def _write_number_range(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'NumberRange')
    el.set('name', prop.name)
    el.text = f"{_fmt_float(prop.value['Min'])} {_fmt_float(prop.value['Max'])}"

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
        SubElement(el, 'AcousticAbsorption').text = _fmt_float(prop.value.get('AcousticAbsorption', 1.0))

def _write_color3uint8(parent: Element, prop: RbxProperty) -> None:
    el = SubElement(parent, 'Color3uint8')
    el.set('name', prop.name)
    r = prop.value['R']
    g = prop.value['G']
    b = prop.value['B']
    packed = 4278190080 | r << 16 | g << 8 | b
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
    random_bits = int(prop.value.get('Random', 0)) & 18446744073709551615
    xml_random = random_bits << 1 & 18446744073709551615 | random_bits >> 63
    time = int(prop.value.get('Time', 0)) & 4294967295
    index = int(prop.value.get('Index', 0)) & 4294967295
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
        if value.is_integer() and abs(value) < 1000000000000000.0:
            return str(int(value))
        return f'{value:.8g}'
    return str(value)
import logging
import struct
from typing import Any
import lz4.block
log = logging.getLogger(__name__)
MAGIC_HEADER = b'<roblox!\x89\xff\r\n\x1a\n'
FILE_HEADER_SIZE = 32
ZSTD_MAGIC = b'(\xb5/\xfd'

def _decompress_chunk(raw: bytes, uncompressed_size: int) -> bytes:
    if raw.startswith(ZSTD_MAGIC):
        try:
            import zstandard
        except ImportError as exc:
            msg = 'RBXM contains a ZSTD-compressed chunk; install zstandard to read it'
            raise RuntimeError(msg) from exc
        return zstandard.ZstdDecompressor().decompress(raw, max_output_size=uncompressed_size)
    return lz4.block.decompress(raw, uncompressed_size=uncompressed_size)
_ORIENTATION_MATRICES: dict[int, tuple[float, ...]] = {0: (1, 0, 0, 0, 1, 0, 0, 0, 1), 1: (1, 0, 0, 0, 0, -1, 0, 1, 0), 2: (1, 0, 0, 0, -1, 0, 0, 0, -1), 3: (1, 0, 0, 0, 0, 1, 0, -1, 0), 4: (0, 1, 0, 1, 0, 0, 0, 0, -1), 5: (0, 0, 1, 1, 0, 0, 0, 1, 0), 6: (0, -1, 0, 1, 0, 0, 0, 0, 1), 7: (0, 0, -1, 1, 0, 0, 0, -1, 0), 8: (0, 1, 0, 0, 0, 1, 1, 0, 0), 9: (0, 0, -1, 0, 1, 0, 1, 0, 0), 10: (0, -1, 0, 0, 0, -1, 1, 0, 0), 11: (0, 0, 1, 0, -1, 0, 1, 0, 0), 12: (-1, 0, 0, 0, 1, 0, 0, 0, -1), 13: (-1, 0, 0, 0, 0, 1, 0, 1, 0), 14: (-1, 0, 0, 0, -1, 0, 0, 0, 1), 15: (-1, 0, 0, 0, 0, -1, 0, -1, 0), 16: (0, 1, 0, -1, 0, 0, 0, 0, 1), 17: (0, 0, -1, -1, 0, 0, 0, 1, 0), 18: (0, -1, 0, -1, 0, 0, 0, 0, -1), 19: (0, 0, 1, -1, 0, 0, 0, -1, 0), 20: (0, 1, 0, 0, 0, -1, -1, 0, 0), 21: (0, 0, 1, 0, 1, 0, -1, 0, 0), 22: (0, -1, 0, 0, 0, 1, -1, 0, 0), 23: (0, 0, -1, 0, -1, 0, -1, 0, 0)}

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
        return RbxDocument(version=self._version, type_count=self._type_count, object_count=self._object_count, metadata=self._metadata, instances=self._instances, roots=roots, shared_strings=self._shared_strings, raw_property_chunks=self._raw_property_chunks, raw_chunks=self._raw_chunks)

    def _read_file_header(self, data: bytes) -> int:
        magic = data[:14]
        if magic != MAGIC_HEADER:
            msg = f'Invalid RBXM header: {magic!r}'
            raise ValueError(msg)
        self._version = struct.unpack_from('<H', data, 14)[0]
        self._type_count = struct.unpack_from('<I', data, 16)[0]
        self._object_count = struct.unpack_from('<I', data, 20)[0]
        log.info('RBXM v%d: %d types, %d objects', self._version, self._type_count, self._object_count)
        return FILE_HEADER_SIZE

    def _read_chunks(self, data: bytes, offset: int) -> int:
        while offset < len(data):
            chunk_name = data[offset:offset + 4].decode('ascii')
            compressed_size = struct.unpack_from('<I', data, offset + 4)[0]
            uncompressed_size = struct.unpack_from('<I', data, offset + 8)[0]
            offset += 16
            chunk_data: bytes
            if compressed_size == 0:
                chunk_data = data[offset:offset + uncompressed_size]
                offset += uncompressed_size
            else:
                raw = data[offset:offset + compressed_size]
                chunk_data = _decompress_chunk(raw, uncompressed_size)
                offset += compressed_size
            self._process_chunk(chunk_name, chunk_data)
            if chunk_name == 'END\x00':
                break
        return offset

    def _process_chunk(self, name: str, data: bytes) -> None:
        handler = {'META': self._handle_meta, 'SSTR': self._handle_sstr, 'INST': self._handle_inst, 'PROP': self._handle_prop, 'PRNT': self._handle_prnt}.get(name)
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
        info = RbxTypeInfo(type_index=type_index, class_name=class_name, is_service=is_service, instance_ids=ids)
        while len(self._type_infos) <= type_index:
            self._type_infos.append(RbxTypeInfo(type_index=len(self._type_infos), class_name='', is_service=False, instance_ids=[]))
        self._type_infos[type_index] = info
        for i, inst_id in enumerate(ids):
            inst = RbxInstance(class_name=class_name, referent=inst_id, is_service=is_service and i < len(service_flags) and service_flags[i])
            self._instances[inst_id] = inst
        log.debug('INST[%d]: %s x%d (service=%s)', type_index, class_name, id_count, is_service)

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
                self._instances[inst_id].properties[prop_name] = RbxProperty(name=prop_name, fmt=fmt, value=values[i])
        log.debug('PROP[%d].%s: fmt=%s, %d values', type_index, prop_name, fmt.name, len(values))

    def _preserve_raw_property(self, type_index: int, prop_name: str, fmt_byte: int, value_data: bytes) -> None:
        if type_index >= len(self._type_infos):
            log.warning('PROP references unknown type index %d', type_index)
            return
        info = self._type_infos[type_index]
        self._raw_property_chunks.append(RbxRawPropertyChunk(class_name=info.class_name, prop_name=prop_name, fmt_byte=fmt_byte, value_data=value_data, instance_count=len(info.instance_ids)))
        log.warning('Unknown property format %d for %s, preserving raw payload', fmt_byte, prop_name)

    def _read_property_values(self, fmt: PropertyFormat, data: bytes, offset: int, count: int) -> list[Any]:
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
            results.append({'origin': {'X': ox, 'Y': oy, 'Z': oz}, 'direction': {'X': dx, 'Y': dy, 'Z': dz}})
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

    def _read_cframes(self, data: bytes, offset: int, count: int, fmt: PropertyFormat) -> list[dict[str, float]]:
        results, _offset = self._read_cframes_with_offset(data, offset, count, fmt)
        return results

    def _read_cframes_with_offset(self, data: bytes, offset: int, count: int, fmt: PropertyFormat) -> tuple[list[dict[str, float]], int]:
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
            results.append({'X': xs[i], 'Y': ys[i], 'Z': zs[i], 'R00': r[0], 'R01': r[1], 'R02': r[2], 'R10': r[3], 'R11': r[4], 'R12': r[5], 'R20': r[6], 'R21': r[7], 'R22': r[8]})
        return (results, offset)

    def _read_enums(self, data: bytes, offset: int, count: int) -> list[int]:
        return deinterleave_u32(data, offset, count)

    def _read_refs(self, data: bytes, offset: int, count: int) -> list[int | None]:
        ids, _ = decode_ids(data, offset, count)
        return [None if v == -1 else v for v in ids]

    def _read_number_sequences(self, data: bytes, offset: int, count: int) -> list[list[dict[str, float]]]:
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

    def _read_color_sequences(self, data: bytes, offset: int, count: int) -> list[list[dict[str, float]]]:
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

    def _read_rect2ds(self, data: bytes, offset: int, count: int) -> list[dict[str, dict[str, float]]]:
        x0s = deinterleave_f32(data, offset, count)
        y0s = deinterleave_f32(data, offset + count * 4, count)
        x1s = deinterleave_f32(data, offset + count * 8, count)
        y1s = deinterleave_f32(data, offset + count * 12, count)
        return [{'min': {'X': x0s[i], 'Y': y0s[i]}, 'max': {'X': x1s[i], 'Y': y1s[i]}} for i in range(count)]

    def _read_physical_properties(self, data: bytes, offset: int, count: int) -> list[dict[str, Any] | None]:
        results: list[dict[str, Any] | None] = []
        for _ in range(count):
            flags, offset = read_u8(data, offset)
            custom = flags & 1 != 0
            has_acoustic_absorption = flags & 2 != 0
            if custom:
                density, offset = read_f32(data, offset)
                friction, offset = read_f32(data, offset)
                elasticity, offset = read_f32(data, offset)
                friction_weight, offset = read_f32(data, offset)
                elasticity_weight, offset = read_f32(data, offset)
                value: dict[str, Any] = {'CustomPhysics': True, 'Density': density, 'Friction': friction, 'Elasticity': elasticity, 'FrictionWeight': friction_weight, 'ElasticityWeight': elasticity_weight}
                if has_acoustic_absorption:
                    acoustic_absorption, offset = read_f32(data, offset)
                    value['AcousticAbsorption'] = acoustic_absorption
                results.append(value)
            elif has_acoustic_absorption:
                results.append({'CustomPhysics': False, 'HasAcousticAbsorption': True})
            else:
                results.append(None)
        return results

    def _read_color3uint8s(self, data: bytes, offset: int, count: int) -> list[dict[str, int]]:
        rs = data[offset:offset + count]
        gs = data[offset + count:offset + 2 * count]
        bs = data[offset + 2 * count:offset + 3 * count]
        return [{'R': rs[i], 'G': gs[i], 'B': bs[i]} for i in range(count)]

    def _read_int64s(self, data: bytes, offset: int, count: int) -> list[int]:
        return deinterleave_i64(data, offset, count)

    def _read_shared_strings(self, data: bytes, offset: int, count: int) -> list[bytes]:
        indices = deinterleave_u32(data, offset, count)
        return [self._shared_strings[idx] if idx < len(self._shared_strings) else b'' for idx in indices]

    def _read_bytecodes(self, data: bytes, offset: int, count: int) -> list[bytes]:
        results: list[bytes] = []
        for _ in range(count):
            raw, offset = read_binary_string(data, offset)
            results.append(raw)
        return results

    def _read_optional_cframes(self, data: bytes, offset: int, count: int) -> list[dict[str, float] | None]:
        cframe_fmt_byte, offset = read_u8(data, offset)
        if cframe_fmt_byte != int(PropertyFormat.CFRAME_MATRIX):
            log.warning('OptionalCoordinateFrame contained unexpected value format %d', cframe_fmt_byte)
        cframes, offset = self._read_cframes_with_offset(data, offset, count, PropertyFormat.CFRAME_MATRIX)
        bool_fmt_byte, offset = read_u8(data, offset)
        if bool_fmt_byte != int(PropertyFormat.BOOL):
            log.warning('OptionalCoordinateFrame contained unexpected presence format %d', bool_fmt_byte)
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
            results.append({'Family': family_raw.decode('utf-8', errors='replace'), 'Weight': weight, 'Style': style, 'CachedFaceId': cached_face_raw.decode('utf-8', errors='replace')})
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
                    ref = external_object_refs[external_object_index] if external_object_index < len(external_object_refs) else None
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
    xx, yy, zz = (x * x, y * y, z * z)
    xy, xz, yz = (x * y, x * z, y * z)
    wx, wy, wz = (w * x, w * y, w * z)
    return (1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy), 2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx), 2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy))
import struct
import zlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import lz4.block
RBXM_MAGIC = b'<roblox!'
RBXM_SIGNATURE = bytes([137, 255, 13, 10, 26, 10])

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
        value = b0 << 24 | b1 << 16 | b2 << 8 | b3
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
        raw = b0 << 24 | b1 << 16 | b2 << 8 | b3
        ieee = (raw >> 1 | (raw & 1) << 31) & 4294967295
        result.append(struct.unpack('<f', struct.pack('<I', ieee))[0])
    return result

def read_string(data: bytes, offset: int) -> Tuple[str, int]:
    length = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    value = data[offset:offset + length].decode('utf-8', errors='replace')
    return (value, offset + length)

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
CFRAME_ROTATIONS = {2: [1, 0, 0, 0, 1, 0, 0, 0, 1], 3: [1, 0, 0, 0, 0, -1, 0, 1, 0], 4: [1, 0, 0, 0, -1, 0, 0, 0, -1], 5: [1, 0, 0, 0, 0, 1, 0, -1, 0], 6: [0, 1, 0, 1, 0, 0, 0, 0, -1], 7: [0, 0, 1, 1, 0, 0, 0, 1, 0], 8: [0, -1, 0, 1, 0, 0, 0, 0, 1], 9: [0, 0, -1, 1, 0, 0, 0, -1, 0], 10: [0, 1, 0, 0, 0, 1, 1, 0, 0], 11: [0, 0, -1, 0, 1, 0, 1, 0, 0], 12: [0, -1, 0, 0, 0, -1, 1, 0, 0], 13: [0, 0, 1, 0, -1, 0, 1, 0, 0], 14: [-1, 0, 0, 0, 1, 0, 0, 0, -1], 15: [-1, 0, 0, 0, 0, 1, 0, 1, 0], 16: [-1, 0, 0, 0, -1, 0, 0, 0, 1], 17: [-1, 0, 0, 0, 0, -1, 0, -1, 0], 18: [0, 1, 0, -1, 0, 0, 0, 0, 1], 19: [0, 0, -1, -1, 0, 0, 0, 1, 0], 20: [0, -1, 0, -1, 0, 0, 0, 0, -1], 21: [0, 0, 1, -1, 0, 0, 0, -1, 0], 22: [0, 1, 0, 0, 0, -1, -1, 0, 0], 23: [0, 0, 1, 0, 1, 0, -1, 0, 0], 24: [0, -1, 0, 0, 0, 1, -1, 0, 0], 25: [0, 0, -1, 0, -1, 0, -1, 0, 0]}

def parse_rbxm(data: bytes) -> Dict[int, RbxmInstance]:
    if len(data) < 32:
        raise ValueError('File too small to be valid RBXM')
    if not data.startswith(RBXM_MAGIC):
        raise ValueError('Invalid RBXM magic header')
    offset = 8
    signature = data[offset:offset + 6]
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
        chunk_name = data[offset:offset + 4].decode('ascii', errors='replace').rstrip('\x00')
        offset += 4
        compressed_size = struct.unpack_from('<I', data, offset)[0]
        offset += 4
        uncompressed_size = struct.unpack_from('<I', data, offset)[0]
        offset += 4
        reserved = struct.unpack_from('<I', data, offset)[0]
        offset += 4
        if compressed_size == 0:
            chunk_data = data[offset:offset + uncompressed_size]
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
    referents_data = data[offset:offset + instance_count * 4]
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
    if type_id == 1:
        offset = 0
        for _ in range(count):
            if offset >= len(data):
                values.append('')
                continue
            string_value, offset = read_string(data, offset)
            values.append(string_value)
    elif type_id == 2:
        for i in range(count):
            if i < len(data):
                values.append(bool(data[i]))
            else:
                values.append(False)
    elif type_id == 3:
        values = decode_interleaved_i32(data, count)
    elif type_id == 4:
        values = decode_interleaved_f32(data, count)
    elif type_id == 5:
        for i in range(count):
            offset = i * 8
            if offset + 8 <= len(data):
                values.append(struct.unpack_from('<d', data, offset)[0])
            else:
                values.append(0.0)
    elif type_id == 16:
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
            rotation_data.append((2, CFRAME_ROTATIONS[2]))
            continue
        rot_id = data[offset]
        offset += 1
        if rot_id == 0:
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
        rot_id, rot = rotation_data[i] if i < len(rotation_data) else (2, CFRAME_ROTATIONS[2])
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
        self.a, self.b, self.c = (a, b, c)

def fix_float(s: str) -> str:
    return s.replace(',', '.')

def read_vertices(data: bytes, offset: int, count: int, vsize: int) -> tuple[list[Vertex], int]:
    verts = []
    pos = offset
    for _ in range(count):
        v = Vertex()
        v.px, = struct.unpack_from('<f', data, pos)
        pos += 4
        v.py, = struct.unpack_from('<f', data, pos)
        pos += 4
        v.pz, = struct.unpack_from('<f', data, pos)
        pos += 4
        v.nx, = struct.unpack_from('<f', data, pos)
        pos += 4
        v.ny, = struct.unpack_from('<f', data, pos)
        pos += 4
        v.nz, = struct.unpack_from('<f', data, pos)
        pos += 4
        v.tu, = struct.unpack_from('<f', data, pos)
        pos += 4
        tv, = struct.unpack_from('<f', data, pos)
        pos += 4
        v.tv = 1.0 - tv
        v.tx, = struct.unpack_from('<b', data, pos)
        pos += 1
        v.ty, = struct.unpack_from('<b', data, pos)
        pos += 1
        v.tz, = struct.unpack_from('<b', data, pos)
        pos += 1
        v.ts, = struct.unpack_from('<b', data, pos)
        pos += 1
        if vsize == 40:
            v.r, = struct.unpack_from('<B', data, pos)
            pos += 1
            v.g, = struct.unpack_from('<B', data, pos)
            pos += 1
            v.b, = struct.unpack_from('<B', data, pos)
            pos += 1
            v.a, = struct.unpack_from('<B', data, pos)
            pos += 1
        verts.append(v)
    return (verts, pos)

def write_obj_data(v_lines: list[str], n_lines: list[str], t_lines: list[str], f_lines: list[str]) -> str:
    lines = ['# Converted from Roblox mesh format\n']
    lines.append(f'# Vertices: {len(v_lines)}, Faces: {len(f_lines)}\n\n')
    lines.extend((line + '\n' for line in v_lines))
    lines.append('\n')
    lines.extend((line + '\n' for line in n_lines))
    lines.append('\n')
    lines.extend((line + '\n' for line in t_lines))
    lines.append('\n')
    lines.extend((line + '\n' for line in f_lines))
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
            uvs.append(f'vt {fix_float(str(uv[0]))} {fix_float(str(1 - uv[1]))} {fix_float(str(uv[2]))}')
        for i in range(0, groups, 3):
            idx = i + 1
            faces.append(f'f {idx}/{idx}/{idx} {idx + 1}/{idx + 1}/{idx + 1} {idx + 2}/{idx + 2}/{idx + 2}')
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
        log_buffer.log('Mesh', f'v{version_num} header: {num_verts} verts, {num_faces} faces, vertex_size={sizeof_vertex}, bones={num_bones}, lod_offsets={num_lod_offsets}')
        offset = 13 + header_size
        verts, offset = read_vertices(data, offset, num_verts, sizeof_vertex)
        if version_num in ('4.00', '4.01', '5.00') and num_bones > 0:
            skinning_size = num_verts * 8
            log_buffer.log('Mesh', f'Skipping {skinning_size} bytes of skinning data ({num_verts} verts × 8 bytes)')
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
                if len(lod_offsets) >= 2 and lod_offsets[1] > 0 and (lod_offsets[1] < len(faces)):
                    original_count = len(faces)
                    faces = faces[:lod_offsets[1]]
                    log_buffer.log('Mesh', f'Applied LOD: {original_count} → {len(faces)} faces (offsets: {lod_offsets})')
            except Exception as e:
                log_buffer.log('Mesh', f'LOD parsing failed: {e}')
        v_lines = [f"v {fix_float(f'{v.px:.6f}')} {fix_float(f'{v.py:.6f}')} {fix_float(f'{v.pz:.6f}')} {fix_float(f'{v.r / 255.0:.6f}')} {fix_float(f'{v.g / 255.0:.6f}')} {fix_float(f'{v.b / 255.0:.6f}')}" for v in verts]
        n_lines = [f"vn {fix_float(f'{v.nx:.6f}')} {fix_float(f'{v.ny:.6f}')} {fix_float(f'{v.nz:.6f}')}" for v in verts]
        t_lines = [f"vt {fix_float(f'{v.tu:.6f}')} {fix_float(f'{v.tv:.6f}')} 0.0" for v in verts]
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
            chunk_type = data[offset:offset + 8].decode('utf-8', errors='ignore').rstrip('\x00')
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
            chunk_content = data[offset:offset + data_size]
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
            if normals is None and hasattr(mesh, 'normals') and (mesh.normals is not None):
                normals = np.array(mesh.normals, dtype=np.float32)
                if normals.ndim == 1:
                    normals = normals.reshape(-1, 3)
            if normals is not None:
                if len(normals) == num_verts:
                    for i in range(num_verts):
                        verts[i].nx, verts[i].ny, verts[i].nz = normals[i]
                else:
                    log_buffer.log('Mesh', f'Warning: Normal count mismatch ({len(normals)} vs {num_verts})')
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
                    log_buffer.log('Mesh', f'Warning: Color count mismatch ({len(colors)} vs {num_verts})')
            if tex_coords is None and hasattr(mesh, 'tex_coord') and (mesh.tex_coord is not None):
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
                    log_buffer.log('Mesh', f'Warning: UV count mismatch ({len(tex_coords)} vs {num_verts})')
            faces = []
            if hasattr(mesh, 'faces') and mesh.faces is not None:
                for tri in mesh.faces:
                    a, b, c = map(int, tri)
                    faces.append(Face(a + 1, b + 1, c + 1))
            log_buffer.log('Mesh', f'Draco mesh decoded: {num_verts:,} vertices, {len(faces):,} faces')
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
                            log_buffer.log('Mesh', f'Applying high-quality LOD: {len(faces):,} → {max_faces:,} faces')
                except Exception as e:
                    log_buffer.log('Mesh', f'LOD parsing failed: {e}')
            if max_faces < len(faces):
                faces = faces[:max_faces]
            v_lines = [f"v {fix_float(f'{v.px:.6f}')} {fix_float(f'{v.py:.6f}')} {fix_float(f'{v.pz:.6f}')} {fix_float(f'{v.r / 255.0:.6f}')} {fix_float(f'{v.g / 255.0:.6f}')} {fix_float(f'{v.b / 255.0:.6f}')}" for v in verts]
            n_lines = [f"vn {fix_float(f'{v.nx:.6f}')} {fix_float(f'{v.ny:.6f}')} {fix_float(f'{v.nz:.6f}')}" for v in verts]
            t_lines = [f"vt {fix_float(f'{v.tu:.6f}')} {fix_float(f'{v.tv:.6f}')} 0.0" for v in verts]
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
SUPPORTED_MESH_HEADERS = ('version 1.', 'version 2.00', 'version 3.00', 'version 3.01', 'version 4.00', 'version 4.01', 'version 5.00', 'version 6.00', 'version 7.00')

def _mesh_header(data: bytes) -> str:
    if data.startswith(b'\x1f\x8b'):
        try:
            data = gzip.decompress(data)
        except Exception:
            return ''
    return data[:12].decode('utf-8', errors='ignore').strip()

def convert(data: bytes, output_path: str=None) -> str:
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
    elif header in ['version 2.00', 'version 3.00', 'version 3.01', 'version 4.00', 'version 4.01', 'version 5.00']:
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
RBXM_MAGIC = b'<roblox!\x89\xff\r\n\x1a\n'

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

def _to_binary_document(data: bytes) -> bytes:
    data = _extract_document_body(data)
    if data.startswith(RBXM_MAGIC):
        RbxmDeserializer().deserialize(data)
        return data
    if _parse_roblox_xml(data) is None:
        raise ValueError('Data is not a valid RBXM/RBXMX document')
    return write_rbxm(_xml_to_document(data))

def _extract_rbxh_document(data: bytes) -> bytes:
    raw = data or b''
    if raw[:4] != RBXH_MAGIC:
        return _extract_document_body(decompress_if_needed(raw))
    meta = parse_rbxh(raw)
    body = meta.get('body') or b''
    body = _maybe_gunzip(body, meta.get('headers') or {})
    return _extract_document_body(decompress_if_needed(body))

def convert_roblox_file(data: bytes, source_ext: str, target_ext: str, template_data: bytes=b'') -> bytes:
    source_ext = (source_ext or '').lower()
    target_ext = (target_ext or '').lower()
    if source_ext == '.rbxh':
        document = _extract_rbxh_document(data)
    else:
        document = _extract_document_body(decompress_if_needed(data or b''))
    if target_ext == '.rbxh':
        return _wrap_rbxm_bytes(_to_binary_document(document), 'application/octet-stream', template_data)
    if target_ext == '.rbxm':
        return _to_binary_document(document)
    if target_ext == '.rbxmx':
        binary = _to_binary_document(document)
        return write_rbxmx(RbxmDeserializer().deserialize(binary))
    raise ValueError(f'Unsupported Roblox conversion target: {target_ext}')

def _wrap_rbxm_bytes(data: bytes, content_type: str='application/octet-stream', template_data: bytes=b'') -> bytes:
    raw = _to_binary_document(data)
    reserved = b'\x00' * 8
    if template_data[:4] == RBXH_MAGIC:
        template_body = _extract_rbxh_document(template_data)
        if template_body == raw and len(template_data) >= 37:
            reserved = template_data[29:37]
    return RBXH_MAGIC + struct.pack('<II', 2, 0) + b'\x00' + struct.pack('<I', 200) + struct.pack('<I', 0) + b'\x00' * 4 + struct.pack('<I', len(raw)) + reserved + raw

def _document_contains_datamodel(doc: RbxDocument) -> bool:
    return any((inst.class_name == 'DataModel' for inst in doc.instances.values()))

def _binary_contains_class(data: bytes, class_name: str) -> bool:
    offset = 32
    target = class_name
    try:
        while offset + 16 <= len(data):
            chunk_name = data[offset:offset + 4].decode('ascii')
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
                raw = data[offset:offset + compressed_size]
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
    return any((_tag_name(elem) == 'Item' and elem.get('class') == 'DataModel' for elem in root.iter()))

def _xml_contains_item(root: ET.Element) -> bool:
    return any((_tag_name(elem) == 'Item' for elem in root.iter()))

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
                inst.properties[prop_name] = RbxProperty(name=prop_name, fmt=fmt, value=_value_for_format(value, fmt, mapped_ref))
        inst.children = [parse_item(child) for child in _children_named(item, 'Item')]
        return inst
    roots = [parse_item(item) for item in _children_named(root, 'Item')]
    metadata = {elem.get('name') or _tag_name(elem): (elem.text or '').strip() for elem in list(root) if _tag_name(elem) == 'Meta'}
    return RbxDocument(version=0, type_count=0, object_count=len(instances), metadata=RbxMetadata(entries=metadata), instances=instances, roots=roots, shared_strings=shared_strings)

def _xml_property_value(elem: ET.Element, type_name: str, shared_by_md5: dict[str, bytes]) -> Any:
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
    aliases = {'class': None, 'refid': None, 'binarystring': PropertyFormat.STRING, 'protectedstring': PropertyFormat.STRING, 'content': PropertyFormat.CONTENT, 'token': PropertyFormat.ENUM, 'optionalcoordinateframe': PropertyFormat.OPTIONAL_CFRAME, 'uniqueid': PropertyFormat.UNIQUE_ID, 'securitycapabilities': PropertyFormat.SECURITY_CAPABILITIES}
    key = normalized.lower()
    if key in aliases:
        return aliases[key]
    return tag_to_format.get(key, PropertyFormat.STRING)

def _value_for_format(value: Any, fmt: PropertyFormat, ref_mapper) -> Any:
    if fmt in {PropertyFormat.INT, PropertyFormat.ENUM, PropertyFormat.BRICK_COLOR, PropertyFormat.SECURITY_CAPABILITIES}:
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
                random_bits = xml_random >> 1 | (xml_random & 1) << 63
                return {'Index': int(text[24:32], 16), 'Time': int(text[16:24], 16), 'Random': random_bits}
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
    if fmt in {PropertyFormat.CFRAME_MATRIX, PropertyFormat.CFRAME_QUAT, PropertyFormat.OPTIONAL_CFRAME}:
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
    pairs = {str(k): v for k, v in value.items()} if isinstance(value, dict) else _parse_key_values(str(value))
    if pairs:
        return {'S': _safe_float(pairs.get('S', 0.0)), 'O': _safe_int(pairs.get('O', 0))}
    numbers = _parse_numbers(str(value))
    return {'S': numbers[0] if len(numbers) > 0 else 0.0, 'O': int(numbers[1]) if len(numbers) > 1 else 0}

def _parse_udim2_value(value: Any) -> dict[str, float | int]:
    pairs = {str(k): v for k, v in value.items()} if isinstance(value, dict) else _parse_key_values(str(value))
    if pairs:
        return {'XS': _safe_float(pairs.get('XS', 0.0)), 'XO': _safe_int(pairs.get('XO', 0)), 'YS': _safe_float(pairs.get('YS', 0.0)), 'YO': _safe_int(pairs.get('YO', 0))}
    numbers = _parse_numbers(str(value))
    return {'XS': numbers[0] if len(numbers) > 0 else 0.0, 'XO': int(numbers[1]) if len(numbers) > 1 else 0, 'YS': numbers[2] if len(numbers) > 2 else 0.0, 'YO': int(numbers[3]) if len(numbers) > 3 else 0}

def _parse_vector_value(value: Any, keys: tuple[str, ...], caster) -> dict[str, Any]:
    pairs = {str(k): v for k, v in value.items()} if isinstance(value, dict) else _parse_key_values(str(value))
    if pairs:
        return {key: _cast_number(pairs.get(key, 0), caster) for key in keys}
    numbers = _parse_numbers(str(value))
    return {key: _cast_number(numbers[index] if index < len(numbers) else 0, caster) for index, key in enumerate(keys)}

def _parse_ray_value(value: Any) -> dict[str, dict[str, float]]:
    if isinstance(value, dict):
        return {'origin': _parse_vector_value(value.get('origin', {}), ('X', 'Y', 'Z'), float), 'direction': _parse_vector_value(value.get('direction', {}), ('X', 'Y', 'Z'), float)}
    numbers = _parse_numbers(str(value))
    padded = numbers + [0.0] * max(0, 6 - len(numbers))
    return {'origin': {'X': padded[0], 'Y': padded[1], 'Z': padded[2]}, 'direction': {'X': padded[3], 'Y': padded[4], 'Z': padded[5]}}

def _parse_cframe_value(value: Any) -> dict[str, float] | None:
    text = str(value).strip()
    if value is None or text.lower() in {'', 'none', 'null'}:
        return None
    result = {'X': 0.0, 'Y': 0.0, 'Z': 0.0, 'R00': 1.0, 'R01': 0.0, 'R02': 0.0, 'R10': 0.0, 'R11': 1.0, 'R12': 0.0, 'R20': 0.0, 'R21': 0.0, 'R22': 1.0}
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
        return {'Min': _safe_float(value.get('Min', 0.0)), 'Max': _safe_float(value.get('Max', 0.0))}
    pairs = _parse_key_values(str(value))
    if pairs:
        return {'Min': _safe_float(pairs.get('Min', 0.0)), 'Max': _safe_float(pairs.get('Max', 0.0))}
    numbers = _parse_numbers(str(value))
    return {'Min': numbers[0] if len(numbers) > 0 else 0.0, 'Max': numbers[1] if len(numbers) > 1 else 0.0}

def _parse_rect2d_value(value: Any) -> dict[str, dict[str, float]]:
    if isinstance(value, dict):
        return {'min': _parse_vector_value(value.get('min', {}), ('X', 'Y'), float), 'max': _parse_vector_value(value.get('max', {}), ('X', 'Y'), float)}
    numbers = _parse_numbers(str(value))
    padded = numbers + [0.0] * max(0, 4 - len(numbers))
    return {'min': {'X': padded[0], 'Y': padded[1]}, 'max': {'X': padded[2], 'Y': padded[3]}}

def _parse_physical_properties_value(value: Any) -> dict[str, Any] | None:
    text = str(value).strip()
    if value is None or text.lower() in {'', 'none', 'null', 'default'}:
        return None
    if isinstance(value, dict):
        return {'CustomPhysics': _safe_bool(value.get('CustomPhysics', True)), 'Density': _safe_float(value.get('Density', 0.0)), 'Friction': _safe_float(value.get('Friction', 0.0)), 'Elasticity': _safe_float(value.get('Elasticity', 0.0)), 'FrictionWeight': _safe_float(value.get('FrictionWeight', 0.0)), 'ElasticityWeight': _safe_float(value.get('ElasticityWeight', 0.0)), 'AcousticAbsorption': _safe_float(value.get('AcousticAbsorption', 1.0))}
    pairs = _parse_key_values(text)
    if pairs:
        return _parse_physical_properties_value(pairs)
    numbers = _parse_numbers(text)
    if len(numbers) < 5:
        return None
    result: dict[str, Any] = {'CustomPhysics': True, 'Density': numbers[0], 'Friction': numbers[1], 'Elasticity': numbers[2], 'FrictionWeight': numbers[3], 'ElasticityWeight': numbers[4]}
    if len(numbers) > 5:
        result['AcousticAbsorption'] = numbers[5]
    return result

def _parse_font_value(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return {'Family': str(value.get('Family', '')), 'Weight': _safe_int(value.get('Weight', 400)), 'Style': _safe_int(value.get('Style', 0)), 'CachedFaceId': str(value.get('CachedFaceId', ''))}
    pairs = _parse_key_values(str(value))
    if pairs:
        return _parse_font_value(pairs)
    parts = [part.strip() for part in str(value).split(',')]
    return {'Family': parts[0] if len(parts) > 0 else '', 'Weight': _safe_int(parts[1] if len(parts) > 1 else 400), 'Style': _safe_int(parts[2] if len(parts) > 2 else 0), 'CachedFaceId': parts[3] if len(parts) > 3 else ''}

def _parse_key_values(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for part in re.split('[,;]\\s*', text.strip().strip('[]{}()')):
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
    return [float(match.group(0)) for match in re.finditer('[-+]?(?:\\d+(?:\\.\\d*)?|\\.\\d+)(?:[eE][-+]?\\d+)?', text)]

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

def apply_visual_polish(root: tk.Tk, theme: Optional[str]='system', palette: Optional[Dict[str, str]]=None):
    global _CURRENT_PALETTE
    try:
        root.tk.call('tk', 'scaling', float(getattr(root, '_dpi_scale', 1.0)))
    except Exception:
        pass
    p = {'bg_dark': '#1e1e1e', 'bg_medium': '#252526', 'bg_light': '#333333', 'bg_hover': '#3c3c3c', 'fg': '#d4d4d4', 'accent': '#007acc', 'border': '#3c3c3c'}
    if palette:
        p.update(palette)
    style = ttk.Style(root)
    use_sv_ttk = sv_ttk is not None
    if use_sv_ttk:
        try:
            sv_ttk.set_theme('dark')
        except Exception:
            use_sv_ttk = False
    if not use_sv_ttk:
        for t in ('clam', 'alt', 'default', 'classic'):
            if t in style.theme_names():
                try:
                    style.theme_use(t)
                except Exception:
                    pass
                break
    try:
        tkfont.nametofont('TkDefaultFont').configure(family='Comic Sans MS', size=10)
        tkfont.nametofont('TkTextFont').configure(family='Consolas', size=10)
        tkfont.nametofont('TkFixedFont').configure(family='Consolas', size=10)
        tkfont.nametofont('TkMenuFont').configure(family='Comic Sans MS', size=10)
        tkfont.nametofont('TkHeadingFont').configure(family='Comic Sans MS', size=10, weight='bold')
    except Exception:
        pass
    _CURRENT_PALETTE = p
    bg_dark, bg_medium, bg_light = (p['bg_dark'], p['bg_medium'], p['bg_light'])
    bg_hover, fg_white, accent, border = (p['bg_hover'], p['fg'], p['accent'], p['border'])
    root.configure(bg=bg_dark)
    for opt, val in (('*background', bg_dark), ('*foreground', fg_white), ('*activeBackground', bg_hover), ('*activeForeground', '#ffffff'), ('*insertBackground', '#ffffff'), ('*selectBackground', accent), ('*selectForeground', '#ffffff'), ('*troughColor', bg_medium), ('*highlightBackground', border), ('*highlightColor', accent)):
        try:
            root.option_add(opt, val, priority=60)
        except Exception:
            pass
    for opt, val in (('*Toplevel.background', bg_dark), ('*Dialog.background', bg_dark), ('*Message.background', bg_dark), ('*Message.foreground', fg_white), ('*Dialog.Entry.background', bg_medium), ('*Dialog.Entry.foreground', fg_white), ('*Dialog.Label.background', bg_dark), ('*Dialog.Label.foreground', fg_white), ('*Dialog.Button.background', bg_light), ('*Dialog.Button.foreground', fg_white), ('*Dialog.Button.activeBackground', bg_hover), ('*Dialog.Button.activeForeground', '#ffffff')):
        try:
            root.option_add(opt, val)
        except Exception:
            pass
    style.configure('.', background=bg_dark, foreground=fg_white, fieldbackground=bg_medium, bordercolor=border, lightcolor=bg_medium, darkcolor=bg_medium, troughcolor=bg_medium, activebackground=bg_hover, selectbackground=accent, selectforeground='#ffffff')
    style.configure('TFrame', background=bg_dark)
    style.configure('TLabel', background=bg_dark, foreground=fg_white, font=('Comic Sans MS', 10))
    style.configure('TLabelframe', background=bg_dark, foreground=fg_white, bordercolor=border)
    style.configure('TLabelframe.Label', background=bg_dark, foreground=fg_white, padding=(4, 0))
    _ui_scale = max(0.5, min(2.0, float(getattr(root, '_dpi_scale', 1.0))))
    _btn_pad = (max(2, int(6 * _ui_scale)), max(2, int(5 * _ui_scale)))
    _ctrl_pad = max(2, int(3 * _ui_scale))
    _check_pad = (max(2, int(4 * _ui_scale)), max(1, int(2 * _ui_scale)))
    _small_font = max(8, int(round(9 * _ui_scale)))
    _label_font = max(9, int(round(10 * _ui_scale)))
    style.configure('TButton', background=bg_light, foreground=fg_white, bordercolor=border, focusthickness=0, padding=_btn_pad, relief='flat', font=('Comic Sans MS', _small_font, 'bold'))
    style.map('TButton', background=[('pressed', accent), ('active', bg_hover), ('disabled', bg_medium)], foreground=[('disabled', '#6f6f6f')], bordercolor=[('active', accent)])
    style.configure('TCheckbutton', background=bg_dark, foreground=fg_white, padding=_check_pad, font=('Comic Sans MS', _small_font))
    style.map('TCheckbutton', background=[('active', bg_dark)], foreground=[('active', fg_white)])
    style.configure('TRadiobutton', background=bg_dark, foreground=fg_white, padding=_check_pad, font=('Comic Sans MS', _small_font))
    style.map('TRadiobutton', background=[('active', bg_dark)], foreground=[('active', fg_white)])
    style.configure('TEntry', fieldbackground=bg_medium, foreground=fg_white, insertcolor='#ffffff', bordercolor=border, padding=_ctrl_pad)
    style.map('TEntry', fieldbackground=[('focus', bg_medium)], bordercolor=[('focus', accent)])
    style.configure('TCombobox', fieldbackground=bg_medium, background=bg_light, foreground=fg_white, arrowcolor=fg_white, bordercolor=border, padding=_ctrl_pad)
    style.map('TCombobox', fieldbackground=[('readonly', bg_medium)], background=[('readonly', bg_light)], foreground=[('readonly', fg_white)], selectbackground=[('readonly', accent)], selectforeground=[('readonly', '#ffffff')], bordercolor=[('focus', accent)])
    style.configure('TSpinbox', fieldbackground=bg_medium, background=bg_light, foreground=fg_white, arrowcolor='#ffffff', bordercolor=border)
    style.map('TSpinbox', fieldbackground=[('focus', bg_medium)], bordercolor=[('focus', accent)])
    style.configure('Vertical.TScrollbar', background=bg_light, troughcolor=bg_dark, arrowcolor=fg_white, bordercolor=border, relief='flat')
    style.configure('Horizontal.TScrollbar', background=bg_light, troughcolor=bg_dark, arrowcolor=fg_white, bordercolor=border, relief='flat')
    style.configure('TProgressbar', background=accent, troughcolor=bg_medium)
    style.configure('TNotebook', background=bg_dark, borderwidth=0, tabmargins=(6, 4, 6, 0))
    style.configure('TNotebook.Tab', background=bg_medium, foreground=fg_white, padding=(12, 5), relief='flat')
    style.map('TNotebook.Tab', background=[('selected', accent)], foreground=[('selected', '#ffffff')], expand=[('selected', (2, 0, 2, 0))])
    style.configure('Treeview', rowheight=max(18, int(23 * _ui_scale)), font=('Consolas', _small_font), background=bg_medium, foreground=fg_white, fieldbackground=bg_medium, bordercolor=border)
    style.configure('Treeview.Heading', background=bg_light, foreground=fg_white, font=('Segoe UI Semibold', _label_font), padding=(max(3, int(6 * _ui_scale)), max(2, int(4 * _ui_scale)), max(3, int(6 * _ui_scale)), max(2, int(4 * _ui_scale))))
    style.map('Treeview', background=[('selected', accent)], foreground=[('selected', '#ffffff')])
    root._palette = p
    try:
        root.unbind_all('<Map>')
        root.bind_all('<Map>', _theme_on_map, add='+')
    except Exception:
        pass
    _theme_open_windows(root)

def darken_menus(menus: Iterable) -> None:
    p = _CURRENT_PALETTE
    bg_dark = p.get('bg_dark', '#1e1e1e')
    bg_light = p.get('bg_light', '#333333')
    fg_white = p.get('fg', '#d4d4d4')
    accent = p.get('accent', '#007acc')
    seen = set()

    def _apply(menu):
        if id(menu) in seen:
            return
        seen.add(id(menu))
        try:
            menu.configure(bg=bg_dark, fg=fg_white, activebackground=accent, activeforeground='#ffffff', selectcolor='#ffffff', bd=1, relief='flat', borderwidth=0, font=('Segoe UI', 10))
        except Exception:
            pass
        try:
            for index in (menu.index('end') or 0) + 1:
                try:
                    sub = menu.entrycget(index, 'menu')
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

def _toggle_toplevel_maximize(win, state=None):
    try:
        if state is None:
            state = getattr(win, '_routils_max_state', {'max': False, 'restore': None})
        if win.state() == 'zoomed' or state.get('max'):
            win.state('normal')
            if state.get('restore'):
                win.geometry(state['restore'])
            state['max'] = False
        else:
            state['restore'] = win.geometry()
            win.state('zoomed')
            state['max'] = True
        win._routils_max_state = state
    except Exception:
        pass

def theme_toplevel(win) -> None:
    p = _CURRENT_PALETTE
    try:
        win.configure(bg=p['bg_dark'])
    except Exception:
        pass
    try:
        children = win.winfo_children()
    except Exception:
        children = []
    for c in children:
        try:
            klass = c.winfo_class()
            if klass in ('Frame', 'Toplevel', 'Panedwindow'):
                c.configure(bg=p['bg_dark'])
            elif klass == 'Label':
                c.configure(bg=p['bg_dark'], fg=p['fg'])
            elif klass in ('Entry', 'Spinbox'):
                c.configure(bg=p['bg_medium'], fg=p['fg'], insertbackground='#ffffff', selectbackground=p['accent'], selectforeground='#ffffff')
            elif klass in ('Listbox', 'Text'):
                c.configure(bg=p['bg_medium'], fg=p['fg'], insertbackground='#ffffff', selectbackground=p['accent'], selectforeground='#ffffff')
            elif klass == 'Canvas':
                c.configure(bg=p['bg_dark'], highlightbackground=p['border'])
            elif klass == 'Button':
                c.configure(bg=p['bg_light'], fg=p['fg'], activebackground=p['bg_hover'], activeforeground='#ffffff', relief='flat', borderwidth=1)
            elif klass == 'Scrollbar':
                c.configure(bg=p['bg_light'], troughcolor=p['bg_dark'], activebackground=p['bg_hover'])
            elif klass == 'Menu':
                c.configure(bg=p['bg_dark'], fg=p['fg'], activebackground=p['accent'], activeforeground='#ffffff')
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
    local = os.environ.get('LOCALAPPDATA') or os.path.expanduser('~')
    db = os.path.join(local, 'Roblox', 'rbx-storage.db')
    shard_root = os.path.join(local, 'Roblox', 'rbx-storage')
    return (db, shard_root)

def human_size(n: int) -> str:
    n = max(0, int(n))
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if n < 1024 or unit == 'TB':
            return f'{n:.0f}{unit}' if unit == 'B' else f'{n:.1f}{unit}'
        n /= 1024.0

def id_bytes_to_hex(b: bytes) -> str:
    return b.hex()

def shard_path(root: str, hash_hex: str) -> str:
    return os.path.join(root, hash_hex[:2], hash_hex)

def read_shard_bytes(root: str, hash_hex: str) -> Optional[bytes]:
    path = shard_path(root, hash_hex)
    try:
        with open(path, 'rb') as f:
            return f.read()
    except Exception:
        return None

def now_hms() -> str:
    return datetime.now().strftime('%H:%M:%S')

def _sanitize_filename_for_windows(s: str) -> str:
    s = str(s or '')
    illegal = '<>:"/\\|?*'
    cleaned = ''.join(('_' if c in illegal or ord(c) < 32 else c for c in s))
    cleaned = cleaned.strip().rstrip(' .')
    if not cleaned:
        return ''
    reserved = {'CON', 'PRN', 'AUX', 'NUL'}
    reserved.update((f'COM{i}' for i in range(1, 10)))
    reserved.update((f'LPT{i}' for i in range(1, 10)))
    stem = cleaned.split('.', 1)[0].upper()
    if stem in reserved:
        cleaned = '_' + cleaned
    return cleaned[:180].rstrip(' .')

def load_settings() -> Dict:
    try:
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_settings(data: Dict) -> None:
    try:
        with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
_BUNDLE_DIR = getattr(sys, '_MEIPASS', BASE_DIR)
ICON_PATH = os.path.join(_BUNDLE_DIR, 'routils.ico')
WEBVIEW2_URL_DEFAULTS = 'https://raw.githubusercontent.com/MaximumADHD/Roblox-FFlag-Tracker/refs/heads/main/PCDesktopClient.json'
WEBVIEW2_URL_OFFSETS_ROOT = 'https://offsets.imtheo.lol/'
WEBVIEW2_URL_OFFSETS_TEMPLATE = 'https://offsets.imtheo.lol/{version}/fflags.hpp'
GITHUB_PRESETS_API = 'https://api.github.com/repos/offp001/routils/contents/src/presets'

class _WindowsTrayIcon:
    WM_USER = 1024
    WM_TRAYICON = WM_USER + 100
    WM_LBUTTONUP = 514
    WM_LBUTTONDBLCLK = 515
    WM_RBUTTONUP = 517
    WM_COMMAND = 273
    WM_DESTROY = 2
    NIM_ADD = 0
    NIM_DELETE = 2
    NIF_MESSAGE = 1
    NIF_ICON = 2
    NIF_TIP = 4
    TPM_LEFTALIGN = 0
    TPM_BOTTOMALIGN = 32
    MF_STRING = 0
    ID_OPEN = 1001
    ID_EXIT = 1002

    class NOTIFYICONDATAW(ctypes.Structure):
        _fields_ = [('cbSize', ctypes.wintypes.DWORD), ('hWnd', ctypes.wintypes.HWND), ('uID', ctypes.wintypes.UINT), ('uFlags', ctypes.wintypes.UINT), ('uCallbackMessage', ctypes.wintypes.UINT), ('hIcon', ctypes.c_void_p), ('szTip', ctypes.wintypes.WCHAR * 128), ('dwState', ctypes.wintypes.DWORD), ('dwStateMask', ctypes.wintypes.DWORD), ('szInfo', ctypes.wintypes.WCHAR * 256), ('uVersion', ctypes.wintypes.UINT), ('szInfoTitle', ctypes.wintypes.WCHAR * 64), ('dwInfoFlags', ctypes.wintypes.DWORD), ('guidItem', ctypes.c_byte * 16), ('hBalloonIcon', ctypes.c_void_p)]

    class WNDCLASSW(ctypes.Structure):
        _fields_ = [('style', ctypes.wintypes.UINT), ('lpfnWndProc', ctypes.WINFUNCTYPE(ctypes.c_ssize_t, ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)), ('cbClsExtra', ctypes.c_int), ('cbWndExtra', ctypes.c_int), ('hInstance', ctypes.c_void_p), ('hIcon', ctypes.c_void_p), ('hCursor', ctypes.c_void_p), ('hbrBackground', ctypes.c_void_p), ('lpszMenuName', ctypes.wintypes.LPCWSTR), ('lpszClassName', ctypes.wintypes.LPCWSTR)]

    def __init__(self, icon_path, on_open, on_exit):
        self.icon_path = icon_path
        self.on_open = on_open
        self.on_exit = on_exit
        self.hwnd = None
        self.hicon = None
        self._class_name = 'RoUtilsTrayWindow'
        self._wndproc_ref = ctypes.WINFUNCTYPE(ctypes.c_ssize_t, ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)(self._wndproc)
        self._class_atom = None
        self._nid = None

    def _wndproc(self, hwnd, msg, wparam, lparam):
        if msg == self.WM_TRAYICON:
            if lparam in (self.WM_LBUTTONUP, self.WM_LBUTTONDBLCLK):
                self.on_open()
            elif lparam == self.WM_RBUTTONUP:
                self._show_menu()
            return 0
        if msg == self.WM_COMMAND:
            command = wparam & 65535
            if command == self.ID_OPEN:
                self.on_open()
            elif command == self.ID_EXIT:
                self.on_exit()
            return 0
        if msg == self.WM_DESTROY:
            try:
                ctypes.windll.shell32.Shell_NotifyIconW(self.NIM_DELETE, ctypes.byref(self._nid))
            except Exception:
                pass
            return 0
        return ctypes.windll.user32.DefWindowProcW(hwnd, msg, wparam, lparam)

    def _show_menu(self):
        user32 = ctypes.windll.user32

        class POINT(ctypes.Structure):
            _fields_ = [('x', ctypes.c_long), ('y', ctypes.c_long)]
        pt = POINT()
        user32.GetCursorPos(ctypes.byref(pt))
        menu = user32.CreatePopupMenu()
        if not menu:
            return
        user32.AppendMenuW(menu, self.MF_STRING, self.ID_OPEN, 'Open RoUtils')
        user32.AppendMenuW(menu, self.MF_STRING, self.ID_EXIT, 'Exit RoUtils')
        user32.SetForegroundWindow(self.hwnd)
        user32.TrackPopupMenu(menu, self.TPM_LEFTALIGN | self.TPM_BOTTOMALIGN, pt.x, pt.y, 0, self.hwnd, None)
        user32.DestroyMenu(menu)

    def run(self):
        user32 = ctypes.windll.user32
        shell32 = ctypes.windll.shell32
        hinstance = ctypes.windll.kernel32.GetModuleHandleW(None)
        wc = self.WNDCLASSW()
        wc.style = 0
        wc.lpfnWndProc = self._wndproc_ref
        wc.cbClsExtra = 0
        wc.cbWndExtra = 0
        wc.hInstance = hinstance
        wc.hIcon = 0
        wc.hCursor = 0
        wc.hbrBackground = 0
        wc.lpszMenuName = None
        wc.lpszClassName = self._class_name
        self._class_atom = user32.RegisterClassW(ctypes.byref(wc))
        if not self._class_atom:
            raise ctypes.WinError()
        self.hwnd = user32.CreateWindowExW(0, self._class_name, 'RoUtils Tray', 0, 0, 0, 0, 0, 0, 0, hinstance, None)
        if not self.hwnd:
            raise ctypes.WinError()
        large = ctypes.c_void_p()
        small = ctypes.c_void_p()
        try:
            ctypes.windll.shell32.ExtractIconExW(self.icon_path, 0, ctypes.byref(large), ctypes.byref(small), 1)
            self.hicon = small.value or large.value
        except Exception:
            self.hicon = None
        if not self.hicon:
            self.hicon = user32.LoadIconW(0, ctypes.c_void_p(32512))
        nid = self.NOTIFYICONDATAW()
        nid.cbSize = ctypes.sizeof(self.NOTIFYICONDATAW)
        nid.hWnd = self.hwnd
        nid.uID = 1
        nid.uFlags = self.NIF_MESSAGE | self.NIF_ICON | self.NIF_TIP
        nid.uCallbackMessage = self.WM_TRAYICON
        nid.hIcon = self.hicon
        nid.szTip = 'RoUtils'
        self._nid = nid
        if not shell32.Shell_NotifyIconW(self.NIM_ADD, ctypes.byref(nid)):
            raise ctypes.WinError()
        msg = ctypes.wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) > 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
        try:
            shell32.Shell_NotifyIconW(self.NIM_DELETE, ctypes.byref(nid))
        except Exception:
            pass
        try:
            if self.hicon:
                user32.DestroyIcon(self.hicon)
        except Exception:
            pass
        try:
            user32.UnregisterClassW(self._class_name, hinstance)
        except Exception:
            pass

    def stop(self):
        if self.hwnd:
            try:
                ctypes.windll.user32.PostMessageW(self.hwnd, self.WM_DESTROY, 0, 0)
                ctypes.windll.user32.PostMessageW(self.hwnd, 18, 0, 0)
            except Exception:
                pass

def _launch_webview2(url: str, title: str) -> None:
    try:
        import webview
    except Exception as e:
        messagebox.showerror('WebView2', 'WebView2 support requires pywebview and the Microsoft Edge WebView2 Runtime.\n\nInstall pywebview with: pip install pywebview\n\n' + str(e))
        return
    try:
        webview.create_window(title, url=url, width=1200, height=800, min_size=(700, 500), text_select=True)
        webview.start(gui='edgechromium', debug=False)
    except Exception as e:
        try:
            messagebox.showerror('WebView2', f'Could not open WebView2 window:\n{e}')
        except Exception:
            pass

def _get_latest_offsets_webview_url() -> str:
    return 'https://offsets.imtheo.lol/FFlags.hpp'

def _open_webview2_process(url: str, title: str) -> None:
    try:
        if getattr(sys, 'frozen', False):
            target = sys.executable
            args = ['--webview2', url, title]
        else:
            target = sys.executable
            args = [os.path.abspath(__file__), '--webview2', url, title]
        subprocess.Popen([target, *args], cwd=BASE_DIR, close_fds=True)
    except Exception as e:
        messagebox.showerror('WebView2', f'Could not start WebView2 window:\n{e}')

def _normalize_fflag_json(data):
    flags = []
    if isinstance(data, dict):
        for n, v in data.items():
            flags.append({'name': fflag_strip_prefix(str(n)), 'value': str(v).lower() if isinstance(v, bool) else str(v), 'type': fflag_infer_type(v)})
    elif isinstance(data, list):
        for x in data:
            if isinstance(x, dict) and x.get('name') is not None:
                v = x.get('value', '')
                flags.append({'name': fflag_strip_prefix(str(x['name'])), 'value': str(v).lower() if isinstance(v, bool) else str(v), 'type': x.get('type') or fflag_infer_type(v)})
    return flags
FFLAG_VK_NAMES = {'SPACE': 32, 'ENTER': 13, 'TAB': 9, 'ESC': 27, 'ESCAPE': 27, 'BACKSPACE': 8, 'DELETE': 46, 'INSERT': 45, 'HOME': 36, 'END': 35, 'PAGEUP': 33, 'PAGEDOWN': 34, 'LEFT': 37, 'UP': 38, 'RIGHT': 39, 'DOWN': 40}
FFLAG_VK_NAMES.update({f'F{i}': 111 + i for i in range(1, 13)})
FFLAG_VK_NAMES.update({f'F{i}': 111 + i for i in range(13, 25)})
FFLAG_VK_NAMES.update({f'NUMPAD{i}': 96 + i for i in range(10)})
FFLAG_VK_NAMES.update({'MOUSE1': 1, 'MOUSE2': 2, 'MOUSE3': 4, 'MOUSE4': 5, 'MOUSE5': 6})
FFLAG_VK_NAMES.update({'OEM1': 186, 'PLUS': 187, 'COMMA': 188, 'MINUS': 189, 'PERIOD': 190, 'SLASH': 191, 'OEM3': 192, 'LBRACKET': 219, 'BACKSLASH': 220, 'RBRACKET': 221, 'QUOTE': 222})
FFLAG_VK_NAMES.update({str(i): 48 + i for i in range(10)})
FFLAG_VK_NAMES.update({chr(ord('A') + i): 65 + i for i in range(26)})

def fflag_key_to_vk(key: str) -> int:
    key = str(key or '').strip().upper()
    if key in FFLAG_VK_NAMES:
        return FFLAG_VK_NAMES[key]
    if len(key) == 1 and sys.platform == 'win32':
        try:
            vk = ctypes.windll.user32.VkKeyScanW(ord(key)) & 255
            return int(vk)
        except Exception:
            pass
    return 0
RBXH_MAGIC = b'RBXH'

def _parse_header_lines(hdr_text: str) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    if not hdr_text:
        return headers
    for line in hdr_text.splitlines():
        line = line.strip()
        if not line or ':' not in line:
            continue
        k, v = line.split(':', 1)
        headers[k.strip().lower()] = v.strip()
    return headers

def parse_rbxh(blob: bytes) -> Dict:
    res = {'wrapped': False, 'version': None, 'url': None, 'status': None, 'headers': {}, 'header_text': None, 'body': blob, 'full_payload': blob}
    if not blob or blob[:4] != RBXH_MAGIC:
        return res
    res['wrapped'] = True
    data = memoryview(blob)[4:]
    res['full_payload'] = bytes(data)
    if len(data) < 8:
        res['body'] = bytes(data)
        return res
    try:
        pos = 0
        version, url_len = struct.unpack_from('<II', data, pos)
        pos += 8
        if version < 1 or version > 16 or url_len > len(data) - pos:
            res['body'] = bytes(data)
            return res
        url = bytes(data[pos:pos + url_len]).decode('utf-8', 'replace')
        pos += url_len
        if pos + 1 + 4 + 4 + 4 + 4 + 8 > len(data):
            res['body'] = bytes(data)
            return res
        pos += 1
        status = struct.unpack_from('<I', data, pos)[0]
        pos += 4
        header_len = struct.unpack_from('<I', data, pos)[0]
        pos += 4
        pos += 4
        content_len = struct.unpack_from('<I', data, pos)[0]
        pos += 4
        pos += 8
        if header_len > len(data) - pos:
            res['body'] = bytes(data)
            return res
        header_bytes = bytes(data[pos:pos + header_len])
        pos += header_len
        content_len = min(content_len, max(0, len(data) - pos))
        body = bytes(data[pos:pos + content_len])
        header_text = header_bytes.decode('utf-8', 'replace')
        res.update({'version': version, 'url': url or None, 'status': status, 'header_text': header_text, 'headers': _parse_header_lines(header_text), 'body': body})
        return res
    except Exception:
        res['body'] = bytes(data)
        return res

def _maybe_gunzip(b: bytes, headers: Dict[str, str]) -> bytes:
    enc = (headers.get('content-encoding') or headers.get('content_encoding') or '').lower()
    if 'gzip' in enc:
        try:
            return gzip.decompress(b)
        except Exception:
            return b
    if len(b) >= 3 and b[:3] == b'\x1f\x8b\x08':
        try:
            return gzip.decompress(b)
        except Exception:
            return b
    return b

def _content_type(headers: Dict[str, str]) -> str:
    ct = (headers.get('content-type') or headers.get('content_type') or '').lower()
    return ct.split(';')[0].strip()
_ticket_url_re = re.compile(b'https?://([A-Za-z0-9\\.\\-]+)\\S+', re.IGNORECASE)

def detect_ticket(payload: bytes, url: Optional[str]) -> Tuple[bool, str]:
    if url and 'rbxcdn.com' in url and any((k in url for k in ('__token_', 'signature', 'key-pair-id', 'policy', 'expires'))):
        return (True, 'Ticket (signed URL)')
    n = len(payload)
    if 100 <= n <= 4096:
        if b'rbxcdn.com' in payload and any((k in payload.lower() for k in (b'key-pair-id', b'signature', b'policy', b'__token_', b'expires'))):
            host = 'rbxcdn'
            m = _ticket_url_re.search(payload)
            if m:
                try:
                    host = m.group(1).decode('ascii', 'ignore')
                except Exception:
                    pass
            return (True, f'Ticket ({host})')
    return (False, '')

def find_embedded_image(body: bytes) -> Tuple[str, int]:
    scan = body[:131072]
    i = scan.find(b'RIFF')
    while i != -1 and i + 12 <= len(scan):
        if scan[i + 8:i + 12] == b'WEBP':
            return ('WEBP', i)
        i = scan.find(b'RIFF', i + 1)
    sigs = [(b'\x89PNG\r\n\x1a\n', 'PNG'), (b'\xff\xd8\xff', 'JPEG'), (b'GIF8', 'GIF'), (b'DDS ', 'DDS'), (b'BM', 'BMP')]
    for sig, lbl in sigs:
        j = scan.find(sig)
        if j != -1:
            return (lbl, j)
    return ('', -1)

def _is_ogg_at(scan: bytes, j: int) -> bool:
    if j < 0 or j + 27 > len(scan):
        return False
    if scan[j:j + 4] != b'OggS':
        return False
    if scan[j + 4] != 0:
        return False
    tail = scan[j:j + 4096]
    return b'vorbis' in tail or b'OpusHead' in tail
_BITRATES = {(3, 3): [0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 0], (3, 2): [0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384, 0], (3, 1): [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0], (2, 3): [0, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256, 0], (2, 2): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0], (2, 1): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0], (0, 3): [0, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256, 0], (0, 2): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0], (0, 1): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0]}
_SAMPLERATES = {3: [44100, 48000, 32000, 0], 2: [22050, 24000, 16000, 0], 0: [11025, 12000, 8000, 0]}

def _read_u32_be(b: bytes, i: int) -> int:
    return b[i] << 24 | b[i + 1] << 16 | b[i + 2] << 8 | b[i + 3] << 0

def _is_valid_mp3_header(h: int) -> Tuple[bool, dict]:
    if h >> 21 & 2047 != 2047:
        return (False, {})
    ver = h >> 19 & 3
    layer = h >> 17 & 3
    br_ix = h >> 12 & 15
    sr_ix = h >> 10 & 3
    pad = h >> 9 & 1
    if ver == 1 or layer == 0:
        return (False, {})
    if sr_ix == 3 or br_ix == 0 or br_ix == 15:
        return (False, {})
    sr = _SAMPLERATES.get(ver, [0, 0, 0, 0])[sr_ix]
    br = _BITRATES.get((ver, layer), [0] * 16)[br_ix] * 1000
    if sr == 0 or br == 0:
        return (False, {})
    return (True, {'ver': ver, 'layer': layer, 'sr': sr, 'br': br, 'pad': pad})

def _mp3_frame_size(info: dict) -> int:
    ver = info['ver']
    layer = info['layer']
    br = info['br']
    sr = info['sr']
    pad = info['pad']
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
        if ok2 and info2['sr'] == info['sr'] and (info2['layer'] == info['layer']):
            return i
        i += 1
    return -1

def find_embedded_audio_robust(body: bytes) -> Tuple[str, int]:
    scan = body[:131072]
    i = scan.find(b'RIFF')
    while i != -1 and i + 12 <= len(scan):
        if scan[i + 8:i + 12] == b'WAVE':
            return ('WAV', i)
        i = scan.find(b'RIFF', i + 1)
    j = scan.find(b'OggS')
    if j != -1 and _is_ogg_at(scan, j):
        return ('OGG', j)
    off = _find_mp3_two_frames(scan)
    if off != -1:
        return ('MP3', off)
    return ('', -1)
KTX1_MAGIC = b'\xabKTX 11\xbb\r\n\x1a\n'
KTX2_MAGIC = b'\xabKTX 20\xbb\r\n\x1a\n'

def _label_ktx1(body: bytes, off: int) -> str:
    if off + 64 > len(body):
        return 'KTX1'
    end = struct.unpack('<I', body[off + 12:off + 16])[0]
    gl_internal = struct.unpack('<I', body[off + 28:off + 32])[0] if end == 67305985 else 0
    dxt_vals = {33776, 33777, 33778, 33779, 34480, 34481}
    astc_min, astc_max = (37808, 37887)
    if gl_internal in dxt_vals:
        return 'KTX1 (BCn)'
    if astc_min <= gl_internal <= astc_max:
        return 'KTX1 (ASTC)'
    return 'KTX1'

def _label_ktx2(body: bytes, off: int) -> str:
    if off + 48 > len(body):
        return 'KTX2'
    vkfmt = struct.unpack('<I', body[off + 12:off + 16])[0]
    bcn = {131, 132, 133, 134, 135, 137, 146}
    astc = set(range(166, 183))
    if vkfmt in bcn:
        return 'KTX2 (BCn)'
    if vkfmt in astc:
        return 'KTX2 (ASTC)'
    return 'KTX2'

def detect_ktx_anywhere(body: bytes) -> Tuple[str, str]:
    scan = body[:131072]
    i1 = scan.find(KTX1_MAGIC)
    if i1 != -1:
        return ('Texture', _label_ktx1(body, i1))
    i2 = scan.find(KTX2_MAGIC)
    if i2 != -1:
        return ('Texture', _label_ktx2(body, i2))
    return ('', '')

def detect_mesh_kind(payload: bytes) -> Tuple[str, str]:
    if payload.startswith(b'version '):
        try:
            first = payload.split(b'\n', 1)[0].decode('ascii', 'ignore')
            m = re.search('version\\s+(\\d+)', first)
            if m:
                v = int(m.group(1))
                if 1 <= v <= 5:
                    return ('Mesh', f'v{v} (ASCII)')
                if v >= 6:
                    return ('Mesh', f'v{v}')
        except Exception:
            return ('Mesh', 'ASCII')
        return ('Mesh', 'ASCII')
    if b'DRACO' in payload[:4096] or b'MESH' in payload[:16]:
        return ('Mesh', 'v6/v7 (binary)')
    return ('', '')

def detect_font_kind(body: bytes, ct: str) -> Tuple[str, str]:
    if ct.startswith('font/') or ct in ('application/font-sfnt', 'application/font-woff', 'application/font-woff2'):
        if 'woff2' in ct:
            return ('Font', 'WOFF2')
        if 'woff' in ct:
            return ('Font', 'WOFF')
        if 'otf' in ct:
            return ('Font', 'OTF')
        if 'ttf' in ct:
            return ('Font', 'TTF')
    if body[:4] == b'OTTO':
        return ('Font', 'OTF')
    if body[:4] == b'ttcf':
        return ('Font', 'TTC')
    if body[:4] == b'wOFF':
        return ('Font', 'WOFF')
    if body[:4] == b'wOF2':
        return ('Font', 'WOFF2')
    if body[:4] == b'\x00\x01\x00\x00':
        return ('Font', 'TTF')
    return ('', '')

def _find_json_head_slice(body: bytes, headers: Dict[str, str]) -> Optional[str]:
    scan = body[:262144]
    i = scan.find(b'{')
    if i != -1:
        try:
            return scan[i:i + 8192].decode('utf-8', 'ignore')
        except Exception:
            pass
    body_unz = _maybe_gunzip(body, headers)
    if body_unz is not body:
        scan2 = body_unz[:262144]
        j = scan2.find(b'{')
        if j != -1:
            try:
                return scan2[j:j + 8192].decode('utf-8', 'ignore')
            except Exception:
                pass
    return None

def is_translation_json_text(text: str) -> bool:
    t = text.lower()
    if 'localizationtable' in t:
        return True
    hits = 0
    for key in ('translationmapping', '"entries"', '"translations"'):
        if key in t:
            hits += 1
    if hits >= 1 and ('"locale"' in t or 'language' in t or 'sourcelanguage' in t):
        return True
    return False

def detect_translation_json(body: bytes, headers: Dict[str, str]) -> Tuple[bool, str]:
    head = _find_json_head_slice(body, headers)
    if not head:
        return (False, '')
    if head.lstrip().startswith('{') and is_translation_json_text(head):
        return (True, 'JSON')
    return (False, '')
_RBXM_BIN_MAGIC = b'<roblox!'
_RBXM_SCAN_LIMIT = 8192

def detect_rbxm_binary(body: bytes) -> int:
    window = body[:_RBXM_SCAN_LIMIT]
    p = window.find(_RBXM_BIN_MAGIC)
    if p != -1 and p <= 64:
        return p
    return -1

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
        for child in getattr(node, 'children', ()) or ():
            visit(child)
    for node in roots:
        visit(node)
    return out

def _has_animation_structure(nodes) -> bool:
    classes = {getattr(node, 'class_name', '') for node in nodes}
    if classes & {'KeyframeSequence', 'CurveAnimation', 'AnimationClip'}:
        return True
    for node in nodes:
        if getattr(node, 'class_name', '') != 'Keyframe':
            continue
        stack = list(getattr(node, 'children', ()) or ())
        while stack:
            child = stack.pop()
            if getattr(child, 'class_name', '') in {'Pose', 'NumberPose'}:
                return True
            stack.extend(getattr(child, 'children', ()) or ())
    return False

def _classify_rbxm_asset(body: bytes):
    _MODEL_CLASSES = {'Model', 'Folder', 'Tool', 'Accessory', 'Accoutrement', 'Handle', 'Part', 'MeshPart', 'WedgePart', 'CornerWedgePart', 'TrussPart', 'CylinderPart', 'UnionOperation', 'PartOperation', 'SpecialMesh', 'FileMesh', 'BasePart', 'Humanoid', 'Motor6D', 'Texture', 'Decal'}
    try:
        try:
            raw = _decompress_document(body)
        except Exception:
            raw = body
        if raw.lstrip().startswith(b'<roblox!'):
            insts = {}
            try:
                insts = parse_rbxm(raw)
            except Exception:
                insts = {}
            nodes = _walk_instance_tree(insts)
            class_names = {getattr(i, 'class_name', '') for i in nodes}
            if _has_animation_structure(nodes):
                return ('RBXM', 'Animation')
            if _RbxmDeserializer is not None:
                try:
                    doc = _RbxmDeserializer().deserialize(raw)
                except Exception:
                    doc = None
                if doc is not None:
                    nodes = _walk_instance_tree(getattr(doc, 'roots', None) or doc.instances)
                    class_names = {getattr(i, 'class_name', '') for i in nodes}
                    if _has_animation_structure(nodes):
                        return ('RBXM', 'Animation')
                    if 'DataModel' in class_names:
                        return ('rbxl (place)', 'RBXL (place)')
                    if class_names & _MODEL_CLASSES:
                        return ('RBXM', 'Model')
            if prop_names & _RIG_NAMES:
                return ('Animation', 'RBXM (bin)')
            return ('RBXM', '')
        elif b'<roblox' in raw[:4096]:
            text = raw[:262144].decode('utf-8', 'replace')
            low = text.lower()
            if re.search('class\\s*=\\s*"(Keyframe|CurveAnimation|KeyframeSequence|AnimationClip|Pose|NumberPose)"', text, re.I):
                return ('Animation', 'KeyframeSequence')
            if re.search('class\\s*=\\s*"DataModel"', text, re.I):
                return ('rbxl (place)', 'RBXL/XML')
            if re.search('class\\s*=\\s*"(Part|MeshPart|WedgePart|CylinderPart|SpecialMesh|BasePart|Tool|Model)"', text, re.I):
                return ('Model', 'RBXMX/XML')
            if b'<roblox' in low and (not b'properties' in low):
                return ('Model', 'RBXMX/XML')
    except Exception:
        return (None, None)
    return (None, None)

def _extract_rbxm_name(body: bytes) -> str:
    try:
        if body.lstrip().startswith(b'<roblox!'):
            instances = parse_rbxm(body)
            for node in instances.values():
                if node.class_name in ('AnimationClip', 'CurveAnimation', 'KeyframeSequence', 'Model', 'Folder', 'Part'):
                    nm = node.properties.get('Name')
                    if isinstance(nm, str) and nm.strip():
                        return nm.strip()
            for node in instances.values():
                nm = node.properties.get('Name')
                if isinstance(nm, str) and nm.strip():
                    return nm.strip()
        elif b'<roblox' in body[:4096]:
            text = body[:262144].decode('utf-8', 'ignore')
            m = re.search('<string name="Name">([^<]{1,120})</string>', text)
            if m and m.group(1).strip():
                return m.group(1).strip()
    except Exception:
        pass
    return ''

def _asset_name(body: bytes, url: Optional[str]) -> str:
    name = _extract_rbxm_name(body)
    if name:
        return name
    if url:
        tail = os.path.basename(urlparse(url).path).strip()
        if tail and '.' not in tail and (len(tail) < 120):
            return tail
    return ''

def sniff_kind(body: bytes, url: Optional[str], headers: Dict[str, str], full_payload: bytes) -> Tuple[str, str, bool]:
    is_t, ticket_label = detect_ticket(full_payload or body, url)
    if is_t:
        return ('Ticket', ticket_label, True)
    is_tr, tr_label = detect_translation_json(body, headers)
    if is_tr:
        return ('Translations', tr_label, False)

    def _is_decal_url(u: Optional[str]) -> bool:
        if not u:
            return False
        ul = u.lower()
        return 'tr.rbxcdn.com' in ul or '/image/' in ul or '/thumbnail/' in ul
    k_cat, k_lbl = detect_ktx_anywhere(body)
    if k_cat:
        return (k_cat, k_lbl, False)
    if detect_rbxm_binary(body) != -1:
        try:
            kind = _classify_document(_decompress_document(body))
            rcat, rlbl = _classify_rbxm_asset(body)
            if rcat:
                return (rcat, rlbl, False)
            if kind and ('anim' in kind.lower() or 'rbxl' not in kind.lower()):
                if any((k in body[:521].lower() for k in (b'keyframesequence', b'animationclip', b'curveanimation', b'pose'))):
                    return ('Animation', 'RBXM (bin)', False)
        except Exception:
            pass
        return ('RBXM', '', False)
    low = body[:131072].lower()
    if b'<roblox' in low:
        rcat, rlbl = _classify_rbxm_asset(body)
        if rcat:
            return (rcat, rlbl, False)
        if b'keyframesequence' in low or b'animationclip' in low:
            return ('Animation', 'KeyframeSequence', False)
        return ('Model', 'RBXMX/XML', False)
    m_cat, m_lbl = detect_mesh_kind(body)
    if m_cat:
        return (m_cat, m_lbl, False)
    ct = _content_type(headers)
    f_cat, f_lbl = detect_font_kind(body, ct)
    if f_cat:
        return (f_cat, f_lbl, False)
    if body[:8] == b'\x89PNG\r\n\x1a\n':
        return ('Decal' if _is_decal_url(url) else 'Image', 'PNG', False)
    if body[:3] == b'GIF':
        return ('Decal' if _is_decal_url(url) else 'Image', 'GIF', False)
    if body[:2] == b'\xff\xd8':
        return ('Decal' if _is_decal_url(url) else 'Image', 'JPEG', False)
    if len(body) >= 12 and body[:4] == b'RIFF' and (body[8:12] == b'WEBP'):
        return ('Decal' if _is_decal_url(url) else 'Image', 'WEBP', False)
    img_lbl, _ = find_embedded_image(body)
    if img_lbl:
        return ('Decal' if _is_decal_url(url) else 'Image', img_lbl, False)
    if body[:4] == b'\x1aE\xdf\xa3':
        return ('Video', 'WebM', False)
    if len(body) >= 12 and body[4:8] == b'ftyp':
        return ('Video', 'MP4', False)
    text_head = body[:8192].decode('utf-8', 'ignore').lstrip().lower()
    if text_head.startswith('#extm3u'):
        return ('Video', 'M3U', False)
    ct = _content_type(headers)
    if ct.startswith('video/'):
        subtype = ct.split('/', 1)[1].upper()
        if subtype in ('X-MATROSKA', 'MATROSKA'):
            subtype = 'WEBM'
        elif subtype in ('MP4', 'X-M4V'):
            subtype = 'MP4'
        elif subtype in ('M3U8', 'X-MPEGURL', 'VND.APPLE.MPEGURL'):
            subtype = 'M3U8'
        return ('Video', subtype, False)
    if body[:3] == b'ID3':
        return ('Sound', 'MP3', False)
    if len(body) >= 12 and body[:4] == b'RIFF' and (body[8:12] == b'WAVE'):
        return ('Sound', 'WAV', False)
    if _is_ogg_at(body, 0):
        return ('Sound', 'OGG', False)
    aud_lbl, _ = find_embedded_audio_robust(body)
    if aud_lbl:
        return ('Sound', aud_lbl, False)
    ct = _content_type(headers)
    if ct.startswith('image/'):
        return ('Decal' if _is_decal_url(url) else 'Image', ct.split('/', 1)[1].upper(), False)
    if ct.startswith('audio/'):
        return ('Sound', 'MP3' if ct.endswith('mpeg') else ct.split('/', 1)[1].upper(), False)
    if ct in ('application/ktx', 'image/ktx', 'image/ktx2'):
        return ('Texture', 'KTX2' if 'ktx2' in ct else 'KTX1', False)
    if ct in ('application/json', 'text/json', 'application/ld+json'):
        if is_translation_json_text(text_head):
            return ('Translations', 'JSON', False)
        return ('Text', 'JSON', False)
    if ct in ('application/xml', 'text/xml'):
        if text_head.startswith('<roblox'):
            rcat, rlbl = _classify_rbxm_asset(body)
            if rcat:
                return (rcat, rlbl, False)
            return ('Model', 'RBXMX/XML', False)
        return ('Text', 'XML', False)
    if ct.startswith('font/'):
        return ('Font', ct.split('/', 1)[1].upper(), False)
    if text_head.startswith('{') or text_head.startswith('['):
        if is_translation_json_text(text_head):
            return ('Translations', 'JSON', False)
        return ('Text', 'JSON', False)
    if text_head.startswith('<roblox'):
        rcat, rlbl = _classify_rbxm_asset(body)
        if rcat:
            return (rcat, rlbl, False)
        if 'keyframesequence' in text_head or 'animationclip' in text_head:
            return ('Animation', 'KeyframeSequence', False)
        return ('Model', 'RBXMX/XML', False)
    if text_head.startswith('<'):
        return ('Text', 'XML/HTML', False)
    if url:
        u = urlparse(url)
        q = parse_qs(u.query or '')
        atype = (q.get('type') or q.get('assetType') or q.get('assettype') or [''])[0].lower()
        if atype == 'unsupported_animation':
            return ('Animation', 'Asset', False)
        if atype == 'mesh':
            return ('Mesh', 'Asset', False)
        tail = (u.path or '').lower()
        if tail.endswith('.mesh'):
            return ('Mesh', 'Asset', False)
        if any((tail.endswith(ext) for ext in ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.dds'))):
            return ('Decal' if 'tr.rbxcdn.com' in u.netloc or '/image/' in tail or '/thumbnail/' in tail else 'Image', tail.split('.')[-1].upper(), False)
        if any((tail.endswith(ext) for ext in ('.ogg', '.mp3', '.wav'))):
            return ('Sound', tail.split('.')[-1].upper(), False)
        if any((tail.endswith(ext) for ext in ('.mp4', '.m4v', '.webm', '.mkv', '.m3u8', '.mov'))):
            ext = tail.split('.')[-1].upper()
            return ('Video', 'WEBM' if ext == 'WEBM' else ext, False)
        if tail.endswith('.ktx') or tail.endswith('.ktx2'):
            return ('Texture', 'KTX2' if tail.endswith('ktx2') else 'KTX1', False)
        if any((tail.endswith(ext) for ext in ('.ttf', '.otf', '.ttc', '.woff', '.woff2'))):
            return ('Font', tail.split('.')[-1].upper(), False)
    if body[:4] == b'(\xb5/\xfd':
        return ('Compressed', 'ZSTD', False)
    if body[:4] == b'\x04"M\x18':
        return ('Compressed', 'LZ4F', False)
    return ('Unknown', '', False)

def connect_ro(db_path: str) -> sqlite3.Connection:
    uri = f'file:{db_path}?mode=ro&cache=shared'
    return sqlite3.connect(uri, uri=True, timeout=0.5, isolation_level=None)

def connect_rw(db_path: str) -> sqlite3.Connection:
    uri = f'file:{db_path}?mode=rwc&cache=shared'
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
    name: str = ''
    id_bytes: bytes = field(repr=False, default=b'')

def scan_db_once(db_path: str, shard_root: str, seen: set, max_rows: Optional[int]=None, offset: int=0) -> List[ScanItem]:
    out: List[ScanItem] = []
    try:
        conn = connect_ro(db_path)
    except Exception:
        return out
    try:
        cur = conn.cursor()
        cur.execute('SELECT id, content FROM files LIMIT ? OFFSET ?', (max_rows or -1, max(0, int(offset))))
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
            url = meta.get('url')
            body = meta.get('body') or b''
            headers = meta.get('headers') or {}
            full_payload = meta.get('full_payload') or body
            cat, lbl, is_ticket = sniff_kind(body, url, headers, full_payload)
            size = len(body)
            name = _asset_name(body, url)
            item = ScanItem(time=now_hms(), hash=h, size=size, kind=f"{cat}{(' (' + lbl + ')' if lbl else '')}", src='inline' if content is not None else 'shard', url=url or '-', wrapped=bool(meta.get('wrapped', False)), header_text=meta.get('header_text'), content_type=_content_type(headers), is_ticket=is_ticket, name=name, id_bytes=id_b)
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


def _safe_number(value, default=0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default




def _cf_position(cf) -> Tuple[float, float, float]:
    if isinstance(cf, dict):
        if 'position' in cf:
            p = cf['position']
            if isinstance(p, (tuple, list)) and len(p) >= 3:
                try:
                    return (float(p[0]), float(p[1]), float(p[2]))
                except Exception:
                    pass
            return (0.0, 0.0, 0.0)
        if 'X' in cf and 'Y' in cf and ('Z' in cf):
            try:
                return (float(cf['X']), float(cf['Y']), float(cf['Z']))
            except Exception:
                return (0.0, 0.0, 0.0)
    if isinstance(cf, (tuple, list)) and len(cf) >= 3:
        try:
            return (float(cf[0]), float(cf[1]), float(cf[2]))
        except Exception:
            pass
    return (0.0, 0.0, 0.0)

def _extract_document_body(data: bytes) -> bytes:
    raw = data or b''
    if raw[:4] == RBXH_MAGIC:
        meta = parse_rbxh(raw)
        raw = meta.get('body') or b''
    pos = raw.find(RBXM_MAGIC)
    if pos >= 0:
        return raw[pos:]
    pos = raw.find(b'<roblox')
    if pos >= 0:
        return raw[pos:]
    return raw

def _copy_pose_properties(src, dst):
    sp = src.find('Properties') if src is not None else None
    if sp is None:
        return
    for tag in ('token', 'float'):
        for el in sp.findall(tag):
            if el.get('name') in ('EasingDirection', 'EasingStyle', 'Weight'):
                ET.SubElement(dst, tag, {'name': el.get('name')}).text = el.text

def _pose_cf(src):
    if src is None:
        return None
    sp = src.find('Properties')
    if sp is None:
        return None
    return sp.find("CoordinateFrame[@name='CFrame']")

def _make_r15_pose(name: str, source_pose=None) -> ET.Element:
    item = ET.Element('Item', {'class': 'Pose', 'referent': f'R15_{os.urandom(8).hex()}'})
    props = ET.SubElement(item, 'Properties')
    ET.SubElement(props, 'string', {'name': 'Name'}).text = name
    src_cf = _pose_cf(source_pose)
    c = ET.SubElement(props, 'CoordinateFrame', {'name': 'CFrame'})
    if src_cf is not None:
        for ch in src_cf:
            ET.SubElement(c, ch.tag).text = ch.text
    else:
        for tag, val in (('X', '0'), ('Y', '0'), ('Z', '0'), ('R00', '1'), ('R01', '0'), ('R02', '0'), ('R10', '0'), ('R11', '1'), ('R12', '0'), ('R20', '0'), ('R21', '0'), ('R22', '1')):
            ET.SubElement(c, tag).text = val
    _copy_pose_properties(source_pose, props)
    return item

def _normalize_roblox_document(data: bytes) -> bytes:
    raw = data or b''
    if raw[:4] == RBXH_MAGIC:
        raw = parse_rbxh(raw).get('body') or b''
    pos = raw.find(RBXM_MAGIC)
    if pos >= 0:
        raw = raw[pos:]
    else:
        pos = raw.find(b'<roblox')
        if pos >= 0:
            raw = raw[pos:]
    raw = raw.lstrip(b'\xef\xbb\xbf \t\r\n')
    if raw.startswith(RBXM_MAGIC):
        if _RbxmDeserializer is None:
            raise RuntimeError('RBXM deserializer is unavailable.')
        return write_rbxmx(_RbxmDeserializer().deserialize(raw))
    return raw
R6_TO_R15_POSE_MAP = {'Torso': 'UpperTorso', 'Left Arm': 'LeftUpperArm', 'Right Arm': 'RightUpperArm', 'Left Leg': 'LeftUpperLeg', 'Right Leg': 'RightUpperLeg', 'LeftArm': 'LeftUpperArm', 'RightArm': 'RightUpperArm', 'LeftLeg': 'LeftUpperLeg', 'RightLeg': 'RightUpperLeg', 'RootJoint': 'Root', 'Root': 'Root', 'HumanoidRootPart': 'HumanoidRootPart', 'Head': 'Head'}

def convert_r6_animation_to_r15(data: bytes) -> bytes:
    raw = _normalize_roblox_document(data)
    text = raw.decode('utf-8-sig', errors='replace')
    text = re.sub('[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]', '', text)
    root = ET.fromstring(text)
    keyframes = [x for x in root.iter('Item') if x.get('class') == 'Keyframe']
    if not keyframes:
        raise ValueError('No Keyframe data found in the selected animation.')
    for m in list(root):
        if m.tag == 'Meta' and m.get('name') == 'RoutilsR6ToR15':
            root.remove(m)

    def get_name(pose):
        props = pose.find('Properties')
        e = props.find("string[@name='Name']") if props is not None else None
        return (e.text or '').strip() if e is not None else ''

    def get_cf(pose):
        props = pose.find('Properties')
        e = props.find("CoordinateFrame[@name='CFrame']") if props is not None else None
        if e is None:
            return [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
        vals = []
        for tag in ('X', 'Y', 'Z', 'R00', 'R01', 'R02', 'R10', 'R11', 'R12', 'R20', 'R21', 'R22'):
            q = e.find(tag)
            vals.append(float(q.text) if q is not None and q.text else 1.0 if tag in ('R00', 'R11', 'R22') else 0.0)
        return vals

    def easing(pose):
        props = pose.find('Properties')
        out = ['0', '0', '1']
        if props is not None:
            a = props.find("token[@name='EasingDirection']")
            b = props.find("token[@name='EasingStyle']")
            w = props.find("float[@name='Weight']")
            if a is not None:
                out[0] = a.text or '0'
            if b is not None:
                out[1] = b.text or '0'
            if w is not None:
                out[2] = w.text or '1'
        return tuple(out)

    def make_pose(name, cf, ease):
        item = ET.Element('Item', {'class': 'Pose', 'referent': 'RBX' + uuid.uuid4().hex.upper()})
        props = ET.SubElement(item, 'Properties')
        ET.SubElement(props, 'string', {'name': 'Name'}).text = name
        ce = ET.SubElement(props, 'CoordinateFrame', {'name': 'CFrame'})
        for tag, val in zip(('X', 'Y', 'Z', 'R00', 'R01', 'R02', 'R10', 'R11', 'R12', 'R20', 'R21', 'R22'), cf):
            ET.SubElement(ce, tag).text = f'{val:.8g}'
        ET.SubElement(props, 'token', {'name': 'EasingDirection'}).text = ease[0]
        ET.SubElement(props, 'token', {'name': 'EasingStyle'}).text = ease[1]
        ET.SubElement(props, 'float', {'name': 'Weight'}).text = ease[2]
        return item

    def collect(kf):
        found = {}

        def walk(parent):
            for ch in parent.findall('Item'):
                if ch.get('class') == 'Pose':
                    found[get_name(ch)] = (get_cf(ch), easing(ch))
                    walk(ch)
        walk(kf)
        return found

    def r6_position_to_r15(cf):
        return [cf[0], cf[2], cf[1]] + cf[3:]
    identity = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
    for kf in keyframes:
        poses = collect(kf)
        extras = [c for c in list(kf) if c.get('class') != 'Pose']
        for c in list(kf):
            kf.remove(c)

        def p(name, source=None, transform_pos=False):
            if source and source in poses:
                cf, e = poses[source]
                if transform_pos:
                    cf = r6_position_to_r15(cf)
                return make_pose(name, cf, e)
            return make_pose(name, identity, ('0', '0', '1'))
        hrp = p('HumanoidRootPart', 'HumanoidRootPart')
        lower = p('LowerTorso', 'Torso', True)
        upper = p('UpperTorso')
        hrp.append(lower)
        lower.append(upper)
        upper.append(p('Head', 'Head', True))
        for side in ('Left', 'Right'):
            ua = p(f'{side}UpperArm', f'{side} Arm', True)
            la = p(f'{side}LowerArm')
            hand = p(f'{side}Hand')
            la.append(hand)
            ua.append(la)
            upper.append(ua)
            ul = p(f'{side}UpperLeg', f'{side} Leg', True)
            ll = p(f'{side}LowerLeg')
            foot = p(f'{side}Foot')
            ll.append(foot)
            ul.append(ll)
            lower.append(ul)
        kf.append(hrp)
        for c in extras:
            kf.append(c)
    try:
        ET.indent(root, space='\t')
    except Exception:
        pass
    return b'<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(root, encoding='utf-8')

def parse_model_parts(data: bytes) -> Tuple[List[Dict], str]:
    parts: List[Dict] = []
    try:
        raw = _decompress_document(data)
    except Exception:
        raw = data

    def _dict_pos(d):
        if isinstance(d, dict):
            try:
                return (float(d.get('X', 0)), float(d.get('Y', 0)), float(d.get('Z', 0)))
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
    if raw.lstrip().startswith(b'<roblox!'):
        if _RbxmDeserializer is not None:
            try:
                doc = _RbxmDeserializer().deserialize(raw)
                for inst in doc.instances.values():
                    if inst.class_name not in ('Part', 'MeshPart', 'WedgePart', 'CylinderPart', 'CornerWedgePart', 'TrussPart', 'BasePart'):
                        continue
                    props = {}
                    for k, v in inst.properties.items():
                        props[k.name if hasattr(k, 'name') else str(k)] = v.value if hasattr(v, 'value') else v
                    cf = None
                    for key in ('CFrame', 'Position'):
                        if key in props:
                            cf = props[key]
                            break
                    pos = _cf_pos(cf) if cf is not None else (0.0, 0.0, 0.0)
                    size = _dict_pos(props.get('Size', {'X': 1, 'Y': 1, 'Z': 1}))
                    color = '#58b6d6'
                    bc = props.get('Color', props.get('BrickColor'))
                    if isinstance(bc, dict):
                        if all((k in bc for k in ('R', 'G', 'B'))):
                            try:
                                color = '#%02x%02x%02x' % (int(bc['R'] * 255), int(bc['G'] * 255), int(bc['B'] * 255))
                            except Exception:
                                pass
                    parts.append({'name': props.get('Name') or inst.class_name, 'pos': pos, 'size': size, 'color': color})
            except Exception:
                parts = []
    else:
        try:
            text = raw.decode('utf-8-sig', errors='replace')
            text = re.sub('[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]', '', text)
            root = ET.fromstring(text)
        except Exception:
            root = None
        if root is not None:
            part_classes = {'Part', 'MeshPart', 'WedgePart', 'CylinderPart', 'CornerWedgePart', 'TrussPart', 'BasePart'}
            for item in root.iter('Item'):
                if item.attrib.get('class') not in part_classes:
                    continue
                props = item.find('Properties')
                if props is None:
                    continue
                size = (1.0, 1.0, 1.0)
                se = props.find("Vector3[@name='Size']")
                if se is not None:
                    xe = se.find('X')
                    ye = se.find('Y')
                    ze = se.find('Z')
                    size = (float(xe.text) if xe is not None and xe.text else 1.0, float(ye.text) if ye is not None and ye.text else 1.0, float(ze.text) if ze is not None and ze.text else 1.0)
                pos = (0.0, 0.0, 0.0)
                cfe = props.find("CoordinateFrame[@name='CFrame']")
                if cfe is not None:
                    xe = cfe.find('X')
                    ye = cfe.find('Y')
                    ze = cfe.find('Z')
                    pos = (float(xe.text) if xe is not None and xe.text else 0.0, float(ye.text) if ye is not None and ye.text else 0.0, float(ze.text) if ze is not None and ze.text else 0.0)
                name = ''
                ne = props.find("string[@name='Name']")
                if ne is not None:
                    name = ne.text or ''
                parts.append({'name': name or item.attrib.get('class'), 'pos': pos, 'size': size, 'color': '#58b6d6'})
    if not parts:
        return ([], 'Model present, but no parts found to render')
    return (parts, f'Model: {len(parts)} parts')

class Viewport3DPanel(ttk.Frame):

    def __init__(self, master, title='3D Viewport'):
        super().__init__(master)
        self.angle_x = 0.3
        self.angle_y = 0.5
        self.cam_distance = 7.0
        self.model_scale = 1.0
        self.mesh_vertices: List[Tuple[float, float, float]] = []
        self.mesh_faces: List[List[int]] = []
        self.mesh_info: str = ''
        self.model_parts: List[Dict] = []
        self.audio_path: Optional[str] = None
        self._last_mouse = (0, 0)
        self.show_wireframe = tk.BooleanVar(value=True)
        self.reduce_polys = tk.BooleanVar(value=True)
        self.is_own_host = False
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.zoom = 1.0
        self.header = ttk.Frame(self)
        self.header.pack(fill='x', padx=4, pady=2)
        ttk.Label(self.header, text='Preview', font=('Segoe UI Semibold', 9)).pack(side='left')
        self.btn_close = ttk.Button(self.header, text='✕', width=3, command=self.hide)
        self.btn_close.pack(side='right')
        self.canvas = tk.Canvas(self, bg='#18181a', highlightthickness=0, height=220)
        self.canvas.pack(fill='both', expand=True, padx=4, pady=2)
        self.controls = ttk.Frame(self)
        self.controls.pack(fill='x', padx=4, pady=4)
        self.lbl_mode = ttk.Label(self.controls, text='Mode: Idle')
        self.lbl_mode.pack(side='left', padx=6)
        ttk.Checkbutton(self.controls, text='Wireframe lines', variable=self.show_wireframe, command=self.draw_frame).pack(side='left', padx=6)
        ttk.Checkbutton(self.controls, text='Optimize >500 vertices', variable=self.reduce_polys, command=self.draw_frame).pack(side='left', padx=6)
        self.canvas.bind('<Button-1>', self._on_mouse_down)
        self.canvas.bind('<B1-Motion>', self._on_mouse_drag)
        self.canvas.bind('<MouseWheel>', self._on_mouse_wheel)
        self.canvas.bind('<Button-4>', lambda e: self._zoom_by(1.15))
        self.canvas.bind('<Button-5>', lambda e: self._zoom_by(0.85))
        self.bind('<KeyPress>', self._on_key_press)
        self.bind('<KeyRelease>', self._on_key_release)
        self.canvas.bind('<KeyPress>', self._on_key_press)
        self.canvas.bind('<KeyRelease>', self._on_key_release)
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
        if 'w' in self._keys_held:
            self.pan_y += step
        if 's' in self._keys_held:
            self.pan_y -= step
        if 'a' in self._keys_held:
            self.pan_x += step
        if 'd' in self._keys_held:
            self.pan_x -= step
        self.draw_frame()

    def set_asset_data_from_temp(self, temp_file_path: str, is_mesh=False, is_model=False, is_audio=False):
        self.mesh_vertices = []
        self.mesh_faces = []
        self.mesh_info = ''
        self.model_parts = []
        self.audio_path = None
        try:
            with open(temp_file_path, 'rb') as f:
                data = f.read()
        except Exception:
            data = b''
        try:
            data = _decompress_document(data)
        except Exception:
            pass
        if is_mesh:
            self._load_mesh(data)
        elif is_model:
            self._load_model(data)
        elif is_audio:
            self._load_audio(data)
        else:
            self.mesh_info = 'No preview for this asset type'
        self.draw_frame()

    def _load_audio(self, data: bytes) -> None:
        ext = ''
        fmt, off = find_embedded_audio_robust(data)
        if fmt and off != -1:
            payload = data[off:]
            ext = {'WAV': 'wav', 'OGG': 'ogg', 'MP3': 'mp3'}.get(fmt, 'bin')
        elif data.startswith(b'ID3') or (len(data) > 2 and data[:3] in (b'\xff\xfb', b'\xff\xf3', b'\xff\xf2')):
            fmt, payload, ext = ('MP3', data, 'mp3')
        elif data.startswith(b'OggS'):
            fmt, payload, ext = ('OGG', data, 'ogg')
        else:
            self.mesh_info = 'Audio present, but no playable stream was found'
            return
        import tempfile as _tf
        self.audio_path = os.path.join(_tf.gettempdir(), f'rdbm_preview_{abs(hash(payload)):x}.{ext}')
        try:
            with open(self.audio_path, 'wb') as f:
                f.write(payload)
        except Exception as e:
            self.audio_path = None
            self.mesh_info = f'Audio present, but could not write temp file ({e})'
            return
        try:
            from datetime import datetime
            stamp = datetime.now().strftime('%H:%M:%S')
        except Exception:
            stamp = ''
        self.mesh_info = f'Audio: {fmt} · {len(payload):,} bytes · {stamp} (▶ plays via system)'

    def _toggle_audio_play(self):
        if not self.audio_path or not os.path.isfile(self.audio_path):
            return
        try:
            os.startfile(self.audio_path)
        except Exception as e:
            messagebox.showerror('Audio', f'Could not open audio:\n{e}')

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
        if not obj and (not data.lstrip().startswith(b'version ')):
            idx = data.find(b'version ')
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
            if parts[0] == 'v':
                try:
                    verts.append((float(parts[1]), float(parts[2]), float(parts[3])))
                except (ValueError, IndexError):
                    pass
            elif parts[0] == 'f':
                idx = []
                for p in parts[1:]:
                    try:
                        idx.append(int(p.split('/')[0]) - 1)
                    except (ValueError, IndexError):
                        pass
                if len(idx) >= 3:
                    faces.append(idx)
        self.mesh_vertices = verts
        self.mesh_faces = faces
        self.mesh_info = f'Vertices: {len(verts):,} · Faces: {len(faces):,}'

    def show(self, is_anim=True, mode_label='Mesh'):
        self.lbl_mode.config(text=f'Mode: {mode_label}')
        if self.is_own_host:
            self.pack(fill='both', expand=True)
        else:
            self.pack(fill='x', padx=8, pady=4)
        self.canvas.focus_set()
        self.draw_frame()

    def hide(self):
        self.pack_forget()


    def _on_mouse_down(self, event):
        self._last_mouse = (event.x, event.y)

    def _on_mouse_drag(self, event):
        dx = event.x - self._last_mouse[0]
        dy = event.y - self._last_mouse[1]
        self.angle_y += dx * 0.01
        self.angle_x += dy * 0.01
        self._last_mouse = (event.x, event.y)
        self.draw_frame()


    def draw_frame(self):
        self.canvas.delete('all')
        w = self.canvas.winfo_width() or 300
        h = self.canvas.winfo_height() or 220
        if self.mesh_vertices and self.mesh_faces:
            self._draw_mesh(w, h)
            if self.mesh_info:
                self.canvas.create_text(8, 8, text=self.mesh_info, anchor='nw', fill='#8ad0ff', font=('Consolas', 8))
            return
        if self.model_parts:
            self._draw_model(w, h)
            if self.mesh_info:
                self.canvas.create_text(8, 8, text=self.mesh_info, anchor='nw', fill='#8ad0ff', font=('Consolas', 8))
            return
        if self.audio_path and self.mesh_info:
            self.canvas.create_text(w / 2, h / 2, text=self.mesh_info, fill='#8ad0ff', font=('Segoe UI', 10))
            self.canvas.create_text(w / 2, h / 2 + 26, text='Press ▶ to play via your system audio player', fill='#c8c8c8', font=('Segoe UI', 9))
        else:
            self.canvas.create_text(w / 2, h / 2, text='No preview available for this asset', fill='#007acc', font=('Segoe UI', 10))
    BONES = [('Head', 'UpperTorso'), ('Head', 'Torso'), ('UpperTorso', 'LowerTorso'), ('Torso', 'LowerTorso'), ('LowerTorso', 'UpperTorso'), ('UpperTorso', 'UpperArm'), ('UpperArm', 'LowerArm'), ('LowerArm', 'Hand'), ('UpperTorso', 'LeftUpperArm'), ('LeftUpperArm', 'LeftLowerArm'), ('LeftLowerArm', 'LeftHand'), ('UpperTorso', 'RightUpperArm'), ('RightUpperArm', 'RightLowerArm'), ('RightLowerArm', 'RightHand'), ('UpperArm', 'LeftUpperArm'), ('UpperArm', 'RightUpperArm'), ('LowerTorso', 'UpperLeg'), ('UpperLeg', 'LowerLeg'), ('LowerLeg', 'Foot'), ('LowerTorso', 'LeftUpperLeg'), ('LeftUpperLeg', 'LeftLowerLeg'), ('LeftLowerLeg', 'LeftFoot'), ('LowerTorso', 'RightUpperLeg'), ('RightUpperLeg', 'RightLowerLeg'), ('RightLowerLeg', 'RightFoot'), ('UpperLeg', 'LeftUpperLeg'), ('UpperLeg', 'RightUpperLeg')]

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
        ax, ay = (self.angle_x, self.angle_y)
        cx, cy = (w / 2 + self.pan_x, h / 2 + self.pan_y)
        base = max(40.0, min(w, h) / 3) * self.zoom
        all_pos = [p['pos'] for p in self.model_parts]
        mins = [min((v[i] for v in all_pos)) for i in range(3)]
        maxs = [max((v[i] for v in all_pos)) for i in range(3)]
        spans = [float(maxs[i] - mins[i]) for i in range(3)]
        span_all = max(max(spans), 1e-06)
        scale = base / span_all
        mid = [(mins[i] + maxs[i]) / 2 for i in range(3)]
        cosx, sinx, cosy, siny = (math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay))

        def _proj(x, y, z):
            px, py, pz = (x - mid[0], y - mid[1], z - mid[2])
            x1 = px * cosy + pz * siny
            z1 = -px * siny + pz * cosy
            y2 = py * cosx - z1 * sinx
            z2 = py * sinx + z1 * cosx
            return (cx + x1 * scale, cy - y2 * scale, z2)
        corners = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]
        faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)]
        items = []
        for part in self.model_parts:
            pos = part['pos']
            sx, sy, sz = part['size']
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
                depth_pts.append((zd / len(face), coords, part['color']))
            items.extend(depth_pts)
        for depth, coords, color in sorted(items, key=lambda t: t[0], reverse=True):
            flat = [c for pt in coords for c in pt]
            if self.show_wireframe.get():
                self.canvas.create_polygon(flat, fill=color, outline='#9aa0a6', width=1)
            else:
                self.canvas.create_polygon(flat, fill=color, outline='')
        try:
            ymin = mins[1] - (maxs[1] - mins[1]) * 0.1
            shadow_pts = []
            for part in self.model_parts:
                pos = part['pos']
                sx = (part['size'][0] or 1.0) * 0.5
                sz = (part['size'][2] or 1.0) * 0.5
                shadow_pts.append((pos[0] - sx, ymin, pos[2] - sz))
                shadow_pts.append((pos[0] + sx, ymin, pos[2] - sz))
                shadow_pts.append((pos[0] + sx, ymin, pos[2] + sz))
                shadow_pts.append((pos[0] - sx, ymin, pos[2] + sz))
            s_xy = [_proj(x, y, z)[:2] for x, y, z in shadow_pts]
            flat_s = [c for pt in s_xy for c in pt]
            self.canvas.create_polygon(flat_s, fill='#000000', outline='', stipple='gray12')
        except Exception:
            pass


    def _draw_mesh(self, w, h):
        verts = self.mesh_vertices
        if not verts:
            return
        ax, ay = (self.angle_x, self.angle_y)
        cx, cy = (w / 2 + self.pan_x, h / 2 + self.pan_y)
        base = max(20.0, min(w, h) / 4) * self.zoom
        xs = [v[0] for v in verts]
        ys = [v[1] for v in verts]
        zs = [v[2] for v in verts]
        mx, my, mz = ((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, (max(zs) + min(zs)) / 2)
        span = max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs), 1e-06)
        scale = base / span
        cosx, sinx, cosy, siny = (math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay))
        pts2d, pts3d = ([], [])
        for x, y, z in verts:
            px, py, pz = (x - mx, y - my, z - mz)
            x1 = px * cosy + pz * siny
            z1 = -px * siny + pz * cosy
            y2 = py * cosx - z1 * sinx
            z2 = py * sinx + z1 * cosx
            pts2d.append((cx + x1 * scale, cy - y2 * scale))
            pts3d.append(z2)
        shadow_poly = []
        for x, y, z in verts:
            px, py, pz = (x - mx, 0.0 - my, z - mz)
            x1 = px * cosy + pz * siny
            z1 = -px * siny + pz * cosy
            y2 = 0.0 * cosx - z1 * sinx
            shadow_poly.append((cx + x1 * scale, cy - y2 * scale))
        items = []
        faces = self.mesh_faces
        if self.reduce_polys.get() and len(verts) > 500 and (len(faces) > 128):
            stride = max(1, (len(faces) + 127) // 128)
            faces = faces[::stride]
        for face in faces:
            coords = [c for i in face for c in pts2d[i % len(pts2d)]]
            depth = sum((pts3d[i % len(pts3d)] for i in face)) / len(face)
            items.append((depth, coords))
        try:
            self.canvas.create_polygon(shadow_poly, fill='#000000', outline='', stipple='gray12')
        except Exception:
            pass
        for depth, coords in sorted(items, key=lambda t: t[0], reverse=True):
            if self.show_wireframe.get():
                self.canvas.create_polygon(coords, fill='#2a2d31', outline='#9aa0a6', width=1)
            else:
                shade = 90 - max(0, min(45, int(-depth * 12)))
                shade = max(35, min(150, shade))
                fill = '#%02x%02x%02x' % (shade, shade + 8, shade + 18)
                self.canvas.create_polygon(coords, fill=fill, outline='')

class ReplacerPane(ttk.Frame):

    def _console_log(self, message):
        try:
            root = self.winfo_toplevel()
            logger = getattr(root, '_console_log', None)
            if callable(logger):
                logger(message)
        except Exception:
            pass

    def __init__(self, master):
        super().__init__(master)
        self.script_dir = DATA_DIR
        self.preinstalled_dir = os.path.join(self.script_dir, 'caches', 'preinstalled')
        self.own_dir = os.path.join(self.script_dir, 'caches', 'Own')
        self.hash_saves_dir = os.path.join(self.script_dir, 'hashsaves')
        self.file_saves_dir = os.path.join(self.script_dir, 'filesaves')
        for path in (self.preinstalled_dir, self.own_dir, self.hash_saves_dir, self.file_saves_dir):
            os.makedirs(path, exist_ok=True)
        self.container = ttk.Frame(self)
        self.container.pack(fill='both', expand=True, padx=8, pady=(7, 6))
        self.top = ttk.Frame(self.container)
        self.top.pack(fill='x', pady=(0, 2))
        self.action_bar = ttk.Frame(self.top)
        self.action_bar.pack(side='left', padx=(4, 8))
        self.source_row = ttk.Frame(self.container)
        self.source_row.pack(fill='x', pady=(0, 6))
        ttk.Label(self.source_row, text='Source:').pack(side='left')
        self.source_var = tk.StringVar(value='Caches')
        for val in ('Caches', 'HashSaves', 'FileSaves'):
            ttk.Radiobutton(self.source_row, text=val, variable=self.source_var, value=val, command=self.refresh_view).pack(side='left', padx=5)
        self.search_row = ttk.Frame(self.container)
        self.search_row.pack(fill='x', pady=(0, 4))
        ttk.Label(self.search_row, text='Filter:').pack(side='left')
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_row, textvariable=self.search_var)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(4, 0))
        self.search_entry.bind('<KeyRelease>', lambda e: self.refresh_view(True))
        self.btn_create = ttk.Button(self.action_bar, text='Create Cache', command=self.create_cache, width=13)
        self.btn_applycache = ttk.Button(self.action_bar, text='Apply', command=self.apply_caches, width=13)
        self.btn_savehash = ttk.Button(self.action_bar, text='Save Hash', command=self.save_hash, width=13)
        self.btn_savefile = ttk.Button(self.action_bar, text='Save File', command=self.save_file, width=13)
        self.list_frame = ttk.Frame(self.container, borderwidth=1, relief='solid')
        self.list_frame.pack(fill='both', expand=True)
        self.item_list = tk.Listbox(self.list_frame, selectbackground='#007acc', selectforeground='#ffffff', selectmode=tk.EXTENDED, exportselection=False, activestyle='none', bg='#252526', fg='#d4d4d4')
        self.item_list.pack(side='left', fill='both', expand=True, pady=5, padx=5)
        scroll = ttk.Scrollbar(self.list_frame, orient='vertical', command=self.item_list.yview)
        scroll.pack(side='right', fill='y')
        self.item_list.config(yscrollcommand=scroll.set)
        self.indent_px = tkfont.nametofont(self.item_list.cget('font')).measure('   ')
        self.view_index = []
        self.group_states = {}
        self.drag_start_x = None
        self.drag_start_y = None
        self.dragging = False
        self.drag_label = None
        self.hover_index = None
        self.item_list.bind('<Motion>', self._on_hover_move)
        self.item_list.bind('<Leave>', self._on_hover_leave)
        self.ctx_menu = tk.Menu(self, tearoff=0)
        darken_menus((self.ctx_menu,))
        self.item_list.bind('<Button-3>', self._on_context_request)
        self.item_list.bind('<Button-2>', self._on_context_request)
        self.item_list.bind('<Double-1>', self._on_double_click)
        self.item_list.bind('<Button-1>', self._on_press)
        self.item_list.bind('<B1-Motion>', self._on_drag_motion)
        self.item_list.bind('<ButtonRelease-1>', self._on_drag_release)
        for widget in (self, self.container, self.top, self.action_bar, self.source_row, self.list_frame):
            widget.bind('<Button-1>', self._clear_selection_bg, add='+')
        self.refresh_view()

    def _obj_key(self, obj):
        k = obj.get('kind')
        if k == 'item':
            return ('item', obj['display'])
        if k == 'group':
            return ('group', obj['path'])
        if k == 'group_item':
            return ('group_item', obj['group_path'], obj['filename'])
        if k == 'hash':
            return ('hash', obj['path'])
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
        indent = row.get('indent', 0)
        start = indent * self.indent_px
        return start <= event.x <= start + 20

    def _clear_hover(self):
        if self.hover_index is not None:
            try:
                self.item_list.itemconfig(self.hover_index, background='')
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
                self.item_list.itemconfig(idx, background='#333333')
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
        self.drag_start_x, self.drag_start_y = (event.x, event.y)
        self.dragging = False
        return self._on_left_click(event)

    def _on_left_click(self, event):
        idx = self._row_index_from_event(event)
        if idx is None:
            self.item_list.selection_clear(0, tk.END)
            return 'break'
        row = self.view_index[idx]
        if row.get('kind') == 'group' and self._is_over_arrow(event, row):
            sel_keys = self._snapshot_selection()
            path = row['path']
            self.group_states[path] = not self.group_states.get(path, False)
            self.after_idle(lambda: self.refresh_view(True, sel_keys))
            return 'break'

    def _on_drag_motion(self, event):
        if self.drag_start_x is None or self.drag_start_y is None:
            return 'break'
        if not self.dragging:
            dx = abs(event.x - self.drag_start_x)
            dy = abs(event.y - self.drag_start_y)
            if dx > 4 or dy > 4:
                sel_objs = self._get_selected_objs()
                if not sel_objs:
                    return 'break'
                text = sel_objs[0].get('display') or sel_objs[0].get('name')
                if len(sel_objs) > 1:
                    text += f' (+{len(sel_objs) - 1})'
                self.drag_label = tk.Toplevel(self)
                self.drag_label.overrideredirect(True)
                theme_toplevel(self.drag_label)
                ttk.Label(self.drag_label, text=text, relief='solid', borderwidth=1).pack()
                self.dragging = True
        if self.dragging and self.drag_label:
            self.drag_label.geometry(f'+{event.x_root + 15}+{event.y_root + 15}')
        return 'break'

    def _base_dir_for_view(self, view=None):
        v = view or self.source_var.get()
        if v == 'HashSaves':
            return self.hash_saves_dir
        if v == 'FileSaves':
            return self.file_saves_dir
        return self.own_dir

    def _move_selection_to(self, target_dir):
        objs = self._get_selected_objs()
        base_dir = self._base_dir_for_view()
        for o in objs:
            if o['kind'] == 'group':
                src = o['path']
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
            elif o['kind'] == 'group_item':
                src = os.path.join(o['group_path'], o['filename'])
                dest = target_dir or base_dir
                try:
                    shutil.move(src, os.path.join(dest, os.path.basename(src)))
                except Exception:
                    try:
                        shutil.copy2(src, os.path.join(dest, os.path.basename(src)))
                        os.remove(src)
                    except Exception:
                        pass
            elif o['kind'] in ('hash',):
                src = o['path']
                dest = target_dir or base_dir
                try:
                    shutil.move(src, os.path.join(dest, os.path.basename(src)))
                except Exception:
                    try:
                        shutil.copy2(src, os.path.join(dest, os.path.basename(src)))
                        os.remove(src)
                    except Exception:
                        pass
            elif o['kind'] == 'item':
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
            return 'break'
        idx = self._row_index_from_event(event)
        target_dir = None
        if idx is not None:
            target_obj = self.view_index[idx]
            k = target_obj.get('kind')
            if k == 'group':
                target_dir = target_obj['path']
            elif k == 'group_item':
                target_dir = target_obj['group_path']
            elif k in ('hash',):
                target_dir = os.path.dirname(target_obj['path'])
        self._move_selection_to(target_dir)
        self.dragging = False
        self.refresh_view()
        return 'break'

    def _on_double_click(self, event):
        idx = self._row_index_from_event(event)
        if idx is None:
            self.item_list.selection_clear(0, tk.END)
            return 'break'
        row = self.view_index[idx]
        if row.get('kind') == 'group' and self._is_over_arrow(event, row):
            sel_keys = self._snapshot_selection()
            path = row['path']
            self.group_states[path] = not self.group_states.get(path, False)
            self.after_idle(lambda: self.refresh_view(True, sel_keys))
        return 'break'

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
        self.ctx_menu.delete(0, 'end')
        delete_state = 'normal'
        if not selected_objs or (clicked_obj and clicked_obj.get('kind') == 'group'):
            delete_state = 'disabled'
        self.ctx_menu.add_command(label='Delete', command=self.delete_selected, state=delete_state)
        rename_state = 'normal' if len(selected_objs) == 1 and selected_objs[0]['kind'] in ('item', 'hash', 'group_item', 'group') else 'disabled'
        self.ctx_menu.add_command(label='Rename', command=self.rename_selected, state=rename_state)
        self.ctx_menu.add_separator()
        self.ctx_menu.add_command(label='Create group', command=self.create_group_from_selection)
        if clicked_obj and clicked_obj.get('kind') == 'group':
            self.ctx_menu.add_separator()
            self.ctx_menu.add_command(label='Delete group', command=self.delete_selected_groups)
            self.ctx_menu.add_command(label='Ungroup', command=self.ungroup_selected_groups)
        try:
            self.ctx_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.ctx_menu.grab_release()

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
        if view == 'HashSaves':
            self.btn_savehash.pack(side='left', padx=(0, 6), pady=0)
        elif view == 'FileSaves':
            self.btn_applycache.pack(side='left', padx=(0, 6), pady=0)
            self.btn_savefile.pack(side='left', padx=(0, 6), pady=0)
        else:
            self.btn_create.pack(side='left', padx=(0, 6), pady=0)
            self.btn_applycache.pack(side='left', padx=(0, 6), pady=0)

    def _sanitize_filename(self, s: str) -> str:
        illegal = '<>:"/\\|?*'
        cleaned = ''.join(('_' if c in illegal else c for c in s))
        return cleaned.rstrip(' .')

    def _swap_hash_display(self, filename: str) -> str:
        parts = filename.split(' - ', 1)
        if len(parts) == 2:
            h, n = (parts[0], parts[1])
            return f'{n} ({h})'
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
        indent_str = '   ' * indent
        for d in dirs:
            path = os.path.join(current, d)
            expanded = self.group_states.get(path, False)
            arrow = '▼ ' if expanded else '▶ '
            line = f'{indent_str}{arrow}{d}'
            if not self._passes_search(line):
                continue
            self.item_list.insert(tk.END, line)
            self.view_index.append({'kind': 'group', 'name': d, 'path': path, 'indent': indent})
            if expanded:
                self._render_saves_tree(base_dir, display_fn, path, indent + 1)
        for f in files:
            disp = display_fn(f)
            path = os.path.join(current, f)
            if not self._passes_search(disp):
                continue
            self.item_list.insert(tk.END, f'{indent_str}{disp}')
            if current == base_dir:
                self.view_index.append({'kind': 'hash', 'name': disp, 'path': path, 'realname': f, 'indent': indent})
            else:
                self.view_index.append({'kind': 'group_item', 'display': disp, 'group_path': current, 'filename': f, 'indent': indent})

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
            elif os.path.isfile(p) and ' - ' in name:
                files.append(name)
        dirs.sort(key=lambda s: s.lower())
        files.sort(key=lambda s: s.lower())
        indent_str = '   ' * indent
        for d in dirs:
            path = os.path.join(current_dir, d)
            expanded = self.group_states.get(path, False)
            arrow = '▼ ' if expanded else '▶ '
            line = f'{indent_str}{arrow}{d}'
            if not self._passes_search(line):
                continue
            self.item_list.insert(tk.END, line)
            self.view_index.append({'kind': 'group', 'name': d, 'path': path, 'indent': indent})
            if expanded:
                self._render_cache_tree(path, indent + 1)
        for f in files:
            disp = f.split(' - ', 1)[1]
            if not self._passes_search(disp):
                continue
            self.item_list.insert(tk.END, f'{indent_str}{disp}')
            if indent == 0:
                self.view_index.append({'kind': 'item', 'display': disp, 'indent': indent})
            else:
                self.view_index.append({'kind': 'group_item', 'display': disp, 'group_path': current_dir, 'filename': f, 'indent': indent})
        if indent == 0:
            return {f.split(' - ', 1)[1] for f in files}

    def refresh_view(self, preserve_selection=False, selection_keys=None):
        if preserve_selection and selection_keys is None:
            selection_keys = self._snapshot_selection()
        self._clear_hover()
        self.item_list.delete(0, tk.END)
        self.view_index = []
        view = self.source_var.get()
        if view == 'HashSaves':
            self._render_saves_tree(self.hash_saves_dir, self._swap_hash_display)
        elif view == 'FileSaves':
            self._render_saves_tree(self.file_saves_dir, lambda s: s)
        else:
            shown = self._render_cache_tree(self.own_dir)
            seen = shown or set()
            if os.path.isdir(self.preinstalled_dir):
                for fname in os.listdir(self.preinstalled_dir):
                    p = os.path.join(self.preinstalled_dir, fname)
                    if os.path.isfile(p) and ' - ' in fname:
                        disp = fname.split(' - ', 1)[1]
                        if disp in seen:
                            continue
                        if not self._passes_search(disp):
                            continue
                        self.item_list.insert(tk.END, disp)
                        self.view_index.append({'kind': 'item', 'display': disp})
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
                if ' - ' not in f:
                    continue
                h, name = f.split(' - ', 1)
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
        dialog.title('Create Cache')
        dialog.transient(self)
        theme_toplevel(dialog)
        body = ttk.Frame(dialog, padding=0)
        body.pack(fill='both', expand=True)
        body.columnconfigure(1, weight=1)
        ttk.Label(body, text='Hash saves:').grid(row=0, column=0, sticky='w', padx=10, pady=(12, 4))
        hs = self._scan_hash_saves()
        hash_names = [name for name, _h, _p in hs]
        hash_combo = ttk.Combobox(body, values=hash_names, state='readonly', width=38)
        hash_combo.grid(row=0, column=1, sticky='we', padx=10, pady=(12, 4))
        if hash_names:
            hash_combo.current(0)
        chosen_hash = {'hex': None}

        def ask_custom_hash():
            ch = simpledialog.askstring('Custom Hash', 'Enter custom hash value (hex):', parent=dialog)
            if ch and ch.strip():
                chosen_hash['hex'] = re.sub('[^0-9A-Fa-f]', '', ch.strip())
                messagebox.showinfo('Info', f"Using custom hash: {chosen_hash['hex']}", parent=dialog)
            elif ch is not None:
                chosen_hash['hex'] = None
        ttk.Button(body, text='Input Custom Hash', command=ask_custom_hash).grid(row=0, column=2, padx=10, pady=(12, 4))
        ttk.Label(body, text='File saves:').grid(row=1, column=0, sticky='w', padx=10, pady=4)
        fs = self._scan_file_saves()
        file_names = [name for name, _p in fs]
        file_combo = ttk.Combobox(body, values=file_names, state='readonly', width=38)
        file_combo.grid(row=1, column=1, sticky='we', padx=10, pady=4)
        if file_names:
            file_combo.current(0)
        chosen_file = {'path': None}

        def pick_custom_file():
            p = filedialog.askopenfilename(title='Choose source file')
            if p:
                chosen_file['path'] = p
                messagebox.showinfo('Info', f'Selected file:\n{p}', parent=dialog)
        ttk.Button(body, text='Input Custom File', command=pick_custom_file).grid(row=1, column=2, padx=10, pady=4)
        ttk.Label(body, text='Enter display name:').grid(row=2, column=0, sticky='w', padx=10, pady=(8, 4))
        entry_name = ttk.Entry(body, width=40)
        entry_name.grid(row=2, column=1, columnspan=2, sticky='we', padx=10, pady=(8, 4))
        btnf = ttk.Frame(body)
        btnf.grid(row=3, column=0, columnspan=3, pady=12)

        def on_ok():
            final_hash = chosen_hash['hex']
            if not final_hash:
                sel = hash_combo.get()
                if sel:
                    for name, h, _p in hs:
                        if name == sel:
                            final_hash = h
                            break
            if not final_hash:
                messagebox.showerror('Create Cache', 'Please choose a hash (or input a custom one).', parent=dialog)
                return
            final_hash = re.sub('[^0-9A-Fa-f]', '', final_hash)
            if len(final_hash) == 0:
                messagebox.showerror('Create Cache', 'Invalid hash.', parent=dialog)
                return
            src_path = chosen_file['path']
            if not src_path:
                selfn = file_combo.get()
                if selfn:
                    for name, p in fs:
                        if name == selfn:
                            src_path = p
                            break
            if not src_path:
                messagebox.showerror('Create Cache', 'Please choose a file (or input a custom one).', parent=dialog)
                return
            if not os.path.isfile(src_path):
                messagebox.showerror('Create Cache', 'Selected file is missing.', parent=dialog)
                return
            disp = entry_name.get().strip()
            if not disp:
                messagebox.showerror('Create Cache', 'Display name is required.', parent=dialog)
                return
            safe_disp = self._sanitize_filename(disp)
            source_ext = os.path.splitext(src_path)[1].lower()
            is_roblox_model = source_ext in ('.rbxm', '.rbxmx')
            if is_roblox_model and (not safe_disp.lower().endswith('.rbxh')):
                safe_disp = os.path.splitext(safe_disp)[0] + '.rbxh'
            dest_name = f'{final_hash} - {safe_disp}'
            dest_path = os.path.join(self.own_dir, dest_name)
            if os.path.exists(dest_path):
                base = dest_name
                i = 1
                while True:
                    cand = f'{base} ({i})'
                    cand_path = os.path.join(self.own_dir, cand)
                    if not os.path.exists(cand_path):
                        dest_path = cand_path
                        break
                    i += 1
            try:
                if is_roblox_model:
                    with open(src_path, 'rb') as f:
                        source_bytes = f.read()
                    template = b''
                    sibling = os.path.splitext(src_path)[0] + '.rbxh'
                    if os.path.isfile(sibling):
                        with open(sibling, 'rb') as f:
                            template = f.read()
                    converted = convert_roblox_file(source_bytes, source_ext, '.rbxh', template)
                    with open(dest_path, 'wb') as f:
                        f.write(converted)
                else:
                    shutil.copy2(src_path, dest_path)
            except Exception as e:
                messagebox.showerror('Create Cache', f'Failed to create cache:\n{e}', parent=dialog)
                return
            dialog.destroy()
            self.refresh_view()
            messagebox.showinfo('Success', f'Created cache:\n{os.path.basename(dest_path)}', parent=self)
            self._console_log(f'Created cache: {os.path.basename(dest_path)}')
        ttk.Button(btnf, text='OK', command=on_ok).pack(side='left', padx=6)
        ttk.Button(btnf, text='Cancel', command=dialog.destroy).pack(side='left', padx=6)
        body.columnconfigure(1, weight=1)
        entry_name.focus_set()

    def save_hash(self):
        dialog = tk.Toplevel(self)
        dialog.title('Save Hash')
        dialog.transient(self)
        theme_toplevel(dialog)
        ttk.Label(dialog, text='Hash:').grid(row=0, column=0, padx=10, pady=(12, 4), sticky='w')
        entry_hash = ttk.Entry(dialog, width=40)
        entry_hash.grid(row=0, column=1, padx=10, pady=(12, 4), sticky='we')
        ttk.Label(dialog, text='Name:').grid(row=1, column=0, padx=10, pady=4, sticky='w')
        entry_name = ttk.Entry(dialog, width=40)
        entry_name.grid(row=1, column=1, padx=10, pady=4, sticky='we')
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=12)
        dialog.columnconfigure(1, weight=1)

        def on_ok():
            hv = entry_hash.get().strip()
            nv = entry_name.get().strip()
            if not hv or not nv:
                messagebox.showerror('Error', 'Both Hash and Name are required.', parent=dialog)
                return
            filename = ' - '.join([re.sub('[^0-9A-Fa-f]', '', hv), nv])
            safe_filename = self._sanitize_filename(filename)
            if not safe_filename:
                messagebox.showerror('Error', 'Resulting file name is empty after sanitization.', parent=dialog)
                return
            base_dir = self.hash_saves_dir
            dest = os.path.join(base_dir, safe_filename)
            if os.path.exists(dest):
                base = safe_filename
                i = 1
                while True:
                    cand = f'{base} ({i})'
                    dest2 = os.path.join(base_dir, cand)
                    if not os.path.exists(dest2):
                        dest = dest2
                        break
                    i += 1
            try:
                with open(dest, 'x'):
                    pass
            except FileExistsError:
                with open(dest, 'wb'):
                    pass
            except Exception as e:
                messagebox.showerror('Error', f'Failed to save: {e}', parent=dialog)
                return
            dialog.destroy()
            self.refresh_view()
            messagebox.showinfo('Success', f"Saved '{os.path.basename(dest)}'.")
            self._console_log(f'Saved hash file: {os.path.basename(dest)}')
        ttk.Button(btn_frame, text='OK', command=on_ok).pack(side='left', padx=6)
        ttk.Button(btn_frame, text='Cancel', command=dialog.destroy).pack(side='left', padx=6)
        entry_hash.focus_set()

    def save_file(self):
        dialog = tk.Toplevel(self)
        dialog.title('Save File')
        dialog.transient(self)
        theme_toplevel(dialog)
        chosen = {'path': None}

        def pick_file():
            p = filedialog.askopenfilename(title='Choose file to save')
            if p:
                chosen['path'] = p
                lbl_file.config(text=p)
        ttk.Label(dialog, text='File:').grid(row=0, column=0, padx=10, pady=(12, 4), sticky='w')
        btn_pick = ttk.Button(dialog, text='Browse…', command=pick_file)
        btn_pick.grid(row=0, column=1, padx=10, pady=(12, 4), sticky='w')
        lbl_file = ttk.Label(dialog, text='No file selected')
        lbl_file.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 8), sticky='w')
        ttk.Label(dialog, text='Name:').grid(row=2, column=0, padx=10, pady=4, sticky='w')
        entry_name = ttk.Entry(dialog, width=40)
        entry_name.grid(row=2, column=1, padx=10, pady=4, sticky='we')
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=12)
        dialog.columnconfigure(1, weight=1)

        def on_ok():
            src = chosen['path']
            name = entry_name.get().strip()
            if not src:
                messagebox.showerror('Error', 'Please choose a file.', parent=dialog)
                return
            if not name:
                messagebox.showerror('Error', 'Please enter a Name.', parent=dialog)
                return
            safe_name = self._sanitize_filename(name)
            if not safe_name:
                messagebox.showerror('Error', 'Resulting file name is empty after sanitization.', parent=dialog)
                return
            is_roblox_model = os.path.splitext(src)[1].lower() in ('.rbxm', '.rbxmx')
            if is_roblox_model:
                safe_name = os.path.splitext(safe_name)[0] + '.rbxh'
            dest = os.path.join(self.file_saves_dir, safe_name)
            if os.path.exists(dest):
                base = safe_name
                i = 1
                while True:
                    cand = f'{base} ({i})'
                    dest2 = os.path.join(self.file_saves_dir, cand)
                    if not os.path.exists(dest2):
                        dest = dest2
                        break
                    i += 1
            try:
                if is_roblox_model:
                    with open(src, 'rb') as f:
                        source_bytes = f.read()
                    template = b''
                    sibling = os.path.splitext(src)[0] + '.rbxh'
                    if os.path.isfile(sibling):
                        with open(sibling, 'rb') as f:
                            template = f.read()
                    blob = convert_roblox_file(source_bytes, os.path.splitext(src)[1], '.rbxh', template)
                    with open(dest, 'wb') as f:
                        f.write(blob)
                else:
                    shutil.copy2(src, dest)
            except Exception as e:
                messagebox.showerror('Error', f'Failed to save file: {e}', parent=dialog)
                return
            dialog.destroy()
            self.refresh_view()
            msg = 'RBXM/RBXMX converted to RBXH blob and saved' if is_roblox_model else 'Saved'
            messagebox.showinfo('Success', f"{msg}: '{os.path.basename(dest)}'.")
            self._console_log(f'{msg}: {os.path.basename(dest)}')
        ttk.Button(btn_frame, text='OK', command=on_ok).pack(side='left', padx=6)
        ttk.Button(btn_frame, text='Cancel', command=dialog.destroy).pack(side='left', padx=6)
        entry_name.focus_set()

    def _clean_hex(self, s: str) -> str:
        s = s.strip()
        if s.lower().startswith('0x'):
            s = s[2:]
        s = re.sub('[^0-9A-Fa-f]', '', s)
        if len(s) % 2 == 1:
            s = '0' + s
        return s

    def _resolve_cache_file_for_item(self, obj) -> Optional[Tuple[str, str, str]]:
        if obj.get('kind') == 'hash':
            fname = obj.get('realname') or os.path.basename(obj.get('path') or '')
            full = obj.get('path')
            if full and os.path.isfile(full) and (' - ' in fname):
                h, display = fname.split(' - ', 1)
                return (h.strip(), full, display)
            return None
        if obj.get('kind') == 'group_item':
            fname = obj['filename']
            full = os.path.join(obj['group_path'], fname)
            if os.path.isfile(full) and ' - ' in fname:
                h = fname.split(' - ', 1)[0].strip()
                return (h, full, obj['display'])
            return None
        if obj.get('kind') == 'item':
            disp = obj['display']
            for folder in (self.own_dir, self.preinstalled_dir):
                if not os.path.isdir(folder):
                    continue
                for fname in os.listdir(folder):
                    if not os.path.isfile(os.path.join(folder, fname)):
                        continue
                    if fname.endswith(f'- {disp}') and ' - ' in fname:
                        h = fname.split(' - ', 1)[0].strip()
                        return (h, os.path.join(folder, fname), disp)
        return None

    def apply_caches(self):
        root = self.winfo_toplevel()
        db_path = getattr(root, 'db_path', None)
        shard_root = getattr(root, 'shard_root', None)
        if not db_path:
            messagebox.showerror('Apply', 'No database path is set in the viewer.')
            return
        objs = self._get_selected_objs()
        if not objs:
            messagebox.showinfo('Apply', 'Select one or more cache items.')
            return
        targets: List[Tuple[bytes, str, str, str]] = []
        for o in objs:
            info = self._resolve_cache_file_for_item(o)
            if not info and o.get('kind') == 'hash':
                full = o.get('path')
                if full and os.path.isfile(full):
                    entered = simpledialog.askstring('Apply File', 'Enter the target Roblox cache hash/asset ID:', parent=self)
                    if entered:
                        info = (self._clean_hex(entered), full, o.get('display') or os.path.basename(full))
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
            messagebox.showerror('Apply', 'No valid cache items found to import.')
            return
        ok = 0
        try:
            conn = connect_rw(db_path)
            cur = conn.cursor()
            for id_b, full, _display, _h_hex in targets:
                try:
                    with open(full, 'rb') as f:
                        blob = f.read()
                except Exception:
                    continue
                try:
                    cur.execute('BEGIN IMMEDIATE')
                    cur.execute('DELETE FROM files WHERE id=?', (id_b,))
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
                    cur.execute('BEGIN IMMEDIATE')
                    cur.execute('INSERT INTO files(id, content) VALUES(?, ?)', (id_b, sqlite3.Binary(blob)))
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
            messagebox.showerror('Apply', f'DB error:\n{e}')
            return
        if ok:
            root = self.winfo_toplevel()
            recorder = getattr(root, '_cc_record_applied_caches', None)
            if callable(recorder):
                applied = []
                for id_b, _full, display, h_hex in targets:
                    applied.append({'name': display, 'hash': h_hex})
                recorder(applied)
        messagebox.showinfo('Apply', f'Imported {ok} of {len(targets)} blob(s).')
        self._console_log(f'Applied {ok}/{len(targets)} selected cache blob(s)')

    def rename_selected(self):
        objs = self._get_selected_objs()
        if len(objs) != 1:
            return
        o = objs[0]
        kind = o.get('kind')
        current = o.get('display') or o.get('name')
        new_name = simpledialog.askstring('Rename', 'Enter new name:', initialvalue=current)
        if not new_name:
            return
        new_name = self._sanitize_filename(new_name)
        try:
            if kind == 'group':
                src = o['path']
                dest = os.path.join(os.path.dirname(src), new_name)
                os.rename(src, dest)
                expanded = self.group_states.pop(src, False)
                self.group_states[dest] = expanded
            elif kind == 'group_item':
                src = os.path.join(o['group_path'], o['filename'])
                h = o['filename'].split(' - ', 1)[0]
                dest = os.path.join(o['group_path'], f'{h} - {new_name}')
                os.rename(src, dest)
            elif kind == 'hash':
                src = o['path']
                h = o.get('realname', os.path.basename(src)).split(' - ', 1)[0]
                dest = os.path.join(os.path.dirname(src), f'{h} - {new_name}')
                os.rename(src, dest)
            elif kind == 'item':
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
                h = os.path.basename(src).split(' - ', 1)[0]
                dest = os.path.join(os.path.dirname(src), f'{h} - {new_name}')
                os.rename(src, dest)
        except Exception as e:
            messagebox.showerror('Error', f'Rename failed: {e}')
            return
        self.refresh_view()

    def delete_selected(self):
        objs = self._get_selected_objs()
        if not objs:
            messagebox.showerror('Error', 'No item selected.')
            return
        prompt = f"Are you sure you want to delete '{objs[0].get('name') or objs[0].get('display')}'?" if len(objs) == 1 else f'Are you sure you want to delete {len(objs)} items?'
        if not messagebox.askyesno('Confirm', prompt):
            return
        deleted_units = 0
        for o in objs:
            if o['kind'] == 'group':
                try:
                    shutil.rmtree(o['path'])
                    deleted_units += 1
                    self.group_states.pop(o['path'], None)
                except Exception as e:
                    messagebox.showerror('Error', f'Failed to delete group: {e}')
                    return
            elif o['kind'] == 'group_item':
                try:
                    os.remove(os.path.join(o['group_path'], o['filename']))
                    deleted_units += 1
                except Exception as e:
                    messagebox.showerror('Error', f'Failed to delete file: {e}')
                    return
            elif o['kind'] in ('item',):
                for folder in (self.preinstalled_dir, self.own_dir):
                    if not os.path.isdir(folder):
                        continue
                    for fname in list(os.listdir(folder)):
                        if fname.endswith(f"- {o['display']}"):
                            try:
                                os.remove(os.path.join(folder, fname))
                                deleted_units += 1
                            except Exception as e:
                                messagebox.showerror('Error', f'Failed to delete file: {e}')
                                return
            elif o['kind'] == 'hash':
                try:
                    os.remove(o['path'])
                    deleted_units += 1
                except Exception as e:
                    messagebox.showerror('Error', f'Failed to delete file: {e}')
                    return
        self.refresh_view()
        messagebox.showinfo('Success', f'Deleted {deleted_units} item(s).')
        self._console_log(f'Deleted {deleted_units} cache item(s)')

    def delete_selected_groups(self):
        objs = self._get_selected_objs()
        groups = [o for o in objs if o.get('kind') == 'group']
        if not groups:
            return
        prompt = f"Are you sure you want to delete group '{groups[0]['name']}'?" if len(groups) == 1 else f'Are you sure you want to delete {len(groups)} groups?'
        if not messagebox.askyesno('Confirm', prompt):
            return
        deleted = 0
        for g in groups:
            try:
                shutil.rmtree(g['path'])
                deleted += 1
                self.group_states.pop(g['path'], None)
            except Exception as e:
                messagebox.showerror('Error', f'Failed to delete group: {e}')
                return
        self.refresh_view()
        messagebox.showinfo('Success', f'Deleted {deleted} group(s).')
        self._console_log(f'Deleted {deleted} cache group(s)')

    def ungroup_selected_groups(self):
        objs = self._get_selected_objs()
        groups = [o for o in objs if o.get('kind') == 'group']
        if not groups:
            return
        prompt = f"Remove group '{groups[0]['name']}' and move its files back?" if len(groups) == 1 else f'Remove {len(groups)} groups and move their files back?'
        if not messagebox.askyesno('Confirm', prompt):
            return
        moved_files = 0
        removed_groups = 0
        for g in groups:
            try:
                for f in os.listdir(g['path']):
                    src = os.path.join(g['path'], f)
                    if not os.path.isfile(src):
                        continue
                    base = os.path.basename(src)
                    dst_dir = os.path.dirname(g['path'])
                    dst = os.path.join(dst_dir, base)
                    if os.path.exists(dst):
                        name, ext = os.path.splitext(base)
                        i = 1
                        while True:
                            alt = f'{name} ({i}){ext}'
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
                shutil.rmtree(g['path'])
                removed_groups += 1
                self.group_states.pop(g['path'], None)
            except Exception as e:
                messagebox.showerror('Error', f'Failed to ungroup: {e}')
                return
        self.refresh_view()
        messagebox.showinfo('Success', f'Ungrouped {removed_groups} group(s), restored {moved_files} file(s).')
        self._console_log(f'Ungrouped {removed_groups} group(s), restored {moved_files} cache file(s)')

    def create_group_from_selection(self):
        objs = self._get_selected_objs()
        view = self.source_var.get()
        if view == 'Caches':
            allowed = {'item', 'group_item'}
        else:
            allowed = {'hash', 'group_item'}
        if any((o['kind'] not in allowed for o in objs)):
            return

        def parent_dir(o):
            if o['kind'] == 'group_item':
                return o['group_path']
            if o['kind'] == 'hash':
                return os.path.dirname(o['path'])
            if o['kind'] == 'item':
                return self.own_dir
            return None
        base = self._base_dir_for_view()
        if objs:
            base = parent_dir(objs[0])
            if not base or any((parent_dir(o) != base for o in objs)):
                messagebox.showerror('Error', 'Items must share the same parent folder.')
                return
        name = simpledialog.askstring('Create group', 'Group name:')
        if not name:
            return
        group_path = os.path.join(base, name)
        if os.path.exists(group_path):
            messagebox.showerror('Error', 'A group with that name already exists.')
            return
        try:
            os.makedirs(group_path, exist_ok=False)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to create group folder: {e}')
            return
        moved_count = 0
        for o in objs:
            if o['kind'] == 'group_item':
                src_path = os.path.join(o['group_path'], o['filename'])
            elif o['kind'] == 'hash':
                src_path = o['path']
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
                    if o['kind'] in ('group_item', 'item') and os.path.dirname(src_path) == self.own_dir:
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
            messagebox.showinfo('Success', f"Created group '{name}' with {moved_count} item(s).")
        else:
            messagebox.showinfo('Success', f"Created empty group '{name}'.")
        self._console_log(f"Created cache group '{name}' with {moved_count} item(s)")
TYPE_FILTERS = [('All', lambda c: True), ('Mesh', lambda c: c == 'Mesh'), ('Audio', lambda c: c == 'Sound'), ('Animation', lambda c: c == 'Animation'), ('Image', lambda c: c in ('Image', 'Decal')), ('Video', lambda c: c == 'Video'), ('KTX Texture', lambda c: c == 'KTX Texture'), ('Model/RBXM', lambda c: c in ('Model', 'RBXM', 'rbxl (place)')), ('Font', lambda c: c == 'Font'), ('Text', lambda c: c in ('Text', 'Translations', 'Compressed', 'Ticket')), ('Unknown', lambda c: c == 'Unknown')]
FFLAG_PREFIXES = ['DFInt', 'DFString', 'DFFlag', 'FInt', 'FString', 'FFlag', 'SFFlag', 'SFInt', 'SFString', 'DFLog', 'FLog']
SKYBOX_TEXTURES = ('sky512_bk.tex', 'sky512_dn.tex', 'sky512_ft.tex', 'sky512_lf.tex', 'sky512_rt.tex', 'sky512_up.tex')
SOUND_FILES = ('action_falling.ogg', 'action_footsteps_plastic.mp3', 'action_get_up.mp3', 'action_jump.mp3', 'action_jump_land.mp3', 'action_swim.mp3', 'impact_explosion_03.mp3', 'impact_water.mp3', 'oof.ogg', 'ouch.ogg', 'volume_slider.ogg')
FFLAG_PATTERN = bytes.fromhex('48 83 EC 38 48 8B 0D 00 00 00 00 4C 8D 05')
FFLAG_MASK = 'xxxxxxx????xxx'
FFLAG_MODULE_SIZE = 200 * 1024 * 1024

def fflag_strip_prefix(name: str) -> str:
    name = str(name).strip()
    for pfx in FFLAG_PREFIXES:
        if name.startswith(pfx):
            return name[len(pfx):]
    return name

def fflag_infer_type(value: str) -> str:
    v = str(value).strip().lower()
    if v in ('true', 'false'):
        return 'bool'
    try:
        int(v, 10)
        return 'int'
    except ValueError:
        try:
            float(v)
            return 'float'
        except ValueError:
            return 'string'

class RobloxFFlagEngine:
    PROCESS_ALL_ACCESS = 2035711
    TH32CS_SNAPMODULE = 8
    TH32CS_SNAPMODULE32 = 16
    MEM_COMMIT = 4096
    PAGE_NOACCESS = 1
    PAGE_GUARD = 256

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
        if os.name != 'nt':
            return False
        h = ctypes.windll.kernel32.OpenProcess(self.PROCESS_ALL_ACCESS, False, int(pid))
        if not h:
            return False
        self.handle = h
        self.pid = int(pid)
        self.module_base = self._get_module_base(pid, 'RobloxPlayerBeta.exe')
        self.cached_singleton = 0
        if not self.module_base:
            self.close()
            return False
        return True

    def _get_module_base(self, pid: int, wanted: str) -> int:

        class MODULEENTRY32W(ctypes.Structure):
            _fields_ = [('dwSize', ctypes.wintypes.DWORD), ('th32ModuleID', ctypes.wintypes.DWORD), ('th32ProcessID', ctypes.wintypes.DWORD), ('GlblcntUsage', ctypes.wintypes.DWORD), ('ProccntUsage', ctypes.wintypes.DWORD), ('modBaseAddr', ctypes.POINTER(ctypes.c_ubyte)), ('modBaseSize', ctypes.wintypes.DWORD), ('hModule', ctypes.c_void_p), ('szModule', ctypes.wintypes.WCHAR * 256), ('szExePath', ctypes.wintypes.WCHAR * 260)]
        snap = ctypes.windll.kernel32.CreateToolhelp32Snapshot(self.TH32CS_SNAPMODULE | self.TH32CS_SNAPMODULE32, int(pid))
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
        ok = ctypes.windll.kernel32.ReadProcessMemory(self.handle, ctypes.c_void_p(address), buf, size, ctypes.byref(got))
        return bytes(buf.raw[:got.value]) if ok and got.value == size else None

    def _read_u64(self, address: int) -> int:
        b = self._read(address, 8)
        return int.from_bytes(b, 'little', signed=False) if b else 0

    def get_singleton(self) -> int:
        if not self.handle or not self.module_base:
            self.cached_singleton = 0
            return 0
        try:
            code = ctypes.c_ulong()
            if not ctypes.windll.kernel32.GetExitCodeProcess(self.handle, ctypes.byref(code)) or code.value != 259:
                self.cached_singleton = 0
                return 0
        except Exception:
            self.cached_singleton = 0
            return 0
        if self.cached_singleton:
            test = self._read(self.cached_singleton + 48, 8)
            if test is not None and int.from_bytes(test, 'little', signed=False):
                return self.cached_singleton
            self.cached_singleton = 0
        mbi = ctypes.create_string_buffer(48)
        addr = self.module_base
        stop = self.module_base + self.module_size
        while addr < stop:
            ret = ctypes.windll.kernel32.VirtualQueryEx(self.handle, ctypes.c_void_p(addr), mbi, ctypes.sizeof(mbi))
            if not ret:
                break
            vbase = int.from_bytes(mbi.raw[0:8], 'little')
            vsize = int.from_bytes(mbi.raw[24:32], 'little')
            state = int.from_bytes(mbi.raw[32:36], 'little')
            protect = int.from_bytes(mbi.raw[44:48], 'little')
            if state == self.MEM_COMMIT and (not protect & (self.PAGE_NOACCESS | self.PAGE_GUARD)) and vsize:
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
                        rel = int.from_bytes(data[idx + 7:idx + 11], 'little', signed=True)
                        fa = vbase + idx
                        singleton = self._read_u64(fa + 11 + rel)
                        if singleton:
                            self.cached_singleton = singleton
                            return singleton
                        idx += 1
            addr = vbase + max(vsize, 4096)
        return 0

    @staticmethod
    def _fnv1a64(name: str) -> int:
        h = 14695981039346656037
        for ch in name:
            h ^= ord(ch)
            h = h * 1099511628211 & 18446744073709551615
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
            str_sz = int.from_bytes(entry[32:40], 'little', signed=True)
            str_alc = int.from_bytes(entry[40:48], 'little', signed=True)
            if str_alc > 15:
                ptr = int.from_bytes(entry[16:24], 'little')
                ename_b = self._read(ptr, max(0, str_sz)) or b''
                ename = ename_b.decode('utf-8', errors='replace')
            else:
                ename = entry[16:16 + max(0, str_sz)].decode('utf-8', errors='replace')
            if ename == name:
                vpr = int.from_bytes(entry[48:56], 'little')
                if not vpr:
                    return False
                vp = self._read_u64(vpr + 192)
                if not vp:
                    return False
                v = str(value).strip().lower()
                try:
                    rv = 1 if v in ('true', '1') else 0 if v in ('false', '0') else int(value)
                except ValueError:
                    return False
                data = int(rv).to_bytes(4, 'little', signed=True)
                written = ctypes.c_size_t()
                return bool(ctypes.windll.kernel32.WriteProcessMemory(self.handle, ctypes.c_void_p(vp), data, 4, ctypes.byref(written)))
            node = int.from_bytes(entry[8:16], 'little', signed=False)
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
            str_sz = int.from_bytes(entry[32:40], 'little', signed=True)
            str_alc = int.from_bytes(entry[40:48], 'little', signed=True)
            if str_alc > 15:
                ptr = int.from_bytes(entry[16:24], 'little')
                ename = (self._read(ptr, max(0, str_sz)) or b'').decode('utf-8', errors='replace')
            else:
                ename = entry[16:16 + max(0, str_sz)].decode('utf-8', errors='replace')
            if ename == name:
                vpr = int.from_bytes(entry[48:56], 'little')
                if not vpr:
                    return 0
                return self._read_u64(vpr + 192)
            node = int.from_bytes(entry[8:16], 'little', signed=False)
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
    if not pid or sys.platform != 'win32':
        return ''
    try:
        handle = ctypes.windll.kernel32.OpenProcess(4096, False, int(pid))
        if not handle:
            return ''
        try:
            buf = ctypes.create_unicode_buffer(32768)
            size = ctypes.wintypes.DWORD(len(buf))
            if ctypes.windll.kernel32.QueryFullProcessImageNameW(handle, 0, buf, ctypes.byref(size)):
                return buf.value
        finally:
            ctypes.windll.kernel32.CloseHandle(handle)
    except Exception:
        pass
    return ''

def _fflag_find_pid() -> int:
    if os.name != 'nt':
        return 0
    PROCESS_QUERY_LIMITED_INFORMATION = 4096
    try:

        class PROCESSENTRY32W(ctypes.Structure):
            _fields_ = [('dwSize', ctypes.wintypes.DWORD), ('cntUsage', ctypes.wintypes.DWORD), ('th32ProcessID', ctypes.wintypes.DWORD), ('th32DefaultHeapID', ctypes.POINTER(ctypes.c_ulong)), ('th32ModuleID', ctypes.wintypes.DWORD), ('cntThreads', ctypes.wintypes.DWORD), ('th32ParentProcessID', ctypes.wintypes.DWORD), ('pcPriClassBase', ctypes.c_long), ('dwFlags', ctypes.wintypes.DWORD), ('szExeFile', ctypes.wintypes.WCHAR * 260)]
        snap = ctypes.windll.kernel32.CreateToolhelp32Snapshot(2, 0)
        if snap in (0, -1):
            return 0
        pe = PROCESSENTRY32W()
        pe.dwSize = ctypes.sizeof(pe)
        try:
            if ctypes.windll.kernel32.Process32FirstW(snap, ctypes.byref(pe)):
                while True:
                    if pe.szExeFile.lower() == 'robloxplayerbeta.exe':
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
    _active = []
    _host = None

    @staticmethod
    @classmethod
    def _get_host(cls, parent):
        host = cls._host
        try:
            if host is not None and host.winfo_exists() and (host.winfo_toplevel() == parent.winfo_toplevel()):
                return host
        except Exception:
            pass
        try:
            host = tk.Frame(parent, bg=_CURRENT_PALETTE.get('bg_dark', '#111111'), bd=0, highlightthickness=0)
            host.place(relx=1.0, rely=1.0, anchor='se', x=-14, y=-14)
            cls._host = host
            return host
        except Exception:
            return None

    @classmethod
    def show(cls, title, message, parent=None, kind='info'):
        try:
            if parent is None:
                parent = tk._default_root
            if parent is None or not parent.winfo_exists():
                return
            root = parent.winfo_toplevel()
            host = cls._get_host(root)
            if host is None:
                return
            accent = _CURRENT_PALETTE.get('accent', '#7f8cff')
            bg = _CURRENT_PALETTE.get('bg_dark', '#111111')
            if kind == 'error':
                accent = '#ff5f57'
            elif kind == 'warning':
                accent = '#febc2e'
            elif kind == 'info':
                accent = _CURRENT_PALETTE.get('accent', '#7f8cff')
            toast = tk.Frame(host, bg='#090909', bd=0, highlightthickness=1, highlightbackground=accent, width=390)
            toast.pack(fill='x', pady=(0, 8))
            toast.pack_propagate(False)
            header = tk.Frame(toast, bg='#090909', height=28)
            header.pack(fill='x')
            header.pack_propagate(False)
            tk.Label(header, text=str(title), bg='#090909', fg='#eeeeee', font=('Segoe UI Semibold', 9)).pack(side='left', padx=(10, 4), pady=5)
            tk.Label(header, text='×', bg='#090909', fg='#888888', font=('Segoe UI', 11)).pack(side='right', padx=(4, 8))
            body = tk.Frame(toast, bg='#111111')
            body.pack(fill='both', expand=True)
            tk.Label(body, text=str(message), bg='#111111', fg='#e5e5e5', justify='left', anchor='w', wraplength=360, font=('Segoe UI', 9)).pack(fill='both', expand=True, padx=10, pady=(4, 10))

            def close():
                try:
                    if toast in cls._active:
                        cls._active.remove(toast)
                    if toast.winfo_exists():
                        toast.destroy()
                    if host.winfo_exists() and (not cls._active):
                        host.place_forget()
                except Exception:
                    pass
            toast.bind('<Button-1>', lambda _e: close())
            for child in (header, body):
                child.bind('<Button-1>', lambda _e: close())
            for child in header.winfo_children():
                child.bind('<Button-1>', lambda _e: close())
            cls._active.append(toast)
            host.place(relx=1.0, rely=1.0, anchor='se', x=-14, y=-14)
            toast.after(3000, close)
        except Exception:
            pass

class _DarkMessageBox:

    @staticmethod
    def showinfo(title, message, parent=None, **kwargs):
        _MacNotification.show(title, message, parent, 'info')

    @staticmethod
    def showwarning(title, message, parent=None, **kwargs):
        _MacNotification.show(title, message, parent, 'warning')

    @staticmethod
    def showerror(title, message, parent=None, **kwargs):
        _MacNotification.show(title, message, parent, 'error')

    @staticmethod
    def askyesno(title, message, parent=None, **kwargs):
        return _NATIVE_MESSAGEBOX.askyesno(title, message, parent=parent, **kwargs)
messagebox = _DarkMessageBox()

class _ScrollableTab(ttk.Frame):

    def __init__(self, master, padding=0, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(self, bg=_CURRENT_PALETTE['bg_dark'], highlightthickness=0, bd=0)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.inner = ttk.Frame(self, padding=padding)
        self.window = self.canvas.create_window((0, 0), window=self.inner, anchor='nw')
        self.inner.bind('<Configure>', self._update_region)
        self.canvas.bind('<Configure>', self._resize_inner)
        self.canvas.bind('<Enter>', lambda e: self.canvas.focus_set())
        self.canvas.bind('<MouseWheel>', self._wheel)
        self.inner.bind('<MouseWheel>', self._wheel)
        self._middle_y = None
        self.canvas.bind('<Button-2>', self._middle_press)
        self.canvas.bind('<B2-Motion>', self._middle_drag)
        self.canvas.bind('<ButtonRelease-2>', self._middle_release)
        self.inner.bind('<Button-2>', self._middle_press)
        self.inner.bind('<B2-Motion>', self._middle_drag)
        self.inner.bind('<ButtonRelease-2>', self._middle_release)

    def _update_region(self, _event=None):
        if getattr(self, '_region_job', None):
            try:
                self.after_cancel(self._region_job)
            except Exception:
                pass
        self._region_job = self.after_idle(self._apply_scroll_region)

    def _apply_scroll_region(self):
        self._region_job = None
        try:
            bbox = self.canvas.bbox('all')
            if bbox != getattr(self, '_last_scrollregion', None):
                self.canvas.configure(scrollregion=bbox)
                self._last_scrollregion = bbox
        except Exception:
            pass

    def _resize_inner(self, event):
        width = int(getattr(event, 'width', 0) or 0)
        if width != getattr(self, '_last_inner_width', -1):
            self._last_inner_width = width
            self.canvas.itemconfigure(self.window, width=width)

    def _wheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(int(-event.delta / 120), 'units')
        return 'break'

    def _middle_press(self, event):
        self._middle_y = event.y
        return 'break'

    def _middle_drag(self, event):
        if self._middle_y is not None:
            self.canvas.yview_scroll(int((self._middle_y - event.y) / 2), 'units')
            self._middle_y = event.y
        return 'break'

    def _middle_release(self, _event):
        self._middle_y = None
        return 'break'

class _ConsoleStream:

    def __init__(self, app, original):
        self.app = app
        self.original = original

    def write(self, data):
        self.original.write(data)
        if str(data).strip():
            self.app._console_log(str(data).rstrip())

    def flush(self):
        try:
            self.original.flush()
        except Exception:
            pass

def _win32_root_hwnd(win):
    if sys.platform != 'win32':
        return 0
    try:
        user32 = ctypes.windll.user32
        raw = int(win.winfo_id())
        return int(user32.GetAncestor(raw, 2) or raw)
    except Exception:
        return 0

def _prepare_borderless_appwindow(win):
    if sys.platform != 'win32':
        return
    hwnd = _win32_root_hwnd(win)
    if not hwnd:
        return
    try:
        user32 = ctypes.windll.user32
        GWL_STYLE = -16
        GWL_EXSTYLE = -20
        GWL_HWNDPARENT = -8
        WS_POPUP = 2147483648
        WS_THICKFRAME = 262144
        WS_MINIMIZEBOX = 131072
        WS_MAXIMIZEBOX = 65536
        WS_SYSMENU = 524288
        WS_EX_APPWINDOW = 262144
        WS_EX_TOOLWINDOW = 128
        WS_EX_NOACTIVATE = 134217728
        get_style = getattr(user32, 'GetWindowLongPtrW', user32.GetWindowLongW)
        set_style = getattr(user32, 'SetWindowLongPtrW', user32.SetWindowLongW)
        style = int(get_style(hwnd, GWL_STYLE))
        style = style | WS_POPUP | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX | WS_SYSMENU
        style &= ~12582912
        style &= ~8388608
        set_style(hwnd, GWL_STYLE, style)
        ex = int(get_style(hwnd, GWL_EXSTYLE))
        ex = (ex | WS_EX_APPWINDOW) & ~WS_EX_TOOLWINDOW & ~WS_EX_NOACTIVATE
        set_style(hwnd, GWL_EXSTYLE, ex)
        try:
            set_style(hwnd, GWL_HWNDPARENT, 0)
        except Exception:
            pass
        SWP_NOSIZE, SWP_NOMOVE, SWP_NOZORDER, SWP_NOACTIVATE, SWP_FRAMECHANGED = (1, 2, 4, 16, 32)
        user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER | SWP_NOACTIVATE | SWP_FRAMECHANGED)
    except Exception:
        pass

def _apply_native_titlebar_theme(win):
    if sys.platform != 'win32':
        return
    hwnd = _win32_root_hwnd(win)
    if not hwnd:
        return
    try:
        dwm = ctypes.windll.dwmapi
        attrs = {33: 2, 34: 0, 35: 0, 36: 16777215, 20: 1, 38: 0, 2: 2, 3: 1}
        for attr, value in attrs.items():
            try:
                val = ctypes.c_int(int(value))
                dwm.DwmSetWindowAttribute(hwnd, attr, ctypes.byref(val), ctypes.sizeof(val))
            except Exception:
                pass
    except Exception:
        pass

class App(tk.Tk):

    def report_callback_exception(self, exc_type, exc_value, exc_tb):
        _report_rotools_error(exc_type, exc_value, exc_tb, self)

    def __init__(self):
        super().__init__()
        self._console_history = self._load_console_history()
        self._console_undo_stack = []
        self._console_save_job = None
        self._console_original_stdout = sys.stdout
        sys.stdout = _ConsoleStream(self, self._console_original_stdout)
        self.settings = load_settings()
        _saved_roblox = str(self.settings.get('roblox_path', '') or '').strip()
        if _saved_roblox and os.path.isdir(_saved_roblox):
            _candidate = os.path.join(_saved_roblox, 'RobloxPlayerBeta.exe')
            if os.path.isfile(_candidate):
                self.settings['roblox_path'] = _candidate
        if not self.settings.get('roblox_path'):
            _pid = _fflag_find_pid()
            _exe = _get_process_exe_path(_pid)
            if _exe and os.path.basename(_exe).lower() == 'robloxplayerbeta.exe':
                self.settings['roblox_path'] = _exe
                save_settings(self.settings)
        self.cconfigs_dir = os.path.join(DATA_DIR, 'cconfigs')
        self.jsons_dir = os.path.join(DATA_DIR, 'jsons')
        os.makedirs(self.cconfigs_dir, exist_ok=True)
        os.makedirs(self.jsons_dir, exist_ok=True)
        self.cc_applied_caches = []
        self._cc_load_applied_state()
        self._reset_version_file()
        self._history_last_game = None
        try:
            self._dpi_scale = max(0.5, min(2.0, int(self.settings.get('dpi_percent', 100)) / 100.0))
        except Exception:
            self._dpi_scale = 1.0
        try:
            self.tk.call('tk', 'scaling', self._dpi_scale)
        except Exception:
            pass
        _t = self.settings.get('theme', DEFAULT_THEME)
        apply_visual_polish(self, theme=UI_THEME, palette=THEMES.get(_t, THEMES[DEFAULT_THEME]))
        self.title('RoUtils')
        saved_geometry = str(self.settings.get('window_geometry', '') or '')
        if re.match('^\\d+x\\d+(?:[+-]\\d+[+-]\\d+)?$', saved_geometry):
            startup_geometry = saved_geometry
        else:
            screen_width = max(800, int(self.winfo_screenwidth() or 1920))
            screen_height = max(600, int(self.winfo_screenheight() or 1080))
            scale = min(screen_width / 1920.0, screen_height / 1080.0)
            startup_geometry = f'{max(900, int(1920 * scale))}x{max(560, int(1080 * scale))}'
        self.geometry(startup_geometry)
        self.minsize(700, 420)
        self.resizable(True, True)
        self._setup_custom_titlebar()
        self.after(120, self._restore_windows_taskbar_presence)
        if not bool(self.settings.get('launch_on_tray', False)):
            self.after(220, self._startup_focus_cycle)
        self.bind('<Map>', lambda _e: self.after_idle(self._restore_windows_taskbar_presence), add='+')
        self.bind('<Map>', lambda _e: self.after(250, self._apply_streamer_mode), add='+')
        self.after_idle(self._restore_windows_taskbar_presence)
        self.after(250, self._apply_streamer_mode)
        try:
            self.iconbitmap(ICON_PATH)
        except Exception:
            pass
        self.protocol('WM_DELETE_WINDOW', self._on_close)
        self._geometry_save_job = None
        self._ui_jobs = {}
        self._global_scroll_support_installed = False
        self._history_render_signature = None
        self._client_tab_active = False
        self.bind('<Configure>', self._on_geometry_configure, add='+')
        self._global_hotkey_q = queue.Queue()
        self._hotkey_stop = threading.Event()
        self.fflag_hotkeys = list(self.settings.get('fflag_hotkeys', []))
        default_fps_hotkeys = {str(fps): '' for fps in (30, 60, 120, 144, 180, 200, 240)}
        saved_fps_hotkeys = self.settings.get('fps_hotkeys', {})
        if isinstance(saved_fps_hotkeys, dict):
            default_fps_hotkeys.update({str(fps): str(saved_fps_hotkeys.get(str(fps), '') or '').upper() for fps in default_fps_hotkeys})
        self.fps_hotkeys = default_fps_hotkeys
        saved_slots = self.settings.get('fps_hotkey_slots', [])
        if isinstance(saved_slots, list):
            configured = []
            for x in saved_slots:
                if isinstance(x, dict) and (x.get('fps') or x.get('key')):
                    configured.append({'fps': int(x.get('fps', 0) or 0), 'key': str(x.get('key', '') or '').upper()})
            self.fps_hotkey_slots = configured[:15] or [{'fps': 0, 'key': ''}]
        else:
            self.fps_hotkey_slots = [{'fps': 0, 'key': ''}]
        self._sync_fps_hotkey_slots()
        self._hotkey_prev = {}
        self._hotkey_thread = None
        self._quick_panel_enabled = True
        self._quick_panel_visible = True
        self._quick_panel_restore_geometry = None
        self._quick_panel_grace_until = 0.0
        self._cache_built = False
        style = ttk.Style(self)
        try:
            style.layout('RoUtils.Hidden.TNotebook.Tab', [])
            style.configure('RoUtils.Hidden.TNotebook', tabmargins=0, padding=0, borderwidth=0)
        except Exception:
            pass
        self._tab_nav = ttk.Frame(self)
        self._tab_nav.pack(fill='x', side='top', padx=8, pady=(6, 4))
        self._tab_nav_inner = ttk.Frame(self._tab_nav)
        self._tab_nav_inner.pack(anchor='center')
        self._setup_tab_nav_styles()
        self.nb = ttk.Notebook(self, style='RoUtils.Hidden.TNotebook')
        self.nb.pack(fill='both', expand=True, padx=8, pady=(0, 8))
        self.tab_viewer = ttk.Frame(self.nb)
        self.nb.add(self.tab_viewer, text='Cache')
        self.hpaned = ttk.PanedWindow(self.tab_viewer, orient='horizontal')
        self.hpaned.pack(fill='both', expand=True)
        self.viewer_root = ttk.Frame(self.hpaned)
        self.hpaned.add(self.viewer_root, weight=3)
        _set_pane_minsize(self.hpaned, self.viewer_root, VIEWER_MIN_WIDTH)
        self.replacer = ReplacerPane(self.hpaned)
        self.hpaned.add(self.replacer, weight=2)
        _set_pane_minsize(self.hpaned, self.replacer, REPLACER_MIN_WIDTH)
        self.hpaned.bind('<B1-Motion>', lambda e: self._clamp_hsash())
        self.hpaned.bind('<ButtonRelease-1>', lambda e: self._clamp_hsash())
        self.viewer_collapsed = False
        self._restore_geom: Optional[Tuple[int, int, int, int]] = None
        self._saved_sash: Optional[int] = None
        self.collapse_btn = ttk.Button(self.replacer.top, text='◀', width=2, command=self._toggle_viewer_pane)
        self.collapse_btn.pack(side='left', padx=(0, 4), before=self.replacer.action_bar)
        default_db, default_shards = default_paths()
        self.db_path = str(self.settings.get('db_path') or default_db)
        self.shard_root = str(self.settings.get('shard_root') or default_shards)
        self.seen_hashes: set = set()
        self.items_by_iid: Dict[str, ScanItem] = {}
        self.items_by_hash: Dict[str, ScanItem] = {}
        self.new_items_q: 'queue.Queue[List[ScanItem]]' = queue.Queue()
        self.watching = False
        self.stop_event = threading.Event()
        self.scan_thread: Optional[threading.Thread] = None
        self._tree_render_pending = []
        self._tree_render_job = None
        self._blob_cache = {}
        self._blob_cache_order = []
        self._blob_cache_limit = 8
        self.autoscroll = tk.BooleanVar(value=self.settings.get('autoscroll', True))
        self.hide_tickets = tk.BooleanVar(value=self.settings.get('hide_tickets', True))
        self.stay_on_top = tk.BooleanVar(value=self.settings.get('stay_on_top', False))
        self.show_lines = tk.BooleanVar(value=self.settings.get('show_lines', True))
        self.streamer_mode = tk.BooleanVar(value=self.settings.get('streamer_mode', False))

        def _trace(*_):
            self._save_settings()
        for v in (self.autoscroll, self.hide_tickets, self.stay_on_top, self.show_lines, self.streamer_mode):
            v.trace_add('write', _trace)
        self.streamer_mode.trace_add('write', lambda *_: self._apply_streamer_mode())
        self.filter_text = tk.StringVar(value='')
        try:
            saved_max_rows = max(0, int(self.settings.get('max_rows', 0)))
        except Exception:
            saved_max_rows = 0
        self.max_rows = tk.IntVar(value=saved_max_rows)
        self.type_filter = tk.StringVar(value=self.settings.get('type_filter', 'All'))
        self.autostart_watch = tk.BooleanVar(value=self.settings.get('autostart_watch', False))
        self.autostart_watch.trace_add('write', lambda *_: self._save_settings())
        try:
            saved_fps = int(self.settings.get('fps_limit', 0))
        except Exception:
            saved_fps = 0
        self.fps_limit = tk.IntVar(value=max(0, min(240, saved_fps)))
        self._hidden_fps_flag_name = 'DFIntTaskSchedulerTargetFps'
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
        self.fflag_engine = RobloxFFlagEngine()
        self.fflag_flags = []
        self.fflag_offsets = {}
        self.fflag_presets = []
        self.fflag_pid = 0
        self.fflag_original_values = {}
        self.fflag_auto_apply = tk.BooleanVar(value=self.settings.get('fflag_auto_apply', False))
        self.launch_on_startup = tk.BooleanVar(value=self.settings.get('launch_on_startup', False))
        self.launch_on_tray = tk.BooleanVar(value=self.settings.get('launch_on_tray', False))
        self.hide_to_tray_on_close = tk.BooleanVar(value=self.settings.get('hide_to_tray_on_close', False))
        self.after_idle(self._update_kill_routils_visibility)
        self.auto_update = tk.BooleanVar(value=self.settings.get('auto_update', False))
        self._latest_version = None
        self._auto_update_in_progress = False
        self._outdated_dialog_shown = False
        self._tray_icon = None
        self._tray_thread = None
        self._tray_starting = False
        self._tray_hidden = False
        self.gemini_api_key = tk.StringVar(value=str(self.settings.get('gemini_api_key', '')))
        self.plugins_dir = os.path.join(DATA_DIR, 'plugins')
        os.makedirs(self.plugins_dir, exist_ok=True)
        self._plugins = []
        self._plugin_modules = {}
        self._plugin_cleanup = {}
        self._plugin_tabs = {}
        self._plugin_enabled = dict(self.settings.get('plugin_enabled', {})) if isinstance(self.settings.get('plugin_enabled', {}), dict) else {}
        self._load_fflag_flags()
        self._sync_fps_flag_to_manager()
        self._lazy_tabs = {}
        self._lazy_tab_ids = {}
        self.nb.bind('<<NotebookTabChanged>>', self._lazy_tab_changed, add='+')
        self._build_home_tab()
        lazy_builders = {'Cache': self._lazy_build_cache, 'FFlags': self._build_fflag_tab, 'Modifications': self._build_utils_tab, 'Configs': self._build_cconfigs_tab, 'Subplace Joiner': self._build_subplace_joiner_tab, 'Server Viewer': self._build_server_viewer_tab, 'History': self._build_history_tab, 'Client': self._build_client_tab, 'Themes': self._build_themes_tab, 'Settings': self._build_settings_tab, 'Plugins': self._build_plugins_tab, 'Console': self._build_console_tab}
        for tab_name in ('Cache', 'FFlags', 'Configs', 'Modifications', 'Subplace Joiner', 'Server Viewer', 'History', 'Client', 'Themes', 'Settings', 'Plugins', 'Console'):
            if tab_name == 'Cache':
                tab = self.tab_viewer
            else:
                tab = ttk.Frame(self.nb)
                self.nb.add(tab, text=tab_name)
            self._lazy_tab_ids[tab_name] = str(tab)
            self._lazy_tabs[str(tab)] = (tab_name, lazy_builders[tab_name], tab)
            if tab_name != 'Cache':
                ttk.Label(tab, text='Loading...', foreground='#9aa0a6').pack(expand=True)
        self._reorder_tabs()
        self._refresh_tab_nav()
        if self.nb.tabs():
            home_id = next((tid for tid in self.nb.tabs() if self.nb.tab(tid, 'text') == 'Home'), self.nb.tabs()[0])
            self.nb.select(home_id)

        self.after(40, self._lazy_tab_changed)
        self.after_idle(self._install_global_scroll_support)

        self.after(350, self._start_history_watcher)
        self.after(900, self._start_version_check)
        self.after(1100, self._install_startup_shortcut)
        if self.launch_on_tray.get():
            self.after_idle(self._hide_to_tray)
        self._start_global_hotkeys()
        self.after(UI_HOTKEY_INTERVAL_MS, self._process_global_hotkeys)
        self.after(UI_QUICK_PANEL_INTERVAL_MS, self._quick_panel_tick)
        if self.settings.get('viewer_collapsed'):
            self.after(250, self._apply_saved_viewer_state)
        self.after(75, self._drain_queue)


        self.after(6000, self._fflag_auto_apply_tick)

    def _schedule_ui(self, key, delay_ms, callback):
        jobs = getattr(self, '_ui_jobs', None)
        if jobs is None:
            jobs = self._ui_jobs = {}
        old = jobs.get(key)
        if old:
            try:
                self.after_cancel(old)
            except Exception:
                pass
        jobs[key] = self.after(delay_ms, lambda: self._run_ui_job(key, callback))

    def _run_ui_job(self, key, callback):
        jobs = getattr(self, '_ui_jobs', None)
        if jobs is not None:
            jobs.pop(key, None)
        try:
            callback()
        except Exception:
            pass

    def _lazy_build_cache(self):
        if getattr(self, '_cache_built', False):
            return
        self._build_viewer_widgets()
        self._cache_built = True
        self.after_idle(self._apply_startup_layouts)
        self.after_idle(self._update_status)

    def _lazy_tab_changed(self, _event=None):


        self._refresh_tab_nav()
        try:
            tab_id = self.nb.select()
        except Exception:
            return
        if not tab_id:
            return
        key = str(tab_id)
        info = self._lazy_tabs.get(key)
        if not info:
            return
        if getattr(self, '_lazy_tab_jobs', None) is None:
            self._lazy_tab_jobs = set()
        if key in self._lazy_tab_jobs:
            return
        self._lazy_tab_jobs.add(key)
        self._lazy_tabs.pop(key, None)
        tab_name, builder, placeholder = info

        def build_selected_tab():
            self._lazy_tab_jobs.discard(key)
            self._tab_building = True
            try:
                if tab_name != 'Cache':
                    if placeholder.winfo_exists():
                        self.nb.forget(placeholder)
                        placeholder.destroy()
                    builder()
                    self._reorder_tabs()
                    self._refresh_tab_nav()
                else:
                    builder()
            except Exception:
                try:
                    if tab_name != 'Cache' and placeholder.winfo_exists():
                        placeholder.destroy()
                except Exception:
                    pass
            self._client_tab_active = tab_name == 'Client'
            try:
                for current_id in self.nb.tabs():
                    if self.nb.tab(current_id, 'text') == tab_name:
                        self.nb.select(current_id)
                        break
            except Exception:
                pass
            try:
                self.after_idle(self._install_global_scroll_support)
            except Exception:
                pass
            finally:
                self._tab_building = False


        self.after(1, build_selected_tab)

    def _start_global_hotkeys(self):
        if self._hotkey_thread and self._hotkey_thread.is_alive():
            return
        if sys.platform != 'win32':
            return

        def worker():
            user32 = ctypes.windll.user32
            while not self._hotkey_stop.is_set():
                try:
                    bindings = [('quick_panel', 'F7', {})]
                    for binding in self.fflag_hotkeys:
                        key = str(binding.get('key', '')).upper()
                        if key:
                            bindings.append(('fflag', key, binding.copy()))
                    for fps, key in self.fps_hotkeys.items():
                        key = str(key or '').upper()
                        if key:
                            bindings.append(('fps', key, {'fps': int(fps), 'key': key}))
                    seen = set()
                    for kind, key, binding in bindings:
                        vk = fflag_key_to_vk(key)
                        if not vk or vk in seen:
                            continue
                        seen.add(vk)
                        down = bool(user32.GetAsyncKeyState(vk) & 32768)
                        was_down = self._hotkey_prev.get(vk, False)
                        self._hotkey_prev[vk] = down
                        if down and (not was_down):
                            self._global_hotkey_q.put((kind, binding))
                except Exception:
                    pass
                time.sleep(0.025)
        self._hotkey_thread = threading.Thread(target=worker, name='RoUtilsGlobalHotkeys', daemon=True)
        self._hotkey_thread.start()

    def _process_global_hotkeys(self):
        try:
            while True:
                kind, binding = self._global_hotkey_q.get_nowait()
                if kind == 'quick_panel':
                    self._toggle_quick_panel()
                elif kind == 'fps':
                    self._handle_fps_hotkey(binding)
                else:
                    self._handle_fflag_hotkey(binding)
        except queue.Empty:
            pass
        except Exception:
            pass
        if not self._hotkey_stop.is_set():
            self.after(UI_HOTKEY_INTERVAL_MS, self._process_global_hotkeys)

    def _show_quick_panel(self):
        if self._quick_panel_visible:
            return
        try:
            self._tray_hidden = False
            self._quick_panel_restore_geometry = self.geometry()
            self._quick_panel_visible = True
            self._quick_panel_grace_until = time.monotonic() + 0.75
            self.attributes('-fullscreen', False)
            if self._quick_panel_restore_geometry:
                self.geometry(self._quick_panel_restore_geometry)
            self.deiconify()
            self.lift()
            self.wm_attributes('-topmost', bool(self.stay_on_top.get()))
            self.focus_force()
            if sys.platform == 'win32':
                try:
                    ctypes.windll.user32.SetForegroundWindow(int(self.winfo_id()))
                except Exception:
                    pass
        except Exception:
            self._quick_panel_visible = False

    def _hide_quick_panel(self, to_tray=False):
        if not self._quick_panel_visible:
            if to_tray:
                self._hide_to_tray()
            return
        try:
            self.attributes('-fullscreen', False)
            self.attributes('-topmost', bool(self.stay_on_top.get()))
            if self._quick_panel_restore_geometry:
                self.geometry(self._quick_panel_restore_geometry)
            self._quick_panel_visible = False
            if to_tray:
                self.withdraw()
                self._start_tray()
                self._tray_hidden = True
            else:
                self.iconify()
        except Exception:
            self._quick_panel_visible = False

    def _toggle_quick_panel(self):
        if self._quick_panel_enabled and (not self._quick_panel_visible):
            self._show_quick_panel()
            return
        if self._quick_panel_enabled:
            self._quick_panel_enabled = False
            self._hide_quick_panel(to_tray=bool(self.hide_to_tray_on_close.get()))
            return
        self._quick_panel_enabled = True
        self._show_quick_panel()

    def _quick_panel_tick(self):
        if not self._hotkey_stop.is_set():
            self.after(UI_QUICK_PANEL_INTERVAL_MS, self._quick_panel_tick)

    def _handle_fps_hotkey(self, binding):
        try:
            fps = max(0, min(240, int(binding.get('fps', 0))))
            self.fps_limit.set(fps)
            self._save_settings()
            self._sync_fps_flag_to_manager()
            self._apply_fps_flag(silent=True)
            if hasattr(self, 'fps_value_label'):
                self.fps_value_label.config(text='FPS: Uncap' if fps == 0 else f'FPS: {fps}')
            if hasattr(self, '_fps_text_var'):
                self._fps_text_var.set(str(fps))
        except Exception:
            pass

    def _sync_fps_hotkey_slots(self):
        self.fps_hotkeys = {str(item.get('fps')): str(item.get('key', '')).upper() for item in getattr(self, 'fps_hotkey_slots', []) if int(item.get('fps', 0) or 0) > 0 and item.get('key')}

    def _fps_slot_editor(self, index):
        dlg = tk.Toplevel(self)
        dlg.title(f'FPS Hotkey {index + 1}')
        dlg.geometry('430x250')
        dlg.transient(self)
        theme_toplevel(dlg)
        outer = ttk.Frame(dlg, padding=14)
        outer.pack(fill='both', expand=True)
        ttk.Label(outer, text='FPS value (1-240):').pack(anchor='w')
        item = self.fps_hotkey_slots[index]
        fps_var = tk.StringVar(value=str(item.get('fps', '') or ''))
        key_var = tk.StringVar(value=str(item.get('key', '') or ''))
        ttk.Entry(outer, textvariable=fps_var).pack(fill='x', pady=(4, 10))
        ttk.Label(outer, text='Press any keyboard or mouse button:').pack(anchor='w')
        key_entry = ttk.Entry(outer, textvariable=key_var)
        key_entry.pack(fill='x', pady=(4, 6))
        ttk.Label(outer, text='Examples: F7, Insert, Mouse1, Mouse4, A, ;', foreground='#9aa0a6').pack(anchor='w')

        def capture(event):
            if getattr(event, 'num', None) is not None:
                key_var.set({1: 'MOUSE1', 2: 'MOUSE2', 3: 'MOUSE3', 4: 'MOUSE4', 5: 'MOUSE5'}.get(event.num, f'MOUSE{event.num}'))
            else:
                key = str(event.keysym or '').upper()
                key_var.set('ESC' if key == 'ESCAPE' else key)
            return 'break'
        key_entry.bind('<KeyPress>', capture)
        for n in range(1, 6):
            key_entry.bind(f'<Button-{n}>', capture)

        def save():
            try:
                fps = int(fps_var.get().strip())
            except Exception:
                messagebox.showerror('FPS Hotkey', 'FPS must be a whole number from 1 to 240.', parent=dlg)
                return
            key = key_var.get().strip().upper()
            if not 1 <= fps <= 240 or not key or (not fflag_key_to_vk(key)):
                messagebox.showerror('FPS Hotkey', 'Enter FPS 1-240 and a supported key.', parent=dlg)
                return
            for i, other in enumerate(self.fps_hotkey_slots):
                if i != index and other.get('key', '').upper() == key:
                    messagebox.showerror('FPS Hotkey', 'That key is already assigned.', parent=dlg)
                    return
            self.fps_hotkey_slots[index] = {'fps': fps, 'key': key}
            self._sync_fps_hotkey_slots()
            self._save_settings()
            self._refresh_fps_hotkey_buttons()
            dlg.destroy()
        btns = ttk.Frame(outer)
        btns.pack(fill='x', pady=(14, 0))
        ttk.Button(btns, text='Save', command=save).pack(side='left')
        ttk.Button(btns, text='Clear', command=lambda: (self.fps_hotkey_slots.__setitem__(index, {'fps': 0, 'key': ''}), self._sync_fps_hotkey_slots(), self._save_settings(), self._refresh_fps_hotkey_buttons(), dlg.destroy())).pack(side='left', padx=6)
        ttk.Button(btns, text='Cancel', command=dlg.destroy).pack(side='right')
        key_entry.focus_set()

    def _refresh_fps_hotkey_buttons(self):
        if not hasattr(self, '_fps_hotkey_buttons'):
            return
        for index, button in list(self._fps_hotkey_buttons.items()):
            if index >= len(self.fps_hotkey_slots):
                try:
                    button.destroy()
                except Exception:
                    pass
                self._fps_hotkey_buttons.pop(index, None)
                continue
            item = self.fps_hotkey_slots[index]
            fps, key = (item.get('fps', 0), str(item.get('key', '') or '').upper())
            button.config(text=f'{fps} FPS [{key}]' if fps and key else 'Empty')

    def _add_fps_hotkey_slot(self):
        if len(self.fps_hotkey_slots) >= 15:
            return
        self.fps_hotkey_slots.append({'fps': 0, 'key': ''})
        self._sync_fps_hotkey_slots()
        self._save_settings()
        self._build_fps_hotkey_buttons()

    def _build_fps_hotkey_buttons(self):
        frame = getattr(self, '_fps_hotkey_frame', None)
        if frame is None:
            return
        for child in frame.winfo_children():
            child.destroy()
        self._fps_hotkey_buttons = {}
        for index in range(len(self.fps_hotkey_slots)):
            button = ttk.Button(frame, text='Empty', width=9, command=lambda slot=index: self._fps_slot_editor(slot), padding=(3, 1))
            button.grid(row=index // 5, column=index % 5, padx=2, pady=2, sticky='ew')
            self._fps_hotkey_buttons[index] = button
        plus_col = len(self.fps_hotkey_slots) % 5
        plus_row = len(self.fps_hotkey_slots) // 5
        if len(self.fps_hotkey_slots) < 15:
            plus = ttk.Button(frame, text='+', width=3, command=self._add_fps_hotkey_slot, padding=(2, 1))
            plus.grid(row=plus_row, column=plus_col, padx=2, pady=2, sticky='ew')
        for col in range(5):
            frame.columnconfigure(col, weight=1)
        self._refresh_fps_hotkey_buttons()

    def _reset_fps_hotkeys(self):
        self.fps_hotkey_slots = [{'fps': 0, 'key': ''}]
        self._sync_fps_hotkey_slots()
        self._hotkey_prev.clear()
        self._save_settings()
        self._build_fps_hotkey_buttons()

    def _handle_fflag_hotkey(self, binding):
        flag_name = fflag_strip_prefix(str(binding.get('flag', '')).strip())
        if not flag_name:
            return
        actual = None
        for item in self.fflag_hotkeys:
            if str(item.get('key', '')).upper() == str(binding.get('key', '')).upper() and fflag_strip_prefix(str(item.get('flag', ''))) == flag_name:
                actual = item
                break
        if actual is None:
            return
        value1 = str(actual.get('value1', 'true'))
        value2 = str(actual.get('value2', 'false'))
        state = bool(actual.get('state', False))
        new_value = value2 if state else value1
        actual['state'] = not state
        found = None
        for flag in self.fflag_flags:
            if fflag_strip_prefix(flag.get('name', '')) == flag_name:
                found = flag
                break
        if found is None:
            found = {'name': flag_name, 'value': new_value, 'type': fflag_infer_type(new_value)}
            self.fflag_flags.append(found)
        else:
            found['value'] = new_value
            found['type'] = fflag_infer_type(new_value)
        self._save_fflag_flags()
        self._save_settings()
        self._refresh_fflag_list()
        if self.fflag_pid and self.fflag_engine.handle:
            try:
                self.fflag_engine.get_singleton()
                self.fflag_engine.set_flag_with_prefixes(flag_name, new_value)
                self.fflag_status.config(text=f'{flag_name} = {new_value}', foreground='#65d98b')
            except Exception:
                pass

    def _fflag_hotkeys_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title('FFlag Hotkeys')
        dlg.geometry('900x500')
        dlg.transient(self)
        theme_toplevel(dlg)
        outer = ttk.Frame(dlg, padding=12)
        outer.pack(fill='both', expand=True)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(1, weight=1)
        ttk.Label(outer, text='Global FFlag Hotkeys', font=('Segoe UI Semibold', 13)).grid(row=0, column=0, sticky='w', pady=(0, 8))
        cols = ('key', 'flag', 'mode', 'value1', 'value2')
        tree = ttk.Treeview(outer, columns=cols, show='headings', selectmode='browse')
        headers = {'key': 'KEY', 'flag': 'FFLAG', 'mode': 'MODE', 'value1': 'TOGGLE 1', 'value2': 'TOGGLE 2'}
        widths = {'key': 100, 'flag': 320, 'mode': 100, 'value1': 140, 'value2': 140}
        for col in cols:
            tree.heading(col, text=headers[col])
            tree.column(col, width=widths[col], anchor='w')
        tree.grid(row=1, column=0, sticky='nsew')

        def refresh():
            tree.delete(*tree.get_children())
            for i, item in enumerate(self.fflag_hotkeys):
                tree.insert('', 'end', iid=str(i), values=(item.get('key', ''), item.get('flag', ''), item.get('mode', 'Toggle'), item.get('value1', 'true'), item.get('value2', 'false')))

        def edit():
            sel = tree.selection()
            if not sel:
                return
            idx = int(sel[0])
            self._fflag_hotkey_editor(idx, dlg, refresh)
        btns = ttk.Frame(outer)
        btns.grid(row=2, column=0, sticky='ew', pady=(8, 0))
        ttk.Button(btns, text='+ Add Hotkey', command=lambda: self._fflag_hotkey_editor(None, dlg, refresh)).pack(side='left')
        ttk.Button(btns, text='Edit', command=edit).pack(side='left', padx=5)
        ttk.Button(btns, text='Remove', command=lambda: self._remove_fflag_hotkey(tree, refresh)).pack(side='left')
        ttk.Button(btns, text='Close', command=dlg.destroy).pack(side='right')
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
        dlg.title('FFlag Hotkey')
        dlg.transient(parent)
        theme_toplevel(dlg)
        existing = self.fflag_hotkeys[index] if index is not None else {}
        key_var = tk.StringVar(value=str(existing.get('key', '')))
        flag_var = tk.StringVar(value=str(existing.get('flag', '')))
        mode_var = tk.StringVar(value=str(existing.get('mode', 'Toggle')))
        v1_var = tk.StringVar(value=str(existing.get('value1', 'true')))
        v2_var = tk.StringVar(value=str(existing.get('value2', 'false')))
        ttk.Label(dlg, text='Key:').grid(row=0, column=0, padx=10, pady=(12, 4), sticky='w')
        key_entry = ttk.Entry(dlg, textvariable=key_var, width=20)
        key_entry.grid(row=1, column=0, padx=10, sticky='ew')
        ttk.Label(dlg, text='FFlag:').grid(row=2, column=0, padx=10, pady=(8, 4), sticky='w')
        flag_combo = ttk.Combobox(dlg, textvariable=flag_var, values=[x.get('name', '') for x in self.fflag_flags], width=48)
        flag_combo.grid(row=3, column=0, padx=10, sticky='ew')
        ttk.Label(dlg, text='Action:').grid(row=4, column=0, padx=10, pady=(8, 4), sticky='w')
        mode_combo = ttk.Combobox(dlg, textvariable=mode_var, values=['Toggle'], state='readonly', width=20)
        mode_combo.grid(row=5, column=0, padx=10, sticky='w')
        ttk.Label(dlg, text='Toggle 1 value:').grid(row=6, column=0, padx=10, pady=(8, 4), sticky='w')
        ttk.Entry(dlg, textvariable=v1_var, width=30).grid(row=7, column=0, padx=10, sticky='ew')
        ttk.Label(dlg, text='Toggle 2 value:').grid(row=8, column=0, padx=10, pady=(8, 4), sticky='w')
        ttk.Entry(dlg, textvariable=v2_var, width=30).grid(row=9, column=0, padx=10, sticky='ew')
        ttk.Label(dlg, text='Example: K + DebugDrawBroadPhaseAABBs + true/false toggles the value globally.', foreground='#9aa0a6').grid(row=10, column=0, padx=10, pady=(8, 4), sticky='w')

        def capture_key(event):
            if event.keysym in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
                return 'break'
            key = event.keysym.upper()
            if key == 'ESCAPE':
                key = 'ESC'
            key_var.set(key)
            return 'break'
        key_entry.bind('<KeyPress>', capture_key)

        def save():
            key = key_var.get().strip().upper()
            flag = fflag_strip_prefix(flag_var.get().strip())
            if not key or not fflag_key_to_vk(key):
                messagebox.showerror('FFlag Hotkeys', 'Enter a supported keyboard key.', parent=dlg)
                return
            if not flag:
                messagebox.showerror('FFlag Hotkeys', 'Enter an FFlag name.', parent=dlg)
                return
            item = {'key': key, 'flag': flag, 'mode': 'Toggle', 'value1': v1_var.get(), 'value2': v2_var.get(), 'state': bool(existing.get('state', False))}
            if index is None:
                self.fflag_hotkeys.append(item)
            else:
                self.fflag_hotkeys[index] = item
            self._save_settings()
            refresh()
            dlg.destroy()
        btns = ttk.Frame(dlg)
        btns.grid(row=11, column=0, pady=12)
        ttk.Button(btns, text='Save', command=save).pack(side='left', padx=4)
        ttk.Button(btns, text='Cancel', command=dlg.destroy).pack(side='left', padx=4)
        dlg.columnconfigure(0, weight=1)
        for button_number in range(1, 6):
            key_entry.bind(f'<Button-{button_number}>', lambda event, n=button_number: (key_var.set(f'MOUSE{n}'), 'break')[1])
        key_entry.focus_set()

    def _apply_streamer_mode(self, _retry=0):
        if sys.platform != 'win32' or not self.winfo_exists():
            return
        try:

            user32 = ctypes.WinDLL('user32', use_last_error=True)
            SetWindowDisplayAffinity = user32.SetWindowDisplayAffinity
            SetWindowDisplayAffinity.argtypes = [ctypes.wintypes.HWND, ctypes.wintypes.DWORD]
            SetWindowDisplayAffinity.restype = ctypes.wintypes.BOOL
            WDA_NONE = 0
            WDA_EXCLUDEFROMCAPTURE = 17
            hwnd = ctypes.wintypes.HWND(int(self.winfo_id()))
            foreground = user32.GetForegroundWindow()
            if foreground:
                try:
                    foreground_pid = ctypes.wintypes.DWORD()
                    user32.GetWindowThreadProcessId(foreground, ctypes.byref(foreground_pid))
                    if foreground_pid.value == os.getpid():
                        hwnd = ctypes.wintypes.HWND(foreground)
                except Exception:
                    pass
            affinity = WDA_EXCLUDEFROMCAPTURE if self.streamer_mode.get() else WDA_NONE
            if SetWindowDisplayAffinity(hwnd, affinity):
                return
            error = ctypes.get_last_error()
            if _retry < 5:
                self.after(150, lambda: self._apply_streamer_mode(_retry + 1))
                return
            if self.streamer_mode.get():
                self.settings['streamer_mode'] = False
                self._save_settings()
                try:
                    self.streamer_mode.set(False)
                except Exception:
                    pass
        except Exception:
            if _retry < 5:
                try:
                    self.after(150, lambda: self._apply_streamer_mode(_retry + 1))
                except Exception:
                    pass

    def _startup_focus_cycle(self):
        try:
            if self.state() != 'normal':
                return
            self._restore_windows_taskbar_presence()
            self.iconify()
            self.after(180, lambda: (self.deiconify(), self._restore_windows_taskbar_presence()))
        except Exception:
            pass

    def _restore_windows_taskbar_presence(self):
        if sys.platform != 'win32' or not self.winfo_exists():
            return
        try:
            _prepare_borderless_appwindow(self)
            _apply_native_titlebar_theme(self)
            if os.path.isfile(ICON_PATH):
                user32 = ctypes.windll.user32
                hwnd = _win32_root_hwnd(self)
                hicon = user32.LoadImageW(None, ICON_PATH, 1, 32, 32, 16 | 64)
                if hicon and hwnd:
                    user32.SendMessageW(hwnd, 128, 1, hicon)
                    user32.SendMessageW(hwnd, 128, 0, hicon)
        except Exception:
            pass

    def _setup_custom_titlebar(self):
        self._prepare_borderless = True
        self._titlebar = tk.Frame(self, bg='#080808', height=38, bd=0, highlightthickness=0)
        self._titlebar.pack(fill='x', side='top')
        self._titlebar.pack_propagate(False)
        self._titlebar_canvas = tk.Canvas(self._titlebar, bg='#080808', bd=0, highlightthickness=0, height=38)
        self._titlebar_canvas.pack(fill='both', expand=True)
        self._titlebar_canvas.create_text(0, 19, text='RoUtils', anchor='center', fill='#f2f2f2', font=('Segoe UI Semibold', 10), tags=('title',))
        self._titlebar_buttons = {}
        self._kill_ro_utils_items = None
        controls = (('close', '#ff5f57', self._titlebar_close), ('max', '#28c840', self._titlebar_toggle_maximize), ('min', '#febc2e', self._titlebar_minimize))
        for name, color, command in controls:
            item = self._titlebar_canvas.create_oval(0, 0, 14, 14, fill=color, outline='', tags=(f'btn_{name}',))
            self._titlebar_buttons[name] = (item, command, color)
        self._titlebar_canvas.bind('<Configure>', self._layout_titlebar, add='+')
        self._titlebar_canvas.bind('<Button-1>', self._titlebar_press, add='+')
        self._titlebar_canvas.bind('<B1-Motion>', self._titlebar_drag, add='+')
        self._titlebar_canvas.bind('<ButtonRelease-1>', self._titlebar_release, add='+')
        self._titlebar_canvas.bind('<Motion>', self._titlebar_motion, add='+')
        self._titlebar_drag_data = None
        self._titlebar_last_xy = None
        self._titlebar_last_layout_width = 0
        self._titlebar_drag_job = None
        self._titlebar_drag_interval_ms = 16
        self._titlebar_move_step_px = 4
        self.after_idle(self._restore_windows_taskbar_presence)

    def _update_kill_routils_visibility(self):
        try:
            enabled = bool(self.hide_to_tray_on_close.get())
        except Exception:
            enabled = bool(self.settings.get('hide_to_tray_on_close', False))
        try:
            if enabled and (not getattr(self, '_kill_ro_utils_items', None)):
                dot = self._titlebar_canvas.create_oval(0, 0, 14, 14, fill='#ff3b30', outline='', tags=('kill_ro_utils',))
                label = self._titlebar_canvas.create_text(0, 19, text='Kill RoUtils', anchor='w', fill='#f2f2f2', font=('Segoe UI Semibold', 9), tags=('kill_ro_utils',))
                self._kill_ro_utils_items = (dot, label)
                self._titlebar_canvas.tag_bind(dot, '<Button-1>', lambda e: self._kill_ro_utils(), add='+')
                self._titlebar_canvas.tag_bind(dot, '<ButtonRelease-1>', lambda e: self._kill_ro_utils(), add='+')
                self._titlebar_canvas.tag_bind(label, '<Button-1>', lambda e: self._kill_ro_utils(), add='+')
                self._titlebar_canvas.tag_bind(label, '<ButtonRelease-1>', lambda e: self._kill_ro_utils(), add='+')
            elif not enabled and getattr(self, '_kill_ro_utils_items', None):
                for item in self._kill_ro_utils_items:
                    self._titlebar_canvas.delete(item)
                self._kill_ro_utils_items = None
            self._layout_titlebar(force=True)
        except Exception:
            pass

    def _kill_ro_utils(self):
        try:
            pid = os.getpid()
            if os.name == 'nt':
                PROCESS_TERMINATE = 1
                kernel32 = ctypes.windll.kernel32
                kernel32.OpenProcess.restype = ctypes.wintypes.HANDLE
                kernel32.OpenProcess.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.BOOL, ctypes.wintypes.DWORD]
                kernel32.TerminateProcess.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.UINT]
                kernel32.TerminateProcess.restype = ctypes.wintypes.BOOL
                kernel32.CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
                kernel32.CloseHandle.restype = ctypes.wintypes.BOOL
                handle = kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
                if handle:
                    kernel32.TerminateProcess(handle, 1)
                    kernel32.CloseHandle(handle)
                    return
            os._exit(1)
        except BaseException:
            try:
                os._exit(1)
            except BaseException:
                pass

    def _layout_titlebar(self, event=None, force=False):
        try:
            w = max(160, self._titlebar_canvas.winfo_width())
            if w == getattr(self, '_titlebar_last_layout_width', 0) and (not force):
                return
            self._titlebar_last_layout_width = w
            self._titlebar_canvas.coords('title', w / 2, 19)
            kill_items = getattr(self, '_kill_ro_utils_items', None)
            if kill_items:
                self._titlebar_canvas.coords(kill_items[0], 10, 12, 24, 26)
                self._titlebar_canvas.coords(kill_items[1], 31, 19)
            x = w - 25
            for name in ('close', 'max', 'min'):
                item = self._titlebar_buttons[name][0]
                self._titlebar_canvas.coords(item, x, 12, x + 14, 26)
                x -= 23
        except Exception:
            pass

    def _titlebar_hit(self, x, y):
        kill_items = getattr(self, '_kill_ro_utils_items', None)
        if kill_items:
            for item in kill_items:
                box = self._titlebar_canvas.bbox(item)
                if box and box[0] - 6 <= x <= box[2] + 6 and (box[1] - 6 <= y <= box[3] + 6):
                    return ('kill_ro_utils', self._kill_ro_utils)
        for name, (item, command, _color) in self._titlebar_buttons.items():
            coords = self._titlebar_canvas.coords(item)
            if coords and coords[0] <= x <= coords[2] and (coords[1] <= y <= coords[3]):
                return (name, command)
        return (None, None)

    def _titlebar_press(self, event):
        name, _ = self._titlebar_hit(event.x, event.y)
        if name:
            self._titlebar_drag_data = ('button', name)
            return 'break'
        if getattr(self, '_custom_maximized', False):
            return 'break'
        self._titlebar_drag_data = ('drag', event.x_root, event.y_root, self.winfo_x(), self.winfo_y())
        return 'break'

    def _titlebar_drag(self, event):
        data = self._titlebar_drag_data
        if not data or data[0] != 'drag':
            return 'break'
        _, sx, sy, ox, oy = data
        new_x = int(ox + event.x_root - sx)
        new_y = int(oy + event.y_root - sy)
        step = max(1, int(getattr(self, '_titlebar_move_step_px', 4)))
        self._titlebar_pending_xy = (round(new_x / step) * step, round(new_y / step) * step)
        if self._titlebar_drag_job is None:

            def apply_drag():
                self._titlebar_drag_job = None
                xy = getattr(self, '_titlebar_pending_xy', None)
                if not xy or xy == self._titlebar_last_xy:
                    return
                last = getattr(self, '_titlebar_last_xy', None)
                if last and abs(xy[0] - last[0]) < 2 and abs(xy[1] - last[1]) < 2:
                    return
                self._titlebar_last_xy = xy
                try:
                    if sys.platform == 'win32':
                        hwnd = _win32_root_hwnd(self)
                        if hwnd:
                            ctypes.windll.user32.SetWindowPos(hwnd, 0, xy[0], xy[1], 0, 0, 1 | 4 | 16)
                            return
                    self.geometry(f'+{xy[0]}+{xy[1]}')
                except Exception:
                    pass
            self._titlebar_drag_job = self.after(getattr(self, '_titlebar_drag_interval_ms', 42), apply_drag)
        return 'break'

    def _titlebar_release(self, event):
        data = self._titlebar_drag_data
        self._titlebar_drag_data = None
        if self._titlebar_drag_job is not None:
            try:
                self.after_cancel(self._titlebar_drag_job)
            except Exception:
                pass
            self._titlebar_drag_job = None
        if data and data[0] == 'drag':
            xy = getattr(self, '_titlebar_pending_xy', None)
            last = getattr(self, '_titlebar_last_xy', None)
            if xy and (last is None or abs(xy[0] - last[0]) >= 1 or abs(xy[1] - last[1]) >= 1):
                try:
                    if sys.platform == 'win32':
                        hwnd = _win32_root_hwnd(self)
                        if hwnd:
                            ctypes.windll.user32.SetWindowPos(hwnd, 0, int(xy[0]), int(xy[1]), 0, 0, 1 | 4 | 16)
                        else:
                            self.geometry(f'+{int(xy[0])}+{int(xy[1])}')
                    else:
                        self.geometry(f'+{int(xy[0])}+{int(xy[1])}')
                except Exception:
                    pass
            return 'break'
        if data and data[0] == 'button':
            name = data[1]
            if name == 'close':
                self._titlebar_close()
            elif name == 'max':
                self._titlebar_toggle_maximize()
            elif name == 'min':
                self._titlebar_minimize()
        return 'break'

    def _titlebar_motion(self, event):
        name, _ = self._titlebar_hit(event.x, event.y)
        self._titlebar_canvas.configure(cursor='hand2' if name else '')
        return 'break'

    def _titlebar_close(self):
        self._on_close()

    def _titlebar_minimize(self):
        try:
            self.iconify()
        except Exception:
            try:
                self.state('iconic')
            except Exception:
                pass

    def _titlebar_toggle_maximize(self):
        try:
            if self.state() == 'zoomed' or getattr(self, '_custom_maximized', False):
                self.state('normal')
                self._custom_maximized = False
            else:
                self.state('zoomed')
                self._custom_maximized = True
        except Exception:
            pass

    def _refresh_tab_nav(self):
        if not hasattr(self, '_tab_nav_inner') or not hasattr(self, 'nb'):
            return
        try:
            active_id = str(self.nb.select()) if self.nb.select() else ''
            current_tabs = list(self.nb.tabs())
            buttons = getattr(self, '_tab_nav_buttons', {})
            for tab_id in tuple(buttons):
                if tab_id not in current_tabs:
                    try:
                        buttons[tab_id].destroy()
                    except Exception:
                        pass
                    buttons.pop(tab_id, None)
            for tab_id in current_tabs:
                name = str(self.nb.tab(tab_id, 'text'))
                button = buttons.get(tab_id)
                if button is None or not button.winfo_exists():
                    button = ttk.Button(self._tab_nav_inner, text=name, takefocus=False, style='RoUtils.Nav.TButton', command=lambda tid=tab_id: self.nb.select(tid))
                    buttons[tab_id] = button
                else:
                    button.configure(text=name)
            self._tab_nav_buttons = buttons
            for tab_id in current_tabs:
                button = buttons[tab_id]
                button.pack_forget()
                button.pack(side='left', padx=2, pady=0)
            for tab_id, button in buttons.items():
                selected = tab_id == active_id
                button.configure(style='RoUtils.ActiveNav.TButton' if selected else 'RoUtils.Nav.TButton')
        except Exception:
            pass

    def _setup_tab_nav_styles(self):
        style = ttk.Style(self)
        self._tab_nav_buttons = {}
        try:
            style.configure('RoUtils.Nav.TButton', padding=(7, 4), font=('Segoe UI Semibold', 9))
            style.configure('RoUtils.ActiveNav.TButton', padding=(7, 4), font=('Segoe UI Semibold', 9), foreground=_CURRENT_PALETTE.get('accent', '#7f8cff'))
        except Exception:
            pass

    def _install_global_scroll_support(self):

        def wheel(event):
            try:
                x, y = (event.x_root, event.y_root)
                target = None
                w = self.winfo_containing(x, y)
                while w is not None:
                    if isinstance(w, (tk.Scrollbar, ttk.Scrollbar)):
                        return 'break'
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
                            cx, cy = (child.canvas.winfo_rootx(), child.canvas.winfo_rooty())
                            cw, ch = (child.canvas.winfo_width(), child.canvas.winfo_height())
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
        middle = {'target': None, 'y': None}

        def middle_target(event):
            w = self.winfo_containing(event.x_root, event.y_root)
            over_scrollbar = False
            while w is not None:
                if isinstance(w, (tk.Scrollbar, ttk.Scrollbar)):
                    over_scrollbar = True
                    break
                if isinstance(w, _ScrollableTab):
                    return w.canvas
                if isinstance(w, tk.Canvas):
                    try:
                        if w.cget('yscrollcommand'):
                            return w
                    except Exception:
                        pass
                try:
                    parent = w.nametowidget(w.winfo_parent())
                    if parent is w:
                        break
                    w = parent
                except Exception:
                    break
            if over_scrollbar:
                return None
            try:
                selected = self.nb.select() if hasattr(self, 'nb') else ''
                page = self.nametowidget(selected) if selected else None
                if isinstance(page, _ScrollableTab) and page.winfo_ismapped():
                    return page.canvas

                def active_canvas(parent):
                    for child in parent.winfo_children():
                        if isinstance(child, tk.Canvas):
                            try:
                                if child.cget('yscrollcommand') and child.winfo_ismapped():
                                    return child
                            except Exception:
                                pass
                        found = active_canvas(child)
                        if found is not None:
                            return found
                    return None
                if page is not None and page.winfo_ismapped():
                    canvas = active_canvas(page)
                    if canvas is not None:
                        return canvas
            except Exception:
                pass

            def find_scroll_canvas(parent):
                try:
                    for child in parent.winfo_children():
                        if isinstance(child, tk.Canvas):
                            x0, y0 = (child.winfo_rootx(), child.winfo_rooty())
                            x1, y1 = (x0 + child.winfo_width(), y0 + child.winfo_height())
                            if x0 <= event.x_root <= x1 and y0 <= event.y_root <= y1 and child.cget('yscrollcommand'):
                                return child
                        found = find_scroll_canvas(child)
                        if found is not None:
                            return found
                except Exception:
                    pass
                return None
            return find_scroll_canvas(self)

        def middle_press(event):
            middle['target'] = middle_target(event)
            middle['y'] = event.y_root if middle['target'] is not None else None
            return 'break'

        def middle_drag(event):
            target = middle.get('target')
            if target is not None and middle.get('y') is not None:
                target.yview_scroll(int((middle['y'] - event.y_root) / 2), 'units')
                middle['y'] = event.y_root
                return 'break'

        def middle_release(_event):
            middle['target'] = None
            middle['y'] = None
            return 'break'
        self.bind_all('<Button-2>', middle_press, add='+')
        self.bind_all('<B2-Motion>', middle_drag, add='+')
        self.bind_all('<ButtonRelease-2>', middle_release, add='+')
        middle_tag = 'RoUtilsMiddleScroll'
        self.bind_class(middle_tag, '<ButtonPress-2>', middle_press)
        self.bind_class(middle_tag, '<B2-Motion>', middle_drag)
        self.bind_class(middle_tag, '<ButtonRelease-2>', middle_release)

        def attach_middle_tag(parent):
            try:
                for child in parent.winfo_children():
                    if isinstance(child, (tk.Scrollbar, ttk.Scrollbar)):
                        child.bind('<Button-2>', lambda _e: 'break', add='+')
                        child.bind('<B2-Motion>', lambda _e: 'break', add='+')
                        child.bind('<ButtonRelease-2>', lambda _e: 'break', add='+')
                    tags = list(child.bindtags())
                    if middle_tag not in tags:
                        child.bindtags((middle_tag, *tags))
                    attach_middle_tag(child)
            except Exception:
                pass
        attach_middle_tag(self)

    def _apply_titlebar_theme(self):
        try:
            _apply_native_titlebar_theme(self)
        except Exception:
            pass
        try:
            style = ttk.Style(self)
            style.configure('RoUtils.ActiveNav.TButton', foreground=_CURRENT_PALETTE.get('accent', '#7f8cff'))
        except Exception:
            pass
        self._refresh_tab_nav()

    def _build_themes_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.add(tab, text='Themes')
        ttk.Label(tab, text='Themes', font=('Segoe UI Semibold', 15)).pack(anchor='w')
        ttk.Label(tab, text='Choose a complete UI palette or create your own.', foreground='#9aa0a6').pack(anchor='w', pady=(0, 10))
        outer = ttk.Frame(tab)
        outer.pack(fill='both', expand=True)
        left = ttk.Frame(outer)
        left.pack(side='left', fill='both', expand=True)
        right = ttk.LabelFrame(outer, text='Custom Theme', padding=12)
        right.pack(side='right', fill='y', padx=(14, 0))
        self.theme_var = tk.StringVar(value=self.settings.get('theme', DEFAULT_THEME))
        lb = tk.Listbox(left, bg=_CURRENT_PALETTE['bg_medium'], fg=_CURRENT_PALETTE['fg'], selectbackground=_CURRENT_PALETTE['accent'], relief='flat', bd=0)
        lb.pack(fill='both', expand=True)
        for name in THEME_NAMES:
            lb.insert('end', name)
        try:
            lb.selection_set(THEME_NAMES.index(self.theme_var.get()))
        except Exception:
            pass
        lb.bind('<<ListboxSelect>>', lambda _e: self._theme_list_apply(lb))
        self.custom_theme_vars = {}
        custom = self.settings.get('custom_theme', {})
        for key in ('bg_dark', 'bg_medium', 'bg_light', 'bg_hover', 'fg', 'accent', 'border'):
            row = ttk.Frame(right)
            row.pack(fill='x', pady=3)
            ttk.Label(row, text=key, width=10).pack(side='left')
            v = tk.StringVar(value=custom.get(key, THEMES[DEFAULT_THEME][key]))
            self.custom_theme_vars[key] = v
            ttk.Entry(row, textvariable=v, width=12).pack(side='left')
        ttk.Button(right, text='Apply Custom', command=self._apply_custom_theme).pack(fill='x', pady=(10, 4))
        ttk.Button(right, text='Save Custom', command=self._save_custom_theme).pack(fill='x')

    def _theme_list_apply(self, lb):
        sel = lb.curselection()
        if not sel:
            return
        self.theme_var.set(lb.get(sel[0]))
        self._apply_theme()

    def _apply_custom_theme(self):
        palette = {k: v.get().strip() for k, v in self.custom_theme_vars.items()}
        self.settings['theme'] = 'Custom'
        self.settings['custom_theme'] = palette
        apply_visual_polish(self, theme=UI_THEME, palette=palette)
        darken_menus(self._collect_menus())
        self._save_settings()

    def _save_custom_theme(self):
        self._apply_custom_theme()
        messagebox.showinfo('Themes', 'Custom theme saved.', parent=self)

    def _apply_theme(self):
        name = self.theme_var.get()
        self.settings['theme'] = name
        palette = self.settings.get('custom_theme', THEMES[DEFAULT_THEME]) if name == 'Custom' else THEMES.get(name, THEMES[DEFAULT_THEME])
        try:
            apply_visual_polish(self, theme=UI_THEME, palette=palette)
        except Exception:
            pass
        self._apply_titlebar_theme()
        darken_menus(self._collect_menus())
        for w in (self._ctx, self._colmenu, getattr(self.replacer, 'ctx_menu', None)):
            if w is not None:
                try:
                    w.configure(bg=palette['bg_dark'], fg=palette['fg'], activebackground=palette['accent'], activeforeground='#ffffff')
                except Exception:
                    pass
        if hasattr(self, '_titlebar'):
            try:
                self._titlebar.configure(bg=_CURRENT_PALETTE['bg_dark'])
                for child in self._titlebar.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=_CURRENT_PALETTE['bg_dark'], fg=_CURRENT_PALETTE['fg'])
            except Exception:
                pass
        if getattr(self, 'viewport_3d', None) is not None and self.viewport_3d.winfo_ismapped():
            self.viewport_3d.draw_frame()
        self._save_settings()

    def _collect_menus(self):
        out = []
        try:
            m = self.nametowidget(self.cget('menu'))
            if m:
                out.append(m)
                for i in range(m.index('end') + 1 if m.index('end') is not None else 0):
                    try:
                        sub = m.entrycget(i, 'menu')
                        if sub:
                            out.append(sub)
                    except Exception:
                        pass
        except Exception:
            pass
        return out

    def _fflag_path(self):
        return os.path.join(DATA_DIR, 'routils_fflags.json')

    def _load_fflag_flags(self):
        try:
            with open(self._fflag_path(), 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.fflag_flags = data if isinstance(data, list) else []
        except Exception:
            self.fflag_flags = []

    def _save_fflag_flags(self):
        try:
            with open(self._fflag_path(), 'w', encoding='utf-8') as f:
                json.dump(self.fflag_flags, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror('FFlags', f'Failed to save flags:\n{e}', parent=self)

    def _wrap_rbxm_as_blob(self, data: bytes, content_type: str='application/octet-stream') -> bytes:
        if data[:4] == RBXH_MAGIC:
            return _wrap_rbxm_bytes(_extract_rbxh_document(data), content_type)
        return _wrap_rbxm_bytes(data, content_type)

    def _utils_r6_to_r15(self):
        src = filedialog.askopenfilename(parent=self, title='R6 Animation → R15', filetypes=[('Roblox Animation', '*.rbxm *.rbxmx'), ('All files', '*.*')])
        if not src:
            return
        try:
            with open(src, 'rb') as f:
                data = f.read()
            out = convert_r6_animation_to_r15(data)
            base = os.path.splitext(os.path.basename(src))[0] + '_R15.rbxmx'
            dest = filedialog.asksaveasfilename(parent=self, title='Save R15 Animation', initialfile=base, defaultextension='.rbxmx', filetypes=[('RBXMX Animation', '*.rbxmx'), ('All files', '*.*')])
            if not dest:
                return
            with open(dest, 'wb') as f:
                f.write(out)
            messagebox.showinfo('R6 → R15', f'R6 animation retargeted to R15.\n\n{dest}', parent=self)
            self._console_log(f'Converted R6 animation to R15: {dest}')
        except Exception as e:
            messagebox.showerror('R6 → R15', f'Could not convert animation:\n{e}', parent=self)

    def _cc_state_path(self):
        return os.path.join(DATA_DIR, 'routils_cconfigs_state.json')

    def _cc_load_applied_state(self):
        try:
            with open(self._cc_state_path(), 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.cc_applied_caches = data if isinstance(data, list) else []
        except Exception:
            self.cc_applied_caches = []

    def _cc_save_applied_state(self):
        try:
            with open(self._cc_state_path(), 'w', encoding='utf-8') as f:
                json.dump(self.cc_applied_caches, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _cc_record_applied_caches(self, caches):
        if not caches:
            return
        now = datetime.now().isoformat(timespec='seconds')
        by_hash = {}
        for item in self.cc_applied_caches:
            if isinstance(item, dict):
                h = str(item.get('hash', '')).lower()
                if h:
                    by_hash[h] = item
        for item in caches:
            if not isinstance(item, dict):
                continue
            h = re.sub('[^0-9A-Fa-f]', '', str(item.get('hash', ''))).lower()
            if not h:
                continue
            by_hash[h] = {'hash': h, 'name': str(item.get('name', '')), 'applied_at': str(item.get('applied_at') or now)}
        self.cc_applied_caches = list(by_hash.values())
        self._cc_save_applied_state()
        if hasattr(self, 'cc_cache_count_label'):
            self.cc_cache_count_label.config(text=f'Current applied caches: {len(self.cc_applied_caches)}')

    def _cc_safe_name(self, name):
        name = re.sub('[<>:"/\\\\\\\\|?*]', '_', str(name)).strip().rstrip('.')
        return name or 'Config'

    def _cc_unique_path(self, directory, filename):
        base, ext = os.path.splitext(filename)
        path = os.path.join(directory, filename)
        i = 1
        while os.path.exists(path):
            path = os.path.join(directory, f'{base} ({i}){ext}')
            i += 1
        return path

    def _cc_snapshot_database(self, src_db, dst_db):
        if not os.path.isfile(src_db):
            raise FileNotFoundError(f'Database not found:\n{src_db}')
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
        src_db = getattr(self, 'db_path', None)
        if not src_db or not os.path.isfile(src_db):
            raise FileNotFoundError('The current rbx-storage.db does not exist.')
        with tempfile.TemporaryDirectory(prefix='routils_cc_') as td:
            snap = os.path.join(td, 'rbx-storage.db')
            self._cc_snapshot_database(src_db, snap)
            metadata = {'format': 'RoUtils CConfigs', 'version': 1, 'name': name, 'created_at': datetime.now().isoformat(timespec='seconds'), 'source_db': os.path.abspath(src_db), 'applied_caches': list(self.cc_applied_caches)}
            with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED) as z:
                z.write(snap, 'rbx-storage.db')
                z.writestr('config.json', json.dumps(metadata, ensure_ascii=False, indent=2))

    def _cc_read_package_info(self, path):
        if path.lower().endswith('.db'):
            conn = sqlite3.connect(path, timeout=3)
            try:
                conn.execute('PRAGMA schema_version').fetchone()
            finally:
                conn.close()
            return {'name': os.path.splitext(os.path.basename(path))[0], 'created_at': '', 'applied_caches': [], 'raw_db': True}
        with zipfile.ZipFile(path, 'r') as z:
            if 'config.json' not in z.namelist():
                raise ValueError('This is not a valid CConfigs package.')
            info = json.loads(z.read('config.json').decode('utf-8'))
            if 'rbx-storage.db' not in z.namelist():
                raise ValueError('CConfigs package is missing rbx-storage.db.')
            info['raw_db'] = False
            return info

    def _cc_scan_packages(self):
        out = []
        try:
            names = os.listdir(self.cconfigs_dir)
        except Exception:
            names = []
        for fname in names:
            if not fname.lower().endswith(('.ccdb', '.db')):
                continue
            path = os.path.join(self.cconfigs_dir, fname)
            try:
                info = self._cc_read_package_info(path)
            except Exception:
                info = {'name': os.path.splitext(fname)[0], 'created_at': '', 'applied_caches': []}
            info['_path'] = path
            info['_file'] = fname
            out.append(info)
        out.sort(key=lambda x: str(x.get('name', '')).lower())
        return out

    def _cc_refresh_list(self, select_path=None):
        if not hasattr(self, 'cc_tree'):
            return
        self.cc_tree.delete(*self.cc_tree.get_children())
        packages = self._cc_scan_packages()
        wanted = os.path.abspath(select_path) if select_path else None
        selected_iid = None
        for i, info in enumerate(packages):
            iid = str(i)
            caches = info.get('applied_caches') or []
            self.cc_tree.insert('', 'end', iid=iid, values=(info.get('name', os.path.splitext(info.get('_file', ''))[0]), info.get('created_at', ''), len(caches), info.get('_file', '')))
            if wanted and os.path.abspath(info.get('_path', '')) == wanted:
                selected_iid = iid
        if selected_iid is not None:
            self.cc_tree.selection_set(selected_iid)
            self.cc_tree.focus(selected_iid)
        self._cc_show_selected()

    def _cc_selected_info(self):
        sel = self.cc_tree.selection() if hasattr(self, 'cc_tree') else ()
        if not sel:
            return None
        try:
            idx = int(sel[0])
        except Exception:
            return None
        packages = self._cc_scan_packages()
        return packages[idx] if 0 <= idx < len(packages) else None

    def _cc_show_selected(self, _event=None):
        if not hasattr(self, 'cc_details'):
            return
        info = self._cc_selected_info()
        self.cc_details.configure(state='normal')
        self.cc_details.delete('1.0', tk.END)
        if not info:
            self.cc_details.insert(tk.END, 'Select a saved DB to view its details.')
        else:
            caches = info.get('applied_caches') or []
            lines = [f"Config: {info.get('name', '')}", f"Created: {info.get('created_at', '')}", f"File: {info.get('_file', '')}", '', f'Applied caches: {len(caches)}', '']
            if caches:
                for i, cache in enumerate(caches, 1):
                    name = cache.get('name', '(unnamed)')
                    h = cache.get('hash', '')
                    at = cache.get('applied_at', '')
                    lines.append(f'{i}. {name}')
                    lines.append(f'   Hash: {h}')
                    if at:
                        lines.append(f'   Applied: {at}')
            else:
                lines.append('No cache applications were recorded for this config.')
            self.cc_details.insert(tk.END, '\n'.join(lines))
        self.cc_details.configure(state='disabled')

    def _cc_save_db(self):
        name = simpledialog.askstring('Save DB', 'Enter a name for this CConfigs DB:', parent=self)
        if not name:
            return
        self._cc_save_named_config(name)

    def _cc_save_named_config(self, name):
        name = self._cc_safe_name(name)
        if not name:
            raise ValueError('Config name cannot be empty.')
        path = self._cc_unique_path(self.cconfigs_dir, name + '.ccdb')
        try:
            self._cc_make_package(path, name)
        except Exception as e:
            messagebox.showerror('CConfigs', f'Failed to save DB:\n{e}', parent=self)
            return
        self._cc_refresh_list(select_path=path)
        messagebox.showinfo('CConfigs', f"DB saved as '{os.path.basename(path)}'.\n\nRecorded applied caches: {len(self.cc_applied_caches)}", parent=self)

    def _cc_upload_db(self):
        path = filedialog.askopenfilename(parent=self, title='Upload DB', filetypes=[('Database files', '*.db *.ccdb'), ('SQLite DB', '*.db'), ('CConfigs DB', '*.ccdb'), ('All files', '*.*')])
        if not path:
            return
        try:
            info = self._cc_read_package_info(path)
            if path.lower().endswith('.db'):
                name = self._cc_safe_name(os.path.splitext(os.path.basename(path))[0] or 'rbx-storage')
                dest = self._cc_unique_path(self.cconfigs_dir, name + '.db')
            else:
                name = self._cc_safe_name(info.get('name') or os.path.splitext(os.path.basename(path))[0])
                dest = self._cc_unique_path(self.cconfigs_dir, name + '.ccdb')
            shutil.copy2(path, dest)
        except Exception as e:
            messagebox.showerror('CConfigs', f'Failed to upload DB:\n{e}', parent=self)
            return
        self._cc_refresh_list(select_path=dest)
        messagebox.showinfo('CConfigs', f"Uploaded '{os.path.basename(dest)}'.", parent=self)

    def _cc_apply_db(self):
        info = self._cc_selected_info()
        if not info:
            messagebox.showinfo('CConfigs', 'Select a saved DB first.', parent=self)
            return
        if not messagebox.askyesno('Apply DB', f"Apply '{info.get('name', '')}' to Roblox?\n\nThis will delete rbx-storage.db, rbx-storage.db-shm, rbx-storage.db-wal and rbx-storage.id, then install only rbx-storage.db.", parent=self):
            return
        was_watching = self.watching
        if was_watching:
            self._stop_watching()
        temp_source = None
        try:
            with tempfile.NamedTemporaryFile(prefix='routils_cc_apply_', suffix='.db', delete=False) as tf:
                temp_source = tf.name
            if info.get('raw_db') or info.get('_file', '').lower().endswith('.db'):
                shutil.copy2(info['_path'], temp_source)
            else:
                with tempfile.TemporaryDirectory(prefix='routils_apply_cc_') as td:
                    with zipfile.ZipFile(info['_path'], 'r') as z:
                        z.extract('rbx-storage.db', td)
                    shutil.copy2(os.path.join(td, 'rbx-storage.db'), temp_source)
            conn = sqlite3.connect(temp_source, timeout=3)
            conn.execute('PRAGMA schema_version').fetchone()
            conn.close()
            self._install_selected_db(temp_source)
            self.cc_applied_caches = list(info.get('applied_caches') or [])
            self._cc_save_applied_state()
            self._update_status()
            if was_watching:
                self._start_watching()
        except Exception as e:
            messagebox.showerror('CConfigs', f'Failed to apply DB.\n\n{e}\n\nClose Roblox and try again. No force-delete was used.', parent=self)
            if was_watching:
                self._start_watching()
            return
        finally:
            if temp_source:
                try:
                    os.remove(temp_source)
                except Exception:
                    pass
        if hasattr(self, 'cc_cache_count_label'):
            self.cc_cache_count_label.config(text=f'Current applied caches: {len(self.cc_applied_caches)}')
        messagebox.showinfo('CConfigs', f"Applied '{info.get('name', '')}'.\nRecorded caches: {len(self.cc_applied_caches)}\n\nInstalled only rbx-storage.db.", parent=self)

    def _cc_export_db(self):
        info = self._cc_selected_info()
        if not info:
            messagebox.showinfo('CConfigs', 'Select a saved DB first.', parent=self)
            return
        base = self._cc_safe_name(info.get('name') or 'config') + '.db'
        path = filedialog.asksaveasfilename(parent=self, title='Export DB as normal .db', initialfile=base, defaultextension='.db', filetypes=[('SQLite DB', '*.db'), ('All files', '*.*')])
        if not path:
            return
        temp_source = None
        try:
            with tempfile.NamedTemporaryFile(prefix='routils_cc_export_', suffix='.db', delete=False) as tf:
                temp_source = tf.name
            if info.get('raw_db') or info.get('_file', '').lower().endswith('.db'):
                shutil.copy2(info['_path'], temp_source)
            else:
                with zipfile.ZipFile(info['_path'], 'r') as z:
                    with z.open('rbx-storage.db') as src, open(temp_source, 'wb') as dst:
                        shutil.copyfileobj(src, dst)
            conn = sqlite3.connect(temp_source, timeout=3)
            conn.execute('PRAGMA schema_version').fetchone()
            conn.close()
            shutil.copy2(temp_source, path)
        except Exception as e:
            messagebox.showerror('CConfigs', f'Failed to export DB:\n{e}', parent=self)
            return
        finally:
            if temp_source:
                try:
                    os.remove(temp_source)
                except Exception:
                    pass
        messagebox.showinfo('CConfigs', f'Normal .db exported:\n{path}', parent=self)

    def _cc_delete_db(self):
        info = self._cc_selected_info()
        if not info:
            return
        if not messagebox.askyesno('Delete DB', f"Delete saved DB '{info.get('name', '')}'?", parent=self):
            return
        try:
            os.remove(info['_path'])
        except Exception as e:
            messagebox.showerror('CConfigs', f'Failed to delete DB:\n{e}', parent=self)
            return
        self._cc_refresh_list()

    def _build_cconfigs_tab(self):
        tab = ttk.Frame(self.nb, padding=0)
        self.nb.add(tab, text='Configs')
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)
        head = ttk.Frame(tab)
        head.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(head, text='Configs', font=('Segoe UI Semibold', 15)).pack(side='left')
        self.cc_cache_count_label = ttk.Label(head, text=f'Current applied caches: {len(self.cc_applied_caches)}', foreground='#9aa0a6')
        self.cc_cache_count_label.pack(side='right')
        bar = ttk.Frame(tab)
        bar.grid(row=1, column=0, sticky='ew', pady=(0, 8))
        for label, command in (('Save Current DB', self._cc_save_db), ('Upload DB', self._cc_upload_db), ('Apply DB', self._cc_apply_db), ('Export DB', self._cc_export_db), ('Delete DB', self._cc_delete_db), ('Refresh', lambda: self._cc_refresh_list())):
            ttk.Button(bar, text=label, command=command).pack(side='left', padx=(0, 6))
        paned = ttk.PanedWindow(tab, orient='vertical')
        paned.grid(row=2, column=0, sticky='nsew')
        top = ttk.Frame(paned)
        bottom = ttk.Frame(paned)
        paned.add(top, weight=3)
        paned.add(bottom, weight=2)
        columns = ('name', 'created', 'caches', 'file')
        self.cc_tree = ttk.Treeview(top, columns=columns, show='headings', selectmode='browse')
        self.cc_tree.heading('name', text='CONFIG')
        self.cc_tree.heading('created', text='CREATED')
        self.cc_tree.heading('caches', text='APPLIED')
        self.cc_tree.heading('file', text='FILE')
        self.cc_tree.column('name', width=240, anchor='w')
        self.cc_tree.column('created', width=160, anchor='w')
        self.cc_tree.column('caches', width=80, anchor='center')
        self.cc_tree.column('file', width=280, anchor='w')
        self.cc_tree.pack(side='left', fill='both', expand=True)
        cc_scroll = ttk.Scrollbar(top, orient='vertical', command=self.cc_tree.yview)
        cc_scroll.pack(side='right', fill='y')
        self.cc_tree.configure(yscrollcommand=cc_scroll.set)
        self.cc_tree.bind('<<TreeviewSelect>>', self._cc_show_selected)
        self.cc_tree.bind('<Double-1>', lambda _e: self._cc_apply_db())
        ttk.Label(bottom, text='Saved DB details', font=('Segoe UI Semibold', 10)).pack(anchor='w', pady=(4, 4))
        self.cc_details = tk.Text(bottom, wrap='word', height=8, font=('Consolas', 9), bg='#252526', fg='#d4d4d4', insertbackground='#ffffff', selectbackground='#007acc', selectforeground='#ffffff', relief='flat', bd=0)
        self.cc_details.pack(fill='both', expand=True)
        self.cc_details.configure(state='disabled')
        self._cc_refresh_list()

    def _open_selected_roblox(self):
        path = self.settings.get('roblox_path', '') if hasattr(self, 'settings') else ''
        if not path:
            try:
                path = self.roblox_path_var.get()
            except Exception:
                path = ''
        if os.path.isdir(path):
            candidate = os.path.join(path, 'RobloxPlayerBeta.exe')
            if os.path.isfile(candidate):
                path = candidate
        if not path or os.path.basename(path).lower() != 'robloxplayerbeta.exe' or (not os.path.isfile(path)):
            try:
                messagebox.showwarning('RoUtils', 'Please select a valid RobloxPlayerBeta.exe first.')
            except Exception:
                pass
            return
        try:
            subprocess.Popen([path], shell=False)
            self._console_log(f'Opened Roblox: {path}')
        except Exception as e:
            try:
                messagebox.showerror('RoUtils', f'Could not open Roblox:\n{e}')
            except Exception:
                pass

    def _build_utils_tab(self):
        tab_outer = _ScrollableTab(self.nb, padding=0)
        tab = tab_outer.inner
        self.nb.insert(2, tab_outer, text='Modifications')
        tab.columnconfigure(0, weight=1)
        ttk.Label(tab, text='Modifications', font=('Segoe UI Semibold', 15)).grid(row=0, column=0, sticky='w')
        ttk.Label(tab, text='Roblox Modifications', foreground='#9aa0a6').grid(row=1, column=0, sticky='w', pady=(0, 14))
        converters = ttk.LabelFrame(tab, text='Converters', padding=14)
        converters.grid(row=2, column=0, sticky='ew', pady=(0, 10))
        ttk.Button(converters, text='R6 Animation → R15', command=self._utils_r6_to_r15).pack(anchor='w', pady=(0, 6))
        ttk.Button(converters, text='Roblox File Converter (.rbxm / .rbxh / .rbxmx)', command=self._utils_roblox_file_convert).pack(anchor='w', pady=(0, 6))
        ttk.Button(converters, text='Mesh to OBJ', command=self._utils_mesh_to_obj).pack(anchor='w')
        mesh = ttk.LabelFrame(tab, text='Default Mesh Changer', padding=14)
        mesh.grid(row=3, column=0, sticky='ew', pady=(0, 10))
        ttk.Label(mesh, text='It allows you to change the default R6 Meshes.').grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 8))
        pathrow = ttk.Frame(mesh)
        pathrow.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 10))
        pathrow.columnconfigure(0, weight=1)
        self.roblox_path_var = tk.StringVar(value=self.settings.get('roblox_path', ''))
        ttk.Entry(pathrow, textvariable=self.roblox_path_var, state='readonly').grid(row=0, column=0, sticky='ew')
        ttk.Button(pathrow, text='Choose', command=self._choose_roblox_path).grid(row=0, column=1, padx=(6, 0))
        ttk.Button(pathrow, text='Open Selected Roblox', command=self._open_selected_roblox).grid(row=0, column=2, padx=(6, 0))
        self.mesh_rows = {}
        for i, name in enumerate(('Head.mesh', 'leftarm.mesh', 'leftleg.mesh', 'rightarm.mesh', 'rightleg.mesh', 'torso.mesh'), start=2):
            ttk.Label(mesh, text=name).grid(row=i, column=0, sticky='w', pady=3)
            ttk.Button(mesh, text='Delete', command=lambda n=name: self._delete_default_mesh(n)).grid(row=i, column=1, padx=5)
            ttk.Button(mesh, text='Choose', command=lambda n=name: self._choose_default_mesh(n)).grid(row=i, column=2)
        mesh.columnconfigure(0, weight=1)
        sky = ttk.LabelFrame(tab, text='Skybox Changer', padding=14)
        sky.grid(row=4, column=0, sticky='ew', pady=(0, 10))
        ttk.Label(sky, text='Replace Roblox skybox texture files from PlatformContent\\pc\\textures\\sky.').grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 8))
        sky_pathrow = ttk.Frame(sky)
        sky_pathrow.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 10))
        sky_pathrow.columnconfigure(0, weight=1)
        ttk.Entry(sky_pathrow, textvariable=self.roblox_path_var, state='readonly').grid(row=0, column=0, sticky='ew')
        ttk.Button(sky_pathrow, text='Choose', command=self._choose_roblox_path).grid(row=0, column=1, padx=(6, 0))
        ttk.Button(sky_pathrow, text='Open Selected Roblox', command=self._open_selected_roblox).grid(row=0, column=2, padx=(6, 0))
        for i, name in enumerate(SKYBOX_TEXTURES, start=2):
            ttk.Label(sky, text=name).grid(row=i, column=0, sticky='w', pady=3)
            ttk.Button(sky, text='Delete', command=lambda n=name: self._delete_skybox_texture(n)).grid(row=i, column=1, padx=5)
            ttk.Button(sky, text='Choose', command=lambda n=name: self._choose_skybox_texture(n)).grid(row=i, column=2)
        sky.columnconfigure(0, weight=1)
        sounds = ttk.LabelFrame(tab, text='Sounds', padding=14)
        sounds.grid(row=5, column=0, sticky='ew', pady=(0, 10))
        ttk.Label(sounds, text='Replace Roblox sound files from content\\sounds.').grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 8))
        sound_pathrow = ttk.Frame(sounds)
        sound_pathrow.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 10))
        sound_pathrow.columnconfigure(0, weight=1)
        ttk.Entry(sound_pathrow, textvariable=self.roblox_path_var, state='readonly').grid(row=0, column=0, sticky='ew')
        ttk.Button(sound_pathrow, text='Choose', command=self._choose_roblox_path).grid(row=0, column=1, padx=(6, 0))
        ttk.Button(sound_pathrow, text='Open Selected Roblox', command=self._open_selected_roblox).grid(row=0, column=2, padx=(6, 0))
        for i, name in enumerate(SOUND_FILES, start=2):
            ttk.Label(sounds, text=name).grid(row=i, column=0, sticky='w', pady=3)
            ttk.Button(sounds, text='Delete', command=lambda n=name: self._delete_roblox_sound(n)).grid(row=i, column=1, padx=5)
            ttk.Button(sounds, text='Choose', command=lambda n=name: self._choose_roblox_sound(n)).grid(row=i, column=2)
        sounds.columnconfigure(0, weight=1)
        others = ttk.LabelFrame(tab, text='Others', padding=14)
        others.grid(row=6, column=0, sticky='ew', pady=(0, 10))
        ttk.Label(others, text='Replace additional Roblox texture and font files.').grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 8))
        other_pathrow = ttk.Frame(others)
        other_pathrow.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 10))
        other_pathrow.columnconfigure(0, weight=1)
        ttk.Entry(other_pathrow, textvariable=self.roblox_path_var, state='readonly').grid(row=0, column=0, sticky='ew')
        ttk.Button(other_pathrow, text='Choose', command=self._choose_roblox_path).grid(row=0, column=1, padx=(6, 0))
        ttk.Button(other_pathrow, text='Open Selected Roblox', command=self._open_selected_roblox).grid(row=0, column=2, padx=(6, 0))
        ttk.Label(others, text='Studs (replaces plastic\nnormal.dds)').grid(row=2, column=0, sticky='w', pady=3)
        ttk.Button(others, text='Delete', command=lambda: self._delete_other_file('studs')).grid(row=2, column=1, padx=5)
        ttk.Button(others, text='Choose', command=lambda: self._choose_other_file('studs')).grid(row=2, column=2)
        ttk.Label(others, text='Diffuse (diffuse.dds)').grid(row=3, column=0, sticky='w', pady=3)
        ttk.Button(others, text='Delete', command=lambda: self._delete_other_file('diffuse')).grid(row=3, column=1, padx=5)
        ttk.Button(others, text='Choose', command=lambda: self._choose_other_file('diffuse')).grid(row=3, column=2)
        ttk.Label(others, text='Font (CustomFont.ttf)').grid(row=4, column=0, sticky='w', pady=3)
        ttk.Button(others, text='Delete', command=lambda: self._delete_other_file('font')).grid(row=4, column=1, padx=5)
        ttk.Button(others, text='Choose', command=lambda: self._choose_other_file('font')).grid(row=4, column=2)
        others.columnconfigure(0, weight=1)

    def _version_path(self):
        return os.path.join(DATA_DIR, 'version.txt')

    def _reset_version_file(self):
        try:
            vp = self._version_path()
            if os.path.exists(vp):
                try:
                    os.remove(vp)
                except Exception:
                    pass
            with open(vp, 'w', encoding='utf-8') as f:
                f.write(APP_VERSION)
        except Exception:
            pass

    def _local_version(self):
        try:
            if not os.path.exists(self._version_path()):
                with open(self._version_path(), 'w', encoding='utf-8') as f:
                    f.write(APP_VERSION)
            with open(self._version_path(), encoding='utf-8') as f:
                return f.read().strip() or APP_VERSION
        except Exception:
            return APP_VERSION

    def _build_home_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.insert(0, tab, text='Home')
        ttk.Label(tab, text='RoUtils', font=('Segoe UI Semibold', 20)).pack(anchor='w')
        ttk.Label(tab, text=f"Welcome Dear, {platform.node() or os.environ.get('COMPUTERNAME', 'System')}", font=('Segoe UI Semibold', 14)).pack(anchor='w', pady=(14, 14))
        links = ttk.Frame(tab)
        links.pack(anchor='w', fill='x')

        def add_link(text_value, url):
            label = tk.Label(links, text=text_value, fg='#4da6ff', bg=_CURRENT_PALETTE['bg_dark'], cursor='hand2', font=('Segoe UI Semibold', 12), anchor='w')
            label.pack(anchor='w', pady=3)
            label.bind('<Button-1>', lambda _e, u=url: webbrowser.open(u))
            label.bind('<Enter>', lambda _e, w=label: w.config(font=('Segoe UI Semibold', 12, 'underline')))
            label.bind('<Leave>', lambda _e, w=label: w.config(font=('Segoe UI Semibold', 12)))
            return label
        add_link('Official Github Link: https://github.com/offp001/routils', 'https://github.com/offp001/routils')
        add_link('Join Discord server: https://discord.gg/849VtrYhm2', 'https://discord.com/invite/849VtrYhm2')
        ttk.Label(links, text='Support with me: offp001 on discord', foreground='#9aa0a6', font=('Segoe UI', 10)).pack(anchor='w', pady=(0, 8))
        _q = bytes.fromhex('446973636c616d65723a20546865206f6666696369616c20646f776e6c6f6164207265706f7369746f727920666f7220526f5574696c732069732068747470733a2f2f6769746875622e636f6d2f6f6666703030312f726f7574696c732053696e636520526f5574696c73206973206f70656e2d736f757263652c206974206973206561737920666f72206d616c6963696f757320636f646520746f20626520696e73657274656420696e746f2069743b20696620796f7520646f776e6c6f616465642069742066726f6d20616e20756e6b6e6f776e20736f75726365206f7220612066696c652073656e7420746f20796f7520627920736f6d656f6e6520656c73652c20706c656173652064656c65746520746861742066696c6520616e6420646f776e6c6f61642069742066726f6d20746865206f6666696369616c20736f757263653a2068747470733a2f2f6769746875622e636f6d2f6f6666703030312f726f7574696c730a0a596f752063616e20616c736f207368617265207468652066696c6520796f752070726576696f75736c7920646f776e6c6f616465642077697468206d6520286f66667030303129206279206a6f696e696e672074686520446973636f7264207365727665722061742068747470733a2f2f646973636f72642e636f6d2f696e766974652f38343956747259686d32').decode('utf-8')
        disclaimer_frame = tk.Frame(tab, bg=_CURRENT_PALETTE.get('bg_dark', '#1e1e1e'))
        disclaimer_frame.pack(fill='x', pady=(2, 8))
        disclaimer_text = tk.Text(disclaimer_frame, bg=_CURRENT_PALETTE.get('bg_dark', '#1e1e1e'), fg='#ff0000', font=('Segoe UI', -14, 'bold'), relief='flat', bd=0, highlightthickness=0, wrap='word', height=6, padx=0, pady=0, cursor='arrow')
        disclaimer_text.pack(fill='x', expand=True)
        disclaimer_text.tag_configure('plain', foreground='#ff0000', font=('Segoe UI', -14, 'bold'))
        disclaimer_text.tag_configure('link', foreground='#0080ff', font=('Segoe UI', -14, 'bold', 'underline'))
        urls = ('https://github.com/offp001/routils', 'https://discord.com/invite/849VtrYhm2')
        for part in re.split('(https://github\\.com/offp001/routils|https://discord\\.com/invite/849VtrYhm2)', _q):
            if not part:
                continue
            if part in urls:
                tag = 'url_' + str(abs(hash(part)))
                disclaimer_text.tag_configure(tag, foreground='#0080ff', font=('Segoe UI', -14, 'bold', 'underline'))
                disclaimer_text.insert('end', part, tag)
                disclaimer_text.tag_bind(tag, '<Button-1>', lambda event, url=part: webbrowser.open(url))
                disclaimer_text.tag_bind(tag, '<Enter>', lambda event: disclaimer_text.configure(cursor='hand2'))
                disclaimer_text.tag_bind(tag, '<Leave>', lambda event: disclaimer_text.configure(cursor='arrow'))
            else:
                disclaimer_text.insert('end', part, 'plain')
        disclaimer_text.configure(state='disabled')
        ttk.Separator(tab).pack(fill='x', pady=10)
        version_row = ttk.Frame(tab)
        version_row.pack(anchor='w')
        ttk.Label(version_row, text='Version: ', font=('Comic Sans MS', 10, 'bold')).pack(side='left')
        self.home_version_value = ttk.Label(version_row, text=self._local_version(), font=('Comic Sans MS', 10, 'bold'))
        self.home_version_value.pack(side='left')
        self.home_version_state = ttk.Label(version_row, text='Checking', font=('Comic Sans MS', 10, 'bold'))
        self.home_version_state.pack(side='left', padx=(6, 0))
        self.home_version_var = tk.StringVar(value=f'Version: {self._local_version()} (Checking)')
        self.home_download_frame = ttk.Frame(tab)
        self.home_download_label = ttk.Label(self.home_download_frame, text='Downloading update…')
        self.home_download_label.pack(anchor='w')
        self.home_download_progress = ttk.Progressbar(self.home_download_frame, orient='horizontal', mode='determinate', length=320)
        self.home_download_progress.pack(anchor='w', fill='x', pady=(3, 0))

    def _set_update_progress(self, downloaded=0, total=0, visible=True):
        try:
            if visible:
                self.home_download_frame.pack(side='bottom', anchor='w', fill='x', padx=10, pady=10)
                if total > 0:
                    self.home_download_progress.configure(mode='determinate', maximum=total, value=downloaded)
                    self.home_download_label.configure(text=f'Downloading update… {downloaded / total * 100:.0f}%')
                else:
                    self.home_download_progress.configure(mode='indeterminate')
                    self.home_download_progress.start(12)
                    self.home_download_label.configure(text='Downloading update…')
            else:
                try:
                    self.home_download_progress.stop()
                except Exception:
                    pass
                self.home_download_frame.pack_forget()
        except Exception:
            pass

    @staticmethod
    def _version_tuple(version):
        parts = re.findall('\\d+', str(version or ''))
        if not parts:
            return (0,)
        return tuple((int(x) for x in parts[:4]))

    def _is_newer_version(self, latest, current):
        return self._version_tuple(latest) > self._version_tuple(current)

    def _show_outdated_dialog(self, latest):
        if self._outdated_dialog_shown or self._auto_update_in_progress:
            return
        self._outdated_dialog_shown = True
        try:
            dlg = tk.Toplevel(self)
            dlg.title('RoUtils is Outdated')
            dlg.resizable(False, False)
            dlg.transient(self)
            theme_toplevel(dlg)
            width, height = (440, 230)
            self.update_idletasks()
            x = max(0, (self.winfo_screenwidth() - width) // 2)
            y = max(0, (self.winfo_screenheight() - height) // 2)
            dlg.geometry(f'{width}x{height}+{x}+{y}')
            outer = ttk.Frame(dlg, padding=24)
            outer.pack(fill='both', expand=True)
            ttk.Label(outer, text='RoUtils is Outdated', font=('Segoe UI Semibold', 18)).pack(pady=(8, 8))
            ttk.Label(outer, text=f'Download New Version ({latest})', font=('Segoe UI', 11)).pack(pady=(0, 20))
            buttons = ttk.Frame(outer)
            buttons.pack()

            def download():
                try:
                    dlg.grab_release()
                except Exception:
                    pass
                try:
                    dlg.destroy()
                except Exception:
                    pass
                webbrowser.open(f'https://github.com/offp001/routils/releases/download/{latest}/RoUtils.exe')

            def later():
                try:
                    dlg.grab_release()
                except Exception:
                    pass
                try:
                    dlg.destroy()
                except Exception:
                    pass
            ttk.Button(buttons, text='Download', command=download).pack(side='left', padx=6)
            ttk.Button(buttons, text='Later', command=later).pack(side='left', padx=6)
            dlg.protocol('WM_DELETE_WINDOW', later)
            dlg.focus_force()
        except Exception:
            self._outdated_dialog_shown = False

    def _start_auto_update(self, latest):
        if self._auto_update_in_progress:
            return
        self._auto_update_in_progress = True

        def worker():
            try:
                current = self._local_version()
                if not self._is_newer_version(latest, current):
                    self._auto_update_in_progress = False
                    return
                download_url = f'https://github.com/offp001/routils/releases/download/{latest}/RoUtils.exe'
                target_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
                target_path = os.path.join(target_dir, f'RoUtils-{latest}.exe')
                temp_path = os.path.join(tempfile.gettempdir(), f'RoUtils-{latest}.download')
                self.after(0, lambda: self._set_update_progress(0, 0, True))
                self.after(0, lambda v=latest: self._console_log(f'Update {v} download started.'))
                req = urllib.request.Request(download_url, headers={'User-Agent': 'RoUtils-AutoUpdater'})
                with urllib.request.urlopen(req, timeout=30) as response:
                    total = int(response.headers.get('Content-Length', '0') or 0)
                    downloaded = 0
                    with open(temp_path, 'wb') as out:
                        while True:
                            chunk = response.read(1024 * 256)
                            if not chunk:
                                break
                            out.write(chunk)
                            downloaded += len(chunk)
                            self.after(0, lambda d=downloaded, t=total: self._set_update_progress(d, t, True))
                if not os.path.isfile(temp_path) or os.path.getsize(temp_path) < 1024:
                    raise RuntimeError('Downloaded update is invalid.')
                os.replace(temp_path, target_path)
                self.after(0, lambda p=target_path: self._console_log(f'Update downloaded to {p}; launching from RoUtils folder.'))
                subprocess.Popen([target_path], cwd=target_dir, close_fds=True, creationflags=getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0))
                self.after(0, lambda: (self._set_update_progress(0, 0, False), self._on_close(force=True)))
            except Exception as e:
                self._auto_update_in_progress = False
                try:
                    self.after(0, lambda err=str(e): self._console_log(f'Update error: {err}'))
                except Exception:
                    pass
                try:
                    self.after(0, lambda: self._set_update_progress(0, 0, False))
                except Exception:
                    pass
                try:
                    temp_path = locals().get('temp_path')
                    if temp_path and os.path.isfile(temp_path):
                        os.remove(temp_path)
                except Exception:
                    pass
                try:
                    self.after(0, lambda err=str(e): self._show_update_error(err))
                except Exception:
                    pass
        threading.Thread(target=worker, daemon=True, name='RoUtils-AutoUpdate').start()

    def _show_update_error(self, error):
        self._auto_update_in_progress = False
        try:
            messagebox.showwarning('RoUtils Update', f'Automatic update failed:\n{error}', parent=self)
        except Exception:
            pass

    def _start_version_check(self):

        def worker():
            current = self._local_version()
            latest = current

            def set_state(state, color):
                try:
                    self.after(0, lambda: (self.home_version_value.config(text=current), self.home_version_state.config(text=state, foreground=color), self.home_version_var.set(f'Version: {current} ({state})')))
                except Exception:
                    pass
            set_state('Checking', '#f2c94c')
            try:
                req = urllib.request.Request('https://api.github.com/repos/offp001/routils/releases/latest', headers={'User-Agent': 'RoUtils'})
                with urllib.request.urlopen(req, timeout=5) as r:
                    data = json.loads(r.read().decode('utf-8', 'replace'))
                tag = str(data.get('tag_name', '')).strip()
                if tag:
                    latest = tag.lstrip('v')
            except Exception:
                set_state('Unknown', '#9aa0a6')
                return
            self._latest_version = latest
            is_outdated = self._is_newer_version(latest, current)
            state = 'Outdated' if is_outdated else 'Latest'
            color = '#ff5f57' if is_outdated else '#65d98b'
            set_state(state, color)
            if is_outdated:
                if self.auto_update.get():
                    self.after(0, lambda v=latest: self._start_auto_update(v))
                else:
                    self.after(0, lambda v=latest: self._show_outdated_dialog(v))
        threading.Thread(target=worker, daemon=True, name='RoUtils-VersionCheck').start()

    def _reorder_tabs(self):
        order = ['Home', 'Cache', 'FFlags', 'Configs', 'Modifications', 'Subplace Joiner', 'Server Viewer', 'History', 'Client', 'Themes', 'Plugins', 'Console', 'Settings']
        for i, name in enumerate(order):
            for tab_id in self.nb.tabs():
                if self.nb.tab(tab_id, 'text') == name:
                    self.nb.insert(i, tab_id)
                    break
        self._refresh_tab_nav()

    def _fflag_json_editor(self):
        dlg = tk.Toplevel(self)
        dlg.title('JSON Editor')
        dlg.geometry('620x460')
        theme_toplevel(dlg)
        txt = tk.Text(dlg, wrap='none', font=('Consolas', 10), bg=_CURRENT_PALETTE['bg_medium'], fg=_CURRENT_PALETTE['fg'], insertbackground='#fff')
        txt.pack(fill='both', expand=True, padx=10, pady=10)
        ttk.Button(dlg, text='Add', command=lambda: self._add_json_editor_value(txt, dlg)).pack(pady=(0, 10))

    def _add_json_editor_value(self, txt, dlg):
        try:
            data = json.loads(txt.get('1.0', 'end'))
            assert isinstance(data, (dict, list))
        except Exception as e:
            messagebox.showerror('JSON Editor', f'Invalid JSON:\n{e}', parent=dlg)
            return
        if isinstance(data, dict):
            for n, v in data.items():
                self.fflag_flags.append({'name': fflag_strip_prefix(str(n)), 'value': str(v).lower() if isinstance(v, bool) else str(v), 'type': fflag_infer_type(v)})
        else:
            for x in data:
                if isinstance(x, dict) and x.get('name') is not None:
                    self.fflag_flags.append({'name': fflag_strip_prefix(str(x['name'])), 'value': str(x.get('value', '')), 'type': x.get('type') or fflag_infer_type(x.get('value', ''))})
        self._save_fflag_flags()
        self._refresh_fflag_list()
        dlg.destroy()

    def _refresh_json_list(self):
        if not hasattr(self, 'json_tree'):
            return
        self.json_tree.delete(0, 'end')
        for n in sorted(os.listdir(self.jsons_dir)) if os.path.isdir(self.jsons_dir) else []:
            if n.lower().endswith('.json'):
                self.json_tree.insert('end', n)

    def _apply_selected_json(self):
        if not hasattr(self, 'json_tree'):
            return
        sel = self.json_tree.curselection()
        if not sel:
            return
        path = os.path.join(self.jsons_dir, self.json_tree.get(sel[0]))
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            flags = []
            if isinstance(data, dict):
                flags = [{'name': fflag_strip_prefix(str(k)), 'value': str(v).lower() if isinstance(v, bool) else str(v), 'type': fflag_infer_type(v)} for k, v in data.items()]
            elif isinstance(data, list):
                flags = [{'name': fflag_strip_prefix(str(x['name'])), 'value': str(x.get('value', '')), 'type': x.get('type') or fflag_infer_type(x.get('value', ''))} for x in data if isinstance(x, dict) and x.get('name') is not None]
            else:
                raise ValueError('JSON must be an object or array.')
            self.fflag_flags = flags
            self._save_fflag_flags()
            self._refresh_fflag_list()
            messagebox.showinfo('FFlags', f'Applied {len(flags)} flags from {os.path.basename(path)}.', parent=self)
        except Exception as e:
            messagebox.showerror('FFlags', f'Failed to apply JSON:\n{e}', parent=self)

    def _choose_roblox_path(self):
        path = filedialog.askopenfilename(parent=self, title='Select RobloxPlayerBeta.exe', filetypes=[('Roblox Player', 'RobloxPlayerBeta.exe'), ('Executable', '*.exe')])
        if path and os.path.basename(path).lower() == 'robloxplayerbeta.exe':
            self.roblox_path_var.set(path)
            self.settings['roblox_path'] = path
            self._save_settings()

    def _default_mesh_path(self, name):
        root = self.roblox_path_var.get().strip()
        if not root or os.path.basename(root).lower() != 'robloxplayerbeta.exe':
            return None
        root = os.path.dirname(root)
        folder = 'heads' if name.lower() == 'head.mesh' else 'meshes'
        return os.path.join(root, 'content', 'avatar', folder, name)

    def _choose_default_mesh(self, name):
        target = self._default_mesh_path(name)
        if not target:
            messagebox.showwarning('Default Mesh Changer', 'Choose RobloxPlayerBeta.exe first.', parent=self)
            return
        src = filedialog.askopenfilename(parent=self, title=f'Choose replacement for {name}', filetypes=[('Mesh files', '*.mesh'), ('All files', '*.*')])
        if not src:
            return
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            if os.path.abspath(src).lower() == os.path.abspath(target).lower():
                return
            if os.path.exists(target):
                os.remove(target)
            shutil.copy2(src, target)
        except Exception as e:
            messagebox.showerror('Default Mesh Changer', f'Failed:\n{e}', parent=self)

    def _delete_default_mesh(self, name):
        target = self._default_mesh_path(name)
        if not target:
            return
        try:
            if os.path.exists(target):
                os.remove(target)
        except Exception as e:
            messagebox.showerror('Default Mesh Changer', f'Failed:\n{e}', parent=self)

    def _skybox_path(self, name):
        root = self.roblox_path_var.get().strip()
        if not root or os.path.basename(root).lower() != 'robloxplayerbeta.exe':
            return None
        return os.path.join(os.path.dirname(root), 'PlatformContent', 'pc', 'textures', 'sky', name)

    def _choose_skybox_texture(self, name):
        target = self._skybox_path(name)
        if not target:
            messagebox.showwarning('Skybox Changer', 'Choose RobloxPlayerBeta.exe first.', parent=self)
            return
        source = filedialog.askopenfilename(parent=self, title=f'Choose replacement for {name}', filetypes=[('Texture files', '*.tex'), ('All files', '*.*')])
        if not source:
            return
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            if os.path.abspath(source).lower() != os.path.abspath(target).lower():
                if os.path.exists(target):
                    os.remove(target)
                shutil.copy2(source, target)
            self._console_log(f'Skybox texture replaced: {name}')
        except Exception as e:
            messagebox.showerror('Skybox Changer', f'Failed:\n{e}', parent=self)

    def _delete_skybox_texture(self, name):
        target = self._skybox_path(name)
        if not target:
            return
        try:
            if os.path.exists(target):
                os.remove(target)
                self._console_log(f'Skybox texture deleted: {name}')
        except Exception as e:
            messagebox.showerror('Skybox Changer', f'Failed:\n{e}', parent=self)

    def _roblox_content_path(self, *parts):
        root = self.roblox_path_var.get().strip()
        if not root or os.path.basename(root).lower() != 'robloxplayerbeta.exe':
            return None
        return os.path.join(os.path.dirname(root), *parts)

    def _sound_path(self, name):
        return self._roblox_content_path('content', 'sounds', name)

    def _choose_roblox_sound(self, name):
        target = self._sound_path(name)
        if not target:
            messagebox.showwarning('Sounds', 'Choose RobloxPlayerBeta.exe first.', parent=self)
            return
        source = filedialog.askopenfilename(parent=self, title=f'Choose replacement for {name}', filetypes=[('Audio files', '*.ogg *.mp3 *.wav'), ('All files', '*.*')])
        if not source:
            return
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            if os.path.abspath(source).lower() != os.path.abspath(target).lower():
                if os.path.exists(target):
                    os.remove(target)
                shutil.copy2(source, target)
            self._console_log(f'Sound replaced: {name}')
        except Exception as e:
            messagebox.showerror('Sounds', f'Failed:\n{e}', parent=self)

    def _delete_roblox_sound(self, name):
        target = self._sound_path(name)
        if not target:
            messagebox.showwarning('Sounds', 'Choose RobloxPlayerBeta.exe first.', parent=self)
            return
        try:
            if os.path.exists(target):
                os.remove(target)
                self._console_log(f'Sound deleted: {name}')
        except Exception as e:
            messagebox.showerror('Sounds', f'Failed:\n{e}', parent=self)

    def _other_path(self, kind):
        if kind == 'studs':
            return self._roblox_content_path('PlatformContent', 'pc', 'textures', 'plastic', 'normal.dds')
        if kind == 'diffuse':
            return self._roblox_content_path('PlatformContent', 'pc', 'textures', 'plastic', 'diffuse.dds')
        if kind == 'font':
            return self._roblox_content_path('content', 'fonts', 'CustomFont.ttf')
        return None

    def _choose_other_file(self, kind):
        target = self._other_path(kind)
        if not target:
            messagebox.showwarning('Others', 'Choose RobloxPlayerBeta.exe first.', parent=self)
            return
        if kind == 'studs':
            title = 'Choose replacement for studs.dds (target: plastic\normal.dds)'
            filetypes = [('DDS texture', '*.dds'), ('All files', '*.*')]
        elif kind == 'diffuse':
            title = 'Choose replacement for diffuse.dds'
            filetypes = [('DDS texture', '*.dds'), ('All files', '*.*')]
        else:
            title = 'Choose replacement for CustomFont.ttf'
            filetypes = [('TrueType Font', '*.ttf'), ('All files', '*.*')]
        source = filedialog.askopenfilename(parent=self, title=title, filetypes=filetypes)
        if not source:
            return
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            if os.path.abspath(source).lower() != os.path.abspath(target).lower():
                if os.path.exists(target):
                    os.remove(target)
                shutil.copy2(source, target)
            self._console_log(f'Other file replaced: {os.path.basename(target)}')
        except Exception as e:
            messagebox.showerror('Others', f'Failed:\n{e}', parent=self)

    def _delete_other_file(self, kind):
        target = self._other_path(kind)
        if not target:
            messagebox.showwarning('Others', 'Choose RobloxPlayerBeta.exe first.', parent=self)
            return
        try:
            if os.path.exists(target):
                os.remove(target)
                self._console_log(f'Other file deleted: {os.path.basename(target)}')
        except Exception as e:
            messagebox.showerror('Others', f'Failed:\n{e}', parent=self)

    def _utils_mesh_to_obj(self):
        src = filedialog.askopenfilename(parent=self, title='Select Roblox Mesh', filetypes=[('Roblox Mesh', '*.mesh'), ('All files', '*.*')])
        if not src:
            return
        out = os.path.splitext(src)[0] + '.obj'
        try:
            with open(src, 'rb') as f:
                data = f.read()
            ver = _mesh_header(data).replace('version ', '') or 'unknown'
            print(f'Selected Mesh Version "{ver}"')
            print('Converting')
            convert(data, out)
            print(f'Converted: {out}')
        except Exception as e:
            messagebox.showerror('Mesh to OBJ', f'Conversion failed:\n{e}', parent=self)

    def _utils_roblox_file_convert(self):
        src = filedialog.askopenfilename(parent=self, title='Select Roblox File', filetypes=[('Roblox Files', '*.rbxm *.rbxh *.rbxmx'), ('RBXM', '*.rbxm'), ('RBXH', '*.rbxh'), ('RBXMX', '*.rbxmx'), ('All files', '*.*')])
        if not src:
            return
        try:
            with open(src, 'rb') as f:
                content = f.read()
            filename, ext = os.path.splitext(os.path.basename(src))
            ext = ext.lower()
            if ext not in ('.rbxm', '.rbxh', '.rbxmx'):
                messagebox.showwarning('Roblox File Converter', 'Please select an .rbxm, .rbxh or .rbxmx file.', parent=self)
                return
            if ext in ('.rbxm', '.rbxmx'):
                new_ext = '.rbxh'
            else:
                new_ext = '.rbxm'
            template = b''
            if new_ext == '.rbxh':
                sibling = os.path.join(os.path.dirname(src), filename + '.rbxh')
                if os.path.isfile(sibling) and os.path.abspath(sibling) != os.path.abspath(src):
                    with open(sibling, 'rb') as f:
                        template = f.read()
            output_data = convert_roblox_file(content, ext, new_ext, template)
            output_path = os.path.join(os.path.dirname(src), f'{filename}_converted{new_ext}')
            with open(output_path, 'wb') as f:
                f.write(output_data)
            messagebox.showinfo('Roblox File Converter', f'Converted successfully.\n\n{os.path.basename(output_path)}\nSize: {human_size(len(output_data))}', parent=self)
            self._console_log(f'Converted Roblox file: {output_path}')
        except Exception as e:
            messagebox.showerror('Roblox File Converter', f'Conversion failed:\n{e}', parent=self)

    def _history_load(self):
        try:
            if not os.path.exists(HISTORY_PATH):
                return []
            with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _history_save(self, data):
        try:
            tmp = HISTORY_PATH + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp, HISTORY_PATH)
        except Exception:
            pass

    def _resolve_history_game_name(self, place_id):
        place_id = str(place_id or '').strip()
        if not place_id.isdigit():
            return None
        for url in (f'https://games.roblox.com/v1/games/multiget-place-details?placeIds={place_id}', f'https://develop.roblox.com/v1/places/{place_id}'):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'RoUtils/3.3'})
                with urllib.request.urlopen(req, timeout=8) as r:
                    data = json.load(r)
                if isinstance(data, list):
                    data = data[0] if data else {}
                name = str(data.get('name') or data.get('universeName') or '').strip()
                if name and (not name.isdigit()):
                    return name
            except Exception:
                pass
        try:
            req = urllib.request.Request(f'https://apis.roblox.com/universes/v1/places/{place_id}/universe', headers={'User-Agent': 'RoUtils/3.3'})
            with urllib.request.urlopen(req, timeout=8) as r:
                universe_id = json.load(r).get('universeId')
            if universe_id:
                req = urllib.request.Request(f'https://games.roblox.com/v1/games?universeIds={universe_id}', headers={'User-Agent': 'RoUtils/3.3'})
                with urllib.request.urlopen(req, timeout=8) as r:
                    data = json.load(r)
                rows = data.get('data', []) if isinstance(data, dict) else []
                if rows:
                    name = str(rows[0].get('name') or '').strip()
                    if name and (not name.isdigit()):
                        return name
        except Exception:
            pass
        return None

    def _history_add(self, place_id, job_id):
        place_id = str(place_id or '').strip()
        job_id = str(job_id or '').strip()
        if not place_id or not job_id:
            return
        key = (place_id, job_id.lower())
        if self._history_last_game == key:
            return
        self._history_last_game = key

        def worker():
            name = self._resolve_history_game_name(place_id) or place_id
            now = datetime.now()
            entry = {'game_name': name, 'place_id': place_id, 'job_id': job_id, 'deeplink': f'roblox://experiences/start?placeId={place_id}&gameInstanceId={job_id}', 'date': now.strftime('%d.%m.%Y'), 'time': now.strftime('%H:%M:%S'), 'timestamp': now.isoformat(timespec='seconds')}
            history = self._history_load()
            history = [x for x in history if not (str(x.get('place_id')) == place_id and str(x.get('job_id', '')).lower() == job_id.lower())]
            history.insert(0, entry)
            history = history[:20]
            self._history_save(history)
            try:
                self.after(0, self._history_refresh)
            except Exception:
                pass
        threading.Thread(target=worker, daemon=True).start()

    def _detect_current_game(self, silent=True):
        logs_dir = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Roblox', 'logs')
        uuid_re = '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
        join_re = re.compile(f"""!\\s*Joining\\s+game\\s+[\\"']?({uuid_re})[\\"']?\\s+place\\s+(\\d+)""", re.IGNORECASE)
        try:
            log_files = sorted([os.path.join(logs_dir, f) for f in os.listdir(logs_dir) if f.lower().endswith('.log')], key=lambda x: os.path.getmtime(x), reverse=True)[:30]
        except Exception:
            return (None, None)
        for log_path in log_files:
            try:
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            except Exception:
                continue
            matches = list(join_re.finditer(text))
            if matches:
                m = matches[-1]
                return (m.group(2), m.group(1))
        place_id = job_id = None
        for log_path in log_files:
            try:
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            except Exception:
                continue
            if not place_id:
                m = re.findall('\\bplaceid\\s*[:=]\\s*(\\d+)', text, re.IGNORECASE)
                if m:
                    place_id = m[-1]
            if not job_id:
                m = re.findall(f"""\\bjobId\\s*[:=]\\s*[\\"']?({uuid_re})""", text, re.IGNORECASE)
                if m:
                    job_id = m[-1]
            if place_id and job_id:
                return (place_id, job_id)
        return (None, None)

    def _start_history_watcher(self):

        def worker():
            while True:
                try:
                    place_id, job_id = self._detect_current_game()
                    if place_id and job_id:
                        self.after(0, lambda p=place_id, j=job_id: self._history_add(p, j))
                except Exception:
                    pass
                time.sleep(2.5)
        threading.Thread(target=worker, daemon=True).start()

    def _build_history_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.add(tab, text='History')
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)
        head = ttk.Frame(tab)
        head.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(head, text='Game History', font=('Segoe UI Semibold', 15)).pack(side='left')
        ttk.Button(head, text='Refresh', command=self._history_refresh).pack(side='right', padx=(6, 0))
        ttk.Button(head, text='Clear History', command=self._history_clear).pack(side='right')
        ttk.Label(tab, text='Game History.', foreground='#9aa0a6').grid(row=1, column=0, sticky='w', pady=(0, 8))
        outer = ttk.Frame(tab)
        outer.grid(row=2, column=0, sticky='nsew')
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(0, weight=1)
        self.history_canvas = tk.Canvas(outer, bg=_CURRENT_PALETTE['bg_dark'], highlightthickness=0, borderwidth=0)
        scroll = ttk.Scrollbar(outer, orient='vertical', command=self.history_canvas.yview)
        self.history_canvas.configure(yscrollcommand=scroll.set)
        self.history_canvas.grid(row=0, column=0, sticky='nsew')
        scroll.grid(row=0, column=1, sticky='ns')
        self.history_inner = ttk.Frame(self.history_canvas)
        self.history_window = self.history_canvas.create_window((0, 0), window=self.history_inner, anchor='nw')
        self.history_inner.bind('<Configure>', lambda _e: self._schedule_ui('history_region', 30, lambda: self.history_canvas.configure(scrollregion=self.history_canvas.bbox('all'))))
        self.history_canvas.bind('<Configure>', lambda e: self._history_resize_canvas(e))
        self._history_refresh()

    def _history_resize_canvas(self, event):
        width = int(getattr(event, 'width', 0) or 0)
        if width != getattr(self, '_history_canvas_width', -1):
            self._history_canvas_width = width
            self.history_canvas.itemconfigure(self.history_window, width=width)

    def _history_refresh(self):
        if not hasattr(self, 'history_inner'):
            return
        history = self._history_load()
        signature = tuple(((str(x.get('timestamp', '')), str(x.get('place_id', '')), str(x.get('job_id', '')), str(x.get('game_name', '')), str(x.get('deeplink', ''))) for x in history)) if history else ()
        if signature == getattr(self, '_history_render_signature', None):
            return
        self._history_render_signature = signature
        for child in self.history_inner.winfo_children():
            child.destroy()
        if not history:
            ttk.Label(self.history_inner, text='No games recorded yet.', foreground='#9aa0a6').pack(anchor='w', padx=12, pady=18)
            return
        header = ttk.Frame(self.history_inner)
        header.pack(fill='x', padx=6, pady=(0, 4))
        for col, weight in enumerate((3, 2, 3, 2, 0, 0)):
            header.columnconfigure(col, weight=weight)
        for col, label in enumerate(('GAME', 'ID', 'JOB ID', 'DATE / TIME', '', '')):
            ttk.Label(header, text=label, foreground='#9aa0a6').grid(row=0, column=col, sticky='w', padx=6)
        for entry in history:
            row = ttk.Frame(self.history_inner)
            row.pack(fill='x', padx=6, pady=2)
            for col, weight in enumerate((3, 2, 3, 2, 0, 0)):
                row.columnconfigure(col, weight=weight)
            game = str(entry.get('game_name') or entry.get('place_id') or 'Unknown Game')
            pid = str(entry.get('place_id') or '')
            jid = str(entry.get('job_id') or '')
            dt = f"{entry.get('date', '')} {entry.get('time', '')}".strip()
            link = str(entry.get('deeplink') or f'roblox://experiences/start?placeId={pid}&gameInstanceId={jid}')
            ttk.Label(row, text=game, font=('Comic Sans MS', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=6, pady=5)
            ttk.Label(row, text=pid).grid(row=0, column=1, sticky='w', padx=6)
            ttk.Label(row, text=jid).grid(row=0, column=2, sticky='w', padx=6)
            ttk.Label(row, text=dt).grid(row=0, column=3, sticky='w', padx=6)
            ttk.Button(row, text='Copy Deeplink', command=lambda l=link: self._history_copy(l)).grid(row=0, column=4, padx=4)
            ttk.Button(row, text='Join', command=lambda l=link: self._history_join(l)).grid(row=0, column=5, padx=(2, 6))

    def _history_copy(self, link):
        try:
            self.clipboard_clear()
            self.clipboard_append(link)
        except Exception as e:
            messagebox.showerror('History', f'Could not copy deeplink:{e}', parent=self)

    def _history_join(self, link):
        try:
            os.startfile(link)
            self._console_log(f'Joined from history: {link}')
        except Exception as e:
            messagebox.showerror('History', f'Could not launch Roblox:{e}', parent=self)

    def _history_clear(self):
        if not messagebox.askyesno('History', 'Clear all saved game history?', parent=self):
            return
        self._history_save([])
        self._history_last_game = None
        self._history_refresh()

    def _build_client_tab(self):
        self._client_tab_active = True
        tab_outer = _ScrollableTab(self.nb, padding=0)
        tab = tab_outer.inner
        self.nb.add(tab_outer, text='Client')
        tab.columnconfigure(0, weight=1)
        ttk.Label(tab, text='Roblox Client', font=('Segoe UI Semibold', 15)).grid(row=0, column=0, sticky='w')
        ttk.Label(tab, text='Live Roblox client information and current game details.', foreground='#9aa0a6').grid(row=1, column=0, sticky='w', pady=(0, 14))
        info = ttk.LabelFrame(tab, text='Client Information', padding=14)
        info.grid(row=2, column=0, sticky='ew', pady=(0, 10))
        info.columnconfigure(1, weight=1)
        self.client_status_var = tk.StringVar(value='Checking...')
        self.client_pid_var = tk.StringVar(value='—')
        self.client_path_var = tk.StringVar(value='—')
        self.client_version_var = tk.StringVar(value='—')
        self.client_game_var = tk.StringVar(value='Detecting...')
        self.client_place_var = tk.StringVar(value='—')
        self.client_job_var = tk.StringVar(value='—')
        self.client_cpu_var = tk.StringVar(value='—')
        self.client_ram_var = tk.StringVar(value='—')
        rows = (('Status', self.client_status_var), ('PID', self.client_pid_var), ('Path', self.client_path_var), ('File Version', self.client_version_var), ('Game', self.client_game_var), ('Place ID', self.client_place_var), ('Job ID', self.client_job_var), ('CPU Usage', self.client_cpu_var), ('RAM Usage', self.client_ram_var))
        for i, (label, var) in enumerate(rows):
            ttk.Label(info, text=label).grid(row=i, column=0, sticky='w', padx=(0, 14), pady=5)
            ttk.Label(info, textvariable=var).grid(row=i, column=1, sticky='w', pady=5)
        actions = ttk.Frame(tab)
        actions.grid(row=3, column=0, sticky='w', pady=(4, 0))
        ttk.Button(actions, text='Refresh', command=self._client_refresh).pack(side='left', padx=(0, 6))
        ttk.Button(actions, text='Open Roblox', command=self._open_selected_roblox).pack(side='left')
        fps_box = ttk.LabelFrame(tab, text='FPS', padding=(10, 8))
        fps_box.grid(row=4, column=0, sticky='ew', pady=(12, 0))
        self.fps_value_label = ttk.Label(fps_box, font=('Segoe UI Semibold', 10))
        self.fps_value_label.pack(anchor='w')
        self.fps_pid_label = ttk.Label(fps_box, text='PID: Waiting for Roblox...', foreground='#9aa0a6')
        self.fps_pid_label.pack(anchor='w', pady=(0, 4))

        def _fps_ui(value=None):
            fps = int(round(float(self.fps_limit.get() if value is None else value)))
            fps = max(0, min(240, fps))
            if self.fps_limit.get() != fps:
                self.fps_limit.set(fps)
            self.fps_value_label.config(text='FPS: Uncap' if fps == 0 else f'FPS: {fps}')
            if hasattr(self, '_fps_text_var') and self._fps_text_var.get() != str(fps):
                self._fps_text_var.set(str(fps))

        def _fps_slider_released(_event=None):
            if getattr(self, '_fps_release_job', None):
                try:
                    self.after_cancel(self._fps_release_job)
                except Exception:
                    pass
            self._fps_release_job = self.after(80, self._apply_fps_after_slider)
        ttk.Scale(fps_box, from_=0, to=240, orient='horizontal', variable=self.fps_limit, command=_fps_ui).pack(fill='x')
        self._fps_scale_widget = fps_box.winfo_children()[-1]
        self._fps_scale_widget.bind('<ButtonRelease-1>', _fps_slider_released, add='+')
        self._fps_text_var = tk.StringVar(value=str(self.fps_limit.get()))
        self._fps_text_entry = ttk.Entry(fps_box, textvariable=self._fps_text_var, width=12)
        self._fps_text_entry.pack(anchor='w', pady=(6, 0))

        def _fps_text_apply(_event=None):
            try:
                fps = int(self._fps_text_var.get().strip())
            except Exception:
                self._fps_text_var.set(str(self.fps_limit.get()))
                return
            fps = max(0, min(240, fps))
            self.fps_limit.set(fps)
            _fps_ui(fps)
            self._apply_fps_after_slider()
        self._fps_text_entry.bind('<Return>', _fps_text_apply)
        self._fps_text_entry.bind('<FocusOut>', _fps_text_apply)
        fps_hotkey_frame = ttk.Frame(fps_box)
        fps_hotkey_frame.pack(fill='x', pady=(8, 0))
        self._fps_hotkey_frame = fps_hotkey_frame
        self._build_fps_hotkey_buttons()
        fps_hotkey_actions = ttk.Frame(fps_box)
        fps_hotkey_actions.pack(fill='x', pady=(6, 0))
        ttk.Button(fps_hotkey_actions, text='Reset Hotkeys', command=self._reset_fps_hotkeys).pack(side='left')
        ttk.Label(fps_box, text='FPS Changer', font=('Segoe UI', 8), foreground='#9aa0a6').pack(anchor='w')
        self._refresh_fps_hotkey_buttons()
        _fps_ui()
        self._client_cpu_prev = None
        self._client_system_prev = None
        self._client_refresh()
        self.after(UI_CLIENT_INTERVAL_MS, self._client_live_update)

    def _client_roblox_pids(self):
        if os.name != 'nt':
            return []
        try:
            import ctypes

            class PROCESSENTRY32W(ctypes.Structure):
                _fields_ = [('dwSize', ctypes.wintypes.DWORD), ('cntUsage', ctypes.wintypes.DWORD), ('th32ProcessID', ctypes.wintypes.DWORD), ('th32DefaultHeapID', ctypes.POINTER(ctypes.c_ulong)), ('th32ModuleID', ctypes.wintypes.DWORD), ('cntThreads', ctypes.wintypes.DWORD), ('th32ParentProcessID', ctypes.wintypes.DWORD), ('pcPriClassBase', ctypes.c_long), ('dwFlags', ctypes.wintypes.DWORD), ('szExeFile', ctypes.wintypes.WCHAR * 260)]
            snap = ctypes.windll.kernel32.CreateToolhelp32Snapshot(2, 0)
            if snap in (0, -1):
                return []
            procs = []
            pe = PROCESSENTRY32W()
            pe.dwSize = ctypes.sizeof(pe)
            try:
                ok = ctypes.windll.kernel32.Process32FirstW(snap, ctypes.byref(pe))
                while ok:
                    name = pe.szExeFile.lower()
                    if name in ('robloxplayerbeta.exe', 'roblox.exe'):
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
        if not pids:
            return (None, None)
        try:
            import ctypes, ctypes.wintypes as wt
            PROCESS_QUERY_LIMITED_INFORMATION = 4096
            PROCESS_VM_READ = 16

            class PMC(ctypes.Structure):
                _fields_ = [('cb', wt.DWORD), ('PageFaultCount', wt.DWORD), ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t), ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t), ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t), ('QuotaNonPagedPoolUsage', ctypes.c_size_t), ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t)]
            total_cpu = 0
            total_ram = 0
            any_cpu = False
            any_ram = False
            for pid in pids:
                h = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_VM_READ, False, int(pid))
                if not h:
                    h = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
                if not h:
                    continue
                try:
                    pm = PMC()
                    pm.cb = ctypes.sizeof(pm)
                    if ctypes.windll.psapi.GetProcessMemoryInfo(h, ctypes.byref(pm), pm.cb):
                        total_ram += int(pm.WorkingSetSize)
                        any_ram = True
                    c = wt.FILETIME()
                    e = wt.FILETIME()
                    k = wt.FILETIME()
                    u = wt.FILETIME()
                    if ctypes.windll.kernel32.GetProcessTimes(h, ctypes.byref(c), ctypes.byref(e), ctypes.byref(k), ctypes.byref(u)):
                        total_cpu += (k.dwHighDateTime << 32 | k.dwLowDateTime) + (u.dwHighDateTime << 32 | u.dwLowDateTime)
                        any_cpu = True
                finally:
                    ctypes.windll.kernel32.CloseHandle(h)
            if not any_cpu and (not any_ram):
                return (None, None)
            st = wt.FILETIME()
            kt = wt.FILETIME()
            ut = wt.FILETIME()
            if ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(st), ctypes.byref(kt), ctypes.byref(ut)):
                system_time = (kt.dwHighDateTime << 32 | kt.dwLowDateTime) + (ut.dwHighDateTime << 32 | ut.dwLowDateTime)
                idle_time = st.dwHighDateTime << 32 | st.dwLowDateTime
                cpu_data = (total_cpu, (system_time, idle_time))
            else:
                cpu_data = total_cpu
            return (cpu_data, total_ram if any_ram else None)
        except Exception:
            return (None, None)

    def _client_game_refresh(self, place_id, job_id):
        place_id = str(place_id or '').strip()
        self.client_place_var.set(place_id or '—')
        self.client_job_var.set(str(job_id or '—'))
        if not place_id:
            self.client_game_var.set('Not in a game')
            return
        self.client_game_var.set('Resolving game name...')

        def worker():
            name = None
            try:
                name = self._resolve_history_game_name(place_id)
            except Exception:
                pass
            if not name:
                name = f'Place {place_id}'
            try:

                def update():
                    self.client_game_var.set(name)
                    self.client_place_var.set(f'{place_id} — {name}')
                self.after(0, update)
            except Exception:
                pass
        threading.Thread(target=worker, daemon=True).start()

    def _client_live_update(self):
        try:
            active = False
            if hasattr(self, 'nb'):
                active = str(self.nb.tab(self.nb.select(), 'text')) == 'Client'
            if not active and (not getattr(self, '_client_tab_active', False)):
                self.after(UI_CLIENT_INTERVAL_MS, self._client_live_update)
                return
            pids = self._client_roblox_pids()
            if pids:
                stats, ram = self._client_process_stats(pids)
                if isinstance(stats, tuple) and len(stats) == 2 and isinstance(stats[1], tuple):
                    proc, system = stats
                    if self._client_cpu_prev and self._client_system_prev:
                        dp = proc - self._client_cpu_prev
                        ds_total = system[0] - self._client_system_prev[0]
                        prev_busy = self._client_system_prev[0] - self._client_system_prev[1]
                        curr_busy = system[0] - system[1]
                        busy = curr_busy - prev_busy
                        if ds_total > 0:
                            cpu_pct = dp / ds_total * 100.0
                            self.client_cpu_var.set(f'{max(0.0, min(100.0, cpu_pct)):.1f}%')
                    self._client_cpu_prev = proc
                    self._client_system_prev = system
                elif isinstance(stats, (int, float)):
                    if self._client_cpu_prev is not None:
                        dp = stats - self._client_cpu_prev
                        if dp >= 0:
                            self.client_cpu_var.set(f'{dp / 10000000 * 100:.1f}%')
                    self._client_cpu_prev = stats
                if ram is not None:
                    self.client_ram_var.set(f'{ram / 1024 / 1024:.1f} MB')
            else:
                self._client_cpu_prev = None
                self._client_system_prev = None
                self.client_cpu_var.set('—')
                self.client_ram_var.set('—')
        except Exception:
            pass
        try:
            self.after(UI_CLIENT_INTERVAL_MS, self._client_live_update)
        except Exception:
            pass

    def _client_refresh(self):
        pids = self._client_roblox_pids()
        pid = pids[0] if pids else _fflag_find_pid()
        path = _get_process_exe_path(pid) if pid else ''
        if not path:
            saved = str(self.settings.get('roblox_path', '') or '')
            if saved and os.path.isfile(saved):
                path = saved
        self.client_pid_var.set(', '.join((str(x) for x in sorted(pids))) if pids else 'Not running' if not pid else str(pid))
        self.client_status_var.set('Running' if pids or pid else 'Not running')
        self.client_path_var.set(path or 'Roblox Game Client not found')
        version = '—'
        if path and os.path.isfile(path):
            try:
                import win32api
                info = win32api.GetFileVersionInfo(path, '\\')
                ms = info['FileVersionMS']
                ls = info['FileVersionLS']
                version = f'{ms >> 16}.{ms & 65535}.{ls >> 16}.{ls & 65535}'
            except Exception:
                pass
        self.client_version_var.set(version)
        place_id, job_id = self._detect_current_game(silent=True) if pids or pid else (None, None)
        self._client_game_refresh(place_id, job_id)
        self._client_cpu_prev = None
        self._client_system_prev = None

    def _build_subplace_joiner_tab(self):
        tab = ttk.Frame(self.nb, padding=0)
        self.nb.add(tab, text='Subplace Joiner')
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)
        ttk.Label(tab, text='Subplace Joiner', font=('Segoe UI Semibold', 15)).grid(row=0, column=0, sticky='w')
        row = ttk.Frame(tab)
        row.grid(row=1, column=0, sticky='ew', pady=8)
        row.columnconfigure(0, weight=1)
        self.subplace_id = tk.StringVar()
        ttk.Entry(row, textvariable=self.subplace_id).grid(row=0, column=0, sticky='ew')
        ttk.Button(row, text='Search', command=self._subplace_search).grid(row=0, column=1, padx=6)
        self.subplace_tree = ttk.Treeview(tab, columns=('id', 'name'), show='headings')
        self.subplace_tree.heading('id', text='PLACE ID')
        self.subplace_tree.heading('name', text='NAME')
        self.subplace_tree.column('id', width=160)
        self.subplace_tree.column('name', width=400)
        self.subplace_tree.grid(row=2, column=0, sticky='nsew')
        buttons = ttk.Frame(tab)
        buttons.grid(row=3, column=0, sticky='e', pady=8)
        ttk.Button(buttons, text='Join Selected', command=self._subplace_join).pack(side='left', padx=(0, 6))
        ttk.Button(buttons, text='Copy Deeplink', command=self._subplace_copy_deeplink).pack(side='left')

    def _subplace_search(self):
        pid = self.subplace_id.get().strip()
        if not pid.isdigit():
            return
        try:
            req = urllib.request.Request(f'https://apis.roblox.com/universes/v1/places/{pid}/universe')
            with urllib.request.urlopen(req, timeout=10) as r:
                universe_id = json.load(r).get('universeId')
            if not universe_id:
                raise ValueError('Universe not found for this Place ID.')
            req = urllib.request.Request(f'https://develop.roblox.com/v1/universes/{universe_id}/places?limit=100&sortOrder=Asc')
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.load(r)
            self.subplace_tree.delete(*self.subplace_tree.get_children())
            for x in data.get('data', []):
                self.subplace_tree.insert('', 'end', values=(x.get('id', ''), x.get('name', x.get('id', ''))))
        except Exception as e:
            messagebox.showerror('Subplace Joiner', f'Search failed:\n{e}', parent=self)

    def _subplace_copy_deeplink(self):
        place_id = None
        game_instance_id = None
        logs_dir = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Roblox', 'logs')
        uuid_re = '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
        try:
            log_files = sorted([os.path.join(logs_dir, f) for f in os.listdir(logs_dir) if f.lower().endswith('.log')], key=lambda x: os.path.getmtime(x), reverse=True)[:30]
            join_re = re.compile(f"""!\\s*Joining\\s+game\\s+[\\"']?({uuid_re})[\\"']?\\s+place\\s+(\\d+)""", re.IGNORECASE)
            for log_path in log_files:
                try:
                    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                except Exception:
                    continue
                matches = list(join_re.finditer(text))
                if matches:
                    m = matches[-1]
                    game_instance_id, place_id = (m.group(1), m.group(2))
                    break
            if not place_id or not game_instance_id:
                for log_path in log_files:
                    try:
                        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                            text = f.read()
                    except Exception:
                        continue
                    if not place_id:
                        m = re.findall('\\bplaceid\\s*[:=]\\s*(\\d+)', text, re.IGNORECASE)
                        if m:
                            place_id = m[-1]
                    if not game_instance_id:
                        m = re.findall(f"""\\bjobId\\s*[:=]\\s*[\\"']?({uuid_re})""", text, re.IGNORECASE)
                        if m:
                            game_instance_id = m[-1]
                    if place_id and game_instance_id:
                        break
        except Exception as e:
            messagebox.showerror('Subplace Joiner', f'Could not read Roblox logs:\n{e}', parent=self)
            return
        if not place_id or not game_instance_id:
            messagebox.showwarning('Subplace Joiner', 'Could not detect the current Roblox server. Make sure you are inside a game, then try again.', parent=self)
            return
        link = f'roblox://experiences/start?placeId={place_id}&gameInstanceId={game_instance_id}'
        self._history_add(place_id, game_instance_id)
        try:
            self.clipboard_clear()
            self.clipboard_append(link)
            self.update_idletasks()
            messagebox.showinfo('Subplace Joiner', "Current game's deeplink copied to clipboard.", parent=self)
        except Exception as e:
            messagebox.showerror('Subplace Joiner', f'Could not copy deeplink:\n{e}', parent=self)

    def _subplace_join(self):
        sel = self.subplace_tree.selection()
        if not sel:
            return
        pid = self.subplace_tree.item(sel[0], 'values')[0]
        try:
            os.startfile(f'roblox://placeId={pid}')
            self._console_log(f'Joined subplace {pid}')
        except Exception as e:
            messagebox.showerror('Subplace Joiner', f'Could not launch Roblox:\n{e}', parent=self)

    def _build_server_viewer_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.add(tab, text='Server Viewer')
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)
        head = ttk.Frame(tab)
        head.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(head, text='Server Viewer', font=('Segoe UI Semibold', 15)).pack(side='left')
        self.server_viewer_status = ttk.Label(head, text='Paste a Roblox server deeplink', foreground='#9aa0a6')
        self.server_viewer_status.pack(side='right')
        row = ttk.Frame(tab)
        row.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        row.columnconfigure(0, weight=1)
        self.server_viewer_link = tk.StringVar()
        ttk.Entry(row, textvariable=self.server_viewer_link).grid(row=0, column=0, sticky='ew')
        ttk.Button(row, text='View Server', command=self._server_viewer_load).grid(row=0, column=1, padx=(6, 0))
        ttk.Button(row, text='Clear', command=self._server_viewer_clear).grid(row=0, column=2, padx=(6, 0))
        body = ttk.PanedWindow(tab, orient='horizontal')
        body.grid(row=2, column=0, sticky='nsew')
        left = ttk.Frame(body)
        right = ttk.Frame(body)
        body.add(left, weight=1)
        body.add(right, weight=1)
        self.server_viewer_body = body
        left.columnconfigure(0, weight=1)
        left.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)
        info = ttk.LabelFrame(left, text='Server Information')
        info.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        for i in range(2):
            info.columnconfigure(i, weight=1)
        self.server_viewer_vars = {}
        fields = [('Place ID', 'place_id'), ('Job ID', 'job_id'), ('Players', 'players'), ('Max Capacity', 'max_players'), ('Ping', 'ping'), ('Server FPS', 'fps'), ('Location', 'location')]
        for i, (label, key) in enumerate(fields):
            r, c = divmod(i, 2)
            ttk.Label(info, text=label, foreground='#9aa0a6').grid(row=r * 2, column=c, sticky='w', padx=8, pady=(6, 0))
            var = tk.StringVar(value='—')
            self.server_viewer_vars[key] = var
            ttk.Label(info, textvariable=var).grid(row=r * 2 + 1, column=c, sticky='w', padx=8, pady=(0, 6))
        note = ttk.Label(left, text='\n', foreground='#9aa0a6', justify='left')
        note.grid(row=1, column=0, sticky='nw', pady=(4, 0))
        ttk.Label(right, text='', font=('Segoe UI Semibold', 10)).grid(row=0, column=0, sticky='w', pady=(0, 6))
        self.server_viewer_players = tk.Listbox(right, bg=_CURRENT_PALETTE['bg_medium'], fg=_CURRENT_PALETTE['fg'], relief='flat', bd=0, highlightthickness=0, selectbackground=_CURRENT_PALETTE['bg_light'])
        self.server_viewer_players.grid(row=1, column=0, sticky='nsew')
        _set_pane_minsize(body, left, 280)
        _set_pane_minsize(body, right, 280)
        self.after_idle(lambda: self._center_server_viewer_pane(body))

    @staticmethod
    def _center_server_viewer_pane(body):
        try:
            width = body.winfo_width()
            if width > 0:
                body.sashpos(0, width // 2)
        except Exception:
            pass

    @staticmethod
    def _server_viewer_parse_deeplink(value):
        value = str(value or '').strip()
        if not value:
            raise ValueError('Paste a Roblox deeplink first.')
        parsed = urlparse(value)
        query = parse_qs(parsed.query)
        place_id = None
        job_id = None
        for key in ('placeId', 'placeid', 'placeID'):
            if query.get(key):
                place_id = query[key][0]
                break
        for key in ('gameInstanceId', 'gameinstanceid', 'jobId', 'jobid'):
            if query.get(key):
                job_id = query[key][0]
                break
        if not place_id or not str(place_id).isdigit():
            m = re.search('(?:placeId|placeid)[=/](\\d+)', value, re.IGNORECASE)
            if m:
                place_id = m.group(1)
        if not job_id:
            m = re.search('(?:gameInstanceId|jobId|jobid)[=/]([0-9a-fA-F-]{32,36})', value, re.IGNORECASE)
            if m:
                job_id = m.group(1)
        if not place_id or not job_id:
            raise ValueError('The deeplink must contain both placeId and gameInstanceId/jobId.')
        return (str(place_id), str(job_id))

    def _server_viewer_clear(self):
        self.server_viewer_link.set('')
        for var in self.server_viewer_vars.values():
            var.set('—')
        self.server_viewer_players.delete(0, tk.END)
        self.server_viewer_status.config(text='Paste a Roblox server deeplink', foreground='#9aa0a6')

    def _server_viewer_load(self):
        try:
            place_id, job_id = self._server_viewer_parse_deeplink(self.server_viewer_link.get())
        except Exception as e:
            messagebox.showerror('Server Viewer', str(e), parent=self)
            return
        self.server_viewer_status.config(text='Loading server...', foreground='#f2c94c')
        self._console_log(f'Loading server deeplink: {self.server_viewer_link.get()}')
        self.server_viewer_players.delete(0, tk.END)
        for var in self.server_viewer_vars.values():
            var.set('—')
        threading.Thread(target=self._server_viewer_worker, args=(place_id, job_id), daemon=True, name='RoUtils-ServerViewer').start()

    def _server_viewer_worker(self, place_id, job_id):
        try:
            cursor = None
            found = None
            pages = 0
            while pages < 50:
                pages += 1
                params = 'sortOrder=Asc&excludeFullGames=false&limit=100'
                if cursor:
                    from urllib.parse import quote
                    params += '&cursor=' + quote(cursor, safe='')
                url = f'https://games.roblox.com/v1/games/{place_id}/servers/Public?{params}'
                req = urllib.request.Request(url, headers={'User-Agent': 'RoUtils/3.4'})
                with urllib.request.urlopen(req, timeout=15) as r:
                    data = json.loads(r.read().decode('utf-8', 'replace'))
                for server in data.get('data', []):
                    if str(server.get('id', '')) == job_id:
                        found = server
                        break
                if found:
                    break
                cursor = data.get('nextPageCursor')
                if not cursor:
                    break
            if not found:
                raise ValueError('That server was not found in the public server list. It may have closed, be private, or no longer be listed.')
            players = found.get('playing', 0)
            max_players = found.get('maxPlayers', 0)
            ping = found.get('ping')
            fps = found.get('fps')
            tokens = found.get('playerTokens') or []
            public_players = found.get('players') or []
            result = {'place_id': place_id, 'job_id': job_id, 'players': f'{players}/{max_players}', 'max_players': str(max_players), 'ping': f'{round(float(ping))} ms' if ping is not None else '—', 'fps': f'{float(fps):.1f}' if fps is not None else '—', 'tokens': tokens, 'public_players': public_players}
            self.after(0, lambda result=result: self._server_viewer_show(result))
        except Exception as e:
            self.after(0, lambda msg=str(e): self._server_viewer_error(msg))

    def _server_viewer_show(self, result):
        for key in ('place_id', 'job_id', 'players', 'max_players', 'ping', 'fps'):
            self.server_viewer_vars[key].set(result[key])
        self.server_viewer_players.delete(0, tk.END)
        public_players = result.get('public_players') or []
        tokens = result.get('tokens') or []
        if public_players:
            for player in public_players:
                if isinstance(player, dict):
                    name = player.get('username') or player.get('name') or player.get('displayName') or str(player)
                else:
                    name = str(player)
                self.server_viewer_players.insert(tk.END, name)
        elif tokens:
            for i, token in enumerate(tokens, 1):
                self.server_viewer_players.insert(tk.END, f'Player {i}')
        else:
            self.server_viewer_players.insert(tk.END, '')
        self.server_viewer_status.config(text='Server loaded', foreground='#65d98b')

    def _server_viewer_error(self, message):
        self.server_viewer_status.config(text='Failed to load server', foreground='#ff6b6b')
        messagebox.showerror('Server Viewer', f'Could not load server:\n{message}', parent=self)

    def _build_fflag_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.insert(1, tab, text='FFlags')
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)
        head = ttk.Frame(tab)
        head.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(head, text='FFlags', font=('Segoe UI Semibold', 15)).pack(side='left')
        self.fflag_status = ttk.Label(head, text='Waiting for Roblox...', foreground='#9aa0a6')
        self.fflag_status.pack(side='right', padx=(8, 0))
        bar = ttk.Frame(tab)
        bar.grid(row=1, column=0, sticky='ew', pady=(0, 8))
        buttons = [('+ Add', self._fflag_add_dialog), ('Remove', self._fflag_remove), ('Remove All', self._fflag_remove_all), ('Presets', self._fflag_presets_dialog), ('Import', self._fflag_import), ('Export', self._fflag_export), ('Hotkeys', self._fflag_hotkeys_dialog), ('JSON Editor', self._fflag_json_editor), ('Default FFlag Values', self._open_default_fflag_values), ('Latest FFlag List', self._open_latest_fflag_list)]
        self._fflag_toolbar = []
        for text, cmd in buttons:
            button = ttk.Button(bar, text=text, command=cmd)
            button.pack(side='left', padx=(0, 5))
            self._fflag_toolbar.append(button)
        bar.bind('<Configure>', self._responsive_fflag_toolbar, add='+')
        self._fflag_toolbar_frame = bar
        frame = ttk.PanedWindow(tab, orient='horizontal')
        frame.grid(row=2, column=0, sticky='nsew')
        left = ttk.Frame(frame)
        right = ttk.Frame(frame)
        frame.add(left, weight=4)
        frame.add(right, weight=1)
        left.columnconfigure(0, weight=1)
        left.rowconfigure(1, weight=1)
        search_row = ttk.Frame(left)
        search_row.grid(row=0, column=0, sticky='ew', pady=(0, 6))
        ttk.Label(search_row, text='Search:').pack(side='left')
        self.fflag_search = tk.StringVar()
        ent = ttk.Entry(search_row, textvariable=self.fflag_search)
        ent.pack(side='left', fill='x', expand=True, padx=6)
        self.fflag_search.trace_add('write', lambda *_: self._refresh_fflag_list())
        cols = ('name', 'type', 'value', 'remove')
        self.fflag_tree = ttk.Treeview(left, columns=cols, show='headings', selectmode='browse')
        self.fflag_tree.heading('name', text='NAME')
        self.fflag_tree.heading('type', text='TYPE')
        self.fflag_tree.heading('value', text='VALUE')
        self.fflag_tree.heading('remove', text='')
        self.fflag_tree.column('name', width=430, anchor='w')
        self.fflag_tree.column('type', width=85, anchor='center', stretch=False)
        self.fflag_tree.column('value', width=200, anchor='w')
        self.fflag_tree.column('remove', width=28, minwidth=28, stretch=False, anchor='center')
        self.fflag_tree.grid(row=1, column=0, sticky='nsew')
        self.fflag_tree.bind('<Double-1>', self._fflag_inline_edit)
        self.fflag_tree.bind('<Button-1>', self._fflag_tree_click_remove, add='+')
        self._fflag_apply_selected_btn = ttk.Button(right, text='Apply Selected Json', command=self._apply_selected_json)
        self._fflag_apply_selected_btn.pack(fill='x', padx=8, pady=(4, 6))
        ttk.Label(right, text='Saved JSONs', font=('Segoe UI Semibold', 10)).pack(anchor='w', padx=8, pady=(0, 6))
        self.json_tree = tk.Listbox(right, bg=_CURRENT_PALETTE['bg_medium'], fg=_CURRENT_PALETTE['fg'], relief='flat', bd=0, highlightthickness=0)
        self.json_tree.pack(fill='both', expand=True, padx=8, pady=(0, 8))
        self.json_tree.bind('<Double-1>', lambda _e: self._apply_selected_json())
        ttk.Button(right, text='Refresh', command=self._refresh_json_list).pack(fill='x', padx=8, pady=(0, 8))
        self._refresh_json_list()
        bottom = ttk.Frame(tab)
        bottom.grid(row=3, column=0, sticky='ew', pady=(8, 0))
        ttk.Button(bottom, text='Apply to Roblox', command=self._fflag_apply).pack(side='right', padx=(5, 0))
        ttk.Button(bottom, text='Save Flags', command=self._save_fflag_flags).pack(side='right')
        ttk.Button(bottom, text='Refresh', command=self._fflag_refresh_process).pack(side='left')
        ttk.Button(bottom, text='AI', command=self._open_ai_chat).pack(side='left', padx=(5, 0))
        self._refresh_fflag_list()
        self.after(1000, self._fflag_refresh_process)

    def _responsive_fflag_toolbar(self, _event=None):
        bar = getattr(self, '_fflag_toolbar_frame', None)
        buttons = getattr(self, '_fflag_toolbar', [])
        if bar is None or not buttons:
            return
        try:
            narrow = bar.winfo_width() > 0 and bar.winfo_width() < 1050
            if narrow == getattr(self, '_fflag_toolbar_narrow', None):
                return
            self._fflag_toolbar_narrow = narrow
            if narrow:
                for index, button in enumerate(buttons):
                    button.pack_forget()
                    button.grid(row=index // 4, column=index % 4, sticky='ew', padx=(0, 5), pady=(0, 3))
                for col in range(4):
                    bar.columnconfigure(col, weight=1)
            else:
                for button in buttons:
                    button.grid_forget()
                    button.pack(side='left', padx=(0, 5), pady=0)
        except Exception:
            pass

    def _fflag_conflicts(self):
        counts = {}
        for flag in self.fflag_flags:
            name = fflag_strip_prefix(str(flag.get('name', '')).strip())
            if name:
                key = name.lower()
                counts[key] = counts.get(key, 0) + 1
        return {name for name, count in counts.items() if count > 1}

    def _refresh_fflag_list(self):
        if not hasattr(self, 'fflag_tree'):
            return
        old_job = getattr(self, '_fflag_render_job', None)
        if old_job:
            try:
                self.after_cancel(old_job)
            except Exception:
                pass
            self._fflag_render_job = None
        tree = self.fflag_tree
        tree.delete(*tree.get_children())
        filt = self.fflag_search.get().strip().lower() if hasattr(self, 'fflag_search') else ''
        conflicts = self._fflag_conflicts()
        try:
            tree.tag_configure('conflict', background='#8b1e1e', foreground='#ffffff')
        except Exception:
            pass

        rows = []
        for i, flag in enumerate(self.fflag_flags):
            name = fflag_strip_prefix(str(flag.get('name', '')))
            if filt and filt not in name.lower():
                continue
            tags = ('conflict',) if name.lower() in conflicts else ()
            rows.append((i, name, flag.get('type', ''), flag.get('value', ''), tags))

        batch_size = 150
        state = {'index': 0}

        def insert_batch():
            start = state['index']
            end = min(start + batch_size, len(rows))
            for i, name, flag_type, value, tags in rows[start:end]:
                try:
                    tree.insert('', 'end', iid=str(i), values=(name, flag_type, value, '×'), tags=tags)
                except tk.TclError:
                    return
            state['index'] = end
            if end < len(rows):
                self._fflag_render_job = self.after(1, insert_batch)
            else:
                self._fflag_render_job = None

        insert_batch()

    def _fflag_tree_click_remove(self, event):
        try:
            row = self.fflag_tree.identify_row(event.y)
            col = self.fflag_tree.identify_column(event.x)
            if row and col == '#4':
                idx = int(row)
                if 0 <= idx < len(self.fflag_flags):
                    self.fflag_flags.pop(idx)
                    self._save_fflag_flags()
                    self._refresh_fflag_list()
                    self._console_log('Removed FFlag')
                return 'break'
        except Exception:
            pass
        return None

    def _fflag_add_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title('Add FFlag')
        dlg.transient(self)
        theme_toplevel(dlg)
        ttk.Label(dlg, text='FFlag name').grid(row=0, column=0, padx=10, pady=(10, 4), sticky='w')
        name = ttk.Entry(dlg, width=48)
        name.grid(row=1, column=0, padx=10, sticky='ew')
        ttk.Label(dlg, text='Value:').grid(row=2, column=0, padx=10, pady=(8, 4), sticky='w')
        value = ttk.Entry(dlg, width=48)
        value.grid(row=3, column=0, padx=10, sticky='ew')

        def add():
            n, v = (name.get().strip(), value.get().strip())
            if not n or not v:
                return
            bare = fflag_strip_prefix(n)
            self.fflag_flags.append({'name': bare, 'value': v, 'type': fflag_infer_type(v)})
            self._save_fflag_flags()
            self._refresh_fflag_list()
            self._fflag_apply(silent=True)
            dlg.destroy()
            self._console_log(f'Added FFlag {bare} = {v}')
        btns = ttk.Frame(dlg)
        btns.grid(row=4, column=0, pady=10)
        ttk.Button(btns, text='Add Flag', command=add).pack(side='left', padx=4)
        ttk.Button(btns, text='Cancel', command=dlg.destroy).pack(side='left', padx=4)
        dlg.columnconfigure(0, weight=1)
        name.focus_set()

    def _fflag_inline_edit(self, event):
        tree = self.fflag_tree
        row = tree.identify_row(event.y)
        col = tree.identify_column(event.x)
        if not row or col not in ('#1', '#3'):
            return
        idx = int(row)
        column = 'name' if col == '#1' else 'value'
        bbox = tree.bbox(row, col)
        if not bbox:
            return
        x, y, w, h = bbox
        entry = ttk.Entry(tree)
        entry.place(x=x, y=y, width=w, height=h)
        entry.insert(0, str(self.fflag_flags[idx].get(column, '')))
        entry.focus_set()
        entry.selection_range(0, 'end')

        def save(_=None):
            value = entry.get().strip()
            if value:
                self.fflag_flags[idx][column] = fflag_strip_prefix(value) if column == 'name' else value
                self.fflag_flags[idx]['type'] = fflag_infer_type(self.fflag_flags[idx].get('value', ''))
                self._save_fflag_flags()
                self._refresh_fflag_list()
                self._fflag_apply(silent=True)
            entry.destroy()
        entry.bind('<Return>', save)
        entry.bind('<FocusOut>', save)
        entry.bind('<Escape>', lambda _e: entry.destroy())

    def _fflag_remove(self):
        sel = self.fflag_tree.selection()
        if not sel:
            return
        removed = self.fflag_flags[int(sel[0])].get('name', '')
        del self.fflag_flags[int(sel[0])]
        self._save_fflag_flags()
        self._refresh_fflag_list()
        self._console_log(f'Removed FFlag {removed}')

    def _fflag_remove_all(self):
        if not self.fflag_flags or not messagebox.askyesno('FFlags', 'Remove all flags?', parent=self):
            return
        self.fflag_flags.clear()
        self._save_fflag_flags()
        self._refresh_fflag_list()
        self._console_log('Removed all FFlags')

    def _fflag_presets_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title('FFlag Presets')
        dlg.geometry('620x520')
        dlg.transient(self)
        theme_toplevel(dlg)
        ttk.Label(dlg, text='FFlag Presets', font=('Segoe UI Semibold', 12)).pack(anchor='w', padx=12, pady=(10, 6))
        ttk.Label(dlg, text='Select a preset, then choose whether to replace or add its FFlags to the current list.', foreground='#9aa0a6').pack(anchor='w', padx=12, pady=(0, 8))
        search = tk.StringVar()
        ttk.Entry(dlg, textvariable=search).pack(fill='x', padx=12, pady=(0, 8))
        body = ttk.Frame(dlg)
        body.pack(fill='both', expand=True, padx=12, pady=4)
        canvas = tk.Canvas(body, bg=_CURRENT_PALETTE['bg_medium'], highlightthickness=0, bd=0)
        scroll = ttk.Scrollbar(body, orient='vertical', command=canvas.yview)
        inner = ttk.Frame(canvas, style='RoUtils.Settings.TFrame')
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        window = canvas.create_window((0, 0), window=inner, anchor='nw')
        inner.bind('<Configure>', lambda _e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfigure(window, width=e.width))
        state = {'files': []}

        def load_preset(url, filename, add_to_current=False):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'RoUtils'})
                with urllib.request.urlopen(req, timeout=15) as r:
                    data = json.loads(r.read().decode('utf-8'))
                flags = _normalize_fflag_json(data)
                if not flags:
                    raise ValueError('Preset JSON did not contain any FFlags.')
                if add_to_current:
                    existing = {str(x.get('name', '')): i for i, x in enumerate(self.fflag_flags)}
                    added = 0
                    updated = 0
                    for flag in flags:
                        name = str(flag.get('name', ''))
                        if name in existing:
                            self.fflag_flags[existing[name]] = flag
                            updated += 1
                        else:
                            self.fflag_flags.append(flag)
                            existing[name] = len(self.fflag_flags) - 1
                            added += 1
                    self._save_fflag_flags()
                    self._refresh_fflag_list()
                    if self.fflag_pid and self.fflag_engine.handle and self.fflag_auto_apply.get():
                        self._fflag_apply(silent=True)
                    messagebox.showinfo('FFlag Preset', f'Added {added} FFlags and updated {updated} existing FFlags from {filename}.', parent=dlg)
                    self._console_log(f'Preset {filename}: added {added}, updated {updated} FFlags')
                else:
                    self.fflag_flags = flags
                    self._save_fflag_flags()
                    self._refresh_fflag_list()
                    if self.fflag_pid and self.fflag_engine.handle and self.fflag_auto_apply.get():
                        self._fflag_apply(silent=True)
                    messagebox.showinfo('FFlag Preset', f'Applied {len(flags)} FFlags from {filename}.', parent=dlg)
                    self._console_log(f'Applied FFlag preset {filename}: {len(flags)} flags')
                dlg.destroy()
            except Exception as e:
                messagebox.showerror('FFlag Preset', f'Failed to load {filename}:\n{e}', parent=dlg)

        def render(*_):
            for w in inner.winfo_children():
                w.destroy()
            needle = search.get().strip().lower()
            for item in state['files']:
                name = item.get('name', '')
                if needle and needle not in name.lower():
                    continue
                label = os.path.splitext(name)[0]
                row = ttk.Frame(inner)
                row.pack(fill='x', pady=3)
                ttk.Button(row, text=label, command=lambda u=item['download_url'], n=label: load_preset(u, n, False)).pack(side='left', fill='x', expand=True, padx=(0, 4))
                ttk.Button(row, text='Add to Current FFlags', command=lambda u=item['download_url'], n=label: load_preset(u, n, True)).pack(side='right')

        def worker():
            try:
                req = urllib.request.Request(GITHUB_PRESETS_API, headers={'User-Agent': 'RoUtils'})
                with urllib.request.urlopen(req, timeout=15) as r:
                    items = json.loads(r.read().decode('utf-8'))
                files = [x for x in items if x.get('type') == 'file' and str(x.get('name', '')).lower().endswith('.json')]
                files.sort(key=lambda x: str(x.get('name', '')).lower())

                def done():
                    state['files'] = files
                    render()
                    if not files:
                        ttk.Label(inner, text='No JSON presets found.', foreground='#9aa0a6').pack(pady=20)
                self.after(0, done)
            except Exception as e:
                self.after(0, lambda: ttk.Label(inner, text=f'Could not load presets: {e}', foreground='#ff6b6b').pack(pady=20))
        search.trace_add('write', render)
        ttk.Label(inner, text='Loading presets...', foreground='#9aa0a6').pack(pady=20)
        threading.Thread(target=worker, daemon=True).start()

    def _open_default_fflag_values(self):
        self._console_log('Opened Default FFlag Values')
        _open_webview2_process(WEBVIEW2_URL_DEFAULTS, 'Default FFlag Values')

    def _open_latest_fflag_list(self):
        self._console_log('Loading Latest FFlag List')

        def worker():
            url = _get_latest_offsets_webview_url()
            self.after(0, lambda: (_open_webview2_process(url, 'Latest FFlag List'), self._console_log('Opened Latest FFlag List')))
        threading.Thread(target=worker, daemon=True).start()

    def _fflag_import(self):
        path = filedialog.askopenfilename(parent=self, title='Import FFlags', filetypes=[('JSON files', '*.json'), ('All files', '*.*')])
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            count = 0
            if isinstance(data, dict):
                for n, v in data.items():
                    bare = fflag_strip_prefix(n)
                    found = next((x for x in self.fflag_flags if x.get('name') == bare), None)
                    item = {'name': bare, 'value': str(v).lower() if isinstance(v, bool) else str(v), 'type': fflag_infer_type(v)}
                    if found:
                        found.update(item)
                    else:
                        self.fflag_flags.append(item)
                    count += 1
            elif isinstance(data, list):
                for x in data:
                    if isinstance(x, dict) and x.get('name') is not None:
                        item = {'name': fflag_strip_prefix(x['name']), 'value': str(x.get('value', '')), 'type': x.get('type') or fflag_infer_type(x.get('value', ''))}
                        self.fflag_flags.append(item)
                        count += 1
            self._save_fflag_flags()
            self._refresh_fflag_list()
            messagebox.showinfo('FFlags', f'Imported {count} flag(s).', parent=self)
            self._console_log(f'Imported {count} FFlag(s) from {os.path.basename(path)}')
        except Exception as e:
            messagebox.showerror('FFlags', f'Import failed:\n{e}', parent=self)

    def _fflag_export(self):
        if not self.fflag_flags:
            return
        data = {x['name']: x['value'] for x in self.fflag_flags}
        dialog = tk.Toplevel(self)
        dialog.title('Export FFlags')
        dialog.geometry('470x170')
        dialog.minsize(430, 150)
        dialog.transient(self)
        theme_toplevel(dialog)
        ttk.Label(dialog, text='Export name', font=('Segoe UI Semibold', 10)).pack(anchor='w', padx=14, pady=(14, 4))
        name_var = tk.StringVar(value=f"fflags_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        ttk.Entry(dialog, textvariable=name_var).pack(fill='x', padx=14, pady=(0, 12))
        buttons = ttk.Frame(dialog)
        buttons.pack(fill='x', padx=14)

        def save_json(path, target_label):
            try:
                base = _sanitize_filename_for_windows(name_var.get().strip()) or 'fflags'
                if not base.lower().endswith('.json'):
                    base += '.json'
                if path is None:
                    path = os.path.join(DATA_DIR, 'jsons', base)
                elif os.path.isdir(path):
                    path = os.path.join(path, base)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                try:
                    in_file_saves = hasattr(self.replacer, 'file_saves_dir') and os.path.commonpath((os.path.abspath(path), os.path.abspath(self.replacer.file_saves_dir))) == os.path.abspath(self.replacer.file_saves_dir)
                except ValueError:
                    in_file_saves = False
                if in_file_saves:
                    self.replacer.source_var.set('FileSaves')
                    self.replacer.refresh_view(preserve_selection=True)
                self._console_log(f'Exported {len(data)} FFlag(s) to {target_label}: {path}')
                dialog.destroy()
            except Exception as e:
                messagebox.showerror('FFlags', f'Export failed:\n{e}', parent=dialog)
        ttk.Button(buttons, text='JSONs (FFlags Saves)', command=lambda: save_json(None, 'JSONs')).pack(side='left', expand=True, fill='x', padx=(0, 6))

        def choose_path():
            path = filedialog.asksaveasfilename(parent=dialog, title='Choose FFlag export location', initialfile=name_var.get().strip() + '.json', defaultextension='.json', filetypes=[('JSON files', '*.json'), ('All files', '*.*')])
            if path:
                save_json(path, 'chosen location')
        ttk.Button(buttons, text='Choose...', command=choose_path).pack(side='left', expand=True, fill='x')

    def _fflag_refresh_process(self):
        pid = _fflag_find_pid()
        if pid and pid != self.fflag_pid:
            self.fflag_original_values.clear()
            self.fflag_pid = pid
            exe_path = _get_process_exe_path(pid)
            if exe_path and os.path.basename(exe_path).lower() == 'robloxplayerbeta.exe':
                self.settings['roblox_path'] = exe_path
                self._save_settings()
                if hasattr(self, 'roblox_path_var'):
                    self.roblox_path_var.set(exe_path)
            if self.fflag_engine.attach(pid):
                self.fflag_status.config(text=f'Roblox attached  PID {pid}', foreground='#65d98b')
                self._console_log(f'Roblox Detected: PID {pid}')
                if hasattr(self, 'fps_pid_label'):
                    self.fps_pid_label.config(text=f'PID: {pid} selected', foreground='#65d98b')
                if self.fflag_auto_apply.get():
                    self.after(6000, self._fflag_apply)
            else:
                self.fflag_status.config(text='Roblox found, attach failed', foreground='#ff6b6b')
                self._console_log(f'Roblox Detected but attach failed: PID {pid}')
        elif not pid:
            had_pid = self.fflag_pid
            if had_pid:
                self.fflag_engine.close()
            self.fflag_original_values.clear()
            self.fflag_pid = 0
            self.fflag_status.config(text='Waiting for Roblox...', foreground='#9aa0a6')
            if had_pid:
                self._console_log('Roblox process closed; FFlag attachment removed')
            if hasattr(self, 'fps_pid_label'):
                self.fps_pid_label.config(text='PID: Waiting for Roblox...', foreground='#9aa0a6')
        self.after(1000, self._fflag_refresh_process)

    def _fps_flag_value(self):
        fps = max(0, min(240, int(self.fps_limit.get())))
        return str(fps)

    def _sync_fps_flag_to_manager(self):
        full_name = 'TaskSchedulerTargetFps'
        normalized_name = fflag_strip_prefix(full_name)
        value = self._fps_flag_value()
        fps_entry = None
        cleaned_flags = []
        for flag in self.fflag_flags:
            flag_name = str(flag.get('name', '')).strip()
            if fflag_strip_prefix(flag_name) == normalized_name:
                if fps_entry is None:
                    flag['name'] = full_name
                    flag['value'] = value
                    flag['type'] = 'int'
                    fps_entry = flag
                    cleaned_flags.append(flag)
                continue
            cleaned_flags.append(flag)
        if fps_entry is None:
            fps_entry = {'name': full_name, 'value': value, 'type': 'int'}
            cleaned_flags.append(fps_entry)
        self.fflag_flags = cleaned_flags
        self._save_fflag_flags()
        if hasattr(self, 'fflag_tree'):
            self._refresh_fflag_list()

    def _apply_fps_flag(self, silent=True):
        self._sync_fps_flag_to_manager()
        if not self.fflag_pid or not self.fflag_engine.handle:
            return False
        if not self.fflag_engine.get_singleton():
            return False
        value = self._fps_flag_value()
        return bool(self.fflag_engine.set_flag_with_prefixes('DFIntTaskSchedulerTargetFps', value))

    def _apply_fps_after_slider(self):
        self._fps_release_job = None
        try:
            self._sync_fps_flag_to_manager()
            self._fflag_apply(silent=True)
            self._save_settings()
        except Exception:
            pass

    def _fps_apply_tick(self):
        return

    def _fflag_apply(self, silent=False):
        conflicts = self._fflag_conflicts()
        if conflicts:
            names = [fflag_strip_prefix(str(f.get('name', ''))) for f in self.fflag_flags if fflag_strip_prefix(str(f.get('name', ''))).lower() in conflicts]
            unique_names = []
            seen = set()
            for name in names:
                key = name.lower()
                if key not in seen:
                    seen.add(key)
                    unique_names.append(name)
            self._console_log('FFlag conflict: duplicate names detected: ' + ', '.join(unique_names))
            if not silent:
                messagebox.showerror('FFlags', 'FFlags conflict.', parent=self)
            return
        if not self.fflag_pid or not self.fflag_engine.handle:
            self._console_log('FFlag injection skipped: Roblox is not attached')
            if not silent:
                messagebox.showwarning('FFlags', 'Roblox is not attached.', parent=self)
            return
        if not self.fflag_engine.get_singleton():
            self.fflag_status.config(text='Singleton not found', foreground='#ff6b6b')
            self._console_log(f'FFlag injection failed: singleton not found for PID {self.fflag_pid}')
            return
        ok = 0
        for flag in self.fflag_flags:
            name = fflag_strip_prefix(str(flag.get('name', '')))
            if not name:
                continue
            address = self.fflag_engine.get_flag_address_with_prefixes(name)
            if address and address not in self.fflag_original_values:
                original = self.fflag_engine._read(address, 4)
                if original is not None:
                    self.fflag_original_values[address] = original
            if self.fflag_engine.set_flag_with_prefixes(name, str(flag.get('value', ''))):
                ok += 1
        self._apply_fps_flag(silent=True)
        self.fflag_status.config(text=f'Applied {ok}/{len(self.fflag_flags)} flags', foreground='#65d98b')
        self._console_log(f'FFlag injection complete: {ok}/{len(self.fflag_flags)} flags applied to PID {self.fflag_pid}')

    def _fflag_unapply(self):
        self.fflag_auto_apply.set(False)
        if not self.fflag_pid or not self.fflag_engine.handle:
            self.fflag_original_values.clear()
            messagebox.showwarning('FFlags', 'Roblox is not attached.', parent=self)
            return
        restored = 0
        failed = 0
        snapshots = list(self.fflag_original_values.items())
        for address, original in snapshots:
            try:
                written = ctypes.c_size_t()
                ok = ctypes.windll.kernel32.WriteProcessMemory(self.fflag_engine.handle, ctypes.c_void_p(address), original, len(original), ctypes.byref(written))
                if ok and written.value == len(original):
                    restored += 1
                else:
                    failed += 1
            except Exception:
                failed += 1
        self.fflag_original_values.clear()
        self.fflag_status.config(text=f'Unapplied {restored} flag(s)' + (f', {failed} failed' if failed else ''), foreground='#65d98b' if not failed else '#ff6b6b')
        self._console_log(f'FFlag restore complete: {restored} restored, {failed} failed')

    def _fflag_auto_apply_tick(self):
        return

    def _plugin_files(self):
        try:
            return sorted((os.path.join(self.plugins_dir, name) for name in os.listdir(self.plugins_dir) if name.lower().endswith('.py')))
        except Exception:
            return []

    def _plugin_load_python(self, path):
        module_name = 'routils_plugin_' + re.sub('[^a-zA-Z0-9_]', '_', os.path.splitext(os.path.basename(path))[0]) + '_' + uuid.uuid4().hex[:8]
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ValueError('Could not create a Python plugin loader.')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not callable(getattr(module, 'register', None)):
            raise ValueError('Python plugin must define register(app).')
        return module

    def _plugin_forget_tabs(self, name):
        tabs = list(self._plugin_tabs.pop(name, []) or [])
        module = self._plugin_modules.get(name)
        if module is not None:
            tabs.extend(list(getattr(module, 'ROUTILS_PLUGIN_TABS', []) or []))
        seen = set()
        for tab in tabs:
            key = str(tab)
            if key in seen:
                continue
            seen.add(key)
            try:
                if tab in self.nb.tabs():
                    self.nb.forget(tab)
            except Exception:
                try:
                    self.nb.forget(tab)
                except Exception:
                    pass

    def _plugin_enable(self, path, enabled=True):
        name = os.path.basename(path)
        enabled = bool(enabled)
        if not enabled:
            cleanup = self._plugin_cleanup.pop(name, None)
            if callable(cleanup):
                try:
                    cleanup()
                except Exception:
                    pass
            self._plugin_forget_tabs(name)
            self._plugin_modules.pop(name, None)
            self._plugin_enabled[name] = False
            self._save_settings()
            self._reorder_tabs()
            return
        if self._plugin_enabled.get(name, False) and name in self._plugin_modules:
            return
        try:
            self._plugin_forget_tabs(name)
            old_module = self._plugin_modules.pop(name, None)
            self._plugin_cleanup.pop(name, None)
            before_tabs = set(self.nb.tabs())
            module = self._plugin_load_python(path)
            result = module.register(self)
            plugin_tabs = []
            if isinstance(result, dict) and isinstance(result.get('tabs'), (list, tuple)):
                plugin_tabs.extend(result['tabs'])
            plugin_tabs.extend((tab for tab in self.nb.tabs() if tab not in before_tabs))
            unique_tabs = []
            seen = set()
            for tab in plugin_tabs:
                key = str(tab)
                if key not in seen:
                    seen.add(key)
                    unique_tabs.append(tab)
            module.ROUTILS_PLUGIN_TABS = unique_tabs
            self._plugin_tabs[name] = unique_tabs
            self._plugin_modules[name] = module
            cleanup = result.get('cleanup') if isinstance(result, dict) else None
            if callable(cleanup):
                self._plugin_cleanup[name] = cleanup
            self._plugin_enabled[name] = True
            self._save_settings()
            self._reorder_tabs()
        except Exception as exc:
            self._plugin_forget_tabs(name)
            self._plugin_modules.pop(name, None)
            self._plugin_cleanup.pop(name, None)
            self._plugin_enabled[name] = False
            self._save_settings()
            messagebox.showerror('Plugin', f'Could not enable {name}:\n{exc}', parent=self)

    def _plugin_open_guide(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            win = tk.Toplevel(self)
            win.title(os.path.basename(path))
            win.geometry('850x650')
            win.transient(None)
            txt = tk.Text(win, wrap='word', font=('Consolas', 10), bg=_CURRENT_PALETTE['bg_medium'], fg=_CURRENT_PALETTE['fg'], insertbackground=_CURRENT_PALETTE['fg'], bd=0, padx=14, pady=14)
            txt.pack(fill='both', expand=True)
            txt.insert('1.0', text)
            txt.configure(state='disabled')
        except Exception as exc:
            messagebox.showerror('Plugin', f'could not open guide:\n{exc}', parent=self)

    def _build_plugins_tab(self):
        tab = ttk.Frame(self.nb, padding=14)
        self.nb.add(tab, text='Plugins')
        header = ttk.Frame(tab)
        header.pack(fill='x', pady=(0, 10))
        ttk.Label(header, text='Plugins', font=('Segoe UI Semibold', 16)).pack(side='left')
        ttk.Button(header, text='Import Python', command=self._import_plugin_file).pack(side='right')
        ttk.Label(tab, text='(Only use trusted plugins cause Plugins has adminastor permissions.)', foreground='#9aa0a6', wraplength=950).pack(anchor='w', pady=(0, 10))
        body = ttk.Frame(tab)
        body.pack(fill='both', expand=True)
        files = self._plugin_files()
        if not files:
            ttk.Label(body, text='No plugins installed yet.\nImport a .py plugin.', foreground='#9aa0a6', justify='center').pack(expand=True)
            return
        for path in files:
            name = os.path.basename(path)
            card = ttk.LabelFrame(body, text=os.path.splitext(name)[0])
            card.pack(fill='x', pady=5)
            if path.lower().endswith('.txt'):
                ttk.Label(card, text='documentation / development guide', foreground='#9aa0a6').pack(anchor='w', padx=10, pady=7)
                ttk.Button(card, text='open guide', command=lambda p=path: self._plugin_open_guide(p)).pack(anchor='w', padx=8, pady=(0, 8))
            else:
                module = self._plugin_modules.get(name)
                desc = str(getattr(module, 'PLUGIN_DESCRIPTION', 'Python plugin') if module else 'Python plugin')
                ttk.Label(card, text=desc, foreground='#9aa0a6', wraplength=950).pack(anchor='w', padx=10, pady=7)
                row = ttk.Frame(card)
                row.pack(fill='x', padx=8, pady=(0, 8))
                enabled = tk.BooleanVar(value=bool(self._plugin_enabled.get(name, False)))
                ttk.Checkbutton(row, text='Enable', variable=enabled, command=lambda p=path, v=enabled: self._plugin_enable(p, v.get())).pack(side='left')
                if self._plugin_enabled.get(name, False) and name not in self._plugin_modules:
                    self._plugin_enable(path, True)

    def _import_plugin_file(self):
        path = filedialog.askopenfilename(parent=self, title='Import RoUtils Python Plugin', filetypes=[('Python plugin', '*.py')])
        if not path:
            return
        try:
            if path.lower().endswith('.py'):
                with open(path, 'r', encoding='utf-8') as f:
                    compile(f.read(), path, 'exec')
            target = os.path.join(self.plugins_dir, os.path.basename(path))
            shutil.copy2(path, target)
            self._reload_lazy_tab('Plugins')
            messagebox.showinfo('Plugin', f'Imported {os.path.basename(path)}.\nEnable it from the Plugins tab to load Python code.', parent=self)
        except Exception as exc:
            messagebox.showerror('Plugin', f'Could not import plugin:\n{exc}', parent=self)

    def _reload_lazy_tab(self, tab_name):
        for tab_id in list(self.nb.tabs()):
            if str(self.nb.tab(tab_id, 'text')) == tab_name:
                try:
                    self.nb.forget(tab_id)
                except Exception:
                    pass
                break
        self._lazy_tabs = {k: v for k, v in self._lazy_tabs.items() if v[0] != tab_name}
        self._lazy_tab_ids.pop(tab_name, None)
        self._recreate_special_tab(tab_name)

    def _recreate_special_tab(self, tab_name):
        builder = {'Plugins': self._build_plugins_tab}.get(tab_name)
        if builder:
            builder()
            self._reorder_tabs()
            self._refresh_tab_nav()

    def _settings_canvas_resize(self, canvas, window_id, event):
        width = int(getattr(event, 'width', 0) or 0)
        key = f'_canvas_width_{id(canvas)}'
        if width != getattr(self, key, -1):
            setattr(self, key, width)
            canvas.itemconfigure(window_id, width=width)

    def _build_settings_tab(self):
        try:
            st = ttk.Style(self)
            st.configure('RoUtils.Settings.TFrame', background=_CURRENT_PALETTE['bg_dark'])
            st.configure('RoUtils.Settings.TLabel', background=_CURRENT_PALETTE['bg_dark'], foreground=_CURRENT_PALETTE['fg'])
            st.configure('RoUtils.Settings.TLabelframe', background=_CURRENT_PALETTE['bg_dark'], foreground=_CURRENT_PALETTE['fg'], bordercolor=_CURRENT_PALETTE['border'])
            st.configure('RoUtils.Settings.TLabelframe.Label', background=_CURRENT_PALETTE['bg_dark'], foreground=_CURRENT_PALETTE['fg'])
            st.configure('RoUtils.Settings.TCheckbutton', background=_CURRENT_PALETTE['bg_dark'], foreground=_CURRENT_PALETTE['fg'])
            st.map('RoUtils.Settings.TCheckbutton', background=[('active', _CURRENT_PALETTE['bg_dark'])])
        except Exception:
            pass
        tab_root = ttk.Frame(self.nb, padding=0, style='RoUtils.Settings.TFrame')
        self.nb.add(tab_root, text='Settings')
        shell = ttk.Frame(tab_root, style='RoUtils.Settings.TFrame')
        shell.pack(fill='both', expand=True)
        canvas = tk.Canvas(shell, bg=_CURRENT_PALETTE['bg_dark'], highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(shell, orient='vertical', command=canvas.yview)
        inner = ttk.Frame(canvas, style='RoUtils.Settings.TFrame')
        window_id = canvas.create_window((0, 0), window=inner, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        inner.bind('<Configure>', lambda _e: self._schedule_ui('settings_region', 30, lambda: canvas.configure(scrollregion=canvas.bbox('all'))))
        canvas.bind('<Configure>', lambda e: self._settings_canvas_resize(canvas, window_id, e))

        def update_scrollbar(_e=None):
            canvas.update_idletasks()
            bbox = canvas.bbox('all')
            needed = bool(bbox and bbox[3] > canvas.winfo_height() + 2)
            if needed:
                scrollbar.pack(side='right', fill='y')
            else:
                scrollbar.pack_forget()
                canvas.yview_moveto(0)
        inner.bind('<Configure>', update_scrollbar, add='+')
        canvas.bind('<Configure>', update_scrollbar, add='+')
        middle = {'y': None}

        def middle_press(event):
            middle['y'] = event.y
            return 'break'

        def middle_drag(event):
            if middle['y'] is not None:
                canvas.yview_scroll(int((middle['y'] - event.y) / 2), 'units')
                middle['y'] = event.y
            return 'break'

        def middle_release(_event):
            middle['y'] = None
            return 'break'
        middle_tag = f'RoUtilsSettingsMiddle_{id(canvas)}'
        canvas.bind_class(middle_tag, '<Button-2>', middle_press)
        canvas.bind_class(middle_tag, '<B2-Motion>', middle_drag)
        canvas.bind_class(middle_tag, '<ButtonRelease-2>', middle_release)

        def attach_middle_scroll(parent):
            for child in parent.winfo_children():
                try:
                    tags = list(child.bindtags())
                    if middle_tag not in tags:
                        child.bindtags((middle_tag, *tags))
                except Exception:
                    pass
                attach_middle_scroll(child)
        attach_middle_scroll(inner)
        for widget in (canvas, inner):
            widget.bind('<Button-2>', middle_press, add='+')
            widget.bind('<B2-Motion>', middle_drag, add='+')
            widget.bind('<ButtonRelease-2>', middle_release, add='+')
        tab = inner
        ttk.Label(tab, style='RoUtils.Settings.TLabel', text='Settings & Options', font=('Segoe UI Semibold', 12)).pack(anchor='w')
        ttk.Label(tab, style='RoUtils.Settings.TLabel', text='General options.', foreground='#9aa0a6').pack(anchor='w', pady=(0, 10))
        dpi_box = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text='Interface Scale')
        dpi_box.pack(fill='x', pady=6)
        try:
            _saved_dpi = int(self.settings.get('dpi_percent', 100) or 100)
        except Exception:
            _saved_dpi = 100
        _saved_dpi = max(50, min(200, _saved_dpi))
        self.dpi_percent = tk.IntVar(value=_saved_dpi)
        dpi_row = ttk.Frame(dpi_box)
        dpi_row.pack(fill='x', padx=8, pady=8)
        ttk.Label(dpi_row, style='RoUtils.Settings.TLabel', text='DPI Scale').pack(side='left')
        dpi_combo = ttk.Combobox(dpi_row, textvariable=self.dpi_percent, state='readonly', width=8, values=(50, 60, 70, 75, 80, 90, 100, 110, 125, 150, 175, 200))
        dpi_combo.pack(side='left', padx=(12, 8))
        ttk.Label(dpi_row, style='RoUtils.Settings.TLabel', text='Window size stays the same; only the interface scales.', foreground='#9aa0a6').pack(side='left')
        ttk.Label(dpi_box, style='RoUtils.Settings.TLabel', text='You Should Restart it to Apply DPI Scale', foreground='#ffb84d').pack(anchor='w', padx=8, pady=(0, 8))
        dpi_combo.bind('<<ComboboxSelected>>', lambda _e: self._save_dpi_setting_only())
        box = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text='Cache Viewer')
        box.pack(fill='x', pady=6)
        ttk.Checkbutton(box, style='RoUtils.Settings.TCheckbutton', text='Start watching for new assets on launch', variable=self.autostart_watch, command=self._save_settings).pack(anchor='w', padx=8, pady=2)
        ttk.Checkbutton(box, style='RoUtils.Settings.TCheckbutton', text='Auto-scroll to newest row', variable=self.autoscroll, command=self._save_settings).pack(anchor='w', padx=8, pady=2)
        ttk.Checkbutton(box, style='RoUtils.Settings.TCheckbutton', text='Hide ticket assets', variable=self.hide_tickets, command=self._apply_filter).pack(anchor='w', padx=8, pady=2)
        ttk.Label(box, text='Show lines (wireframe) for the Preview', foreground='#c8c8c8').pack(anchor='w', padx=8, pady=(6, 0))
        ttk.Checkbutton(box, style='RoUtils.Settings.TCheckbutton', text='Wireframe lines on', variable=self.show_lines, command=self._apply_show_lines).pack(anchor='w', padx=8, pady=2)
        self.mesh_preview_vertices = tk.BooleanVar(value=bool(self.settings.get('preview_optimize_vertices', True)))
        ttk.Checkbutton(box, style='RoUtils.Settings.TCheckbutton', text='Optimize Mesh Preview Vertices (>500)', variable=self.mesh_preview_vertices, command=self._apply_mesh_preview_vertices_setting).pack(anchor='w', padx=8, pady=2)
        startup = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text='Startup')
        startup.pack(fill='x', pady=6)
        ttk.Checkbutton(startup, style='RoUtils.Settings.TCheckbutton', text='Launch on Tray', variable=self.launch_on_tray, command=self._startup_setting_changed).pack(anchor='w', padx=8, pady=2)
        ttk.Checkbutton(startup, style='RoUtils.Settings.TCheckbutton', text='Launch on Boot', variable=self.launch_on_startup, command=self._startup_setting_changed).pack(anchor='w', padx=8, pady=2)
        ttk.Checkbutton(startup, style='RoUtils.Settings.TCheckbutton', text='Hide to Tray when Close (F7 to Hide/Show)', variable=self.hide_to_tray_on_close, command=self._startup_setting_changed).pack(anchor='w', padx=8, pady=2)
        streamer = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text='Streamer Mode')
        streamer.pack(fill='x', pady=6)
        ttk.Checkbutton(streamer, style='RoUtils.Settings.TCheckbutton', text='Hide RoUtils from screen sharing and recording', variable=self.streamer_mode, command=self._apply_streamer_mode).pack(anchor='w', padx=8, pady=4)
        ttk.Label(streamer, text='RoUtils does not appear in screen shares. (Only you can see it.)', foreground='#9aa0a6').pack(anchor='w', padx=8, pady=(0, 6))
        updates = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text='Updates')
        updates.pack(fill='x', pady=6)
        ttk.Checkbutton(updates, style='RoUtils.Settings.TCheckbutton', text='Auto Update', variable=self.auto_update, command=self._save_settings).pack(anchor='w', padx=8, pady=(6, 1))
        ttk.Label(updates, text='Updates RoUtils on Background', foreground='#9aa0a6').pack(anchor='w', padx=8, pady=(0, 7))
        gemini = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text='Gemini AI')
        gemini.pack(fill='x', pady=6)
        ttk.Label(gemini, text='Gemini API Key').grid(row=0, column=0, sticky='w', padx=8, pady=(8, 4))
        key_entry = ttk.Entry(gemini, textvariable=self.gemini_api_key, show='•')
        key_entry.grid(row=1, column=0, columnspan=2, sticky='ew', padx=8, pady=(0, 8))
        gemini.columnconfigure(0, weight=1)
        ttk.Button(gemini, text='Tutorial', command=lambda: _open_webview2_process('https://raw.githubusercontent.com/offp001/routils/refs/heads/main/src/API%20Key%20Tutorial.txt', 'Gemini API Key Tutorial')).grid(row=2, column=0, sticky='w', padx=8, pady=(0, 8))
        ttk.Button(gemini, text='Add Key', command=self._save_gemini_api_key).grid(row=2, column=1, sticky='e', padx=8, pady=(0, 8))
        db = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text='Database')
        db.pack(fill='x', pady=6)
        ttk.Button(db, text='Choose DB File…', command=self._choose_db).pack(anchor='w', padx=8, pady=4)
        ttk.Button(db, text='Choose Shard Root…', command=self._choose_shard_root).pack(anchor='w', padx=8, pady=4)
        settings_box = ttk.LabelFrame(tab, style='RoUtils.Settings.TLabelframe', text='Settings Backup')
        settings_box.pack(fill='x', pady=6)
        ttk.Button(settings_box, text='Export Settings…', command=self._export_settings).pack(side='left', padx=8, pady=8)
        ttk.Button(settings_box, text='Import Settings…', command=self._import_settings).pack(side='left', padx=(0, 8), pady=8)

    def _save_dpi_setting_only(self):
        try:
            percent = max(50, min(200, int(self.dpi_percent.get())))
            self.settings['dpi_percent'] = percent
            self._save_settings()
        except Exception as exc:
            self._console_log(f'DPI setting error: {exc}')

    def _export_settings(self):
        self._save_settings()
        path = filedialog.asksaveasfilename(parent=self, title='Export RoUtils Settings', defaultextension='.json', filetypes=[('JSON', '*.json')])
        if not path:
            return
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=2)
        self._console_log(f'Exported settings to {path}')

    def _import_settings(self):
        path = filedialog.askopenfilename(parent=self, title='Import RoUtils Settings', filetypes=[('JSON', '*.json')])
        if not path:
            return
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError('Settings file must contain a JSON object.')
        self.settings.update(data)
        for name in ('autoscroll', 'hide_tickets', 'stay_on_top', 'show_lines', 'streamer_mode', 'autostart_watch', 'auto_update', 'launch_on_tray', 'launch_on_startup', 'hide_to_tray_on_close'):
            var = getattr(self, name, None)
            if var is not None and name in data:
                var.set(bool(data[name]))
        if 'fps_limit' in data:
            self.fps_limit.set(max(0, min(240, int(data['fps_limit']))))
        if 'theme' in data and hasattr(self, 'theme_var'):
            self.theme_var.set(str(data['theme']))
            self._apply_theme()
        self._save_settings()
        self._console_log(f'Imported settings from {path}')

    def _console_log(self, message):
        lines = str(message).replace('\r', '').splitlines() or ['']
        history = getattr(self, '_console_history', [])
        history.extend(lines)
        self._console_history = history[-1000:]
        if self._console_save_job is None:
            try:
                self._console_save_job = self.after(350, self._save_console_history)
            except Exception:
                self._console_save_job = None
        if hasattr(self, 'console_text'):
            if getattr(self, '_console_render_pending', False):
                return
            self._console_render_pending = True

            def render():
                try:
                    self._console_render_pending = False
                    self.console_text.configure(state='normal')
                    self.console_text.delete('1.0', 'end')
                    self.console_text.insert('end', '\n'.join(self._console_history) + '\n')
                    self.console_text.see('end')
                    self.console_text.configure(state='disabled')
                except Exception:
                    self._console_render_pending = False
            try:
                self.after(0, render)
            except Exception:
                pass

    def _load_console_history(self):
        try:
            with open(CONSOLE_HISTORY_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [str(x) for x in data][-1000:] if isinstance(data, list) else []
        except Exception:
            return []

    def _save_console_history(self):
        self._console_save_job = None
        try:
            os.makedirs(os.path.dirname(CONSOLE_HISTORY_PATH), exist_ok=True)
            temp = CONSOLE_HISTORY_PATH + '.tmp'
            with open(temp, 'w', encoding='utf-8') as f:
                json.dump(self._console_history[-1000:], f, ensure_ascii=False, indent=2)
            os.replace(temp, CONSOLE_HISTORY_PATH)
        except Exception:
            pass

    def _console_undo(self):
        if not self._console_undo_stack:
            self._console_log('Nothing to undo.')
            return
        kind, payload = self._console_undo_stack.pop()
        if kind == 'fflags':
            self.fflag_flags = payload
            self._save_fflag_flags()
            self._refresh_fflag_list()
            self._console_log('Undid the last FFlag change.')
        elif kind == 'cache':
            clean, blob = payload
            conn = connect_rw(self.db_path)
            try:
                conn.execute('INSERT OR REPLACE INTO files(id, content) VALUES(?, ?)', (bytes.fromhex(clean), sqlite3.Binary(blob)))
                conn.commit()
            finally:
                conn.close()
            self._console_log(f'Restored cache {clean}.')
        elif kind == 'config':
            path, data = payload
            with open(path, 'wb') as f:
                f.write(data)
            self._cc_refresh_list()
            self._console_log(f'Restored config {os.path.basename(path)}.')

    def _console_select_tab(self, name):
        for tab_id in self.nb.tabs():
            if self.nb.tab(tab_id, 'text') == name:
                self.nb.select(tab_id)
                return True
        return False

    def _console_cache_search(self, query=''):
        query = str(query or '').lower().strip()
        rows = []
        for it in self.items_by_hash.values():
            text = f'{it.name} {it.hash} {it.kind} {it.src}'.lower()
            if not query or query in text:
                rows.append(f'{it.name} | {it.hash} | {it.kind}')
        self._console_log('Cache search:\n' + ('\n'.join(rows) if rows else '(no matches)'))

    def _console_create_backup(self, name='backup'):
        safe = _sanitize_filename_for_windows(str(name).strip()) or 'backup'
        backup_dir = os.path.join(DATA_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        path = os.path.join(backup_dir, f"{safe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
        with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as archive:
            for filename in ('routils_settings.json', 'routils_fflags.json', 'console_history.json'):
                source = os.path.join(DATA_DIR, filename)
                if os.path.isfile(source):
                    archive.write(source, filename)
            for folder in ('filesaves', 'hashsaves'):
                root = os.path.join(DATA_DIR, folder)
                if os.path.isdir(root):
                    for current, _, files in os.walk(root):
                        for filename in files:
                            source = os.path.join(current, filename)
                            archive.write(source, os.path.relpath(source, DATA_DIR))
        self._console_log(f'Created backup: {path}')

    def _console_restore_backup(self, path):
        path = os.path.abspath(os.path.expandvars(os.path.expanduser(str(path))))
        if not os.path.isfile(path) or not path.lower().endswith('.zip'):
            raise ValueError('Backup ZIP file was not found.')
        root = os.path.abspath(DATA_DIR)
        with zipfile.ZipFile(path, 'r') as archive:
            for member in archive.infolist():
                target = os.path.abspath(os.path.join(root, member.filename))
                if os.path.commonpath((root, target)) != root:
                    raise ValueError('Unsafe backup path.')
            archive.extractall(root)
        if hasattr(self, 'replacer'):
            self.replacer.refresh_view(preserve_selection=True)
        self._console_log(f'Restored backup: {path}')

    def _console_command(self, raw):
        raw = str(raw or '').strip()
        if not raw:
            return
        self._console_log('$> ' + raw)
        try:
            args = shlex.split(raw, posix=False)
            args = [x[1:-1] if len(x) >= 2 and x[0] == x[-1] and (x[0] in '"\'') else x for x in args]
            command = args[0].lower()
            values = args[1:]
            if command == 'help':
                self._console_log('Commands:\n  cache "blob file path" "hash"  Apply a blob file to Roblox.\n  cache delete "hash"  Delete one cache by hash.\n  cache list [filter]  List visible caches.\n  cache search [text]  Search loaded caches by name, hash or type.\n  fflag "name" "value"  Add and apply one FastFlag.\n  fflag delete "name"  Remove one FastFlag.\n  fflag clear  Remove all saved FastFlags.\n  fflag list  List saved FastFlags.\n  fflag apply  Inject all saved FastFlags into Roblox.\n  fflag unapply  Restore the original FastFlag values.\n  fflag defaults  Open Default FFlag Values.\n  fflag latest  Open Latest FFlag List.\n  undo  Undo the last reversible console change.\n  history  Show saved console history from console_history.json.\n  config "name/prefix"  Apply a saved CConfig.\n  config save "name"  Save the current Roblox database as a CConfig.\n  config list  List saved CConfigs.\n  config delete "name/prefix"  Delete one saved CConfig.\n  modif meshtoobj "mesh file path"  Convert that mesh file to OBJ.\n  modif "head" "replacement mesh path" ["RobloxPlayerBeta.exe path"]  Replace R6 body mesh (head, torso, left arm, right arm, left leg, right leg).\n  join "place id"  Open a Roblox subplace.\n  viewserver "deeplink"  Load a server deeplink.\n  information  Open the live Client information.\n  theme "theme name"  Apply a saved theme.\n  theme list  List available themes.\n  watch start|stop  Start or stop cache watching.\n  fps "number"  Set and apply the FPS limit.\n  export all  Open the full cache export tool.\n  backup create "name"  Back up settings and File/Hash Saves.\n  backup restore "zip path"  Restore a RoUtils backup ZIP.\n  ai  Open RoUtils AI.\n  open "tab name"  Open a RoUtils tab.\n  status  Show Roblox PID, watcher and database status.\n  clear  Clear the Console.')
            elif command == 'cache' and len(values) >= 2 and (values[0].lower() not in ('delete', 'list', 'clear', 'search')):
                self._console_apply_cache(values[0], values[1])
            elif command == 'cache' and values and (values[0].lower() == 'delete') and (len(values) >= 2):
                self._console_delete_cache(values[1])
            elif command == 'cache' and values and (values[0].lower() == 'list'):
                self._console_list_caches(values[1] if len(values) >= 2 else '')
            elif command == 'cache' and values and (values[0].lower() == 'search'):
                self._console_cache_search(' '.join(values[1:]))
            elif command == 'fflag' and len(values) >= 2 and (values[0].lower() not in ('delete', 'list', 'clear')):
                self._console_undo_stack.append(('fflags', json.loads(json.dumps(self.fflag_flags))))
                name, value = (fflag_strip_prefix(values[0]), values[1])
                self.fflag_flags = [x for x in self.fflag_flags if fflag_strip_prefix(x.get('name', '')).lower() != name.lower()]
                self.fflag_flags.append({'name': name, 'value': value, 'type': fflag_infer_type(value)})
                self._save_fflag_flags()
                self._refresh_fflag_list()
                self._fflag_apply(silent=True)
                self._console_log(f'Applied FFlag {name} = {value}')
            elif command == 'fflag' and values and (values[0].lower() == 'delete') and (len(values) >= 2):
                self._console_undo_stack.append(('fflags', json.loads(json.dumps(self.fflag_flags))))
                self._console_delete_fflag(values[1])
            elif command == 'fflag' and values and (values[0].lower() == 'clear'):
                self._console_undo_stack.append(('fflags', json.loads(json.dumps(self.fflag_flags))))
                self.fflag_flags = []
                self._save_fflag_flags()
                self._refresh_fflag_list()
                self._fflag_apply(silent=True)
                self._console_log('Cleared all saved FFlags')
            elif command == 'fflag' and values and (values[0].lower() == 'list'):
                self._console_list_fflags()
            elif command == 'fflag' and values and (values[0].lower() == 'apply'):
                self._fflag_apply(silent=True)
                self._console_log('FFlag injection requested')
            elif command == 'fflag' and values and (values[0].lower() == 'unapply'):
                self._fflag_unapply()
                self._console_log('FFlag values restored')
            elif command == 'fflag' and values and (values[0].lower() in ('defaults', 'default')):
                self._open_default_fflag_values()
                self._console_log('Opened Default FFlag Values')
            elif command == 'fflag' and values and (values[0].lower() in ('latest', 'latestlist')):
                self._open_latest_fflag_list()
                self._console_log('Opened Latest FFlag List')
            elif command == 'config' and values:
                if values[0].lower() == 'list':
                    self._console_list_configs()
                elif values[0].lower() == 'save' and len(values) >= 2:
                    self._cc_save_named_config(' '.join(values[1:]))
                    self._console_log(f"Saved current DB as config '{' '.join(values[1:])}'.")
                elif values[0].lower() == 'delete' and len(values) >= 2:
                    self._console_delete_config(values[1])
                else:
                    self._console_apply_config(values[0])
            elif command == 'modif' and values and (values[0].lower() == 'meshtoobj') and (len(values) >= 2):
                self._console_mesh_to_obj(values[1])
            elif command == 'modif' and len(values) >= 2:
                self._console_replace_mesh(values[0], values[1], values[2] if len(values) >= 3 else '')
            elif command == 'join' and values and str(values[0]).isdigit():
                os.startfile(f'roblox://placeId={values[0]}')
                self._console_log(f'Opened subplace {values[0]}')
            elif command == 'viewserver' and values:
                self._console_select_tab('Server Viewer')
                self.after(100, lambda link=' '.join(values): (self.server_viewer_link.set(link), self._server_viewer_load()))
            elif command == 'information':
                self._console_select_tab('Client')
                self.after(150, self._client_refresh)
                self._console_log('Opened Client information')
            elif command == 'theme' and values:
                if values[0].lower() == 'list':
                    self._console_log('Themes: ' + ', '.join(THEME_NAMES))
                else:
                    self._console_apply_theme(' '.join(values))
            elif command == 'watch' and values and (values[0].lower() in ('start', 'stop')):
                if values[0].lower() == 'start':
                    if self._start_watching():
                        self._console_log('Cache watching started')
                    else:
                        self._console_log('Cache watching could not start: database file was not found.')
                else:
                    self._stop_watching()
                    self._console_log('Cache watching stopped')
            elif command == 'fps' and values:
                fps = max(0, min(240, int(values[0])))
                self.fps_limit.set(fps)
                self._save_settings()
                self._sync_fps_flag_to_manager()
                self._apply_fps_flag(silent=True)
                self._console_log(f"FPS limit set to {(fps if fps else 'uncapped')}")
            elif command == 'export' and values and (values[0].lower() == 'all'):
                self._dump_all_caches()
                self._console_log('Opened full cache export tool')
            elif command == 'backup' and values and (values[0].lower() == 'create'):
                self._console_create_backup(' '.join(values[1:]) if len(values) > 1 else 'backup')
            elif command == 'backup' and values and (values[0].lower() == 'restore') and (len(values) >= 2):
                self._console_restore_backup(values[1])
            elif command == 'ai':
                self._open_ai_chat()
            elif command == 'open' and values:
                tab_name = ' '.join(values)
                if not self._console_select_tab(tab_name):
                    raise ValueError(f'Tab not found: {tab_name}')
                self._console_log(f'Opened tab {tab_name}')
            elif command == 'status':
                self._console_log(f"Roblox PID: {self.fflag_pid or 'not attached'}\nCache watcher: {('running' if self.watching else 'stopped')}\nDatabase: {self.db_path}")
            elif command == 'clear':
                self._console_history = []
                self._save_console_history()
                if hasattr(self, 'console_text'):
                    self.console_text.configure(state='normal')
                    self.console_text.delete('1.0', 'end')
                    self.console_text.configure(state='disabled')
            elif command == 'history':
                self._console_log('Saved history:\n' + ('\n'.join(self._console_history) if self._console_history else '(empty)'))
            elif command == 'undo':
                self._console_undo()
            else:
                self._console_log('Invalid command or arguments. Type help for English command descriptions.')
        except Exception as e:
            self._console_log('Error: ' + str(e))

    def _console_apply_cache(self, path, hash_value):
        path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
        clean = re.sub('[^0-9A-Fa-f]', '', str(hash_value))
        if not os.path.isfile(path) or not clean or len(clean) % 2:
            raise ValueError('Cache file or hash is invalid.')
        with open(path, 'rb') as f:
            blob = f.read()
        id_b = bytes.fromhex(clean)
        conn = connect_rw(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute('BEGIN IMMEDIATE')
            cur.execute('DELETE FROM files WHERE id=?', (id_b,))
            cur.execute('INSERT INTO files(id, content) VALUES(?, ?)', (id_b, sqlite3.Binary(blob)))
            conn.commit()
        finally:
            conn.close()
        self._console_log(f'Applied cache {clean} from {path}')

    def _console_delete_cache(self, hash_value):
        clean = re.sub('[^0-9A-Fa-f]', '', str(hash_value)).lower()
        if not clean or len(clean) % 2:
            raise ValueError('Cache hash is invalid.')
        id_b = bytes.fromhex(clean)
        old_blob = None
        conn = connect_rw(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute('BEGIN IMMEDIATE')
            row = cur.execute('SELECT content FROM files WHERE id=?', (id_b,)).fetchone()
            if row and row[0] is not None:
                old_blob = bytes(row[0])
            cur.execute('DELETE FROM files WHERE id=?', (id_b,))
            deleted = cur.rowcount
            conn.commit()
        finally:
            conn.close()
        try:
            sp = shard_path(self.shard_root, clean)
            if os.path.isfile(sp):
                os.remove(sp)
        except Exception:
            pass
        self.seen_hashes.discard(clean)
        self.items_by_hash.pop(clean, None)
        self.items_by_iid.pop(clean, None)
        if hasattr(self, 'tree'):
            try:
                self.tree.delete(clean)
            except Exception:
                pass
        if hasattr(self, 'status_label'):
            self._update_status()
        if deleted and old_blob is not None:
            self._console_undo_stack.append(('cache', (clean, old_blob)))
        self._console_log(f'Deleted cache {clean}' if deleted else f'Cache not found: {clean}')

    def _console_list_caches(self, query=''):
        query = str(query or '').lower()
        rows = []
        for item in self.items_by_hash.values():
            text = f'{item.hash} {item.name} {item.kind}'.lower()
            if not query or query in text:
                rows.append(f"{item.hash} | {item.name or '(unnamed)'} | {item.kind}")
        self._console_log('Caches:\n' + ('\n'.join(rows) if rows else '(none loaded)'))

    def _console_delete_fflag(self, query):
        query = fflag_strip_prefix(str(query)).lower()
        matches = [x for x in self.fflag_flags if fflag_strip_prefix(x.get('name', '')).lower() == query]
        if len(matches) != 1:
            raise ValueError('FFlag was not found or is ambiguous.')
        self.fflag_flags = [x for x in self.fflag_flags if fflag_strip_prefix(x.get('name', '')).lower() != query]
        self._save_fflag_flags()
        self._refresh_fflag_list()
        self._fflag_apply(silent=True)
        self._console_log(f'Deleted FFlag {query}')

    def _console_list_fflags(self):
        rows = [f"{x.get('name', '')} = {x.get('value', '')}" for x in self.fflag_flags]
        self._console_log('FFlags:\n' + ('\n'.join(rows) if rows else '(none)'))

    def _console_list_configs(self):
        configs = self._cc_scan_packages()
        rows = [f"{x.get('name', '')} | {x.get('_file', '')}" for x in configs]
        self._console_log('Configs:\n' + ('\n'.join(rows) if rows else '(none)'))

    def _console_delete_config(self, query):
        q = str(query).lower()
        matches = [x for x in self._cc_scan_packages() if str(x.get('name', '')).lower().startswith(q)]
        if len(matches) != 1:
            raise ValueError('Config was not found or the prefix is ambiguous.')
        path = matches[0]['_path']
        with open(path, 'rb') as f:
            self._console_undo_stack.append(('config', (path, f.read())))
        os.remove(path)
        self._cc_refresh_list()
        self._console_log(f"Deleted config {matches[0].get('name', '')}")

    def _console_apply_config(self, query):
        self._console_select_tab('Configs')

        def apply():
            candidates = self._cc_scan_packages()
            q = str(query).lower()
            matches = [x for x in candidates if str(x.get('name', '')).lower().startswith(q)]
            if len(q) < 4 and len(matches) != 1:
                raise ValueError('Use at least the first 4 unique config characters.')
            if len(matches) != 1:
                raise ValueError('Config prefix is missing or ambiguous.')
            wanted = os.path.abspath(matches[0]['_path'])
            self._cc_refresh_list(select_path=wanted)
            self._cc_apply_db()
            self._console_log(f"Applying config {matches[0].get('name', '')}")
        self.after(150, lambda: self._console_safe_call(apply))

    def _console_safe_call(self, fn):
        try:
            fn()
        except Exception as e:
            self._console_log('Error: ' + str(e))

    def _console_mesh_to_obj(self, path):
        path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
        if not os.path.isfile(path):
            raise FileNotFoundError(path)
        out = os.path.splitext(path)[0] + '.obj'
        with open(path, 'rb') as f:
            data = f.read()
        convert(data, out)
        self._console_log(f'Converted mesh to {out}')

    def _console_replace_mesh(self, mesh_name, replacement, roblox_path=''):
        mesh_aliases = {'head': 'Head.mesh', 'torso': 'Torso.mesh', 'left arm': 'Left Arm.mesh', 'right arm': 'Right Arm.mesh', 'left leg': 'Left Leg.mesh', 'right leg': 'Right Leg.mesh'}
        mesh_name = mesh_aliases.get(str(mesh_name).strip().lower(), str(mesh_name).strip())
        if not mesh_name.lower().endswith('.mesh'):
            mesh_name += '.mesh'
        source = os.path.abspath(os.path.expandvars(os.path.expanduser(replacement)))
        if not os.path.isfile(source):
            raise FileNotFoundError(source)
        if roblox_path:
            self.roblox_path_var.set(os.path.abspath(os.path.expandvars(os.path.expanduser(roblox_path))))
        target = self._default_mesh_path(mesh_name)
        if not target:
            raise ValueError('Choose RobloxPlayerBeta.exe first or pass its path.')
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copy2(source, target)
        self._console_log(f'Replaced {mesh_name}')

    def _console_apply_theme(self, query):
        names = [x for x in THEME_NAMES if x.lower() == str(query).lower() or x.lower().startswith(str(query).lower())]
        if len(names) != 1:
            raise ValueError('Theme not found or prefix is ambiguous.')
        self._console_select_tab('Themes')

        def apply():
            self.theme_var.set(names[0])
            self._apply_theme()
            self._console_log(f'Applied theme {names[0]}')
        self.after(150, lambda: self._console_safe_call(apply))

    def _build_console_tab(self):
        tab = ttk.Frame(self.nb, padding=10)
        self.nb.add(tab, text='Console')
        tab.rowconfigure(1, weight=1)
        tab.columnconfigure(0, weight=1)
        ttk.Label(tab, text='Console', font=('Segoe UI Semibold', 15)).grid(row=0, column=0, sticky='w', pady=(0, 8))
        self.console_text = tk.Text(tab, wrap='word', state='disabled', font=('Consolas', 9), bg=_CURRENT_PALETTE['bg_medium'], fg=_CURRENT_PALETTE['fg'], insertbackground='#ffffff', relief='flat', bd=0)
        self.console_text.grid(row=1, column=0, sticky='nsew')
        row = ttk.Frame(tab)
        row.grid(row=2, column=0, sticky='ew', pady=(8, 0))
        row.columnconfigure(1, weight=1)
        ttk.Label(row, text='$>', font=('Consolas', 10, 'bold')).grid(row=0, column=0, padx=(0, 6))
        self.console_entry = ttk.Entry(row)
        self.console_entry.grid(row=0, column=1, sticky='ew')
        self.console_entry.bind('<Return>', lambda _e: (self._console_command(self.console_entry.get()), self.console_entry.delete(0, 'end'), 'break')[2])
        self._console_log('RoUtils Console ready. Type help for commands.')

    def _save_gemini_api_key(self):
        key = self.gemini_api_key.get().strip()
        if not key:
            messagebox.showwarning('Gemini AI', 'Please enter a Gemini API Key.', parent=self)
            return
        self.settings['gemini_api_key'] = key
        self._save_settings()
        messagebox.showinfo('Gemini AI', 'Gemini API Key added successfully.', parent=self)

    def _ai_canvas_resize(self, canvas, window_id, event):
        width = int(getattr(event, 'width', 0) or 0)
        key = f'_ai_canvas_width_{id(canvas)}'
        if width != getattr(self, key, -1):
            setattr(self, key, width)
            canvas.itemconfigure(window_id, width=width)

    def _open_ai_chat(self):
        existing = getattr(self, '_ai_chat_window', None)
        if existing is not None:
            try:
                if existing.winfo_exists():
                    existing.destroy()
            except tk.TclError:
                pass
            self._ai_chat_window = None
        self._console_log('Opened RoUtils AI')
        key = self.gemini_api_key.get().strip()
        if not key:
            messagebox.showwarning('Gemini AI', "You didn't add Gemini API Key.\nAdd API Key on Settings Tab.", parent=self)
            return

        win = tk.Toplevel(self)
        self._ai_chat_window = win
        win.title('RoUtils AI • Updated')
        screen_w, screen_h = win.winfo_screenwidth(), win.winfo_screenheight()
        initial_w = min(1100, max(760, int(screen_w * 0.72)))
        initial_h = min(850, max(580, int(screen_h * 0.76)))
        win.geometry(f'{initial_w}x{initial_h}')
        win.minsize(760, 560)
        win.transient(None)
        win.resizable(True, True)
        win.attributes('-topmost', False)
        win.grab_release()
        theme_toplevel(win)

        root = ttk.Frame(win, padding=0)
        root.pack(fill='both', expand=True)
        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)

        header = ttk.Frame(root, padding=(16, 12))
        header.grid(row=0, column=0, sticky='ew')
        ttk.Label(header, text='RoUtils AI', font=('Segoe UI Semibold', 16)).pack(side='left')
        ttk.Label(header, text='Powered by Gemini', foreground='#9aa0a6').pack(side='left', padx=8)
        model_names = {
            'Gemini 3.8 Flash': 'gemini-3.8-flash',
            'Gemini 3.7 Flash': 'gemini-3.7-flash',
            'Gemini 3.6 Flash': 'gemini-3.6-flash',
            'Gemini 3.5 Flash': 'gemini-3.5-flash',
            'Gemini 3.5 Flash-Lite': 'gemini-3.5-flash-lite',
            'Gemini 3.1 Flash-Lite': 'gemini-3.1-flash-lite',
            'Gemini 3.1 Pro': 'gemini-3.1-pro-preview',
            'Gemini 2.5 Pro': 'gemini-2.5-pro',
            'Gemini 2.5 Flash': 'gemini-2.5-flash',
            'Gemini 2.5 Flash-Lite': 'gemini-2.5-flash-lite'
        }
        model_var = tk.StringVar(value='Gemini 3.5 Flash-Lite')
        model_box = ttk.Combobox(header, textvariable=model_var, values=list(model_names.keys()), state='readonly', width=24)
        model_box.pack(side='right')
        ttk.Label(header, text='Model', foreground='#9aa0a6').pack(side='right', padx=(0, 8))

        body = ttk.Frame(root)
        body.grid(row=1, column=0, sticky='nsew', padx=12, pady=(0, 8))
        body.rowconfigure(0, weight=1)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=0, minsize=230)

        chat_area = tk.Frame(body, bg=_CURRENT_PALETTE['bg_dark'])
        chat_area.grid(row=0, column=0, sticky='nsew')
        chat_area.rowconfigure(0, weight=1)
        chat_area.columnconfigure(0, weight=1)
        canvas = tk.Canvas(chat_area, bg=_CURRENT_PALETTE['bg_dark'], highlightthickness=0, bd=0)
        scroll = ttk.Scrollbar(chat_area, orient='vertical', command=canvas.yview)
        messages = tk.Frame(canvas, bg=_CURRENT_PALETTE['bg_dark'])
        messages.columnconfigure(0, weight=1)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.grid(row=0, column=0, sticky='nsew')
        scroll.grid(row=0, column=1, sticky='ns')
        window_id = canvas.create_window((0, 0), window=messages, anchor='nw')

        def refresh_scrollregion(_event=None):
            try:
                canvas.configure(scrollregion=canvas.bbox('all'))
            except tk.TclError:
                pass

        def refresh_width(event=None):
            try:
                canvas.itemconfigure(window_id, width=max(1, canvas.winfo_width()))
                for item in messages.winfo_children():
                    item.event_generate('<Configure>')
            except tk.TclError:
                pass

        messages.bind('<Configure>', refresh_scrollregion)
        canvas.bind('<Configure>', refresh_width)

        def wheel(event):
            if getattr(event, 'delta', 0):
                canvas.yview_scroll(-int(event.delta / 120), 'units')
            return 'break'

        canvas.bind('<MouseWheel>', wheel, add='+')
        messages.bind('<MouseWheel>', wheel, add='+')

        history_panel = tk.Frame(body, bg=_CURRENT_PALETTE['bg_medium'], width=230)
        history_panel.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
        history_panel.grid_propagate(False)
        history_panel.rowconfigure(1, weight=1)
        history_panel.columnconfigure(0, weight=1)
        history_top = tk.Frame(history_panel, bg=_CURRENT_PALETTE['bg_medium'])
        history_top.grid(row=0, column=0, sticky='ew', padx=8, pady=8)
        history_top.columnconfigure(0, weight=1)
        tk.Label(history_top, text='Chat history', bg=_CURRENT_PALETTE['bg_medium'], fg=_CURRENT_PALETTE['fg'], font=('Segoe UI Semibold', 10)).grid(row=0, column=0, sticky='w')
        history_canvas = tk.Canvas(history_panel, bg=_CURRENT_PALETTE['bg_dark'], highlightthickness=0, bd=0)
        history_scroll = ttk.Scrollbar(history_panel, orient='vertical', command=history_canvas.yview)
        history_list = tk.Frame(history_canvas, bg=_CURRENT_PALETTE['bg_dark'])
        history_list.columnconfigure(0, weight=1)
        history_window = history_canvas.create_window((0, 0), window=history_list, anchor='nw')
        history_canvas.configure(yscrollcommand=history_scroll.set)
        history_canvas.grid(row=1, column=0, sticky='nsew', padx=(8, 0), pady=(0, 8))
        history_scroll.grid(row=1, column=1, sticky='ns', padx=(0, 8), pady=(0, 8))
        history_list.bind('<Configure>', lambda _e: history_canvas.configure(scrollregion=history_canvas.bbox('all')))
        history_canvas.bind('<Configure>', lambda e: history_canvas.itemconfigure(history_window, width=max(1, e.width)))
        new_chat_btn = ttk.Button(history_top, text='+ New chat')
        new_chat_btn.grid(row=1, column=0, sticky='ew', pady=(8, 0))

        composer = ttk.Frame(root, padding=(12, 4, 12, 12))
        composer.grid(row=2, column=0, sticky='ew')
        composer.columnconfigure(0, weight=1)
        input_box = tk.Text(composer, height=4, wrap='word', font=('Segoe UI', 10), bg=_CURRENT_PALETTE['bg_medium'], fg=_CURRENT_PALETTE['fg'], insertbackground='#ffffff', relief='flat', bd=0, padx=10, pady=8)
        input_box.grid(row=0, column=0, sticky='ew', padx=(0, 8))
        attached_files = []
        attach_btn = ttk.Button(composer, text='+', width=3)
        attach_btn.grid(row=0, column=1, sticky='se', padx=(0, 5))
        send_btn = ttk.Button(composer, text='➤  Send', width=12)
        send_btn.grid(row=0, column=2, sticky='se')

        sessions = []
        active = {'index': 0}
        busy = {'value': False}
        thinking_box = {'widget': None}
        bubble_refs = []

        def session_title(session):
            title = str(session.get('title') or 'New chat').strip()
            return title if title else 'New chat'

        def refresh_history_list():
            for child in history_list.winfo_children():
                child.destroy()
            for index, session in enumerate(sessions):
                selected = index == active['index']
                row_bg = '#164a9c' if selected else _CURRENT_PALETTE['bg_dark']
                row = tk.Frame(history_list, bg=row_bg, padx=5, pady=4)
                row.grid(row=index, column=0, sticky='ew', pady=(0, 4))
                row.columnconfigure(0, weight=1)
                title = tk.Label(row, text=('●  ' if selected else '   ') + session_title(session), bg=row_bg, fg='#ffffff', anchor='w', justify='left', font=('Segoe UI', 9), cursor='hand2')
                title.grid(row=0, column=0, sticky='ew', padx=(4, 5))
                rename_btn = ttk.Button(row, text='✎', width=3, command=lambda i=index: rename_session(i))
                rename_btn.grid(row=0, column=1, sticky='e')
                title.bind('<Button-1>', lambda _e, i=index: load_session(i) if not busy['value'] else None)
                row.bind('<Button-1>', lambda _e, i=index: load_session(i) if not busy['value'] else None)

        def clear_messages():
            for child in messages.winfo_children():
                child.destroy()
            bubble_refs.clear()

        def add_code(parent, code, language=''):
            box = tk.Frame(parent, bg='#202124', highlightthickness=1, highlightbackground='#55575c')
            box.pack(fill='x', padx=12, pady=(5, 8))
            top = tk.Frame(box, bg='#292b2f')
            top.pack(fill='x')
            tk.Label(top, text=language or 'code', bg='#292b2f', fg='#aeb3ba', font=('Segoe UI', 8)).pack(side='left', padx=9, pady=5)
            tk.Button(top, text='Copy', command=lambda: copy_code(code), bg='#3a3d42', fg='#eeeeee', activebackground='#484b51', activeforeground='#ffffff', relief='flat', bd=0, padx=9, pady=2, font=('Segoe UI Semibold', 8)).pack(side='right', padx=5, pady=4)
            code_box = tk.Text(box, height=max(2, min(18, code.count('\n') + 2)), wrap='none', bg='#202124', fg='#eeeeee', insertbackground='#ffffff', relief='flat', bd=0, padx=10, pady=8, font=('Consolas', 9))
            code_box.insert('1.0', code)
            code_box.configure(state='disabled')
            code_box.pack(fill='x')

        def copy_code(code):
            try:
                win.clipboard_clear()
                win.clipboard_append(code)
            except Exception:
                pass

        def add_message(text, role, persist=True):
            if text is None:
                return
            text = str(text).replace('\r\n', '\n').replace('\r', '\n')
            is_user = role == 'user'
            outer = tk.Frame(messages, bg=_CURRENT_PALETTE['bg_dark'])
            outer.pack(fill='x', pady=(5, 5), padx=8)
            bubble_bg = _CURRENT_PALETTE['accent'] if is_user else '#f4f4f5'
            bubble_fg = '#ffffff' if is_user else '#202124'
            anchor = 'e' if is_user else 'w'
            bubble = tk.Frame(outer, bg=bubble_bg, padx=12, pady=9)
            bubble.pack(anchor=anchor, fill='x' if not is_user else None, padx=(70, 0) if is_user else (0, 70))
            bubble.columnconfigure(0, weight=1)
            text_box = tk.Text(bubble, wrap='word', height=1, width=72, bg=bubble_bg, fg=bubble_fg, insertbackground=bubble_fg, selectbackground=_CURRENT_PALETTE['accent'], relief='flat', bd=0, padx=0, pady=0, highlightthickness=0, font=('Segoe UI', 10), spacing1=2, spacing3=2)
            text_box.grid(row=0, column=0, sticky='ew')
            text_box.tag_configure('bold', font=('Segoe UI', 10, 'bold'))
            text_box.tag_configure('italic', font=('Segoe UI', 10, 'italic'))
            text_box.tag_configure('code', font=('Consolas', 9), background='#252526', foreground='#d4d4d4')
            text_box.tag_configure('link', foreground='#4da3ff', underline=True)
            text_box.tag_configure('heading', font=('Segoe UI Semibold', 11, 'bold'))
            link_index = {'value': 0}

            def insert_formatted(value, code_mode=False):
                if not value:
                    return
                if code_mode:
                    text_box.insert('end', value, 'code')
                    return
                pattern = re.compile(r'(\[[^\]\n]+\]\((?:https?://|www\.)[^)\s]+\)|https?://[^\s<>]+|^[ \t]*#{1,6}[ \t]+[^\n]+$|\*\*[^*\n]+\*\*|`[^`\n]+`|(?<!\*)\*[^*\n]+\*)', re.M)
                cursor = 0
                for match in pattern.finditer(value):
                    if match.start() > cursor:
                        text_box.insert('end', value[cursor:match.start()])
                    token = match.group(0)
                    if re.match(r'^[ \t]*#{1,6}[ \t]+', token):
                        heading_text = re.sub(r'^[ \t]*#{1,6}[ \t]+', '', token).strip()
                        text_box.insert('end', heading_text + ('\n' if token.endswith('\n') else ''), 'heading')
                    elif token.startswith('[') and '](' in token:
                        label, url = token[1:].split('](', 1)
                        url = url.rstrip(')')
                        if url.startswith('www.'):
                            url = 'https://' + url
                        tag = f'link_{link_index["value"]}'
                        link_index['value'] += 1
                        text_box.insert('end', label, ('link', tag))
                        text_box.tag_bind(tag, '<Button-1>', lambda _event, target=url: webbrowser.open(target))
                        text_box.tag_bind(tag, '<Enter>', lambda _event: text_box.configure(cursor='hand2'))
                        text_box.tag_bind(tag, '<Leave>', lambda _event: text_box.configure(cursor='xterm'))
                    elif token.startswith('http://') or token.startswith('https://'):
                        url = token.rstrip('.,;:!?)]}')
                        tag = f'link_{link_index["value"]}'
                        link_index['value'] += 1
                        text_box.insert('end', url, ('link', tag))
                        text_box.tag_bind(tag, '<Button-1>', lambda _event, target=url: webbrowser.open(target))
                        text_box.tag_bind(tag, '<Enter>', lambda _event: text_box.configure(cursor='hand2'))
                        text_box.tag_bind(tag, '<Leave>', lambda _event: text_box.configure(cursor='xterm'))
                    elif token.startswith('**'):
                        text_box.insert('end', token[2:-2], 'bold')
                    elif token.startswith('`'):
                        text_box.insert('end', token[1:-1], 'code')
                    else:
                        text_box.insert('end', token[1:-1], 'italic')
                    cursor = match.end()
                if cursor < len(value):
                    text_box.insert('end', value[cursor:])

            code_pattern = re.compile(r'```(?:[\w+-]*)\n?(.*?)```', re.S)
            cursor = 0
            for match in code_pattern.finditer(text):
                insert_formatted(re.sub(r'(?m)^[ \t]*(?:[-*]|\d+[.)])[ \t]+', '• ', text[cursor:match.start()]))
                insert_formatted(match.group(1).rstrip('\n'), True)
                if match.end() < len(text):
                    text_box.insert('end', '\n')
                cursor = match.end()
            insert_formatted(re.sub(r'(?m)^[ \t]*(?:[-*]|\d+[.)])[ \t]+', '• ', text[cursor:]))
            text_box.configure(state='disabled')

            def fit_text(_event=None):
                try:
                    text_box.update_idletasks()
                    line_count = int(text_box.count('1.0', 'end-1c', 'displaylines')[0]) if text_box.get('1.0', 'end-1c') else 1
                    text_box.configure(height=max(1, min(line_count, 120)))
                except (tk.TclError, TypeError, IndexError):
                    pass

            text_box.bind('<Configure>', fit_text)
            text_box.after_idle(fit_text)
            bubble_refs.append((bubble, text, is_user))
            canvas.after_idle(lambda: canvas.yview_moveto(1.0))

        def load_session(index):
            if not (0 <= index < len(sessions)):
                return
            active['index'] = index
            clear_messages()
            for item in sessions[index].get('messages', []):
                try:
                    role = item.get('role', 'model')
                    value = ''.join(str(part.get('text', '')) for part in item.get('parts', []))
                    if value:
                        add_message(value, role, persist=False)
                except Exception:
                    pass
            refresh_history_list()

        def new_chat():
            if busy['value']:
                return
            sessions.append({'title': 'New chat', 'messages': []})
            active['index'] = len(sessions) - 1
            load_session(active['index'])
            input_box.focus_set()

        def rename_session(index):
            if busy['value'] or not (0 <= index < len(sessions)):
                return
            current = session_title(sessions[index])
            new_title = simpledialog.askstring('Rename chat', 'Enter a new chat name:', initialvalue=current, parent=win)
            if new_title is None:
                return
            new_title = ' '.join(str(new_title).split()).strip()[:80]
            if not new_title:
                return
            sessions[index]['title'] = new_title
            refresh_history_list()

        def attach_file():
            paths = filedialog.askopenfilenames(parent=win, title='Attach files')
            if not paths:
                return
            attached_files.clear()
            attached_files.extend(paths[:5])
            attach_btn.configure(text=f'+ {len(attached_files)}')

        def finish(answer, generated_title=None):
            if not win.winfo_exists():
                return
            pending = thinking_box.get('widget')
            if pending is not None:
                try:
                    pending.destroy()
                except tk.TclError:
                    pass
                thinking_box['widget'] = None
            current = sessions[active['index']]
            current['messages'].append({'role': 'model', 'parts': [{'text': answer}]})
            if generated_title and session_title(current) == 'New chat':
                current['title'] = generated_title
            add_message(answer, 'model')
            refresh_history_list()
            busy['value'] = False
            send_btn.configure(state='normal')
            attach_btn.configure(state='normal')
            input_box.configure(state='normal')
            input_box.focus_set()

        def send():
            if busy['value']:
                return
            text = input_box.get('1.0', 'end-1c').strip()
            if attached_files:
                file_context = []
                for path in attached_files:
                    try:
                        size = os.path.getsize(path)
                        if size <= 300000:
                            content = Path(path).read_text(encoding='utf-8', errors='replace')
                            file_context.append(f'\n[Attached file: {os.path.basename(path)}]\n{content[:120000]}')
                        else:
                            file_context.append(f'\n[Attached file: {os.path.basename(path)}; too large to read]')
                    except Exception as exc:
                        file_context.append(f'\n[Attached file: {os.path.basename(path)}; unavailable: {exc}]')
                text += ''.join(file_context)
            if not text:
                return
            session = sessions[active['index']]
            input_box.delete('1.0', 'end')
            add_message(text, 'user')
            session['messages'].append({'role': 'user', 'parts': [{'text': text}]})
            refresh_history_list()
            busy['value'] = True
            send_btn.configure(state='disabled')
            attach_btn.configure(state='disabled')
            input_box.configure(state='disabled')
            add_message('Thinking ...', 'model')
            try:
                thinking_box['widget'] = messages.winfo_children()[-1]
            except (IndexError, tk.TclError):
                thinking_box['widget'] = None
            selected_model = model_names.get(model_var.get(), 'gemini-3.5-flash-lite')
            request_history = list(session['messages'])

            def worker():
                try:
                    system_text = "You are RoUtils AI, the built-in assistant for the RoUtils desktop application. Answer questions about RoUtils features, Cache, FFlags, Modifications, Configs, Themes, Console, Settings, plugins, macros, Roblox, Windows, programming, and general topics. Use the current conversation history. Do not explain how to apply a FastFlag unless the user explicitly asks how to apply it. If the user asks about RoUtils, use the known application context instead of claiming that you do not know the app. Be concise, accurate, practical, and honest about uncertainty. Use clean Markdown and preserve newlines in code and structured text."
                    payload = {'systemInstruction': {'parts': [{'text': system_text}]}, 'contents': request_history}
                    req = urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/' + selected_model + ':generateContent', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json', 'x-goog-api-key': key}, method='POST')
                    with urllib.request.urlopen(req, timeout=60) as response:
                        result = json.loads(response.read().decode('utf-8'))
                    parts = result.get('candidates', [{}])[0].get('content', {}).get('parts', [])
                    answer = ''.join(str(part.get('text', '')) for part in parts).strip()
                    if not answer:
                        raise RuntimeError('Gemini returned an empty response.')
                    generated = None
                    if session_title(session) == 'New chat':
                        first_request = session['messages'][0]['parts'][0].get('text', '')[:1200]
                        try:
                            title_payload = {'contents': [{'role': 'user', 'parts': [{'text': 'Create a short natural chat title in the same language as this request. Return only the title, without quotes, markdown, or explanation. Maximum 45 characters. Request: ' + first_request}]}]}
                            title_req = urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/' + selected_model + ':generateContent', data=json.dumps(title_payload).encode('utf-8'), headers={'Content-Type': 'application/json', 'x-goog-api-key': key}, method='POST')
                            with urllib.request.urlopen(title_req, timeout=20) as title_response:
                                title_result = json.loads(title_response.read().decode('utf-8'))
                            title_parts = title_result.get('candidates', [{}])[0].get('content', {}).get('parts', [])
                            generated = ''.join(str(part.get('text', '')) for part in title_parts).strip().replace('\n', ' ')
                            generated = re.sub(r'["\'`]+', '', generated).strip(' .:;,-')[:45] or None
                        except Exception:
                            generated = None
                    win.after(0, lambda result=answer, title=generated: finish(result, title))
                except Exception as exc:
                    win.after(0, lambda error=str(exc): finish('Error: ' + error))

            threading.Thread(target=worker, daemon=True).start()

        new_chat_btn.configure(command=new_chat)
        attach_btn.configure(command=attach_file)
        send_btn.configure(command=send)
        input_box.bind('<Control-Return>', lambda _e: (send(), 'break')[1])
        sessions[:] = [{'title': 'New chat', 'messages': []}]
        active['index'] = 0
        refresh_history_list()
        load_session(active['index'])
        input_box.focus_set()

        def close_ai_chat():
            try:
                win.destroy()
            except tk.TclError:
                pass
            self._ai_chat_window = None

        win.protocol('WM_DELETE_WINDOW', close_ai_chat)

    def _build_viewer_widgets(self):
        top = ttk.Frame(self.viewer_root, padding=(8, 6))
        top.pack(fill='x')
        self._cache_top = top
        ttk.Checkbutton(top, style='TCheckbutton', text='Auto-scroll', variable=self.autoscroll).grid(row=0, column=0, sticky='w')
        ttk.Checkbutton(top, style='TCheckbutton', text='Hide tickets', variable=self.hide_tickets, command=self._apply_filter).grid(row=0, column=1, sticky='w', padx=(4, 0))
        ttk.Checkbutton(top, style='TCheckbutton', text='Stay on top', variable=self.stay_on_top, command=self._apply_stay_on_top).grid(row=0, column=2, sticky='w', padx=(4, 0))
        ttk.Checkbutton(top, style='TCheckbutton', text='Show lines', variable=self.show_lines, command=self._apply_show_lines).grid(row=0, column=3, sticky='w', padx=(4, 0))
        self.btn_clear = ttk.Button(top, text='Clear rbx-storage', command=self._clear_storage_now)
        self.btn_clear.grid(row=0, column=5, sticky='e', padx=(0, 6))
        self.btn_delete_type = ttk.Button(top, text='Delete Cache Type', command=self._open_delete_cache_type)
        self.btn_delete_type.grid(row=0, column=6, sticky='e', padx=(0, 6))
        self.toggle_btn = ttk.Button(top, text='Start Watching', command=self._toggle_watch)
        self.toggle_btn.grid(row=0, column=7, sticky='e', padx=(0, 6))
        self.btn_dump = ttk.Button(top, text='Dump Caches', command=self._dump_all_caches)
        self.btn_dump.grid(row=0, column=8, sticky='e')
        self._cache_db_label = ttk.Label(top, text='DB:')
        self._cache_db_label.grid(row=1, column=0, sticky='w', pady=(4, 0))
        self.db_label = ttk.Label(top, text=self.db_path, width=50)
        self.db_label.grid(row=1, column=1, columnspan=6, sticky='ew', padx=(4, 12), pady=(4, 0))
        self._cache_type_label = ttk.Label(top, text='Type:')
        self._cache_type_label.grid(row=2, column=0, sticky='w', pady=(4, 0))
        type_combo = ttk.Combobox(top, textvariable=self.type_filter, values=[t[0] for t in TYPE_FILTERS], state='readonly', width=14)
        self._cache_type_combo = type_combo
        type_combo.grid(row=2, column=1, sticky='w', padx=(8, 0), pady=(4, 0))
        type_combo.bind('<<ComboboxSelected>>', lambda e: self._apply_filter())
        self._cache_filter_label = ttk.Label(top, text='Filter:')
        self._cache_filter_label.grid(row=3, column=0, sticky='w', pady=(4, 0))
        f_entry = ttk.Entry(top, textvariable=self.filter_text)
        self._cache_filter_entry = f_entry
        f_entry.grid(row=3, column=1, columnspan=6, sticky='ew', pady=(4, 0))
        f_entry.bind('<KeyRelease>', lambda e: self._schedule_ui('cache_filter', 120, self._apply_filter))
        for c in (3, 4):
            top.columnconfigure(c, weight=1)
        for c in (5, 6, 7, 8):
            top.columnconfigure(c, weight=0)
        top.bind('<Configure>', lambda _e: self._schedule_ui('cache_toolbar', 80, self._responsive_cache_toolbar), add='+')
        self.after_idle(self._responsive_cache_toolbar)
        self.vpaned = ttk.PanedWindow(self.viewer_root, orient='vertical')
        self.vpaned.pack(fill='both', expand=True, padx=8, pady=(0, 6))
        self.table_frame = ttk.Frame(self.vpaned)
        self.vpaned.add(self.table_frame, weight=3)
        _set_pane_minsize(self.vpaned, self.table_frame, 200)
        columns = ('time', 'name', 'hash', 'size', 'kind', 'src')
        self.columns = columns
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings', selectmode='extended')
        self.tree.heading('time', text='TIME', command=lambda: self._sort_by('time'))
        self.tree.heading('name', text='NAME', command=lambda: self._sort_by('name'))
        self.tree.heading('hash', text='HASH', command=lambda: self._sort_by('hash'))
        self.tree.heading('size', text='SIZE', command=lambda: self._sort_by('size', numeric=True))
        self.tree.heading('kind', text='TYPE', command=lambda: self._sort_by('kind'))
        self.tree.heading('src', text='SOURCE', command=lambda: self._sort_by('src'))
        self.tree.column('time', width=70, minwidth=60, anchor='w', stretch=True)
        self.tree.column('name', width=140, minwidth=80, anchor='w', stretch=True)
        self.tree.column('hash', width=200, minwidth=200, anchor='w', stretch=True)
        self.tree.column('size', width=70, minwidth=60, anchor='w', stretch=True)
        self.tree.column('kind', width=150, minwidth=120, anchor='w', stretch=True)
        self.tree.column('src', width=80, minwidth=60, anchor='w', stretch=True)
        vsb = ttk.Scrollbar(self.table_frame, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, columnspan=2, sticky='ew')
        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.columnconfigure(0, weight=1)
        self.tree.tag_configure('hover', background='#333333')
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)
        self.tree.bind('<Delete>', lambda e: self._action_delete_blob())
        self.tree.bind('<F2>', lambda e: self._action_change_hash())
        self._ctx = tk.Menu(self, tearoff=0)
        self._ctx.add_command(label='Export ▸ Full Blob…', command=self._export_selected_full)
        self._ctx.add_command(label='Export ▸ RBXM…', command=self._export_selected_rbxm)
        self._ctx_rbxm_index = self._ctx.index('end')
        self._ctx.add_command(label='Export as OBJ', command=self._export_selected_mesh_obj)
        self._ctx_obj_index = self._ctx.index('end')
        self._ctx.add_command(label='Export ▸ Image…', command=self._export_selected_image)
        self._ctx_img_index = self._ctx.index('end')
        self._ctx.add_command(label='Export ▸ Video…', command=self._export_selected_video)
        self._ctx_video_index = self._ctx.index('end')
        self._ctx.add_separator()
        for lbl, cmd in [('Change Hash…', self._action_change_hash), ('Delete Blob', self._action_delete_blob)]:
            self._ctx.add_command(label=lbl, command=cmd)
        self._ctx.add_separator()
        self._ctx.add_command(label='Copy Hash', command=lambda: self._copy_selected_hash())
        self._ctx.add_separator()
        self._ctx.add_command(label='Save Hash…', command=self._action_save_hash_to_saves)
        self._ctx.add_command(label='Save Blob…', command=self._action_save_blob_to_saves)
        darken_menus((self._ctx,))
        self._col_vars = {}
        self._colmenu = tk.Menu(self, tearoff=0)
        col_defs = {'time': ('TIME', True), 'name': ('NAME', True), 'hash': ('HASH', True), 'size': ('SIZE', True), 'kind': ('TYPE', True), 'src': ('SOURCE', False)}
        for col in self.columns:
            label, default = col_defs[col]
            var = tk.BooleanVar(value=self.settings.get('columns', {}).get(col, default))
            self._col_vars[col] = var
            self._colmenu.add_checkbutton(label=label, variable=var, command=self._update_displaycolumns)
        self._update_displaycolumns(save=False)
        darken_menus((self._colmenu,))
        self.tree.bind('<Button-3>', self._on_tree_right_click)
        self.tree.bind('<Control-Button-1>', self._on_tree_right_click)
        self.tree.bind('<Motion>', self._on_tree_motion)
        self.tree.bind('<Leave>', self._on_tree_leave)
        self.details = ttk.Frame(self.vpaned)
        self.vpaned.add(self.details, weight=2)
        _set_pane_minsize(self.vpaned, self.details, 100)
        self.detail_pane = ttk.PanedWindow(self.details, orient='horizontal')
        self.detail_pane.pack(fill='both', expand=True)
        self.viewport_host = ttk.Frame(self.detail_pane)
        self.detail_pane.add(self.viewport_host, weight=2)
        self.viewport_3d = Viewport3DPanel(self.viewport_host)
        self.viewport_3d.is_own_host = True
        self.viewport_3d.reduce_polys.set(bool(self.settings.get('preview_optimize_vertices', True)))
        self.viewport_3d.reduce_polys.trace_add('write', lambda *_: self._save_settings())
        self.text_host = ttk.Frame(self.detail_pane)
        self.detail_pane.add(self.text_host, weight=1)
        description = ttk.LabelFrame(self.text_host, text='Asset Description', padding=(6, 4))
        description.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.details_text = tk.Text(description, wrap='word', height=6, font=('Consolas', 10), bg='#252526', fg='#d4d4d4', insertbackground='#ffffff', selectbackground='#007acc', selectforeground='#ffffff', relief='flat', bd=0)
        d_vsb = ttk.Scrollbar(description, orient='vertical', command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=d_vsb.set)
        self.details_text.grid(row=0, column=0, sticky='nsew')
        d_vsb.grid(row=0, column=1, sticky='ns')
        description.rowconfigure(0, weight=1)
        description.columnconfigure(0, weight=1)
        self.text_host.rowconfigure(0, weight=1)
        self.text_host.columnconfigure(0, weight=1)
        _set_pane_minsize(self.detail_pane, self.viewport_host, 260)
        _set_pane_minsize(self.detail_pane, self.text_host, 220)
        self.after(50, self._ensure_pane_order)
        status = ttk.Frame(self.viewer_root, padding=(8, 6, 8, 8))
        status.pack(fill='x')
        self.status_label = ttk.Label(status, text='')
        self.status_label.pack(side='left')

    def _responsive_cache_toolbar(self, _event=None):
        top = getattr(self, '_cache_top', None)
        if top is None:
            return
        narrow = False
        try:
            if getattr(self, '_cache_toolbar_layout_applied', False):
                return
            self._cache_toolbar_layout_applied = True
            toggles = sorted([w for w in top.grid_slaves(row=0) if w not in (self.btn_clear, self.btn_delete_type, self.toggle_btn, self.btn_dump)], key=lambda w: int(w.grid_info().get('column', 0)))
            if narrow:
                for index, widget in enumerate(toggles):
                    widget.grid_configure(row=index // 2, column=index % 2, sticky='w', padx=(0, 6), pady=(0, 2))
                self.btn_clear.grid_configure(row=2, column=0, sticky='ew', padx=(0, 6), pady=(4, 0))
                self.btn_delete_type.grid_configure(row=2, column=1, sticky='ew', padx=(0, 6), pady=(4, 0))
                self.toggle_btn.grid_configure(row=3, column=0, sticky='ew', padx=(0, 6), pady=(4, 0))
                self.btn_dump.grid_configure(row=3, column=1, sticky='ew', pady=(4, 0))
                self._cache_db_label.grid_configure(row=4, column=0)
                self.db_label.grid_configure(row=4, column=1, columnspan=3)
                self._cache_type_label.grid_configure(row=5, column=0)
                self._cache_type_combo.grid_configure(row=5, column=1)
                self._cache_filter_label.grid_configure(row=6, column=0)
                self._cache_filter_entry.grid_configure(row=6, column=1, columnspan=3)
                for col in range(4):
                    top.columnconfigure(col, weight=1)
            else:
                for index, widget in enumerate(toggles):
                    widget.grid_configure(row=0, column=index, sticky='w', padx=(0 if index == 0 else 4, 0), pady=0)
                self.btn_clear.grid_configure(row=0, column=5, sticky='e', padx=(0, 6), pady=0)
                self.btn_delete_type.grid_configure(row=0, column=6, sticky='e', padx=(0, 6), pady=0)
                self.toggle_btn.grid_configure(row=0, column=7, sticky='e', padx=(0, 6), pady=0)
                self.btn_dump.grid_configure(row=0, column=8, sticky='e', pady=0)
                self._cache_db_label.grid_configure(row=1, column=0)
                self.db_label.grid_configure(row=1, column=1, columnspan=6)
                self._cache_type_label.grid_configure(row=2, column=0)
                self._cache_type_combo.grid_configure(row=2, column=1)
                self._cache_filter_label.grid_configure(row=3, column=0)
                self._cache_filter_entry.grid_configure(row=3, column=1, columnspan=6)
                for col in (5, 6, 7, 8):
                    top.columnconfigure(col, weight=0)
        except Exception:
            pass

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
                    self.geometry(f'{w}x{h}+{new_x}+{cur_y}')
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
            self.collapse_btn.config(text='◀')
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
                self.geometry(f'{new_w}x{h}+{new_x}+{y}')
            except Exception:
                pass
            self.viewer_collapsed = True
            self.collapse_btn.config(text='▶')
            self._save_settings()

    def _set_resize_redraw(self, enabled):

        if sys.platform != 'win32':
            return
        try:
            user32 = ctypes.windll.user32
            WM_SETREDRAW = 0x000B
            widgets = [getattr(self, 'tree', None), getattr(self, 'details_text', None)]
            for widget in widgets:
                if widget is None:
                    continue
                target = widget.canvas if hasattr(widget, 'canvas') else widget
                try:
                    hwnd = int(target.winfo_id())
                    user32.SendMessageW(hwnd, WM_SETREDRAW, 1 if enabled else 0, 0)
                    if enabled and widget is getattr(self, 'tree', None):
                        user32.InvalidateRect(hwnd, None, True)
                except Exception:
                    continue
        except Exception:
            pass

    def _finish_live_resize(self):
        self._resize_restore_job = None
        if getattr(self, '_resize_redraw_suspended', False):
            self._resize_redraw_suspended = False
            self._set_resize_redraw(True)

    def _on_geometry_configure(self, event=None):
        if event is not None and event.widget is not self:
            return
        try:
            geom = self.geometry()
            if geom == getattr(self, '_last_geometry_seen', None):
                return
            self._last_geometry_seen = geom
            match = re.match(r'^(\d+)x(\d+)', geom)
            if match:
                size = (int(match.group(1)), int(match.group(2)))
                previous = getattr(self, '_last_resize_size', None)
                if previous is not None and abs(size[0] - previous[0]) < 12 and abs(size[1] - previous[1]) < 12:
                    return
                self._last_resize_size = size
        except Exception:
            pass


        if not getattr(self, '_resize_redraw_suspended', False):
            self._resize_redraw_suspended = True
            self._set_resize_redraw(False)
        old_job = getattr(self, '_resize_restore_job', None)
        if old_job is not None:
            try:
                self.after_cancel(old_job)
            except Exception:
                pass
        self._resize_restore_job = self.after(150, self._finish_live_resize)
        if self._geometry_save_job is not None:
            try:
                self.after_cancel(self._geometry_save_job)
            except Exception:
                pass
        try:
            def save_geometry_once():
                self._geometry_save_job = None
                self._save_settings()
            self._geometry_save_job = self.after(1200, save_geometry_once)
        except Exception:
            self._geometry_save_job = None

    def _apply_mesh_preview_vertices_setting(self):
        value = bool(self.mesh_preview_vertices.get())
        self.settings['preview_optimize_vertices'] = value
        try:
            if hasattr(self, 'viewport_3d'):
                self.viewport_3d.reduce_polys.set(value)
        except Exception:
            pass
        self._save_settings()

    def _save_settings(self):
        data = {'autoscroll': self.autoscroll.get(), 'hide_tickets': self.hide_tickets.get(), 'stay_on_top': self.stay_on_top.get(), 'show_lines': self.show_lines.get(), 'preview_optimize_vertices': self.viewport_3d.reduce_polys.get() if hasattr(self, 'viewport_3d') else self.settings.get('preview_optimize_vertices', True), 'streamer_mode': self.streamer_mode.get() if hasattr(self, 'streamer_mode') else self.settings.get('streamer_mode', False), 'fps_limit': self.fps_limit.get() if hasattr(self, 'fps_limit') else self.settings.get('fps_limit', 0), 'autostart_watch': self.autostart_watch.get() if hasattr(self, 'autostart_watch') else self.settings.get('autostart_watch', False), 'max_rows': self.max_rows.get() if hasattr(self, 'max_rows') else self.settings.get('max_rows', 0), 'type_filter': self.type_filter.get(), 'columns': {c: var.get() for c, var in getattr(self, '_col_vars', {}).items()}, 'viewer_collapsed': self.viewer_collapsed, 'theme': self.theme_var.get() if hasattr(self, 'theme_var') else self.settings.get('theme', DEFAULT_THEME), 'fflag_hotkeys': self.fflag_hotkeys, 'fps_hotkeys': self.fps_hotkeys, 'fps_hotkey_slots': self.fps_hotkey_slots, 'fflag_auto_apply': self.fflag_auto_apply.get() if hasattr(self, 'fflag_auto_apply') else self.settings.get('fflag_auto_apply', False), 'launch_on_tray': self.launch_on_tray.get() if hasattr(self, 'launch_on_tray') else self.settings.get('launch_on_tray', False), 'launch_on_startup': self.launch_on_startup.get() if hasattr(self, 'launch_on_startup') else self.settings.get('launch_on_startup', False), 'hide_to_tray_on_close': self.hide_to_tray_on_close.get() if hasattr(self, 'hide_to_tray_on_close') else self.settings.get('hide_to_tray_on_close', False), 'auto_update': self.auto_update.get() if hasattr(self, 'auto_update') else self.settings.get('auto_update', False), 'dpi_percent': int(self.dpi_percent.get()) if hasattr(self, 'dpi_percent') else int(getattr(self, '_dpi_scale', 1.0) * 100), 'plugin_enabled': getattr(self, '_plugin_enabled', self.settings.get('plugin_enabled', {})), 'roblox_path': self.settings.get('roblox_path', ''), 'gemini_api_key': self.gemini_api_key.get().strip() if hasattr(self, 'gemini_api_key') else self.settings.get('gemini_api_key', ''), 'custom_theme': self.settings.get('custom_theme', {}), 'db_path': getattr(self, 'db_path', self.settings.get('db_path', '')), 'shard_root': getattr(self, 'shard_root', self.settings.get('shard_root', '')), 'window_geometry': self.geometry() if self.winfo_exists() else self.settings.get('window_geometry', STARTUP_GEOMETRY)}
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
        cols = self.tree['columns']
        for c in cols:
            try:
                w = tkfont.Font().measure(self.tree.heading(c)['text'])
            except Exception:
                w = 80
            for i, iid in enumerate(self.tree.get_children('')):
                if i > 120:
                    break
                text = str(self.tree.set(iid, c))
                w = max(w, tkfont.Font().measure(text))
            measured = min(max(w + padding, 80), 520)
            current = int(self.tree.column(c, 'width'))
            self.tree.column(c, width=max(current, measured))

    def _cache_type_matches(self, it, selected):
        cat = str(it.kind or '').split(' ', 1)[0].strip().lower()
        selected = str(selected).strip().lower()
        if selected == 'mesh':
            return cat == 'mesh'
        if selected == 'model/rbxm':
            return cat in {'model', 'rbxm', 'rbxl', 'rbxl (place)'}
        if selected == 'unsupported_animation':
            return cat == 'unsupported_animation'
        if selected == 'image':
            return cat in {'image', 'decal', 'texture'}
        if selected == 'audio':
            return cat in {'sound', 'audio'}
        if selected == 'video':
            return cat == 'video'
        if selected == 'font':
            return cat == 'font'
        if selected == 'text':
            return cat in {'text', 'translations', 'translation'}
        if selected == 'unknown':
            return cat == 'unknown'
        return False

    def _open_delete_cache_type(self):
        dlg = tk.Toplevel(self)
        dlg.title('Delete Cache Type')
        dlg.resizable(False, False)
        dlg.transient(self)
        theme_toplevel(dlg)
        outer = ttk.Frame(dlg, padding=12)
        outer.pack(fill='both', expand=True)
        ttk.Label(outer, text='Delete all caches of this type:').pack(anchor='w', pady=(0, 7))
        type_var = tk.StringVar(value='Mesh')
        combo = ttk.Combobox(outer, textvariable=type_var, values=('Mesh', 'Model/RBXM', 'Animation', 'Image', 'Audio', 'Video', 'Font', 'Text', 'Unknown'), state='readonly', width=18)
        combo.pack(fill='x')

        def do_delete():
            selected = type_var.get()
            dlg.destroy()
            self._delete_cache_type(selected)
        btns = ttk.Frame(outer)
        btns.pack(fill='x', pady=(10, 0))
        ttk.Button(btns, text='Delete', command=do_delete).pack(side='left')
        ttk.Button(btns, text='Cancel', command=dlg.destroy).pack(side='right')
        combo.focus_set()

    def _delete_cache_type(self, selected):
        if getattr(self, '_cache_type_busy', False):
            return
        self._cache_type_busy = True
        try:
            self.btn_delete_type.config(state='disabled')
        except Exception:
            pass
        was_running = bool(self.watching)
        if was_running:
            self._stop_watching()

        def scan_worker():
            try:
                if not os.path.isfile(self.db_path):
                    result = ('error', 'rbx-storage.db was not found.')
                else:
                    items = scan_db_once(self.db_path, self.shard_root, set(), None)
                    targets = [it for it in items if self._cache_type_matches(it, selected)]
                    result = ('found', targets)
            except Exception as e:
                result = ('error', str(e))
            self.after(0, lambda r=result: self._delete_cache_type_scan_done(selected, r, was_running))
        threading.Thread(target=scan_worker, daemon=True, name='RoUtils-DeleteTypeScan').start()

    def _delete_cache_type_scan_done(self, selected, result, was_running):
        if result[0] == 'error':
            self._finish_delete_cache_type(('error', result[1]), was_running)
            return
        targets = result[1]
        if not targets:
            self._finish_delete_cache_type(('none', None), was_running)
            return
        try:
            ok = messagebox.askyesno('Delete Cache Type', f'Delete all {len(targets)} {selected} cache(s)?\n\nThis cannot be undone.', parent=self)
        except Exception as e:
            self._finish_delete_cache_type(('error', str(e)), was_running)
            return
        if not ok:
            self._finish_delete_cache_type(('cancel', None), was_running)
            return

        def delete_worker():
            deleted_ids = []
            failed = 0
            try:
                conn = connect_rw(self.db_path)
                try:
                    cur = conn.cursor()
                    cur.execute('BEGIN IMMEDIATE')
                    for it in targets:
                        try:
                            cur.execute('DELETE FROM files WHERE id=?', (it.id_bytes,))
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
                self.after(0, lambda: self._finish_delete_cache_type(('ok', len(deleted_ids), failed, deleted_ids, selected), was_running))
            except Exception as e:
                self.after(0, lambda e=e: self._finish_delete_cache_type(('error', str(e)), was_running))
        threading.Thread(target=delete_worker, daemon=True, name='RoUtils-DeleteTypeDelete').start()

    def _finish_delete_cache_type(self, result, was_running):
        try:
            kind = result[0]
            if kind == 'none':
                messagebox.showinfo('Delete Cache Type', 'No caches of the selected type were found.', parent=self)
            elif kind == 'cancel':
                pass
            elif kind == 'ok':
                _, deleted, failed, targets, selected = result
                for it in targets:
                    self.seen_hashes.discard(it.hash)
                    self.items_by_iid.pop(it.hash, None)
                    self.items_by_hash.pop(it.hash, None)
                    for iid in self.tree.get_children(''):
                        try:
                            vals = self.tree.item(iid, 'values')
                            if len(vals) > 2 and str(vals[2]) == str(it.hash):
                                self.tree.delete(iid)
                                break
                        except Exception:
                            pass
                self._update_status()
                msg = f'Deleted {deleted} {selected} cache(s).'
                if failed:
                    msg += f'\nFailed: {failed}'
                messagebox.showinfo('Delete Cache Type', msg, parent=self)
            else:
                messagebox.showerror('Delete Cache Type', str(result[1]), parent=self)
        except Exception as e:
            try:
                messagebox.showerror('Delete Cache Type', str(e), parent=self)
            except Exception:
                pass
        finally:
            self._cache_type_busy = False
            try:
                self.btn_delete_type.config(state='normal')
            except Exception:
                pass
            if was_running and (not self.watching):
                self._start_watching()

    def _cache_type_label(self, result):
        return 'selected type'

    def _dump_blob_body(self, blob):
        meta = parse_rbxh(blob)
        body = meta.get('body') or b''
        if not body:
            return (b'', meta)
        try:
            body = _maybe_gunzip(body, meta.get('headers') or {})
        except Exception:
            pass
        try:
            body = decompress_if_needed(body)
        except Exception:
            pass
        return (body, meta)

    def _dump_image_payload(self, body):
        try:
            label, off = find_embedded_image(body)
            if off > 0:
                body = body[off:]
            img = Image.open(io.BytesIO(body))
            out = io.BytesIO()
            fmt = (img.format or 'PNG').upper()
            if fmt == 'JPEG':
                ext = '.jpg'
                img.save(out, format='JPEG')
            elif fmt == 'WEBP':
                ext = '.webp'
                img.save(out, format='WEBP')
            elif fmt == 'GIF':
                ext = '.gif'
                img.save(out, format='GIF')
            else:
                ext = '.png'
                if img.mode not in ('RGB', 'RGBA', 'L', 'LA', 'P'):
                    img = img.convert('RGBA')
                img.save(out, format='PNG')
            return (out.getvalue(), ext)
        except Exception:
            return (None, None)

    def _dump_one_cache(self, it, dump_root):
        blob = self._fetch_full_blob(it)
        if not blob:
            return False
        body, meta = self._dump_blob_body(blob)
        if not body:
            body = blob
            meta = {}
        if not body:
            return False
        cat = str(it.kind or 'Unknown').split(' ', 1)[0].strip()
        cat_low = cat.lower()
        folder = 'Unknown'
        payload = body
        ext = '.bin'
        if cat_low == 'mesh':
            folder, ext = ('Meshes', '.obj')
            try:
                obj = convert(body)
            except Exception:
                obj = None
            if not obj:
                return False
            payload = obj.encode('utf-8')
        elif cat_low in {'model', 'rbxm', 'rbxl', 'rbxl (place)'}:
            folder = 'Model-RBXM'
            out = self._rbxm_body(it)
            if out:
                payload, is_binary = out
                ext = '.rbxm' if is_binary else '.rbxmx'
            else:
                ext = '.rbxh'
                payload = blob
        elif cat_low == 'unsupported_animation':
            folder = 'Animations'
            out = self._rbxm_body(it)
            if out:
                payload, is_binary = out
                ext = '.rbxm' if is_binary else '.rbxmx'
            else:
                ext = '.bin'
        elif cat_low in {'image', 'decal', 'texture'}:
            folder = 'Images'
            img_payload, img_ext = self._dump_image_payload(body)
            if img_payload:
                payload, ext = (img_payload, img_ext)
            else:
                ext = '.ktx2' if b'KTX 20' in body[:64] else '.ktx' if b'KTX 11' in body[:64] else '.bin'
        elif cat_low in {'sound', 'audio'}:
            folder = 'Audios'
            lbl = str(it.kind).lower()
            if 'ogg' in lbl or body.startswith(b'OggS'):
                ext = '.ogg'
            elif 'wav' in lbl or (len(body) >= 12 and body[:4] == b'RIFF' and (body[8:12] == b'WAVE')):
                ext = '.wav'
            elif body.startswith(b'ID3'):
                ext = '.mp3'
            else:
                ext = '.bin'
        elif cat_low == 'font':
            folder, ext = ('Fonts', '.ttf')
            if b'OTTO' in body[:4]:
                ext = '.otf'
        elif cat_low in {'translations', 'translation'}:
            folder, ext = ('Translations', '.json')
        elif cat_low == 'text':
            folder, ext = ('Text', '.txt')
        elif cat_low == 'video':
            folder = 'Videos'
            ext = '.webm' if body[:4] == b'\x1aE\xdf\xa3' else '.mp4'
        elif cat_low == 'compressed':
            folder, ext = ('Compressed', '.bin')
        out_dir = os.path.join(dump_root, folder)
        os.makedirs(out_dir, exist_ok=True)
        name = _sanitize_filename_for_windows(it.name or it.hash) or it.hash
        path = os.path.join(out_dir, f'{name}_{it.hash}{ext}')
        with open(path, 'wb') as f:
            f.write(payload)
        return True

    def _dump_all_caches(self):
        if getattr(self, '_dump_running', False):
            return
        dialog = tk.Toplevel(self)
        dialog.title('Dump Caches')
        dialog.transient(self)
        dialog.geometry('620x300')
        dialog.minsize(520, 250)
        dialog.resizable(True, True)
        theme_toplevel(dialog)
        frame = ttk.Frame(dialog, padding=16)
        frame.pack(fill='both', expand=True)
        frame.rowconfigure(4, weight=1)
        frame.columnconfigure(0, weight=1)
        status = tk.StringVar(value='Preparing cache dump...')
        ttk.Label(frame, text='Dump Caches', font=('Segoe UI', 13, 'bold')).grid(row=0, column=0, sticky='w')
        ttk.Label(frame, textvariable=status, wraplength=560).grid(row=1, column=0, sticky='ew', pady=(8, 10))
        progress = ttk.Progressbar(frame, mode='determinate')
        progress.grid(row=2, column=0, sticky='ew', pady=(0, 6))
        details_frame = ttk.Frame(frame)
        details_frame.grid(row=4, column=0, sticky='nsew', pady=(10, 0))
        details_frame.rowconfigure(0, weight=1)
        details_frame.columnconfigure(0, weight=1)
        details = tk.Text(details_frame, wrap='word', height=8, state='disabled', bg='#252526', fg='#d4d4d4', insertbackground='#ffffff', relief='flat', bd=0, font=('Consolas', 9))
        details_scroll = ttk.Scrollbar(details_frame, orient='vertical', command=details.yview)
        details.configure(yscrollcommand=details_scroll.set)
        details.grid(row=0, column=0, sticky='nsew')
        details_scroll.grid(row=0, column=1, sticky='ns')
        details_frame.grid_remove()
        controls = ttk.Frame(frame)
        controls.grid(row=5, column=0, sticky='e', pady=(12, 0))
        details_button = ttk.Button(controls, text='Details')
        details_button.pack(side='left', padx=(0, 8))
        close_button = ttk.Button(controls, text='Close')
        close_button.pack(side='left')
        self._dump_running = True
        cancel = threading.Event()
        closed = threading.Event()
        expanded = {'value': False}

        def append_detail(message):
            if closed.is_set() or not dialog.winfo_exists():
                return
            details.configure(state='normal')
            details.insert('end', str(message) + '\n')
            details.see('end')
            details.configure(state='disabled')

        def safe_ui(callback):
            if closed.is_set():
                return
            try:
                if dialog.winfo_exists():
                    dialog.after(0, callback)
            except tk.TclError:
                pass

        def finish():
            self._dump_running = False
            if closed.is_set():
                return
            try:
                close_button.configure(state='normal', text='Close')
                status.set(status.get() if status.get().startswith(('Finished', 'Error', 'Cancelled')) else 'Finished.')
            except tk.TclError:
                pass

        def close_dialog():
            if self._dump_running:
                cancel.set()
                status.set('Cancelling...')
            closed.set()
            try:
                dialog.destroy()
            except tk.TclError:
                pass

        def toggle_details():
            expanded['value'] = not expanded['value']
            if expanded['value']:
                details_frame.grid()
                dialog.geometry('760x600')
                details_button.configure(text='Hide details')
            else:
                details_frame.grid_remove()
                dialog.geometry('620x300')
                details_button.configure(text='Details')

        details_button.configure(command=toggle_details)
        close_button.configure(command=close_dialog)
        dialog.protocol('WM_DELETE_WINDOW', close_dialog)

        def worker():
            dump_root = os.path.join(DATA_DIR, 'Dump')
            os.makedirs(dump_root, exist_ok=True)
            db_path, shard_root = default_paths()
            if not os.path.isfile(db_path):
                safe_ui(lambda: status.set('rbx-storage.db was not found.'))
                safe_ui(finish)
                return
            helper = object.__new__(App)
            helper.db_path = db_path
            helper.shard_root = shard_root
            helper._blob_cache = {}
            helper._blob_cache_order = []
            helper._blob_cache_limit = 256
            try:
                safe_ui(lambda: append_detail(f'Database: {db_path}'))
                safe_ui(lambda: append_detail(f'Output: {dump_root}'))
                safe_ui(lambda: append_detail('Scanning cache database...'))
                items = scan_db_once(db_path, shard_root, set(), None)
                total = len(items)
                dumped = 0
                failed = 0
                safe_ui(lambda n=total: (progress.configure(maximum=max(1, n), value=0), status.set(f'Found {n} cache(s).'), append_detail(f'Found {n} cache(s).')))
                for index, item in enumerate(items, 1):
                    if cancel.is_set():
                        safe_ui(lambda: status.set('Cancelled.'))
                        break
                    ok = False
                    error_text = ''
                    try:
                        ok = bool(App._dump_one_cache(helper, item, dump_root))
                    except Exception as exc:
                        error_text = str(exc)
                    if ok:
                        dumped += 1
                        result_text = f'{index}/{total} dumped: {item.name or item.hash}'
                    else:
                        failed += 1
                        result_text = f'{index}/{total} failed: {item.name or item.hash}' + (f' | {error_text}' if error_text else '')
                    if index % 5 == 0 or index == total:
                        safe_ui(lambda i=index, n=total, d=dumped, f=failed, msg=result_text: (progress.configure(value=i), status.set(f'Processed {i}/{n} | dumped={d} | failed={f}'), append_detail(msg)))
                if cancel.is_set():
                    safe_ui(lambda: append_detail('Dump cancelled by user.'))
                else:
                    safe_ui(lambda d=dumped, f=failed: (status.set(f'Finished. Dumped: {d} | Failed: {f}'), append_detail(f'Finished. Dumped: {d} | Failed: {f}')))
            except Exception as exc:
                safe_ui(lambda e=str(exc): (status.set(f'Error: {e}'), append_detail(f'Error: {e}')))
            finally:
                try:
                    self.after(0, finish)
                except tk.TclError:
                    self._dump_running = False

        threading.Thread(target=worker, daemon=True, name='RoUtilsDumpWorker').start()

    def _run_dump_caches_cli(self):
        if os.name == 'nt':
            try:
                ctypes.windll.kernel32.AllocConsole()
            except Exception:
                pass
        dump_root = os.path.join(DATA_DIR, 'Dump')
        os.makedirs(dump_root, exist_ok=True)
        db_path, shard_root = default_paths()
        if not os.path.isfile(db_path):
            print('ERROR: rbx-storage.db was not found.', flush=True)
            return 1
        print('RoUtils - Dump Caches', flush=True)
        print(f'Database: {db_path}', flush=True)
        print(f'Dump folder: {dump_root}', flush=True)
        print('Scanning cache...', flush=True)
        helper = object.__new__(App)
        helper.db_path = db_path
        helper.shard_root = shard_root
        helper._blob_cache = {}
        helper._blob_cache_order = []
        helper._blob_cache_limit = 256
        try:
            items = scan_db_once(db_path, shard_root, set(), None)
        except Exception as e:
            print(f'ERROR while scanning: {e}', flush=True)
            return 1
        dumped = 0
        failed = 0
        total = len(items)
        print(f'Found {total} cache(s).', flush=True)
        print()
        for index, it in enumerate(items, 1):
            try:
                if App._dump_one_cache(helper, it, dump_root):
                    dumped += 1
                else:
                    failed += 1
            except Exception as e:
                failed += 1
                print(f'Failed {it.hash}: {e}', flush=True)
            if index % 10 == 0 or index == total:
                print(f'Processed {index}/{total} | dumped={dumped} failed={failed}', flush=True)
        print()
        print(f'Finished. Dumped: {dumped} | Failed: {failed}', flush=True)
        print(f'Output: {dump_root}', flush=True)
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
        self._tree_displayed_iids = set()
        self.tree.delete(*self.tree.get_children())
        self._update_status()
        self._console_log(f"Cleared rbx-storage: {deleted_shards} shard(s), DB={('yes' if deleted_db else 'no')}")
        messagebox.showinfo('Clear rbx-storage', f"Deleted shards: {deleted_shards}\nDeleted DB: {('yes' if deleted_db else 'no')}")
        if was:
            self._start_watching()

    def _install_selected_db(self, source_db):
        local = os.environ.get('LOCALAPPDATA') or os.path.expanduser('~')
        roblox_dir = os.path.join(local, 'Roblox')
        target = os.path.join(roblox_dir, 'rbx-storage.db')
        sidecars = [target, target + '-shm', target + '-wal', os.path.join(roblox_dir, 'rbx-storage.id')]
        os.makedirs(roblox_dir, exist_ok=True)
        source_db = os.path.abspath(source_db)
        if not os.path.isfile(source_db):
            raise FileNotFoundError(f'DB file not found: {source_db}')
        with tempfile.NamedTemporaryFile(prefix='routils_db_install_', suffix='.db', delete=False) as tf:
            temp_source = tf.name
        try:
            shutil.copy2(source_db, temp_source)
            conn = sqlite3.connect(temp_source, timeout=3)
            conn.execute('PRAGMA schema_version').fetchone()
            conn.close()
            backup_dir = tempfile.mkdtemp(prefix='routils_db_backup_')
            backups = {}
            try:
                for idx, path in enumerate(sidecars):
                    if os.path.isfile(path):
                        bp = os.path.join(backup_dir, f'{idx}.bak')
                        shutil.copy2(path, bp)
                        backups[path] = bp
                deleted = []
                try:
                    for path in sidecars:
                        if os.path.exists(path):
                            try:
                                os.remove(path)
                            except PermissionError as e:
                                raise PermissionError(f"Cannot delete '{os.path.basename(path)}'. Roblox or another program may be using it.") from e
                            except OSError as e:
                                raise OSError(f"Cannot delete '{os.path.basename(path)}': {e}") from e
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
        self.shard_root = os.path.join(roblox_dir, 'rbx-storage')
        self.db_label.config(text=self.db_path)
        self._reset_seen(clear_list=True)
        return target

    def _choose_db(self):
        path = filedialog.askopenfilename(title='Select rbx-storage.db', filetypes=[('SQLite DB', '*.db'), ('All Files', '*.*')])
        if not path:
            return
        was_watching = self.watching
        if was_watching:
            self._stop_watching()
        try:
            self._install_selected_db(path)
        except Exception as e:
            messagebox.showerror('Choose DB File', f'Could not replace Roblox storage files.\n\n{e}\n\nClose Roblox and try again. No force-delete was used.')
            if was_watching:
                self._start_watching()
            return
        if was_watching:
            self._start_watching()
        messagebox.showinfo('Choose DB File', 'Installed selected DB successfully.\n\nDeleted: rbx-storage.db, rbx-storage.db-shm, rbx-storage.db-wal, rbx-storage.id\nInstalled: rbx-storage.db only.')

    def _choose_shard_root(self):
        d = filedialog.askdirectory(title='Select shard root folder (rbx-storage)')
        if not d:
            return
        self.shard_root = d
        self._reset_seen(clear_list=False)

    def _toggle_watch(self):
        if self.watching:
            self._stop_watching()
            self._console_log('Cache watching stopped')
        elif self._start_watching():
            self._console_log('Cache watching started')
        else:
            self._console_log('Cache watching could not start: database file was not found.')

    def _start_watching(self):
        if not os.path.isfile(self.db_path):
            self._update_status()
            return False
        self.stop_event.clear()
        self.watching = True
        if hasattr(self, 'toggle_btn'):
            self.toggle_btn.config(text='Stop Watching')
        self._update_status()
        self._launch_scan_loop()
        return True

    def _stop_watching(self):
        self.stop_event.set()
        self.watching = False
        if hasattr(self, 'toggle_btn'):
            self.toggle_btn.config(text='Start Watching')
        self._update_status()

    def _launch_scan_loop(self):
        if self.scan_thread and self.scan_thread.is_alive():
            return
        self.scan_thread = threading.Thread(target=self._scan_loop, daemon=True)
        self.scan_thread.start()

    def _scan_loop(self):


        batch_size = 250
        offset = 0
        while not self.stop_event.is_set():
            try:
                configured_limit = int(self.max_rows.get())
            except Exception:
                configured_limit = 0
            limit = configured_limit if configured_limit > 0 else batch_size
            limit = max(50, min(limit, batch_size))
            items = scan_db_once(self.db_path, self.shard_root, self.seen_hashes, limit, offset)
            offset += limit
            if items:
                self.new_items_q.put(items)
                self.stop_event.wait(0.02)
            else:


                offset = 0
                self.stop_event.wait(WATCH_INTERVAL_SEC)

    def _drain_queue(self):


        try:
            active_id = self.nb.select()
            active_name = self.nb.tab(active_id, 'text') if active_id else ''
        except Exception:
            active_name = ''

        tab_busy = bool(getattr(self, '_tab_building', False))
        cache_visible = active_name == 'Cache' and not tab_busy
        processed = 0
        try:


            while processed < (1 if cache_visible else 2):
                items = self.new_items_q.get_nowait()
                for it in items:
                    self.items_by_hash[it.hash] = it
                if cache_visible:
                    self._queue_tree_render(items)
                processed += 1
        except queue.Empty:
            pass
        finally:
            self.after(220 if not cache_visible else 90, self._drain_queue)

    def _should_display(self, it: ScanItem, filt: str) -> bool:
        if self.hide_tickets.get() and it.is_ticket:
            return False
        cat = it.kind.split(' ', 1)[0]
        tf = self.type_filter.get()
        if tf != 'All':
            for label, matcher in TYPE_FILTERS:
                if label == tf:
                    if not matcher(cat):
                        return False
                    break
        row = (it.time, it.name, it.hash, human_size(it.size), it.kind, it.src)
        row_join = ' '.join(map(str, row)).lower()
        if filt and filt not in row_join:
            return False
        return True

    def _queue_tree_render(self, items):


        if not hasattr(self, '_tree_displayed_iids'):
            self._tree_displayed_iids = set()
        if not hasattr(self, '_tree_render_limit'):
            self._tree_render_limit = 1800


        pending = getattr(self, '_tree_render_pending', None)
        if pending is None:
            pending = self._tree_render_pending = []
        pending.extend(items)
        if not getattr(self, '_tree_render_job', None):
            self._tree_render_job = self.after_idle(self._render_tree_batch)

    def _render_tree_batch(self):
        self._tree_render_job = None
        pending = getattr(self, '_tree_render_pending', None) or []
        if not pending:
            return
        filt = self.filter_text.get().lower().strip()
        cursor = getattr(self, '_tree_render_cursor', 0)
        limit = getattr(self, '_tree_render_limit', 3000)
        batch = pending[cursor:cursor + 35]
        self._tree_render_cursor = cursor + len(batch)
        displayed = getattr(self, '_tree_displayed_iids', set())
        rendered = len(displayed)
        for it in batch:
            if rendered >= limit:
                break
            if not self._should_display(it, filt):
                continue
            iid = it.hash
            if iid in displayed:
                continue
            self.tree.insert('', 'end', iid=iid,
                             values=(it.time, it.name, it.hash,
                                     human_size(it.size), it.kind, it.src))
            displayed.add(iid)
            self.items_by_iid[iid] = it
            rendered += 1
        if self._tree_render_cursor < len(pending) and rendered < limit:
            self._tree_render_job = self.after(8, self._render_tree_batch)
        else:
            if self.autoscroll.get():
                children = self.tree.get_children()
                if children:
                    self.tree.see(children[-1])
            self._update_status()

    def _insert_items(self, items: List[ScanItem]):
        for it in items:
            self.items_by_hash[it.hash] = it
        self._queue_tree_render(items)

    def _apply_filter(self):
        if getattr(self, '_tree_render_job', None):
            try:
                self.after_cancel(self._tree_render_job)
            except Exception:
                pass
            self._tree_render_job = None
        self._tree_render_pending = []
        self._tree_render_cursor = 0
        self._tree_displayed_iids = set()
        children = self.tree.get_children()
        if children:
            self.tree.delete(*children)
        self.items_by_iid.clear()
        self._queue_tree_render(list(self.items_by_hash.values()))

    def _apply_stay_on_top(self):
        self.wm_attributes('-topmost', self.stay_on_top.get())

    def _apply_show_lines(self):
        self.viewport_3d.show_wireframe.set(self.show_lines.get())
        if hasattr(self, '_titlebar'):
            try:
                self._titlebar.configure(bg=_CURRENT_PALETTE['bg_dark'])
                for child in self._titlebar.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=_CURRENT_PALETTE['bg_dark'], fg=_CURRENT_PALETTE['fg'])
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
        self.details_text.configure(state='normal')
        self.details_text.delete('1.0', 'end')
        lines = [f'Hash:    {it.hash}', f'Name:    {it.name}', f'Time:    {it.time}', f'Source:  {it.src}', f'Wrapped: {it.wrapped}', f'Size:    {human_size(it.size)}', f'Type:    {it.kind}']
        if multi > 1:
            lines.append(f'Selection: {multi} rows (actions apply to all selected)')
        if it.content_type:
            lines.append(f'Content-Type: {it.content_type}')
        lines.append(f'URL:     {it.url}')
        lines.append('')
        if it.header_text:
            lines.append('RBXH headers (best-effort):')
            lines.append(it.header_text.strip())
            lines.append('')
        if it.is_ticket:
            lines.append('Note: This is a signed-URL ticket cached by the client before fetching the real asset.')
        self.details_text.insert('1.0', '\n'.join(lines))
        self.details_text.configure(state='disabled')

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
        body = meta.get('body') or b''
        cat = it.kind.split(' ', 1)[0]
        is_mesh = cat == 'Mesh'
        is_audio = cat == 'Sound'
        is_model = cat in ('Model', 'RBXM', 'rbxl (place)')
        if not (is_mesh or is_audio or is_model):
            self.viewport_3d.hide()
            return
        temp_pkg_path = os.path.join(TEMP_EMU_DIR, f'preview_{it.hash}.bin')
        try:
            with open(temp_pkg_path, 'wb') as f:
                f.write(body)
        except Exception:
            pass
        self.viewport_3d.set_asset_data_from_temp(temp_pkg_path, is_mesh=is_mesh, is_model=is_model, is_audio=is_audio)
        if is_mesh:
            self.viewport_3d.show(is_anim=False, mode_label='Mesh View')
        elif is_model:
            self.viewport_3d.show(is_anim=False, mode_label='Model View')
        else:
            self.viewport_3d.show(is_anim=False, mode_label='Audio View')


    def _update_displaycolumns(self, save: bool=True):
        cols = [c for c in self.columns if self._col_vars[c].get()]
        if not cols:
            first = self.columns[0]
            self._col_vars[first].set(True)
            cols = [first]
        self.tree.config(displaycolumns=cols)
        for c in cols:
            w = self.tree.column(c, width=None)
            self.tree.column(c, width=w)
        if save:
            self._save_settings()

    def _on_tree_select(self, event):
        self._clear_tree_hover()
        self._schedule_ui('tree_select', 20, self._update_selected_view)

    def _update_selected_view(self):
        self._show_details()
        self._update_preview()

    def _clear_tree_hover(self):
        if self._tree_hover_iid:
            tags = list(self.tree.item(self._tree_hover_iid, 'tags'))
            if 'hover' in tags:
                tags.remove('hover')
                self.tree.item(self._tree_hover_iid, tags=tags)
            self._tree_hover_iid = None

    def _on_tree_leave(self, event):
        self._cancel_image_preview()
        self._clear_tree_hover()

    def _on_tree_right_click(self, event):
        self._cancel_image_preview()
        region = self.tree.identify_region(event.x, event.y)
        if region == 'heading':
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
            any_model = any((i.kind.split(' ', 1)[0] in ('RBXM', 'Model') for i in items))
            any_mesh = any((i.kind.split(' ', 1)[0] == 'Mesh' for i in items))
            any_img = any((i.kind.split(' ', 1)[0] in ('Image', 'Decal', 'Texture') for i in items))
            any_video = any((i.kind.split(' ', 1)[0] == 'Video' for i in items))
            self._ctx.entryconfigure(self._ctx_rbxm_index, state=tk.NORMAL if any_model else tk.DISABLED)
            self._ctx.entryconfigure(self._ctx_obj_index, state=tk.NORMAL if any_mesh else tk.DISABLED)
            self._ctx.entryconfigure(self._ctx_img_index, state=tk.NORMAL if any_img else tk.DISABLED)
            self._ctx.entryconfigure(self._ctx_video_index, state=tk.NORMAL if any_video else tk.DISABLED)
            try:
                self._ctx.tk_popup(event.x_root, event.y_root)
            finally:
                self._ctx.grab_release()

    def _copy_selected_hash(self):
        items = self._get_selected_items()
        if not items:
            return
        joined = '\n'.join((it.hash for it in items))
        self.clipboard_clear()
        self.clipboard_append(joined)
        messagebox.showinfo('Copied', f'Copied {len(items)} hash(es) to clipboard.')

    def _on_tree_motion(self, event):
        row = self.tree.identify_row(event.y)
        self._hover_preview_xy = (event.x_root, event.y_root)
        if row != self._tree_hover_iid:
            self._clear_tree_hover()
            if row:
                tags = list(self.tree.item(row, 'tags'))
                if 'hover' not in tags:
                    tags.append('hover')
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
        cat = it.kind.split(' ', 1)[0]
        if cat in ('Image', 'Decal', 'Texture'):
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
        body = meta.get('body') or b''
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
        self._img_preview_win.geometry(f'+{x + 16}+{y + 16}')
        try:
            self._img_preview_win.attributes('-alpha', 0.0)
        except Exception:
            pass
        self._img_preview_win.deiconify()
        self._img_preview_win.lift()
        self._fade_preview(1.0)

    def _fade_preview(self, target: float, step: float=0.12):
        if not self._img_preview_win or not self._img_preview_win.winfo_exists():
            return
        try:
            cur = float(self._img_preview_win.attributes('-alpha'))
        except Exception:
            self._img_preview_win.attributes('-alpha', target)
            if target == 0.0:
                self._img_preview_win.withdraw()
            return
        if target > cur and cur >= target - step or (target < cur and cur <= target + step):
            self._img_preview_win.attributes('-alpha', target)
            if target == 0.0:
                self._img_preview_win.withdraw()
            self._img_preview_fade_job = None
            return
        cur += step if target > cur else -step
        self._img_preview_win.attributes('-alpha', cur)
        self._img_preview_fade_job = self.after(25, self._fade_preview, target, step)

    def _fetch_full_blob(self, it: ScanItem) -> Optional[bytes]:
        cached = self._blob_cache.get(it.hash)
        if cached is not None:
            try:
                self._blob_cache_order.remove(it.hash)
            except ValueError:
                pass
            self._blob_cache_order.append(it.hash)
            return cached
        conn = None
        row = None
        try:
            conn = connect_ro(self.db_path)
            cur = conn.cursor()
            cur.execute('SELECT content FROM files WHERE id=?', (it.id_bytes,))
            row = cur.fetchone()
        except Exception:
            row = None
        finally:
            try:
                conn.close()
            except Exception:
                pass
        if row is None:
            content = read_shard_bytes(self.shard_root, it.hash)
        else:
            content = row[0] if row[0] is not None else read_shard_bytes(self.shard_root, it.hash)
        if content is not None:
            self._blob_cache[it.hash] = content
            try:
                self._blob_cache_order.remove(it.hash)
            except ValueError:
                pass
            self._blob_cache_order.append(it.hash)
            while len(self._blob_cache_order) > self._blob_cache_limit:
                old_hash = self._blob_cache_order.pop(0)
                self._blob_cache.pop(old_hash, None)
        return content

    def _export_selected_full(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo('Export Blob', 'Select a row first.')
            return
        if len(items) == 1:
            self._export_one_full(items[0])
            return
        directory = filedialog.askdirectory(title='Export Full Blobs to folder')
        if not directory:
            return
        saved = 0
        for it in items:
            blob = self._fetch_full_blob(it)
            if not blob:
                continue
            ext = '.rbxh' if blob[:4] == RBXH_MAGIC else '.bin'
            path = os.path.join(directory, f'{it.hash}{ext}')
            try:
                with open(path, 'wb') as f:
                    f.write(blob)
                saved += 1
            except Exception:
                pass
        messagebox.showinfo('Export Blob', f'Exported {saved} of {len(items)} blobs to:\n{directory}')

    def _export_one_full(self, it):
        blob = self._fetch_full_blob(it)
        if not blob:
            messagebox.showerror('Export Blob', 'Unable to read blob (DB/shard).')
            return
        ext = '.rbxh' if blob[:4] == RBXH_MAGIC else '.bin'
        default_name = f'{it.hash}{ext}'
        path = filedialog.asksaveasfilename(title='Export Full Blob', defaultextension=ext, initialfile=default_name, filetypes=[('RBXH blob', '*.rbxh'), ('Binary', '*.bin'), ('All files', '*.*')])
        if not path:
            return
        try:
            with open(path, 'wb') as f:
                f.write(blob)
            messagebox.showinfo('Export Blob', f'Saved full blob:\n{path}')
        except Exception as e:
            messagebox.showerror('Export Blob', f'Failed to save file:\n{e}')

    def _export_selected_rbxm(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo('Export RBXM', 'Select a row first.')
            return
        if len(items) > 1:
            directory = filedialog.askdirectory(title='Export RBXM models to folder')
            if not directory:
                return
            saved = 0
            for it in items:
                out = self._rbxm_body(it)
                if not out:
                    continue
                ext = '.rbxm' if out[1] else '.rbxmx'
                path = os.path.join(directory, f'{it.hash}{ext}')
                try:
                    with open(path, 'wb') as f:
                        f.write(out[0])
                    saved += 1
                except Exception:
                    pass
            messagebox.showinfo('Export RBXM', f'Exported {saved} of {len(items)} models to:\n{directory}')
            return
        it = items[0]
        out = self._rbxm_body(it)
        if not out:
            return
        body, is_binary = out
        ext = '.rbxm' if is_binary else '.rbxmx'
        default_name = f'{it.hash}{ext}'
        path = filedialog.asksaveasfilename(title='Export RBXM', defaultextension=ext, initialfile=default_name, filetypes=[('Roblox model', f'*{ext}'), ('All files', '*.*')])
        if not path:
            return
        try:
            with open(path, 'wb') as f:
                f.write(body)
            messagebox.showinfo('Export RBXM', f'Saved model:\n{path}')
        except Exception as e:
            messagebox.showerror('Export RBXM', f'Failed to save file:\n{e}')

    def _export_selected_mesh_obj(self):
        items = [it for it in self._get_selected_items() if (it.kind or '').split(' ', 1)[0] == 'Mesh']
        if not items:
            messagebox.showinfo('Export as OBJ', 'Select a Mesh cache first.', parent=self)
            return
        directory = None
        if len(items) > 1:
            directory = filedialog.askdirectory(title='Export meshes as OBJ', parent=self)
            if not directory:
                return
        saved = 0
        errors = []
        for it in items:
            try:
                blob = self._fetch_full_blob(it)
                if not blob:
                    raise ValueError('cache blob could not be read')
                if blob[:4] == RBXH_MAGIC:
                    meta = parse_rbxh(blob)
                    data = _maybe_gunzip(meta.get('body') or b'', meta.get('headers') or {})
                else:
                    data = blob
                data = decompress_if_needed(data)
                base = _sanitize_filename_for_windows(os.path.splitext(it.name or it.hash)[0]) or it.hash
                if directory:
                    path = os.path.join(directory, base + '.obj')
                else:
                    path = filedialog.asksaveasfilename(title='Export Mesh as OBJ', parent=self, defaultextension='.obj', initialfile=base + '.obj', filetypes=[('Wavefront OBJ', '*.obj'), ('All files', '*.*')])
                    if not path:
                        return
                convert(data, path)
                saved += 1
                self._console_log(f'Exported Mesh as OBJ: {path}')
            except Exception as exc:
                errors.append(f'{it.name or it.hash}: {exc}')
        if errors:
            messagebox.showerror('Export as OBJ', 'Some meshes failed:\n' + '\n'.join(errors), parent=self)
        elif saved:
            messagebox.showinfo('Export as OBJ', f'Exported {saved} mesh(es).', parent=self)

    def _video_signed_query_values(self, source_url: str) -> Dict[str, str]:
        values = {}
        try:
            raw_query = urlparse(source_url or '').query
            for key, vals in parse_qs(raw_query, keep_blank_values=True).items():
                if vals:
                    values[key.lower()] = vals[0]
        except Exception:
            pass
        return values

    @staticmethod
    def _video_has_placeholders(text: str) -> bool:
        low = str(text or '').lower()
        return any((x in low for x in ('{$__token_}', '{$__token__}', '{$expires}', '{$policy}', '{$signature}', '{$key-pair-id}', '${__token_}', '${expires}', '${policy}', '${signature}', '${key-pair-id}')))

    @staticmethod
    def _extract_signed_urls_from_bytes(payload: bytes) -> List[str]:
        if not payload:
            return []
        text = payload.decode('utf-8', 'ignore')
        urls = []
        for m in re.finditer('https?://[^\\s"\\\'<>]+', text, re.I):
            u = m.group(0).rstrip(',);]}')
            low = u.lower()
            if 'rbxcdn.com' in low and any((k in low for k in ('__token_', 'signature', 'key-pair-id', 'policy', 'expires'))):
                urls.append(u)
        return list(dict.fromkeys(urls))

    def _find_video_ticket_urls(self, video_it: ScanItem, manifest: bytes) -> List[str]:
        candidates = []
        manifest_text = manifest.decode('utf-8', 'ignore')
        paths = []
        for line in manifest_text.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                paths.append(urlparse(line).path.lower())
            except Exception:
                pass
        path_tokens = set()
        for path in paths:
            for part in path.split('/'):
                if len(part) >= 5:
                    path_tokens.add(part)
        try:
            conn = connect_ro(self.db_path)
            cur = conn.cursor()
            cur.execute('SELECT id, content FROM files')
            for id_b, content in cur:
                h = id_bytes_to_hex(id_b)
                blob = content if content is not None else read_shard_bytes(self.shard_root, h)
                if not blob:
                    continue
                meta = parse_rbxh(blob)
                url = str(meta.get('url') or '')
                body = meta.get('body') or b''
                full = meta.get('full_payload') or body
                is_ticket, _ = detect_ticket(full, url)
                if not is_ticket:
                    continue
                found = []
                if url:
                    found.append(url)
                found.extend(self._extract_signed_urls_from_bytes(body))
                found.extend(self._extract_signed_urls_from_bytes(full))
                for u in found:
                    low = u.lower()
                    score = 0
                    if 'rbxcdn.com' in low:
                        score += 10
                    if any((k in low for k in ('__token_', 'signature', 'key-pair-id', 'policy', 'expires'))):
                        score += 20
                    try:
                        upath = urlparse(u).path.lower()
                        for token in path_tokens:
                            if token in upath:
                                score += 25
                    except Exception:
                        pass
                    if any((x in low for x in ('.m3u8', 'playlist', 'video'))):
                        score += 15
                    candidates.append((score, u))
        except Exception:
            pass
        finally:
            try:
                conn.close()
            except Exception:
                pass
        candidates.sort(key=lambda x: x[0], reverse=True)
        out = []
        seen = set()
        for _score, u in candidates:
            if u in seen:
                continue
            seen.add(u)
            out.append(u)
            if len(out) >= 80:
                break
        return out

    def _resolve_hls_uri(self, uri: str, base_url: str, token_values: Dict[str, str]) -> str:
        uri = str(uri or '').strip().strip('"\'')
        if not uri:
            return ''

        def repl(match):
            key = match.group(1).strip().lower()
            return token_values.get(key, match.group(0))
        uri = re.sub('\\{\\$([^}]+)\\}', repl, uri)
        uri = re.sub('\\$\\{([^}]+)\\}', repl, uri)
        uri = re.sub('\\$([A-Za-z0-9_-]+)', repl, uri)
        return urljoin(base_url, uri)

    def _download_hls_video(self, manifest: bytes, source_url: str, video_it: Optional[ScanItem]=None, timeout: int=20):
        session = urllib.request.build_opener()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) RoUtils/3.8', 'Accept': '*/*', 'Accept-Encoding': 'identity'}

        def fetch(url):
            req = urllib.request.Request(url, headers=headers)
            with session.open(req, timeout=timeout) as r:
                return (r.read(), r.geturl(), dict(r.headers.items()))
        ticket_urls = []
        if video_it is not None and self._video_has_placeholders(manifest.decode('utf-8', 'ignore')):
            ticket_urls = self._find_video_ticket_urls(video_it, manifest)
        initial_urls = []
        if source_url and (not self._video_has_placeholders(source_url)) and (source_url != '-'):
            initial_urls.append(source_url)
        initial_urls.extend(ticket_urls)

        def parse_manifest(data, base_url, token_values=None, depth=0):
            if depth > 5:
                raise RuntimeError('HLS playlist nesting is too deep.')
            token_values = dict(token_values or {})
            token_values.update(self._video_signed_query_values(base_url))
            text = data.decode('utf-8-sig', 'replace')
            lines = [x.strip() for x in text.splitlines() if x.strip()]
            if not any((x.upper().startswith('#EXTM3U') for x in lines)):
                raise RuntimeError('The cached video is not a valid HLS manifest.')
            variants = []
            pending_inf = None
            for line in lines:
                if line.upper().startswith('#EXT-X-STREAM-INF:'):
                    pending_inf = line.split(':', 1)[1]
                    continue
                if pending_inf is not None and (not line.startswith('#')):
                    bw = 0
                    res_area = 0
                    m = re.search('(?:^|,)BANDWIDTH=(\\d+)', pending_inf, re.I)
                    if m:
                        bw = int(m.group(1))
                    m = re.search('(?:^|,)RESOLUTION=(\\d+)x(\\d+)', pending_inf, re.I)
                    if m:
                        res_area = int(m.group(1)) * int(m.group(2))
                    variants.append((bw, res_area, line))
                    pending_inf = None
            if variants:
                variants.sort(key=lambda x: (x[0], x[1]), reverse=True)
                errors = []
                for _bw, _area, variant in variants:
                    uri = self._resolve_hls_uri(variant, base_url, token_values)
                    try:
                        child, child_url, child_headers = fetch(uri)
                        child_values = dict(token_values)
                        child_values.update(self._video_signed_query_values(child_url))
                        return parse_manifest(child, child_url, child_values, depth + 1)
                    except Exception as e:
                        errors.append(str(e))
                raise RuntimeError('Unable to open any HLS quality playlist: ' + (errors[-1] if errors else 'unknown error'))
            parts = []
            init_uri = None
            for line in lines:
                upper = line.upper()
                if upper.startswith('#EXT-X-KEY:'):
                    method = re.search('METHOD=([^,]+)', line, re.I)
                    if method and method.group(1).upper() != 'NONE':
                        raise RuntimeError('This HLS video is encrypted and the required key is not present in the cache.')
                    continue
                if upper.startswith('#EXT-X-MAP:'):
                    m = re.search('URI="([^"]+)"', line, re.I)
                    if m:
                        init_uri = self._resolve_hls_uri(m.group(1), base_url, token_values)
                    continue
                if not line.startswith('#'):
                    parts.append(self._resolve_hls_uri(line, base_url, token_values))
            if not parts:
                raise RuntimeError('The HLS playlist contains no media segments.')
            output = bytearray()
            if init_uri:
                init_data, _, _ = fetch(init_uri)
                output.extend(init_data)
            for n, part_url in enumerate(parts, 1):
                segment, _, _ = fetch(part_url)
                if not segment:
                    raise RuntimeError(f'HLS segment {n} was empty.')
                output.extend(segment)
            return bytes(output)
        errors = []
        for candidate in initial_urls:
            try:
                candidate_values = self._video_signed_query_values(candidate)
                resolved_candidate = self._resolve_hls_uri(candidate, candidate, candidate_values)
                data, final_url, _headers = fetch(resolved_candidate)
                if data.lstrip().startswith(b'#EXTM3U'):
                    values = dict(candidate_values)
                    values.update(self._video_signed_query_values(final_url))
                    return parse_manifest(data, final_url, values)
                cached_text = manifest.decode('utf-8', 'ignore')
                master_path = next((x.strip() for x in cached_text.splitlines() if x.strip() and (not x.lstrip().startswith('#')) and ('playlist.m3u8' in x.lower())), None)
                if master_path:
                    base = final_url if final_url.endswith('/') else final_url.rsplit('/', 1)[0] + '/'
                    playlist_url = self._resolve_hls_uri(master_path, base, values)
                    pdata, pfinal, _ = fetch(playlist_url)
                    if pdata.lstrip().startswith(b'#EXTM3U'):
                        values.update(self._video_signed_query_values(pfinal))
                        return parse_manifest(pdata, pfinal, values)
                errors.append('Ticket URL did not return an HLS playlist')
            except Exception as e:
                errors.append(str(e))
        if source_url and (not self._video_has_placeholders(manifest.decode('utf-8', 'ignore'))):
            return parse_manifest(manifest, source_url, self._video_signed_query_values(source_url))
        detail = errors[0] if errors else 'No signed ticket URL was found in the cache.'
        raise RuntimeError('Could not recover the Roblox video ticket from cache. ' + detail)

    def _export_selected_video(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo('Export Video', 'Select a row first.')
            return
        video_items = [it for it in items if it.kind.split(' ', 1)[0].lower() == 'video']
        if not video_items:
            messagebox.showerror('Export Video', 'The selected cache does not contain a detected video.')
            return

        def get_video_payload(it):
            blob = self._fetch_full_blob(it)
            if not blob:
                return (None, None)
            body, meta = self._dump_blob_body(blob)
            if not body:
                return (None, None)
            ct = str(meta.get('headers', {}).get('content-type', '') or '').lower()
            kind = str(it.kind or '').lower()
            if body[:4] == b'\x1aE\xdf\xa3' or 'webm' in kind or 'video/webm' in ct:
                ext = '.webm'
            elif len(body) >= 12 and body[4:8] == b'ftyp' or 'mp4' in kind or 'video/mp4' in ct:
                ext = '.mp4'
            elif body.lstrip().lower().startswith(b'#extm3u') or 'm3u' in kind or 'mpegurl' in ct:
                try:
                    resolved = self._download_hls_video(body, it.url, it)
                    if resolved:
                        if len(resolved) >= 12 and resolved[4:8] == b'ftyp':
                            return (resolved, '.mp4')
                        if resolved[:4] == b'\x1aE\xdf\xa3':
                            return (resolved, '.webm')
                        return (resolved, '.ts')
                except Exception:
                    ext = '.m3u8'
            elif 'mkv' in kind or 'matroska' in ct:
                ext = '.mkv'
            elif 'm4v' in kind or 'x-m4v' in ct:
                ext = '.m4v'
            elif 'mov' in kind or 'quicktime' in ct:
                ext = '.mov'
            else:
                return (None, None)
            return (body, ext)
        if len(video_items) > 1:
            directory = filedialog.askdirectory(title='Export videos to folder')
            if not directory:
                return
            saved = 0
            failed = 0
            for it in video_items:
                payload, ext = get_video_payload(it)
                if not payload:
                    failed += 1
                    continue
                name = _sanitize_filename_for_windows(it.name or it.hash) or it.hash
                path = os.path.join(directory, f'{name}_{it.hash}{ext}')
                try:
                    with open(path, 'wb') as f:
                        f.write(payload)
                    saved += 1
                except Exception:
                    failed += 1
            messagebox.showinfo('Export Video', f'Exported {saved} of {len(video_items)} video(s) to:\n{directory}' + (f'\nFailed: {failed}' if failed else ''))
            return
        it = video_items[0]
        payload, ext = get_video_payload(it)
        if not payload:
            messagebox.showerror('Export Video', 'The cached blob was detected as video, but its video payload could not be extracted.')
            return
        default_name = f'{_sanitize_filename_for_windows(it.name or it.hash) or it.hash}{ext}'
        path = filedialog.asksaveasfilename(title='Export Video', defaultextension=ext, initialfile=default_name, filetypes=[('Video', f'*{ext}'), ('All files', '*.*')])
        if not path:
            return
        try:
            with open(path, 'wb') as f:
                f.write(payload)
            messagebox.showinfo('Export Video', f'Saved video:\n{path}\n\nSize: {human_size(len(payload))}')
        except Exception as e:
            messagebox.showerror('Export Video', f'Failed to save video:\n{e}')

    def _rbxm_body(self, it):
        try:
            blob = self._fetch_full_blob(it)
            if not blob:
                return None
            meta = parse_rbxh(blob)
            body = meta.get('body') or b''
            if not body:
                return None
            body = _maybe_gunzip(body, meta.get('headers') or {})
            body = decompress_if_needed(body)
            magic = body.find(b'<roblox!')
            if magic == -1:
                magic = body.find(b'<roblox')
            if magic > 0:
                body = body[magic:]
            stripped = body.lstrip()
            if stripped.startswith(b'\xef\xbb\xbf'):
                stripped = stripped[3:].lstrip()
            if stripped.startswith(b'<roblox!'):
                return (body, True)
            if b'<roblox' in body[:4096]:
                if _write_rbxm is not None:
                    try:
                        return (write_rbxm(_xml_to_document(body)), True)
                    except Exception:
                        return (body, False)
                return (body, False)
        except Exception:
            return None
        return None

    def _export_selected_image(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo('Export Image', 'Select a row first.')
            return
        if len(items) > 1:
            directory = filedialog.askdirectory(title='Export images to folder')
            if not directory:
                return
            saved = 0
            for it in items:
                img = self._image_from_item(it)
                if not img:
                    continue
                fmt = (img.format or 'PNG').upper()
                ext = f'.{fmt.lower()}'
                path = os.path.join(directory, f'{it.hash}{ext}')
                try:
                    img.save(path)
                    saved += 1
                except Exception:
                    pass
            messagebox.showinfo('Export Image', f'Exported {saved} of {len(items)} images to:\n{directory}')
            return
        it = items[0]
        img = self._image_from_item(it)
        if not img:
            messagebox.showerror('Export Image', 'Blob does not contain a valid image.')
            return
        fmt = (img.format or 'PNG').upper()
        ext = f'.{fmt.lower()}'
        default_name = f'{it.hash}{ext}'
        path = filedialog.asksaveasfilename(title='Export Image', defaultextension=ext, initialfile=default_name, filetypes=[(f'{fmt} image', f'*{ext}'), ('All files', '*.*')])
        if not path:
            return
        try:
            img.save(path)
            messagebox.showinfo('Export Image', f'Saved image:\n{path}')
        except Exception as e:
            messagebox.showerror('Export Image', f'Failed to save file:\n{e}')

    def _image_from_item(self, it) -> Optional[Image.Image]:
        blob = self._fetch_full_blob(it)
        if not blob:
            return None
        meta = parse_rbxh(blob)
        body = meta.get('body') or b''
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
            messagebox.showinfo('No Selection', 'Select a row first.')
            return None
        it = self.items_by_iid.get(sel[0]) or self.items_by_hash.get(sel[0])
        if not it:
            messagebox.showerror('Selection Error', 'Selected row is no longer available.')
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
            raise ValueError('Empty input.')
        s = s.strip()
        if s.lower().startswith('0x'):
            s = s[2:]
        s = re.sub('[^0-9A-Fa-f]', '', s)
        if len(s) != expected_nibbles:
            raise ValueError(f'Hash must be {expected_nibbles} hex characters (got {len(s)}).')
        try:
            return bytes.fromhex(s)
        except Exception:
            raise ValueError('Invalid hex characters.')

    def _action_change_hash(self):
        it = self._get_selected_item()
        if not it:
            return
        expected_nibbles = len(it.id_bytes) * 2
        new_hash = simpledialog.askstring('Change Hash', f'Enter new {expected_nibbles}-hex hash for this blob:', initialvalue=it.hash)
        if not new_hash:
            return
        try:
            new_id_b = self._parse_new_hash(new_hash, expected_nibbles)
            new_hash_hex = new_id_b.hex()
        except Exception as e:
            messagebox.showerror('Invalid Hash', str(e))
            return
        if not messagebox.askyesno('Confirm Change Hash', f'Update DB id and rename shard?\n\nOld: {it.hash}\nNew: {new_hash_hex}'):
            return
        was_running = self._pause_scanner()
        try:
            conn = connect_rw(self.db_path)
            try:
                cur = conn.cursor()
                cur.execute('BEGIN IMMEDIATE')
                cur.execute('UPDATE files SET id=? WHERE id=?', (new_id_b, it.id_bytes))
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
                    messagebox.showwarning('Shard Rename', f'DB updated, but shard rename failed:\n{e}')
            old_hash = it.hash
            self.seen_hashes.discard(old_hash)
            self.items_by_iid.pop(old_hash, None)
            self.items_by_hash.pop(old_hash, None)
            try:
                self.tree.delete(old_hash)
            except Exception:
                pass
            it.hash, it.id_bytes = (new_hash_hex, new_id_b)
            self.seen_hashes.add(new_hash_hex)
            self.items_by_hash[new_hash_hex] = it
            self.tree.insert('', 'end', iid=new_hash_hex, values=(it.time, it.name, it.hash, human_size(it.size), it.kind, it.src))
            self.tree.selection_set(new_hash_hex)
            self._update_status()
            messagebox.showinfo('Change Hash', 'Hash updated successfully.')
        except Exception as e:
            messagebox.showerror('Change Hash', f'Failed to change hash:\n{e}')
        finally:
            self._resume_scanner(was_running)

    def _action_delete_blob(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo('Delete Blob', 'Select a row first.')
            return
        names = ', '.join((it.hash for it in items[:12])) + ('…' if len(items) > 12 else '')
        if not messagebox.askyesno('Confirm Delete', f'Delete {len(items)} blob(s) from DB and remove shard files?\n\n{names}'):
            return
        was_running = self._pause_scanner()
        deleted = 0
        try:
            for it in items:
                try:
                    conn = connect_rw(self.db_path)
                    cur = conn.cursor()
                    cur.execute('BEGIN IMMEDIATE')
                    cur.execute('DELETE FROM files WHERE id=?', (it.id_bytes,))
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
            messagebox.showinfo('Delete Blob', f'Deleted {deleted} blob(s).')
        except Exception as e:
            messagebox.showerror('Delete Blob', f'Failed to delete blob:\n{e}')
        finally:
            self._resume_scanner(was_running)

    def _action_save_hash_to_saves(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo('Save Hash', 'Select a row first.')
            return
        name = simpledialog.askstring('Save Hash', 'Name to show in Hash saves:')
        if not name:
            return
        safe_name = _sanitize_filename_for_windows(name.strip())
        if not safe_name:
            messagebox.showerror('Save Hash', 'Name cannot be empty.')
            return
        base_dir = getattr(self.replacer, 'hash_saves_dir', None)
        if not base_dir:
            messagebox.showerror('Save Hash', 'Hash saves folder not available.')
            return
        os.makedirs(base_dir, exist_ok=True)
        saved = 0
        for idx, it in enumerate(items):
            label = safe_name if len(items) == 1 else f'{safe_name}_{idx + 1}'
            filename = f'{it.hash} - {label}'
            dest = os.path.join(base_dir, filename)
            if os.path.exists(dest):
                base = filename
                i = 1
                while True:
                    cand = f'{base} ({i})'
                    cand_path = os.path.join(base_dir, cand)
                    if not os.path.exists(cand_path):
                        dest = cand_path
                        break
                    i += 1
            try:
                with open(dest, 'x'):
                    pass
            except FileExistsError:
                with open(dest, 'wb'):
                    pass
            except Exception as e:
                messagebox.showerror('Save Hash', f'Failed to save: {e}')
                return
            saved += 1
        try:
            if self.replacer.source_var.get() == 'HashSaves':
                self.replacer.refresh_view()
        except Exception:
            pass
        messagebox.showinfo('Save Hash', f'Saved {saved} hash(es).')

    def _action_save_blob_to_saves(self):
        items = self._get_selected_items()
        if not items:
            messagebox.showinfo('Save Blob', 'Select a row first.')
            return
        name = simpledialog.askstring('Save Blob', 'File name to save in File saves:')
        if not name:
            return
        safe_name = _sanitize_filename_for_windows(name.strip())
        if not safe_name:
            messagebox.showerror('Save Blob', 'Name cannot be empty.')
            return
        base_dir = getattr(self.replacer, 'file_saves_dir', None)
        if not base_dir:
            messagebox.showerror('Save Blob', 'File saves folder not available.')
            return
        os.makedirs(base_dir, exist_ok=True)
        saved = 0
        for idx, it in enumerate(items):
            blob = self._fetch_full_blob(it)
            if not blob:
                continue
            fname = safe_name if len(items) == 1 else f'{safe_name}_{idx + 1}'
            dest = os.path.join(base_dir, fname)
            if os.path.exists(dest):
                b = fname
                i = 1
                while True:
                    cand = f'{b} ({i})'
                    cand_path = os.path.join(base_dir, cand)
                    if not os.path.exists(cand_path):
                        dest = cand_path
                        break
                    i += 1
            try:
                with open(dest, 'wb') as f:
                    f.write(blob)
            except Exception as e:
                messagebox.showerror('Save Blob', f'Failed to save blob: {e}')
                return
            saved += 1
        try:
            if self.replacer.source_var.get() == 'FileSaves':
                self.replacer.refresh_view()
        except Exception:
            pass
        messagebox.showinfo('Save Blob', f'Saved {saved} blob(s).')

    def _reset_seen(self, clear_list: bool):
        self.seen_hashes.clear()
        if clear_list:
            self.tree.delete(*self.tree.get_children())
            self.items_by_iid.clear()
            self.items_by_hash.clear()
        self._update_status()

    def _sort_by(self, col_key: str, numeric: bool=False):

        def parse_size(s: str) -> float:
            s = s.strip().upper()
            try:
                if s.endswith('KB'):
                    return float(s[:-2]) * 1024
                if s.endswith('MB'):
                    return float(s[:-2]) * 1024 ** 2
                if s.endswith('GB'):
                    return float(s[:-2]) * 1024 ** 3
                if s.endswith('TB'):
                    return float(s[:-2]) * 1024 ** 4
                if s.endswith('B'):
                    return float(s[:-1])
                return float(s)
            except Exception:
                return 0.0
        items = [(self.tree.set(k, col_key), k) for k in self.tree.get_children('')]
        if col_key == 'size':
            items.sort(key=lambda t: parse_size(t[0]))
        else:
            items.sort(key=lambda t: t[0])
        if getattr(self, '_last_sort', None) == (col_key, 'asc'):
            items.reverse()
            self._last_sort = (col_key, 'desc')
        else:
            self._last_sort = (col_key, 'asc')
        for idx, (_, k) in enumerate(items):
            self.tree.move(k, '', idx)

    def _update_status(self):
        if not hasattr(self, 'status_label'):
            return
        total = len(self.items_by_hash)
        vis = len(self.tree.get_children())
        stat = 'Watching' if self.watching else 'Idle'
        self.status_label.config(text=f'Status: {stat}   Visible: {vis}   Total seen: {total}   Interval: {WATCH_INTERVAL_SEC:.1f}s')

    def _startup_setting_changed(self):
        self._save_settings()
        self._install_startup_shortcut()
        self._update_kill_routils_visibility()

    def _install_startup_shortcut(self):
        if os.name != 'nt':
            return
        startup = os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        link = os.path.join(startup, 'RoUtils.lnk')
        if not self.launch_on_startup.get():
            try:
                os.remove(link)
            except OSError:
                pass
            return
        try:
            if getattr(sys, 'frozen', False):
                target = sys.executable
                args = ''
            else:
                target = sys.executable
                args = f'"{os.path.abspath(__file__)}"'
            ps = '& { $w=New-Object -ComObject WScript.Shell; $s=$w.CreateShortcut($env:LINK); $s.TargetPath=$env:TARGET; $s.Arguments=$env:ARGS; $s.WorkingDirectory=$env:WORK; $s.Save() }'
            env = os.environ.copy()
            env.update({'LINK': link, 'TARGET': target, 'ARGS': args, 'WORK': BASE_DIR})
            subprocess.run(['powershell', '-NoProfile', '-WindowStyle', 'Hidden', '-Command', ps], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0), timeout=10)
        except Exception:
            pass

    def _start_tray(self):
        if self._tray_icon is not None or self._tray_starting or os.name != 'nt':
            return
        self._tray_starting = True

        def worker():
            try:
                self._tray_icon = _WindowsTrayIcon(icon_path=ICON_PATH, on_open=lambda: self.after(0, self._restore_from_tray), on_exit=lambda: self.after(0, self._exit_from_tray))
                self._tray_icon.run()
            except Exception:
                self._tray_icon = None
            finally:
                self._tray_starting = False
        self._tray_thread = threading.Thread(target=worker, daemon=True)
        self._tray_thread.start()

    def _hide_to_tray(self):
        self._start_tray()
        self._tray_hidden = True
        try:
            self.withdraw()
        except Exception:
            pass

    def _restore_from_tray(self):
        self._tray_hidden = False
        try:
            self.deiconify()
            self.state('normal')
            self.lift()
            self.focus_force()
        except Exception:
            pass

    def _exit_from_tray(self):
        self._tray_hidden = False
        self._on_close(force=True)

    def _on_close(self, force=False):
        if not force and self.hide_to_tray_on_close.get():
            self._save_settings()
            self._hide_to_tray()
            return
        self.watching = False
        self.stop_event.set()
        self._hotkey_stop.set()
        self._save_settings()
        try:
            if self._tray_icon:
                self._tray_icon.stop()
        except Exception:
            pass
        try:
            self.fflag_engine.close()
        except Exception:
            pass
        try:
            if isinstance(sys.stdout, _ConsoleStream):
                sys.stdout = self._console_original_stdout
        except Exception:
            pass
        self._save_console_history()
        self.destroy()

def main():
    global _ACTIVE_APP
    _install_error_hooks()
    if '--webview2' in sys.argv:
        try:
            idx = sys.argv.index('--webview2')
            url = sys.argv[idx + 1]
            title = sys.argv[idx + 2] if len(sys.argv) > idx + 2 else 'RoUtils WebView2'
            _launch_webview2(url, title)
        except Exception as e:
            try:
                messagebox.showerror('WebView2', str(e))
            except Exception:
                pass
        return
    if '--dump-caches' in sys.argv:
        try:
            helper = object.__new__(App)
            code = App._run_dump_caches_cli(helper)
        except Exception as e:
            print(f'ERROR: {e}', flush=True)
            code = 1
        input('\npress enter to close')
        raise SystemExit(code)
    try:
        app = App()
    except Exception as e:
        _report_rotools_error(type(e), e, e.__traceback__)
        return
    _ACTIVE_APP = app
    app.mainloop()
if __name__ == '__main__':
    main()
