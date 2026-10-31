import base64
import ctypes
import ctypes.wintypes
from fflag.processes import list_roblox_clients
if not hasattr(ctypes, "WINFUNCTYPE"):
    ctypes.WINFUNCTYPE = ctypes.CFUNCTYPE
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import difflib
import enum
import gzip
import hashlib
import heapq
import html
import importlib.util
import io
import json
import logging
import math
import mimetypes
import numpy as np
import os
import queue
import re
import shlex
import shutil
import sqlite3
import struct
import subprocess
import sys
import tempfile
import threading
import time
import tkinter as tk
import traceback
import urllib.error
import urllib.request
import uuid
import webbrowser
try:
    import winreg
except ImportError:
    winreg = None
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from PIL import Image, ImageTk
try:
    from pypresence import Presence as _DiscordPresence
except Exception:
    _DiscordPresence = None
from tkinter import colorchooser, filedialog, messagebox, simpledialog, ttk
from tkinter import font as tkfont
from typing import Any, Dict, Iterable, List, Optional, Tuple, TYPE_CHECKING
from urllib.parse import parse_qs, quote, urljoin, urlparse
from sober_support import _prefix_from_name, apply_sober_fflags, is_sober_process, open_path, restore_sober_fflags, set_sober_fps_cap, sober_appdata_root, sober_config_path, sober_logs_dir, sober_process_pid, sober_process_pids, sober_flatpak_running, sober_storage_paths, resolve_storage_selection, sober_is_focused, type_sober_emote
from xml.etree.ElementTree import Element, SubElement, indent, tostring
import lz4.block
try:
    import sv_ttk
except Exception:
    sv_ttk = None
try:
    import ttkbootstrap as ttkbootstrap
except Exception:
    ttkbootstrap = None
UI_TEXT = {
    'a1': 'While refreshing a item changed, so the previous selection was skipped.',
    'b1': 'The issue happend again. The duplicate was skipped',
    'c1': 'Unexpected issue occurred, Details were saved to error folder',
    'd1': 'RoUtils could not complete this action\n\nA report was saved in the error folder\n\nTry again and check the Console if it keeps happening',
    'e1': 'RoUtils ran into a problem',
    'f1': 'WebView2',
    'g1': 'WebView2 support requires pywebview.\n\nInstall pywebview with: pip install pywebview\n\n',
    'h1': 'Could not open WebView2 window:\n{p0}',
    'i1': 'Could not start WebView2 window:\n{p0}',
    'j1': 'Preview',
    'k1': '✕',
    'l1': '▶ Play',
    'm1': '',
    'n1': 'Wireframe lines',
    'o1': 'Optimize vertices',
    'p1': 'Audio',
    'q1': 'Could not open audio:\n{p0}',
    'r1': '⏸ Pause',
    's1': 'Press ▶ to play Audio',
    't1': 'Animation: no keyframes to draw a skeleton (No keyframe)',
    'u1': 'No pose position data in skeleton (keyframe count shown above)',
    'v1': 'Source:',
    'w1': 'Filter:',
    'x1': 'Create Cache',
    'y1': 'Apply',
    'z1': 'Save Hash',
    'a2': 'Save File',
    'b2': 'Delete',
    'c2': 'Rename',
    'd2': 'Create group',
    'e2': 'Delete group',
    'f2': 'Ungroup',
    'g2': 'Hash saves:',
    'h2': 'Custom Hash',
    'i2': 'Enter custom hash value (hex):',
    'j2': 'Info',
    'k2': 'Using custom hash: {p0}',
    'l2': 'Input Custom Hash',
    'm2': 'File saves:',
    'n2': 'Choose source file',
    'o2': 'Selected file:\n{p0}',
    'p2': 'Input Custom File',
    'q2': 'Enter display name:',
    'r2': 'Please choose a hash (or input a custom one).',
    's2': 'Invalid hash.',
    't2': 'Please choose a file (or input a custom one).',
    'u2': 'Selected file is missing.',
    'v2': 'Display name is required.',
    'w2': 'Failed to create cache:\n{p0}',
    'x2': 'Success',
    'y2': 'Created cache:\n{p0}',
    'z2': 'Created cache: {p0}',
    'a3': 'OK',
    'b3': 'Cancel',
    'c3': 'Loading…',
    'd3': 'No saved hashes found',
    'e3': 'No saved files found',
    'f3': 'Hash:',
    'g3': 'Name:',
    'h3': 'Error',
    'i3': 'Both Hash and Name are required.',
    'j3': 'Resulting file name is empty after sanitization.',
    'k3': 'Failed to save: {p0}',
    'l3': "Saved '{p0}'.",
    'm3': 'Saved hash file: {p0}',
    'n3': 'Choose file to save',
    'o3': 'File:',
    'p3': 'Browse…',
    'q3': 'No file selected',
    'r3': 'Please choose a file.',
    's3': 'Please enter a Name.',
    't3': 'Failed to save file: {p0}',
    'u3': "{p0}: '{p1}'.",
    'v3': '{p0}: {p1}',
    'w3': 'No database path is set in the viewer.',
    'x3': 'Select one or more cache items.',
    'y3': 'Apply File',
    'z3': 'Enter the target Roblox cache hash/asset ID:',
    'a4': 'No valid cache items found to import.',
    'b4': 'DB error:\n{p0}',
    'c4': 'Imported {p0} of {p1} blob(s).',
    'd4': 'Applied {p0}/{p1} selected cache blob(s)',
    'e4': 'Enter new name:',
    'f4': 'Rename failed: {p0}',
    'g4': 'No item selected.',
    'h4': "Are you sure you want to delete '{p0}'?",
    'i4': 'Are you sure you want to delete {p0} items?',
    'j4': 'Confirm',
    'k4': 'Failed to delete group: {p0}',
    'l4': 'Failed to delete file: {p0}',
    'm4': 'Deleted {p0} item(s).',
    'n4': 'Deleted {p0} cache item(s)',
    'o4': "Are you sure you want to delete group '{p0}'?",
    'p4': 'Are you sure you want to delete {p0} groups?',
    'q4': 'Deleted {p0} group(s).',
    'r4': 'Deleted {p0} cache group(s)',
    's4': "Remove group '{p0}' and move its files back?",
    't4': 'Remove {p0} groups and move their files back?',
    'u4': 'Failed to ungroup: {p0}',
    'v4': 'Ungrouped {p0} group(s), restored {p1} file(s).',
    'w4': 'Ungrouped {p0} group(s), restored {p1} cache file(s)',
    'x4': 'Items must share the same parent folder.',
    'y4': 'Group name:',
    'z4': 'A group with that name already exists.',
    'a5': 'Failed to create group folder: {p0}',
    'b5': "Created group '{p0}' with {p1} item(s).",
    'c5': "Created empty group '{p0}'.",
    'd5': "Created cache group '{p0}' with {p1} item(s)",
    'e5': '×',
    'f5': 'Cache',
    'g5': '◀',
    'h5': 'FFlags',
    'i5': 'Emote Manager',
    'j5': 'AI',
    'k5': 'Modifications',
    'l5': 'Configs',
    'm5': 'Subplace Joiner',
    'n5': 'Server Viewer',
    'o5': 'History',
    'p5': 'Client',
    'q5': 'Customize',
    'r5': 'Settings',
    's5': 'Plugins',
    't5': 'Release Notes',
    'u5': 'Console',
    'v5': 'Loading...',
    'w5': 'Home',
    'x5': 'RoUtils',
    'y5': 'Could not load {p0}: {p1}',
    'z5': 'FPS: Uncap',
    'a6': 'FPS: {p0}',
    'b6': 'FPS value (1-240):',
    'c6': 'Press any keyboard or mouse button:',
    'd6': 'Examples: F7, Insert, Mouse1, Mouse4, A, ;',
    'e6': 'FPS Hotkey',
    'f6': 'FPS must be a whole number from 1 to 240.',
    'g6': 'Enter FPS 1-240 and a supported key.',
    'h6': 'That key is already assigned.',
    'i6': 'Save',
    'j6': 'Clear',
    'k6': '{p0} FPS [{p1}]',
    'l6': 'Empty',
    'm6': '+',
    'n6': 'Global FFlag Hotkeys',
    'o6': '+ Add Hotkey',
    'p6': 'Edit',
    'q6': 'Remove',
    'r6': 'Close',
    's6': 'Key:',
    't6': 'FFlag:',
    'u6': 'Action:',
    'v6': 'Toggle 1 value:',
    'w6': 'Toggle 2 value:',
    'x6': 'Example: K + DebugDrawBroadPhaseAABBs + true/false toggles the value globally.',
    'y6': 'FFlag Hotkeys',
    'z6': 'Enter a supported keyboard key.',
    'a7': 'Enter an FFlag name.',
    'b7': '⌕ Search - (Ctrl + K)',
    'c7': '🔔',
    'd7': 'Notifications',
    'e7': 'Search failed: {p0}',
    'f7': 'Kill RoUtils',
    'g7': '⠿',
    'h7': 'Tab move failed: {p0}',
    'i7': 'Customize App',
    'j7': 'Choose a theme and personalize the app colors.',
    'k7': 'Appearance',
    'l7': 'Appearance colors',
    'm7': '    ',
    'n7': 'Choose…',
    'o7': 'Reset color',
    'p7': 'Apply Appearance Colors',
    'q7': 'Save Custom Theme',
    'r7': 'Topbar button colors',
    's7': 'Choose {p0} color',
    't7': 'Your custom appearance has been saved.',
    'u7': 'Choose {p0} button color',
    'v7': 'Theme update failed: {p0}',
    'w7': 'Failed to save flags:\n{p0}',
    'x7': 'R6 Animation → R15',
    'y7': 'Roblox Animation',
    'z7': 'All files',
    'a8': 'Save R15 Animation',
    'b8': 'RBXMX Animation',
    'c8': 'R6 → R15',
    'd8': 'R6 animation retargeted to R15.\n\n{p0}',
    'e8': 'Converted R6 animation to R15: {p0}',
    'f8': 'Could not convert animation:\n{p0}',
    'g8': 'Current applied caches: {p0}',
    'h8': 'Save DB',
    'i8': 'Enter a name for this CConfigs DB:',
    'j8': 'CConfigs',
    'k8': 'Failed to save DB:\n{p0}',
    'l8': "DB saved as '{p0}'.\n\nRecorded applied caches: {p1}",
    'm8': 'Upload DB',
    'n8': 'Database files',
    'o8': 'SQLite DB',
    'p8': 'CConfigs DB',
    'q8': 'Failed to upload DB:\n{p0}',
    'r8': "Uploaded '{p0}'.",
    's8': 'Select a saved DB first.',
    't8': 'Apply DB',
    'u8': "Apply '{p0}' to Roblox?\n\nThis will delete rbx-storage.db, rbx-storage.db-shm, rbx-storage.db-wal and rbx-storage.id, then install only rbx-storage.db.",
    'v8': 'Failed to apply DB.\n\n{p0}\n\nClose Roblox and try again. No force-delete was used.',
    'w8': "Applied '{p0}'.\nRecorded caches: {p1}\n\nInstalled only rbx-storage.db.",
    'x8': 'Export DB as normal .db',
    'y8': 'Failed to export DB:\n{p0}',
    'z8': 'Normal .db exported:\n{p0}',
    'a9': 'Delete DB',
    'b9': "Delete saved DB '{p0}'?",
    'c9': 'Failed to delete DB:\n{p0}',
    'd9': 'CONFIG',
    'e9': 'CREATED',
    'f9': 'APPLIED',
    'g9': 'FILE',
    'h9': 'Saved DB details',
    'i9': 'Please select a valid RobloxPlayerBeta.exe first.',
    'j9': 'Opened Roblox: {p0}',
    'k9': 'Could not open Roblox:\n{p0}',
    'l9': 'Roblox Modifications',
    'm9': 'Converters',
    'n9': 'Roblox File Converter (.rbxm / .rbxh / .rbxmx)',
    'o9': 'Mesh to OBJ',
    'p9': 'Default Mesh Changer',
    'q9': 'It allows you to change the default R6 Meshes.',
    'r9': 'Choose',
    's9': 'Open Selected Roblox',
    't9': 'Skybox Changer',
    'u9': 'Replace Roblox skybox texture files from PlatformContent\\pc\\textures\\sky.',
    'v9': 'Sounds',
    'w9': 'Replace Roblox sound files from content\\sounds.',
    'x9': 'Others',
    'y9': 'Replace additional Roblox texture and font files.',
    'z9': 'Studs (replaces plastic\nnormal.dds)',
    'a10': 'Diffuse (diffuse.dds)',
    'b10': 'Font (CustomFont.ttf)',
    'c10': 'Welcome to RoUtils',
    'd10': 'Support with me: offp001 on discord',
    'e10': 'Version: ',
    'f10': 'Checking',
    'g10': 'Downloading update…',
    'h10': 'Downloading update… {p0:.0f}%',
    'i10': 'RoUtils is Outdated',
    'j10': 'Download New Version ({p0})',
    'k10': 'Download',
    'l10': 'Later',
    'm10': 'Update {p0} download started.',
    'n10': 'Update downloaded to {p0}; launching from RoUtils folder.',
    'o10': 'Update error: {p0}',
    'p10': 'RoUtils Update',
    'q10': 'Automatic update failed:\n{p0}',
    'r10': 'Version: {p0} ({p1})',
    's10': 'Add',
    't10': 'JSON Editor',
    'u10': 'Invalid JSON:\n{p0}',
    'v10': 'Applied {p0} flags from {p1}.',
    'w10': 'Failed to apply JSON:\n{p0}',
    'x10': 'Select RobloxPlayerBeta.exe',
    'y10': 'Roblox Player',
    'z10': 'Executable',
    'a11': 'Choose RobloxPlayerBeta.exe first.',
    'b11': 'Choose replacement for {p0}',
    'c11': 'Mesh files',
    'd11': 'Failed:\n{p0}',
    'e11': 'Texture files',
    'f11': 'Skybox texture replaced: {p0}',
    'g11': 'Skybox texture deleted: {p0}',
    'h11': 'Audio files',
    'i11': 'Sound replaced: {p0}',
    'j11': 'Sound deleted: {p0}',
    'k11': 'Other file replaced: {p0}',
    'l11': 'Other file deleted: {p0}',
    'm11': 'Select Roblox Mesh',
    'n11': 'Roblox Mesh',
    'o11': 'Selected Mesh Version "{p0}"',
    'p11': 'Converting',
    'q11': 'Converted: {p0}',
    'r11': 'Conversion failed:\n{p0}',
    's11': 'Select Roblox File',
    't11': 'Roblox Files',
    'u11': 'RBXM',
    'v11': 'RBXH',
    'w11': 'RBXMX',
    'x11': 'Roblox File Converter',
    'y11': 'Please select an .rbxm, .rbxh or .rbxmx file.',
    'z11': 'Converted successfully.\n\n{p0}\nSize: {p1}',
    'a12': 'Converted Roblox file: {p0}',
    'b12': 'Game History',
    'c12': 'Refresh',
    'd12': 'Clear History',
    'e12': 'Game History.',
    'f12': 'No games recorded yet.',
    'g12': 'Copy Deeplink',
    'h12': 'Join',
    'i12': 'Could not copy deeplink:{p0}',
    'j12': 'Joined from history: {p0}',
    'k12': 'Could not launch Roblox:{p0}',
    'l12': 'Clear all saved game history?',
    'm12': 'Roblox Client',
    'n12': 'Live Roblox client information and current game details.',
    'o12': 'Client Information',
    'p12': 'Open Roblox',
    'q12': 'FPS',
    'r12': 'PID: Waiting for Roblox...',
    's12': 'Reset Hotkeys',
    't12': 'FPS Changer',
    'u12': 'Running',
    'v12': 'Not running',
    'w12': 'Search',
    'x12': 'PLACE ID',
    'y12': 'NAME',
    'z12': 'Join Selected',
    'a13': 'Search failed:\n{p0}',
    'b13': 'Could not read Roblox logs:\n{p0}',
    'c13': 'Could not detect the current Roblox server. Make sure you are inside a game, then try again.',
    'd13': "Current game's deeplink copied to clipboard.",
    'e13': 'Could not copy deeplink:\n{p0}',
    'f13': 'Joined subplace {p0}',
    'g13': 'Could not launch Roblox:\n{p0}',
    'h13': 'Paste a Roblox server deeplink',
    'i13': 'View Server',
    'j13': 'Server Information',
    'k13': '\n',
    'l13': 'Loading server...',
    'm13': 'Loading server deeplink: {p0}',
    'n13': 'Server loaded',
    'o13': 'Failed to load server',
    'p13': 'Could not load server:\n{p0}',
    'q13': 'Waiting for Roblox...',
    'r13': 'Remove Bind',
    's13': 'Add Bind',
    't13': 'Hotkey',
    'u13': 'Dance',
    'v13': 'Last hotkey: none',
    'w13': 'Hotkeys: ON',
    'x13': 'Emote Controls',
    'y13': 'Select a dance from the list first.',
    'z13': 'Press any key for {p0}',
    'a14': '{p0} is already assigned to {p1}. Choose a different key.',
    'b14': 'Binds saved',
    'c14': 'Hotkeys: {p0}',
    'd14': 'Close Controls',
    'e14': 'Choose a key...',
    'f14': '<\n{p0}',
    'g14': '>\n{p0}',
    'h14': '{p0}\n{p1}',
    'i14': 'Emote Manager - Hide: Ctrl + F3',
    'j14': 'Roblox attached  PID {p0}',
    'k14': 'Search:',
    'l14': 'TYPE',
    'm14': 'VALUE',
    'n14': 'Latest FFlags',
    'o14': 'Saved JSONs',
    'p14': 'Loading offsets…',
    'q14': 'FFLAG',
    'r14': 'OFFSET',
    's14': 'DEFAULT VALUE',
    't14': 'Apply Selected',
    'u14': 'Auto Apply: ON',
    'v14': 'Auto Apply: OFF',
    'w14': 'Apply to Roblox',
    'x14': 'Save Flags',
    'y14': 'Could not load flags',
    'z14': 'FFlag reference load failed: {p0}',
    'a15': '{p0:,} flags',
    'b15': 'Removed FFlag',
    'c15': 'FFlag name',
    'd15': 'Value:',
    'e15': 'Added FFlag {p0} = {p1}',
    'f15': 'Add Flag',
    'g15': 'Removed FFlag {p0}',
    'h15': 'Remove all flags?',
    'i15': 'Removed all FFlags',
    'j15': 'FFlag Presets',
    'k15': 'Select a preset, then choose whether to replace or add its FFlags to the current list.',
    'l15': 'FFlag Preset',
    'm15': 'Added {p0} FFlags and updated {p1} existing FFlags from {p2}.',
    'n15': 'Preset {p0}: added {p1}, updated {p2} FFlags',
    'o15': 'Applied {p0} FFlags from {p1}.',
    'p15': 'Applied FFlag preset {p0}: {p1} flags',
    'q15': 'Failed to load {p0}:\n{p1}',
    'r15': 'Add to Current FFlags',
    's15': 'No JSON presets found.',
    't15': 'Could not load presets: {p0}',
    'u15': 'Loading presets...',
    'v15': 'Copied to clipboard.',
    'w15': 'FFlag copy failed: {p0}',
    'x15': 'Import FFlags',
    'y15': 'JSON files',
    'z15': 'Imported {p0} flag(s).',
    'a16': 'Imported {p0} FFlag(s) from {p1}',
    'b16': 'Import failed:\n{p0}',
    'c16': 'Export name',
    'd16': 'Exported {p0} FFlag(s) to {p1}: {p2}',
    'e16': 'Export failed:\n{p0}',
    'f16': 'JSONs (FFlags Saves)',
    'g16': 'Choose FFlag export location',
    'h16': 'Choose...',
    'i16': 'Roblox Detected: PID {p0}',
    'j16': 'PID: {p0} selected',
    'k16': 'Roblox found, attach failed',
    'l16': 'Roblox Detected but attach failed: PID {p0}',
    'm16': 'Roblox process closed; FFlag attachment removed',
    'n16': 'FFlag conflict: duplicate names detected: ',
    'o16': 'FFlags conflict.',
    'p16': 'FFlag injection skipped: Roblox is not attached',
    'q16': 'Roblox is not attached.',
    'r16': 'Offset data is being refreshed. Apply again after it loads.',
    's16': 'Applied {p0}/{p1}',
    't16': 'FFlag {p0} apply complete: {p1}/{p2} flags applied, {p3} failed for PID {p4}',
    'u16': 'No flags were applied using {p0}. Check the current offsets and Roblox version.',
    'v16': 'Unapplied {p0} flag(s)',
    'w16': ', {p0} failed',
    'x16': 'FFlag restore complete: {p0} restored, {p1} failed',
    'y16': 'Plugin',
    'z16': 'Could not enable {p0}:\n{p1}',
    'a17': 'Could not open guide:\n{p0}',
    'b17': 'Import Python',
    'c17': 'Only install plugins you trust. Python plugins can access the same files and processes as RoUtils.',
    'd17': 'No plugins yet.\nImport a Python plugin to get started.',
    'e17': 'Documentation / development guide',
    'f17': 'Open Guide',
    'g17': 'Enable',
    'h17': 'Import RoUtils Python Plugin',
    'i17': 'Python plugin',
    'j17': 'Imported {p0}.\nEnable it from the Plugins tab to load Python code.',
    'k17': 'Could not import plugin:\n{p0}',
    'l17': 'Settings & Options',
    'm17': 'General options.',
    'n17': 'Interface Scale',
    'o17': 'DPI Scale',
    'p17': 'Window size stays the same; only the interface scales.',
    'q17': 'You Should Restart it to Apply DPI Scale',
    'r17': 'Cache Viewer',
    's17': 'Start watching for new assets on launch',
    't17': 'Auto-scroll to newest row',
    'u17': 'Hide ticket assets',
    'v17': 'Show lines (wireframe) for the Preview',
    'w17': 'Wireframe lines on',
    'x17': 'Optimize Mesh Preview Vertices (>500)',
    'y17': 'Startup',
    'z17': 'Launch on Tray',
    'a18': 'Launch on Boot',
    'b18': 'Hide to Tray when Close (F7 to Hide/Show)',
    'c18': 'Streamer Mode',
    'd18': 'Hide RoUtils from screen sharing and recording',
    'e18': 'RoUtils does not appear in screen shares. (Only you can see it.)',
    'f18': 'Updates',
    'g18': 'Auto Update',
    'h18': 'Updates RoUtils on Background',
    'i18': 'Gemini AI',
    'j18': 'Gemini API Key',
    'k18': 'Tutorial',
    'l18': 'Add Key',
    'm18': 'Database',
    'n18': 'Choose DB File…',
    'o18': 'Choose Shard Root…',
    'p18': 'Config Backup',
    'q18': 'Include CConfigs',
    'r18': 'Include Cache Dumps',
    's18': 'Export Config…',
    't18': 'Import Config…',
    'u18': 'DPI setting error: {p0}',
    'v18': 'Export RoUtils Config',
    'w18': 'RoUtils Config',
    'x18': 'ZIP archive',
    'y18': 'JSON settings',
    'z18': 'Exported RoUtils config to {p0}',
    'a19': 'Config exported successfully.',
    'b19': 'Could not export config:\n{p0}',
    'c19': 'Import RoUtils Config',
    'd19': 'Imported RoUtils config from {p0}',
    'e19': 'Config imported successfully. Restart RoUtils to apply every saved setting.',
    'f19': 'Could not import config:\n{p0}',
    'g19': 'Nothing to undo.',
    'h19': 'Undid the last FFlag change.',
    'i19': 'Restored cache {p0}.',
    'j19': 'Restored config {p0}.',
    'k19': 'Cache search:\n',
    'l19': '(no matches)',
    'm19': 'Created backup: {p0}',
    'n19': 'Restored backup: {p0}',
    'o19': '$> ',
    'p19': 'Please enter Y or N.',
    'q19': 'Do you want to dump videos? (Y)es or (N)o:',
    'r19': 'Commands:\n  cache "blob file path" "hash"  Apply a blob file to Roblox.\n  cache delete "hash"  Delete one cache by hash.\n  cache list [filter]  List visible caches.\n  cache search [text]  Search loaded caches by name, hash or type.\n  fflag "name" "value"  Add and apply one FastFlag.\n  fflag delete "name"  Remove one FastFlag.\n  fflag clear  Remove all saved FastFlags.\n  fflag list  List saved FastFlags.\n  fflag apply  Inject all saved FastFlags into Roblox.\n  fflag unapply  Restore the original FastFlag values.\n  fflag defaults  Open Default FFlag Values.\n  fflag latest  Open Latest FFlag List.\n  undo  Undo the last reversible console change.\n  history  Show saved console history from console_history.json.\n  config "name/prefix"  Apply a saved CConfig.\n  config save "name"  Save the current Roblox database as a CConfig.\n  config list  List saved CConfigs.\n  config delete "name/prefix"  Delete one saved CConfig.\n  modif meshtoobj "mesh file path"  Convert that mesh file to OBJ.\n  modif "head" "replacement mesh path" ["RobloxPlayerBeta.exe path"]  Replace R6 body mesh (head, torso, left arm, right arm, left leg, right leg).\n  join "place id"  Open a Roblox subplace.\n  viewserver "deeplink"  Load a server deeplink.\n  information  Open the live Client information.\n  theme "theme name"  Apply a saved theme.\n  theme list  List available themes.\n  watch start|stop  Start or stop cache watching.\n  fps "number"  Set and apply the FPS limit.\n  export all  Dump all caches; progress is shown in Console.\n  dump-folder  Open the folder where dumped caches are saved.\n  backup create "name"  Back up settings and File/Hash Saves.\n  backup restore "zip path"  Restore a RoUtils backup ZIP.\n  ai  Open RoUtils AI.\n  open "tab name"  Open a RoUtils tab.\n  status  Show Roblox PID, watcher and database status.\n  clear  Clear the Console.',
    's19': 'Applied FFlag {p0} = {p1}',
    't19': 'Cleared all saved FFlags',
    'u19': 'FFlag injection requested',
    'v19': 'FFlag values restored',
    'w19': 'Opened Default FFlag Values',
    'x19': 'Opened Latest FFlag List',
    'y19': "Saved current DB as config '{p0}'.",
    'z19': 'Opened subplace {p0}',
    'a20': 'Opened Client information',
    'b20': 'Themes: ',
    'c20': 'Cache watching started',
    'd20': 'Cache watching could not start: database file was not found.',
    'e20': 'Cache watching stopped',
    'f20': 'FPS limit set to {p0}',
    'g20': 'Opened dump folder: {p0}',
    'h20': 'Started full cache dump; progress is shown in Console.',
    'i20': 'Opened tab {p0}',
    'j20': 'Roblox PID: {p0}\nCache watcher: {p1}\nDatabase: {p2}',
    'k20': 'Saved history:\n',
    'l20': '(empty)',
    'm20': 'Invalid command or arguments. Type help for command descriptions.',
    'n20': 'Error: ',
    'o20': 'Applied cache {p0} from {p1}',
    'p20': 'Deleted cache {p0}',
    'q20': 'Cache not found: {p0}',
    'r20': 'Caches:\n',
    's20': '(none loaded)',
    't20': 'Deleted FFlag {p0}',
    'u20': 'FFlags:\n',
    'v20': '(none)',
    'w20': 'Configs:\n',
    'x20': 'Deleted config {p0}',
    'y20': 'Applying config {p0}',
    'z20': 'Converted mesh to {p0}',
    'a21': 'Replaced {p0}',
    'b21': 'Applied theme {p0}',
    'c21': 'ROUTILS  /  RELEASE NOTES',
    'd21': 'RoUtils Release History',
    'e21': 'Open GitHub ↗',
    'f21': 'Connecting to GitHub…',
    'g21': 'Fetching official GitHub releases…',
    'h21': 'Could not reach GitHub. Check the connection and try Refresh.',
    'i21': 'Release notes are temporarily unavailable',
    'j21': 'Open release page in browser',
    'k21': 'Preview unavailable · {p0}',
    'l21': 'No published releases were found.',
    'm21': '{p0} Releases loaded',
    'n21': '  {p0}  ',
    'o21': 'Loading image · {p0}',
    'p21': 'Open image on browser ↗',
    'q21': 'Open release ↗',
    'r21': '{p0} asset',
    's21': 's',
    't21': '+{p0} more',
    'u21': 'No published releases to show.',
    'v21': '$>',
    'w21': 'RoUtils Console ready. Type help for commands.',
    'x21': 'Please enter a Gemini API Key.',
    'y21': 'Gemini API Key added successfully.',
    'z21': 'Opened RoUtils AI',
    'a22': '✦ RoUtils AI',
    'b22': 'RoUtils AI · Powered by Gemini',
    'c22': 'MODEL',
    'd22': 'Save AI generated file',
    'e22': 'Generated file',
    'f22': 'RoUtils AI',
    'g22': 'File saved successfully.',
    'h22': 'Could not save file:\n{p0}',
    'i22': 'Download / Save as…',
    'j22': 'Copy',
    'k22': ' · {p0}',
    'l22': 'Thinking...',
    'm22': 'RoUtils AI · Thinking... {p0}s',
    'n22': 'Attach a file',
    'o22': 'Supported files',
    'p22': '📎  {p0}  ·  {p1}',
    'q22': 'Image preview · {p0} × {p1}',
    'r22': 'Preview unavailable: {p0}',
    's22': 'PDF attached · content will be sent to Gemini',
    't22': 'Add your Gemini API key in Settings before sending a message.',
    'u22': 'you are routils ai a helper inside the windows app routils made by offp001\nuse simple words and short helpful replies\nwrite like a real person and do not repeat greetings\nuse normal sentence case and do not capitalize every word\navoid full stops at the end of short messages unless using an ellipsis\nuse commas only when they help\ndo not show raw tracebacks or long technical errors to the user\n\nwhen the user only says hello hi or hey say hey need a hand with routils\ndo not bring up settings or api keys unless the user asks\nwhen they ask about settings explain the right option in simple steps\n\nuse the real features and tab names in this guide\nfflags are in the fflags tab and can be edited in the list or json editor\nuse apply to roblox when available and do not promise every flag works\ncache is used to inspect cached files with search and filters\nstart watching turns cache watching on or off\nback up cache data before changing or removing it\nconfigs can be saved imported selected applied exported or deleted\nthemes are in customize\nthe gemini api key is in settings under gemini ai\nconsole commands include help fflag list fflag apply fflag unapply config list watch start watch stop theme list status and ai\nofficial github https://github.com/offp001/routils\nofficial discord https://discord.gg/849VtrYhm2\nnever make up a feature setting result or link\nanswer general questions directly and do not add unrelated offers to help with settings\nif unsure say so and tell the user where to check',
    'v22': 'RoUtils AI · {p0}s',
    'w22': 'Send  ➤',
    'x22': 'Auto-scroll',
    'y22': 'Hide tickets',
    'z22': 'Stay on top',
    'a23': 'Show lines',
    'b23': 'Clear rbx-storage',
    'c23': 'Delete Cache Type',
    'd23': 'Start Watching',
    'e23': 'Dump Caches',
    'f23': 'Type:',
    'g23': 'TIME',
    'h23': 'HASH',
    'i23': 'SIZE',
    'j23': 'SOURCE',
    'k23': 'Export ▸ Full Blob…',
    'l23': 'Export ▸ RBXM…',
    'm23': 'Export as OBJ',
    'n23': 'Export ▸ Image…',
    'o23': 'Export ▸ Video…',
    'p23': 'Copy Hash',
    'q23': 'Save Hash…',
    'r23': 'Save Blob…',
    's23': 'Asset Description',
    't23': '▶',
    'u23': 'Delete all caches of this type:',
    'v23': 'Delete all {p0} {p1} cache(s)?\n\nThis cannot be undone.',
    'w23': 'No caches of the selected type were found.',
    'x23': 'A cache dump is already running.',
    'y23': '=== Dump Caches ===',
    'z23': 'Database: {p0}',
    'a24': 'Dump folder: {p0}',
    'b24': 'Video export enabled. Matching cached tickets may take a while.',
    'c24': 'Video dumping skipped.',
    'd24': 'Scanning cache...',
    'e24': 'ERROR: rbx-storage.db was not found.',
    'f24': 'RoUtils - Dump Caches',
    'g24': 'ERROR while scanning: {p0}',
    'h24': 'Found {p0} cache(s), including {p1} video cache(s).',
    'i24': 'Skipping {p0} video cache(s).',
    'j24': 'Failed {p0}: {p1}',
    'k24': 'Processed {p0}/{p1} | dumped={p2} failed={p3}',
    'l24': 'Finished. Dumped: {p0} | Failed: {p1}',
    'm24': 'Output: {p0}',
    'n24': 'Cleared rbx-storage: {p0} shard(s), DB={p1}',
    'o24': 'Deleted shards: {p0}\nDeleted DB: {p1}',
    'p24': 'Select rbx-storage.db',
    'q24': 'All Files',
    'r24': 'Choose DB File',
    's24': 'Could not replace Roblox storage files.\n\n{p0}\n\nClose Roblox and try again. No force-delete was used.',
    't24': 'Installed selected DB successfully.\n\nDeleted: rbx-storage.db, rbx-storage.db-shm, rbx-storage.db-wal, rbx-storage.id\nInstalled: rbx-storage.db only.',
    'u24': 'Select shard root folder (rbx-storage)',
    'v24': 'Cache watching failed: {p0}',
    'w24': 'Stop Watching',
    'x24': 'Cache scan error: {p0}',
    'y24': 'Cache view refresh was retried: {p0}',
    'z24': 'Copied',
    'a25': 'Copied {p0} hash(es) to clipboard.',
    'b25': 'Export Blob',
    'c25': 'Select a row first.',
    'd25': 'Export Full Blobs to folder',
    'e25': 'Exported {p0} of {p1} blobs to:\n{p2}',
    'f25': 'Unable to read blob (DB/shard).',
    'g25': 'Export Full Blob',
    'h25': 'RBXH blob',
    'i25': 'Binary',
    'j25': 'Saved full blob:\n{p0}',
    'k25': 'Failed to save file:\n{p0}',
    'l25': 'Export RBXM',
    'm25': 'Export RBXM models to folder',
    'n25': 'Exported {p0} of {p1} models to:\n{p2}',
    'o25': 'Roblox model',
    'p25': 'Saved model:\n{p0}',
    'q25': 'Select a Mesh cache first.',
    'r25': 'Export meshes as OBJ',
    's25': 'Export Mesh as OBJ',
    't25': 'Wavefront OBJ',
    'u25': 'Exported Mesh as OBJ: {p0}',
    'v25': 'Some meshes failed:\n',
    'w25': 'Exported {p0} mesh(es).',
    'x25': 'A video export is already running.',
    'y25': 'Export Video',
    'z25': 'The selected cache does not contain a detected video.',
    'a26': 'Export videos to folder',
    'b26': 'Video files',
    'c26': 'Exporting {p0} video(s) in the background...',
    'd26': 'Video export: {p0}/{p1} · {p2}',
    'e26': 'Video export: {p0}/{p1} · failed',
    'f26': 'Video export finished. Saved: {p0}/{p1} | Failed: {p2}',
    'g26': 'Exported {p0} of {p1} video(s) to:\n{p2}',
    'h26': 'Saved video:\n{p0}\n\nSize: {p1}',
    'i26': 'No videos could be exported.',
    'j26': 'Export Image',
    'k26': 'Export images to folder',
    'l26': 'Exported {p0} of {p1} images to:\n{p2}',
    'm26': 'Blob does not contain a valid image.',
    'n26': '{p0} image',
    'o26': 'Saved image:\n{p0}',
    'p26': 'Change Hash',
    'q26': 'Enter new {p0}-hex hash for this blob:',
    'r26': 'Invalid Hash',
    's26': 'Confirm Change Hash',
    't26': 'Update DB id and rename shard?\n\nOld: {p0}\nNew: {p1}',
    'u26': 'Shard Rename',
    'v26': 'DB updated, but shard rename failed:\n{p0}',
    'w26': 'Hash updated successfully.',
    'x26': 'Failed to change hash:\n{p0}',
    'y26': 'Delete Blob',
    'z26': 'Confirm Delete',
    'a27': 'Delete {p0} blob(s) from DB and remove shard files?\n\n{p1}',
    'b27': 'Deleted {p0} blob(s).',
    'c27': 'Failed to delete blob:\n{p0}',
    'd27': 'Name to show in Hash saves:',
    'e27': 'Name cannot be empty.',
    'f27': 'Hash saves folder not available.',
    'g27': 'Saved {p0} hash(es).',
    'h27': 'Save Blob',
    'i27': 'File name to save in File saves:',
    'j27': 'File saves folder not available.',
    'k27': 'Failed to save blob: {p0}',
    'l27': 'Saved {p0} blob(s).',
    'm27': 'Status: {p0}   Visible: {p1}   Total seen: {p2}   Interval: {p3:.1f}s',
    'n27': 'Could not update startup setting: {p0}',
    'o27': 'Could not update Start with system:\n{p0}',
    'p27': 'ERROR: {p0}',
    'q27': 'FFlag Hotkey',
    'r27': 'Search RoUtils',
    's27': 'Select a saved DB to view its details.',
    't27': 'No notifications yet. RoUtils will keep recent updates here.',
    'u27': '✦ Ask to AI',
    'v27': 'Emote hotkeys require Windows.',
    'w27': 'Change Hash…',
    'x27': 'Delete Blob',
    'y27': 'TIME',
    'z27': 'NAME',
    'a28': 'TYPE',
    'b28': 'SOURCE',
    'c28': 'Do you want to dump videos? (Y)es or (N)o: ',
    'd28': '\\nPress Enter',
    'e28': 'Hey! Need a hand with RoUtils?',
    'f28': 'Please analyze the attached file.',
    'g28': 'Open RoUtils',
    'h28': 'Exit RoUtils',
    'i28': 'RoUtils Tray',
    'j28': '3D Viewport',
    'k28': 'Choose replacement for studs.dds (target: plastic\\normal.dds)',
    'l28': 'Choose replacement for diffuse.dds',
    'm28': 'Choose replacement for CustomFont.ttf',
    'n28': 'Resolving game name...',
    'o28': 'Place ID',
    'p28': 'Job ID',
    'q28': 'File Version',
    'r28': 'CPU Usage',
    's28': 'RAM Usage',
    't28': 'Roblox Game Client not found',
    'u28': 'Paste a Roblox deeplink first.',
    'v28': 'The deeplink must contain both placeId and gameInstanceId/jobId.',
    'w28': 'Waiting for key...',
    'x28': 'Emote hotkeys are on.',
    'y28': 'Emote hotkeys are off.',
    'z28': 'Auto Apply enabled (every 15 seconds)',
    'a29': 'Auto Apply disabled',
    'b29': 'Could not create a Python plugin loader.',
    'c29': 'Python plugin must define register(app).',
    'd29': 'Backup ZIP file was not found.',
    'e29': 'Cache file or hash is invalid.',
    'f29': 'Cache hash is invalid.',
    'g29': 'FFlag was not found or is ambiguous.',
    'h29': 'Config was not found or the prefix is ambiguous.',
    'i29': 'Choose RobloxPlayerBeta.exe first or pass its path.',
    'j29': 'Theme not found or prefix is ambiguous.',
    'k29': 'Date unavailable',
    'l29': 'LATEST STABLE',
    'm29': 'No description was provided for this release.',
    'n29': 'No signed ticket URL was found in the cache.',
    'o29': 'Official Github Link: https://github.com/offp001/routils',
    'p29': 'Join Discord server: https://discord.gg/849VtrYhm2',
    'q29': 'Model present, but no parts found to render',
    'r29': 'Mesh present, but this variant isn’t supported by the converter',
    's29': 'No Keyframe data found in the selected animation.',
    't29': 'The current rbx-storage.db does not exist.',
    'v29': 'Config name cannot be empty.',
    'w29': 'Save Current DB',
    'x29': 'Export DB',
    'y29': 'Not in a game',
    'a30': 'Max Capacity',
    'b30': 'Server FPS',
    'c30': 'No usable offset list was found.',
    'd30': 'Checking...',
    'e30': 'Detecting...',
    'g30': 'Gemini 3.8 Flash',
    'h30': 'Gemini 3.7 Flash',
    'i30': 'Gemini 3.6 Flash',
    'j30': 'Gemini 3.5 Flash',
    'k30': 'Gemini 3.5 Flash-Lite',
    'l30': 'Gemini 3.1 Flash-Lite',
    'm30': 'Gemini 3.1 Pro Preview',
    'n30': 'Gemini 3 Flash Preview',
    'o30': 'Gemini 2.5 Flash',
    'p30': 'Gemini 2.5 Pro',
    'q30': 'Gemini 2.5 Flash-Lite',
    'r30': 'Previous emote',
    's30': 'Next emote',
    't30': 'Play current emote',
    'u30': 'Current emote: ',
    'v30': 'Emote error: ',
    'd31': 'Players',
    'e31': 'Ping',
    'f31': 'Status',
    'g31': 'PID',
    'h31': 'Path',
    'i31': 'Game',
    'j31': 'JOB ID',
    'k31': 'DATE / TIME',
    'y31': 'Add FFlag',
    'z31': 'Export FFlags',
    'f32': 'Release image',
    'g32': 'Ticket (signed URL)',
    'h32': 'Settings file must contain a JSON object.',
    'i32': 'DracoPy not installed. v6/v7 mesh conversion will not work.',
    'j32': 'DracoPy not available - cannot process v6/v7 meshes',
    'k32': 'Invalid mesh data: file too small',
    'l32': 'Data is not a valid RBXM/RBXMX document',
    'm32': 'Unsupported Roblox conversion target: ',
    'n32': 'XML root is not a Roblox document',
    'o32': 'RBXM deserializer is unavailable.',
    'p32': 'FPS Hotkey ',
    'q32': '+ Add',
    'r32': 'Remove All',
    's32': 'Model: ',
    't32': ' video cache(s).',
    'u32': 'LOD parsing failed: ',
    'v32': 'RBXM contains a ZSTD-compressed chunk; install zstandard to read it',
    'w32': 'Invalid RBXM header: ',
    'x32': 'No COREMESH chunk found in v6/v7 mesh',
    'y32': 'Detected mesh version: ',
    'z32': 'RBXM/RBXMX converted to RBXH blob and saved',
    'a33': 'Hotkey ',
    'b33': ': starting...',
    'c33': ' key set to ',
}
if sys.platform.startswith('linux'):
    UI_TEXT['h5'] = 'FFlag'
_TkAppBase = tk.Tk
if os.name != 'nt' and not hasattr(os, 'startfile'):
    os.startfile = open_path
UI_HOTKEY_INTERVAL_MS = 75
UI_QUICK_PANEL_INTERVAL_MS = 50
UI_QUEUE_INTERVAL_MS = 25
UI_CLIENT_INTERVAL_MS = 250
_ROUTILS_ORIGINAL_URLOPEN = urllib.request.urlopen
def _routils_is_network_error(error):
    markers = ('getaddrinfo failed', 'urlopen error', '[errno 11001]', 'name or service not known', 'temporary failure in name resolution', 'nodename nor servname provided', 'connection timed out', 'timed out', 'network is unreachable', 'connection refused', 'connection reset', 'failed to establish a new connection')
    pending = [error]
    seen = set()
    while pending:
        current = pending.pop()
        if current is None or id(current) in seen:
            continue
        seen.add(id(current))
        try:
            detail = str(current).lower()
        except Exception:
            detail = ''
        if any(marker in detail for marker in markers):
            return True
        for name in ('reason', '__cause__', '__context__'):
            try:
                nested = getattr(current, name, None)
                if nested is not None and nested is not current:
                    pending.append(nested)
            except Exception:
                pass
    return False
def _routils_urlopen(url, *args, **kwargs):
    request = url if isinstance(url, urllib.request.Request) else None
    request_data = getattr(request, 'data', None) if request is not None else (args[0] if args else kwargs.get('data'))
    request_method = getattr(request, 'method', None) if request is not None else kwargs.get('method')
    method = str(request_method or ('POST' if request_data is not None else 'GET')).upper()
    retryable = method in {'GET', 'HEAD'} and request_data is None
    attempts = 4 if retryable else 1
    transient_statuses = {408, 425, 429, 500, 502, 503, 504}
    for attempt in range(attempts):
        try:
            return _ROUTILS_ORIGINAL_URLOPEN(url, *args, **kwargs)
        except urllib.error.HTTPError as error:
            retryable_error = retryable and error.code in transient_statuses
            if not retryable_error or attempt + 1 >= attempts:
                raise
            retry_after = None
            try:
                retry_after = float(error.headers.get('Retry-After', ''))
            except (TypeError, ValueError, AttributeError):
                retry_after = None
            try:
                error.close()
            except Exception:
                pass
            delay = min(3.0, max(0.35 * (2 ** attempt), retry_after or 0.0))
            time.sleep(delay)
        except Exception as error:
            if not retryable or attempt + 1 >= attempts or not _routils_is_network_error(error):
                raise
            time.sleep(min(2.5, 0.35 * (2 ** attempt)))
UI_THEME = 'clam'
THEMES = {'Midnight': {'bg_dark': '#1b1b1c', 'bg_medium': '#252526', 'bg_light': '#3a3a3c', 'bg_hover': '#464648', 'fg': '#dcdcdc', 'accent': '#7f8cff', 'border': '#444446'}, 'Ocean': {'bg_dark': '#0f2436', 'bg_medium': '#153248', 'bg_light': '#1f425e', 'bg_hover': '#2a5474', 'fg': '#d7e6f0', 'accent': '#3aa0ff', 'border': '#28506e'}, 'Hacker': {'bg_dark': '#0a0f0a', 'bg_medium': '#0f180f', 'bg_light': '#1a2a1a', 'bg_hover': '#223522', 'fg': '#b8ffb0', 'accent': '#2fff2f', 'border': '#2a4a2a'}, 'Amethyst': {'bg_dark': '#1a1423', 'bg_medium': '#241b31', 'bg_light': '#35284a', 'bg_hover': '#453665', 'fg': '#e0d6f0', 'accent': '#b06bff', 'border': '#4a3a63'}, 'Onyx': {'bg_dark': '#101010', 'bg_medium': '#171717', 'bg_light': '#262626', 'bg_hover': '#303030', 'fg': '#cfcfcf', 'accent': '#c0c0c0', 'border': '#333333'}}
THEMES.update({'Nord': {'bg_dark': '#1e2430', 'bg_medium': '#252d3a', 'bg_light': '#303a4a', 'bg_hover': '#3a4658', 'fg': '#d8dee9', 'accent': '#88c0d0', 'border': '#414b5d'}, 'Dracula': {'bg_dark': '#282a36', 'bg_medium': '#303241', 'bg_light': '#44475a', 'bg_hover': '#565a70', 'fg': '#f8f8f2', 'accent': '#bd93f9', 'border': '#44475a'}, 'Monokai': {'bg_dark': '#272822', 'bg_medium': '#2e2f2a', 'bg_light': '#3e3d32', 'bg_hover': '#49483e', 'fg': '#f8f8f2', 'accent': '#a6e22e', 'border': '#49483e'}, 'Solarized': {'bg_dark': '#002b36', 'bg_medium': '#073642', 'bg_light': '#586e75', 'bg_hover': '#657b83', 'fg': '#eee8d5', 'accent': '#2aa198', 'border': '#586e75'}, 'Rose Pine': {'bg_dark': '#191724', 'bg_medium': '#1f1d2e', 'bg_light': '#26233a', 'bg_hover': '#403d52', 'fg': '#e0def4', 'accent': '#ebbcba', 'border': '#403d52'}, 'Catppuccin': {'bg_dark': '#1e1e2e', 'bg_medium': '#313244', 'bg_light': '#45475a', 'bg_hover': '#585b70', 'fg': '#cdd6f4', 'accent': '#cba6f7', 'border': '#45475a'}, 'Gruvbox': {'bg_dark': '#282828', 'bg_medium': '#3c3836', 'bg_light': '#504945', 'bg_hover': '#665c54', 'fg': '#ebdbb2', 'accent': '#fabd2f', 'border': '#504945'}, 'Tokyo Night': {'bg_dark': '#16161e', 'bg_medium': '#1f2335', 'bg_light': '#292e42', 'bg_hover': '#3b4261', 'fg': '#c0caf5', 'accent': '#7aa2f7', 'border': '#3b4261'}, 'Synthwave': {'bg_dark': '#241b2f', 'bg_medium': '#30233d', 'bg_light': '#45304f', 'bg_hover': '#5a3e64', 'fg': '#f5d7fe', 'accent': '#ff7edb', 'border': '#5a3e64'}, 'Forest': {'bg_dark': '#102018', 'bg_medium': '#183025', 'bg_light': '#254638', 'bg_hover': '#315a48', 'fg': '#d8f3dc', 'accent': '#74c69d', 'border': '#315a48'}, 'Ruby': {'bg_dark': '#241417', 'bg_medium': '#351b20', 'bg_light': '#4a252d', 'bg_hover': '#63323d', 'fg': '#f7dfe3', 'accent': '#ff6b81', 'border': '#63323d'}, 'Amber': {'bg_dark': '#211a0e', 'bg_medium': '#33270f', 'bg_light': '#4a3815', 'bg_hover': '#61491d', 'fg': '#fff0c2', 'accent': '#ffb84d', 'border': '#61491d'}, 'Arctic': {'bg_dark': '#17212b', 'bg_medium': '#21303d', 'bg_light': '#304554', 'bg_hover': '#405b6d', 'fg': '#e7f5ff', 'accent': '#66c7ff', 'border': '#405b6d'}, 'Lavender': {'bg_dark': '#211d2b', 'bg_medium': '#2d263b', 'bg_light': '#3c3350', 'bg_hover': '#514466', 'fg': '#eee7ff', 'accent': '#c4a7ff', 'border': '#514466'}, 'Coffee': {'bg_dark': '#211915', 'bg_medium': '#30231d', 'bg_light': '#45332a', 'bg_hover': '#5b4437', 'fg': '#f1dfd0', 'accent': '#d69e78', 'border': '#5b4437'}, 'Slate': {'bg_dark': '#181c20', 'bg_medium': '#232a30', 'bg_light': '#313a42', 'bg_hover': '#414c56', 'fg': '#d9e1e8', 'accent': '#8ab4c7', 'border': '#414c56'}, 'Cyber': {'bg_dark': '#080b12', 'bg_medium': '#101522', 'bg_light': '#182033', 'bg_hover': '#26334d', 'fg': '#d9f7ff', 'accent': '#00e5ff', 'border': '#26334d'}, 'Sunset': {'bg_dark': '#241516', 'bg_medium': '#35201e', 'bg_light': '#4a2b27', 'bg_hover': '#633b35', 'fg': '#ffe4d6', 'accent': '#ff8a65', 'border': '#633b35'}, 'Mint': {'bg_dark': '#10211e', 'bg_medium': '#17312c', 'bg_light': '#24473f', 'bg_hover': '#315d52', 'fg': '#dcfff5', 'accent': '#62e6c8', 'border': '#315d52'}, 'Deep Blue': {'bg_dark': '#0b1424', 'bg_medium': '#10213a', 'bg_light': '#193153', 'bg_hover': '#24446f', 'fg': '#dcecff', 'accent': '#5ca9ff', 'border': '#24446f'}, 'Obsidian': {'bg_dark': '#111318', 'bg_medium': '#1a1d24', 'bg_light': '#292e38', 'bg_hover': '#363d49', 'fg': '#e6e9ef', 'accent': '#8ab4f8', 'border': '#3b4351'}, 'Aurora': {'bg_dark': '#101820', 'bg_medium': '#172633', 'bg_light': '#234353', 'bg_hover': '#2d5c6d', 'fg': '#e4fbff', 'accent': '#66e3d4', 'border': '#376878'}, 'Plasma': {'bg_dark': '#160d24', 'bg_medium': '#24143b', 'bg_light': '#38215b', 'bg_hover': '#4d2b79', 'fg': '#f4eaff', 'accent': '#e38cff', 'border': '#5d3d83'}, 'Ember': {'bg_dark': '#20110d', 'bg_medium': '#321a14', 'bg_light': '#4a2820', 'bg_hover': '#63362a', 'fg': '#ffede5', 'accent': '#ff9d5c', 'border': '#714334'}, 'Meadow': {'bg_dark': '#0d1b16', 'bg_medium': '#142a20', 'bg_light': '#204433', 'bg_hover': '#2c5c43', 'fg': '#e4ffef', 'accent': '#8be28b', 'border': '#38694e'}})
THEME_NAMES = list(THEMES.keys())
DEFAULT_THEME = 'Midnight'
DISCORD_APPLICATION_ID = '1563194941868351519'
DISCORD_RPC_INTERVAL = 1.0
_CURRENT_PALETTE = dict(THEMES[DEFAULT_THEME])
STARTUP_GEOMETRY = '1400x800'
PANED_TOP_FRACTION = 0.45
HPANED_LEFT_FRACTION = 0.73
VIEWER_MIN_WIDTH = 480
REPLACER_MIN_WIDTH = 220
WATCH_INTERVAL_SEC = 0.5
BASE_DIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
if os.name == 'nt':
    _LOCAL_APPDATA = os.environ.get('LOCALAPPDATA') or os.path.expanduser('~')
    DATA_DIR = os.path.join(_LOCAL_APPDATA, 'RoUtils')
else:
    _XDG_DATA_HOME = os.environ.get('XDG_DATA_HOME') or os.path.join(os.path.expanduser('~'), '.local', 'share')
    DATA_DIR = os.path.join(_XDG_DATA_HOME, 'RoUtils')
os.makedirs(DATA_DIR, exist_ok=True)
HTTP_CACHE_DIR = os.path.join(DATA_DIR, 'http_cache')
FFLAG_REFERENCE_CACHE_PATH = os.path.join(DATA_DIR, 'fflag_reference_cache.json')
HTTP_RESPONSE_CACHE_MAX_BYTES = 6 * 1024 * 1024
_HTTP_RESPONSE_CACHE = {}
_HTTP_RESPONSE_CACHE_LOCK = threading.RLock()
def _routils_request_cache_ttl(request):
    if request.get_method().upper() != 'GET' or getattr(request, 'data', None) is not None:
        return 0
    url = str(request.full_url)
    if url == RELEASES_API_URL:
        return 600
    if url == 'https://api.github.com/repos/offp001/routils/releases/latest':
        return 300
    if url == WEBVIEW2_URL_DEFAULTS:
        return 900
    if url in (_get_latest_offsets_webview_url(), 'https://raw.githubusercontent.com/4anti/Roblox-Fastflag-Manager/main/data/FFlags.hpp'):
        return 900
    if url == GITHUB_PRESETS_API:
        return 600
    if 'games.roblox.com/v1/games/' in url and '/servers/Public?' in url:
        return 5
    if ('apis.roblox.com/universes/v1/places/' in url or 'develop.roblox.com/v1/places/' in url or 'games.roblox.com/v1/games/multiget-place-details?' in url or 'games.roblox.com/v1/games?universeIds=' in url or 'develop.roblox.com/v1/universes/' in url):
        return 1800
    return 0
def _routils_http_cache_path(url):
    return os.path.join(HTTP_CACHE_DIR, hashlib.sha256(str(url).encode('utf-8', 'replace')).hexdigest() + '.json')
def _routils_load_http_cache(url, ttl, allow_stale=False):
    now = time.time()
    key = str(url)
    with _HTTP_RESPONSE_CACHE_LOCK:
        item = _HTTP_RESPONSE_CACHE.get(key)
        if item and (allow_stale or now - item[0] <= ttl):
            return item[1], item[2]
    path = _routils_http_cache_path(key)
    try:
        with open(path, 'r', encoding='utf-8') as source:
            record = json.load(source)
        saved_at = float(record.get('saved_at', 0))
        if record.get('url') != key or saved_at <= 0 or (not allow_stale and now - saved_at > ttl):
            return None
        body = base64.b64decode(record.get('body', ''), validate=True)
        response_headers = record.get('headers') if isinstance(record.get('headers'), dict) else {}
        if len(body) > HTTP_RESPONSE_CACHE_MAX_BYTES:
            return None
        with _HTTP_RESPONSE_CACHE_LOCK:
            _HTTP_RESPONSE_CACHE[key] = (saved_at, body, response_headers)
        return body, response_headers
    except Exception:
        return None
class _RoUtilsCachedResponse(io.BytesIO):
    def __init__(self, body, url, headers=None):
        super().__init__(body)
        self.url = str(url)
        self.headers = dict(headers or {})
        self.status = 200
        self.code = 200
        self.reason = 'OK'
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
        return False
    def getcode(self):
        return self.status
    def geturl(self):
        return self.url
    def info(self):
        return self.headers
class _RoUtilsResponseCacheCapture:
    def __init__(self, response, url, ttl):
        self._response = response
        self._url = str(url)
        self._ttl = int(ttl)
        self._body = bytearray()
        self._saved = False
        try:
            self._expected = int(response.headers.get('Content-Length', 0) or 0)
        except Exception:
            self._expected = 0
    def __getattr__(self, name):
        return getattr(self._response, name)
    def __enter__(self):
        try:
            enter = getattr(self._response, '__enter__', None)
            if callable(enter):
                enter()
        except Exception:
            pass
        return self
    def __exit__(self, exc_type, exc_value, exc_traceback):
        exit_method = getattr(self._response, '__exit__', None)
        if callable(exit_method):
            return exit_method(exc_type, exc_value, exc_traceback)
        try:
            self._response.close()
        except Exception:
            pass
        return False
    def read(self, size=-1):
        chunk = self._response.read(size)
        if not chunk or self._saved:
            return chunk
        self._body.extend(chunk)
        if len(self._body) > HTTP_RESPONSE_CACHE_MAX_BYTES:
            self._body.clear()
            self._saved = True
            return chunk
        try:
            headers = dict(self._response.headers.items())
        except Exception:
            headers = {}
        complete = size is None or size < 0 or (self._expected > 0 and len(self._body) >= self._expected) or (size > 0 and len(chunk) < size)
        if complete:
            self._saved = True
            try:
                body = bytes(self._body)
                saved_at = time.time()
                with _HTTP_RESPONSE_CACHE_LOCK:
                    _HTTP_RESPONSE_CACHE[self._url] = (saved_at, body, headers)
                os.makedirs(HTTP_CACHE_DIR, exist_ok=True)
                path = _routils_http_cache_path(self._url)
                temporary = path + '.tmp'
                with open(temporary, 'w', encoding='utf-8') as output:
                    json.dump({'url': self._url, 'saved_at': saved_at, 'headers': headers, 'body': base64.b64encode(body).decode('ascii')}, output, separators=(',', ':'))
                os.replace(temporary, path)
            except Exception:
                pass
        return chunk
SPLASH_DIR = os.path.join(DATA_DIR, 'src')
SPLASH_IMAGE_PATH = os.path.join(SPLASH_DIR, 'routils.png')
SPLASH_IMAGE_URL = 'https://raw.githubusercontent.com/offp001/routils/refs/heads/main/src/routils.png'
APP_VERSION = '5.2.6'
RELEASES_URL = 'https://github.com/offp001/routils/releases'
RELEASES_API_URL = 'https://api.github.com/repos/offp001/routils/releases?per_page=30'
def _routils_request(url, timeout=10, headers=None, data=None, method=None, cache_bypass=False):
    request_headers = {'User-Agent': f'RoUtils/{APP_VERSION}', 'Accept': 'application/json, */*'}
    if headers:
        request_headers.update(headers)
    request = urllib.request.Request(url, data=data, headers=request_headers, method=method)
    try:
        ttl = _routils_request_cache_ttl(request)
    except Exception:
        ttl = 0
    if ttl and not cache_bypass:
        try:
            cached = _routils_load_http_cache(request.full_url, ttl)
            if cached is not None:
                body, cached_headers = cached
                return _RoUtilsCachedResponse(body, request.full_url, cached_headers)
        except Exception:
            pass
    response = _routils_urlopen(request, timeout=timeout)
    if ttl:
        return _RoUtilsResponseCacheCapture(response, request.full_url, ttl)
    return response
HISTORY_PATH = os.path.join(DATA_DIR, 'history.json')
FFLAG_HISTORY_PATH = os.path.join(DATA_DIR, 'fflag_history.json')
SETTINGS_PATH = os.path.join(DATA_DIR, 'routils_settings.json')
ERROR_REPORT_DIR = os.path.join(DATA_DIR, 'errors')
_ACTIVE_APP = None
_ERROR_REPORTING = False
def _routils_darken_color(color, amount=0.2):
    try:
        value = str(color).lstrip('#')
        if len(value) == 3:
            value = ''.join(char * 2 for char in value)
        if len(value) != 6:
            return color
        channels = [int(value[index:index + 2], 16) for index in (0, 2, 4)]
        factor = max(0.0, min(1.0, 1.0 - float(amount)))
        return '#%02x%02x%02x' % tuple(round(channel * factor) for channel in channels)
    except Exception:
        return color
def _ensure_splash_image_file():
    os.makedirs(SPLASH_DIR, exist_ok=True)
    if os.path.isfile(SPLASH_IMAGE_PATH):
        try:
            with Image.open(SPLASH_IMAGE_PATH) as source:
                source.verify()
            return True
        except Exception:
            try:
                os.remove(SPLASH_IMAGE_PATH)
            except Exception:
                pass
    temporary = SPLASH_IMAGE_PATH + '.download'
    try:
        with _routils_request(SPLASH_IMAGE_URL, timeout=12) as response:
            data = response.read(8 * 1024 * 1024 + 1)
        if not data or len(data) > 8 * 1024 * 1024:
            return False
        with Image.open(io.BytesIO(data)) as source:
            source.verify()
        with open(temporary, 'wb') as output:
            output.write(data)
        os.replace(temporary, SPLASH_IMAGE_PATH)
        return True
    except Exception:
        try:
            if os.path.exists(temporary):
                os.remove(temporary)
        except Exception:
            pass
        return False
_NOTIFICATION_HISTORY_PATH = os.path.join(DATA_DIR, 'notifications.json')
_NOTIFICATION_HISTORY = []
_NOTIFICATION_HISTORY_LOCK = threading.Lock()
_ERROR_DEDUPE = {}
def _load_notification_history():
    global _NOTIFICATION_HISTORY
    try:
        with open(_NOTIFICATION_HISTORY_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            _NOTIFICATION_HISTORY = [x for x in data if isinstance(x, dict)][-200:]
    except Exception:
        _NOTIFICATION_HISTORY = []
def _save_notification_history():
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        temporary = _NOTIFICATION_HISTORY_PATH + '.tmp'
        with open(temporary, 'w', encoding='utf-8') as f:
            json.dump(_NOTIFICATION_HISTORY[-200:], f, ensure_ascii=False, indent=2)
        os.replace(temporary, _NOTIFICATION_HISTORY_PATH)
    except Exception:
        pass
def _record_notification(title, message, kind='info'):
    entry = {'time': datetime.now().strftime('%H:%M:%S'), 'date': datetime.now().strftime('%Y-%m-%d'), 'title': _routils_visible_text(str(title)), 'message': _routils_visible_text(str(message)), 'kind': str(kind)}
    with _NOTIFICATION_HISTORY_LOCK:
        _NOTIFICATION_HISTORY.append(entry)
        del _NOTIFICATION_HISTORY[:-200]
        _save_notification_history()
    try:
        app = _ACTIVE_APP
        if app is not None and app.winfo_exists():
            app.after(0, app._refresh_notification_center)
    except Exception:
        pass
    return entry
_load_notification_history()
def _report_rotools_error(exc_type, exc_value, exc_tb, app=None):
    global _ERROR_REPORTING
    if _ERROR_REPORTING:
        return
    short = str(exc_value).strip().splitlines()[0] if str(exc_value).strip() else exc_type.__name__
    target = app or _ACTIVE_APP
    if isinstance(exc_value, tk.TclError) and re.search(r"Item .+ not found", short, re.IGNORECASE):
        try:
            if target is not None:
                target._console_log(UI_TEXT['a1'])
        except Exception:
            pass
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
        signature = f'{exc_type.__name__}:{short}'
        now = time.monotonic()
        previous = _ERROR_DEDUPE.get(signature, 0)
        _ERROR_DEDUPE[signature] = now
        if now - previous < 5:
            if target is not None:
                try:
                    target._console_log(UI_TEXT['b1'])
                except Exception:
                    pass
            return
        if target is not None:
            try:
                target._console_log(UI_TEXT['c1'])
            except Exception:
                pass
        message = UI_TEXT['d1']
        try:
            if target is not None and target.winfo_exists():
                target.after(0, lambda: messagebox.showerror(UI_TEXT['e1'], message, parent=target))
            else:
                messagebox.showerror(UI_TEXT['e1'], message)
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
log = logging.getLogger(__name__)
MAGIC_HEADER = b'<roblox!\x89\xff\r\n\x1a\n'
FILE_HEADER_SIZE = 32
ZSTD_MAGIC = b'(\xb5/\xfd'
def _decompress_chunk(raw: bytes, uncompressed_size: int) -> bytes:
    if raw.startswith(ZSTD_MAGIC):
        try:
            import zstandard
        except ImportError as exc:
            msg = UI_TEXT['v32']
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
            msg = f"{UI_TEXT['w32']}{magic!r}"
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
try:
    import DracoPy
    DRACO_AVAILABLE = True
except ImportError:
    DRACO_AVAILABLE = False
    log_buffer.log('Mesh', UI_TEXT['i32'])
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
                log_buffer.log('Mesh', f"{UI_TEXT['u32']}{e}")
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
        log_buffer.log('Mesh', UI_TEXT['j32'])
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
            log_buffer.log('Mesh', UI_TEXT['x32'])
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
                    log_buffer.log('Mesh', f"{UI_TEXT['u32']}{e}")
            if max_faces < len(faces):
                faces = faces[:max_faces]
            v_lines = [f"v {fix_float(f'{v.px:.6f}')} {fix_float(f'{v.py:.6f}')} {fix_float(f'{v.pz:.6f}')} {fix_float(f'{v.r / 255.0:.6f}')} {fix_float(f'{v.g / 255.0:.6f}')} {fix_float(f'{v.b / 255.0:.6f}')}" for v in verts]
            n_lines = [f"vn {fix_float(f'{v.nx:.6f}')} {fix_float(f'{v.ny:.6f}')} {fix_float(f'{v.nz:.6f}')}" for v in verts]
            t_lines = [f"vt {fix_float(f'{v.tu:.6f}')} {fix_float(f'{v.tv:.6f}')} 0.0" for v in verts]
            f_lines = [f'f {f.a}/{f.a}/{f.a} {f.b}/{f.b}/{f.b} {f.c}/{f.c}/{f.c}' for f in faces]
            return write_obj_data(v_lines, n_lines, t_lines, f_lines)
        except Exception as e:
            log_buffer.log('Mesh', f'DracoPy decoding error: {e}')
            traceback.print_exc()
            return None
    except Exception as e:
        log_buffer.log('Mesh', f'Error processing v6/v7 mesh: {e}')
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
        log_buffer.log('Mesh', UI_TEXT['k32'])
        return None
    if data.startswith(b'\x1f\x8b'):
        try:
            data = gzip.decompress(data)
        except Exception as e:
            log_buffer.log('Mesh', f'Failed to decompress gzip mesh data: {e}')
            return None
    header = _mesh_header(data)
    log_buffer.log('Mesh', f"{UI_TEXT['y32']}{header}")
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
        raise ValueError(UI_TEXT['l32'])
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
    raise ValueError(f"{UI_TEXT['m32']}{target_ext}")
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
        raise ValueError(UI_TEXT['n32'])
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
    use_external_theme = False
    if ttkbootstrap is not None:
        try:
            bootstrap_style = getattr(root, '_routils_bootstrap_style', None)
            if bootstrap_style is None:
                try:
                    bootstrap_style = ttkbootstrap.Style(master=root, theme='darkly')
                except TypeError:
                    bootstrap_style = ttkbootstrap.Style(theme='darkly')
                root._routils_bootstrap_style = bootstrap_style
            else:
                bootstrap_style.theme_use('darkly')
            style = ttk.Style(root)
            use_external_theme = True
        except Exception:
            use_external_theme = False
    if not use_external_theme:
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
        tkfont.nametofont('TkDefaultFont').configure(family='Segoe UI', size=10)
        tkfont.nametofont('TkTextFont').configure(family='Consolas', size=10)
        tkfont.nametofont('TkFixedFont').configure(family='Consolas', size=10)
        tkfont.nametofont('TkMenuFont').configure(family='Segoe UI', size=10)
        tkfont.nametofont('TkHeadingFont').configure(family='Segoe UI', size=10, weight='bold')
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
    style.configure('TLabel', background=bg_dark, foreground=fg_white, font=('Segoe UI', 10))
    style.configure('TLabelframe', background=bg_dark, foreground=fg_white, bordercolor=border)
    style.configure('TLabelframe.Label', background=bg_dark, foreground=fg_white, padding=(4, 0))
    _ui_scale = max(0.5, min(2.0, float(getattr(root, '_dpi_scale', 1.0))))
    _btn_pad = (max(2, int(6 * _ui_scale)), max(2, int(5 * _ui_scale)))
    _ctrl_pad = max(2, int(3 * _ui_scale))
    _check_pad = (max(2, int(4 * _ui_scale)), max(1, int(2 * _ui_scale)))
    _small_font = max(8, int(round(9 * _ui_scale)))
    _label_font = max(9, int(round(10 * _ui_scale)))
    style.configure('TButton', background=bg_light, foreground=fg_white, bordercolor=border, focusthickness=0, padding=_btn_pad, relief='flat', font=('Segoe UI', _small_font, 'bold'))
    style.map('TButton', background=[('pressed', accent), ('active', bg_hover), ('disabled', bg_medium)], foreground=[('disabled', '#6f6f6f')], bordercolor=[('active', accent)])
    style.configure('TCheckbutton', background=bg_dark, foreground=fg_white, padding=_check_pad, font=('Segoe UI', _small_font))
    style.map('TCheckbutton', background=[('active', bg_dark)], foreground=[('active', fg_white)])
    style.configure('primary.TCheckbutton', background=bg_dark, foreground=fg_white, padding=_check_pad, font=('Segoe UI', _small_font))
    style.map('primary.TCheckbutton', background=[('active', bg_dark)], foreground=[('disabled', '#6f6f6f'), ('active', fg_white)])
    style.configure('TRadiobutton', background=bg_dark, foreground=fg_white, padding=_check_pad, font=('Segoe UI', _small_font))
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
        if isinstance(widget, tk.Toplevel):
            theme_toplevel(widget)
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
    if os.name == 'nt':
        local = os.environ.get('LOCALAPPDATA') or os.path.expanduser('~')
        roblox_dir = os.path.join(local, 'Roblox')
        return (os.path.join(roblox_dir, 'rbx-storage.db'), os.path.join(roblox_dir, 'rbx-storage'))
    return sober_storage_paths()
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
ICON_PATH = os.path.join(_BUNDLE_DIR, 'routils.ico' if os.name == 'nt' else 'routils_rpc.png')
RPC_LOGO_PATH = os.path.join(DATA_DIR, 'routils_rpc.png')
def _ensure_discord_rpc_logo():
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        if os.path.isfile(RPC_LOGO_PATH):
            return RPC_LOGO_PATH
        for source in (os.path.join(_BUNDLE_DIR, 'routils_rpc.png'), os.path.join(BASE_DIR, 'routils_rpc.png')):
            if os.path.isfile(source):
                shutil.copy2(source, RPC_LOGO_PATH)
                return RPC_LOGO_PATH
    except Exception:
        pass
    return RPC_LOGO_PATH
_ensure_discord_rpc_logo()
WEBVIEW2_URL_DEFAULTS = 'https://raw.githubusercontent.com/MaximumADHD/Roblox-FFlag-Tracker/refs/heads/main/PCDesktopClient.json'
WEBVIEW2_URL_OFFSETS_ROOT = 'https://offsets.imtheo.lol/'
WEBVIEW2_URL_OFFSETS_TEMPLATE = 'https://offsets.imtheo.lol/{version}/fflags.hpp'
GITHUB_PRESETS_API = 'https://api.github.com/repos/offp001/routils/contents/routils_linux/src/presets?ref=main'
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
        user32.AppendMenuW(menu, self.MF_STRING, self.ID_OPEN, UI_TEXT['g28'])
        user32.AppendMenuW(menu, self.MF_STRING, self.ID_EXIT, UI_TEXT['h28'])
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
        self.hwnd = user32.CreateWindowExW(0, self._class_name, UI_TEXT['i28'], 0, 0, 0, 0, 0, 0, 0, hinstance, None)
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
        messagebox.showerror(UI_TEXT['f1'], UI_TEXT['g1'] + str(e))
        return
    try:
        webview.create_window(title, url=url, width=1200, height=800, min_size=(700, 500), text_select=True)
        webview.start(gui='gtk' if sys.platform.startswith('linux') else 'edgechromium', debug=False)
    except Exception as e:
        try:
            messagebox.showerror(UI_TEXT['f1'], UI_TEXT['h1'].format(p0=e))
        except Exception:
            pass
def _get_latest_offsets_webview_url() -> str:
    return 'https://imtheo.lol/Offsets/FFlags.hpp'
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
        messagebox.showerror(UI_TEXT['f1'], UI_TEXT['i1'].format(p0=e))
def _normalize_fflag_json(data):
    flags = []
    if isinstance(data, dict):
        for n, v in data.items():
            raw_name = str(n).strip()
            prefix = _prefix_from_name(raw_name)
            item = {'name': fflag_strip_prefix(raw_name), 'value': str(v).lower() if isinstance(v, bool) else str(v), 'type': fflag_infer_type(v)}
            if prefix:
                item['prefix'] = prefix
            flags.append(item)
    elif isinstance(data, list):
        for x in data:
            if isinstance(x, dict) and x.get('name') is not None:
                raw_name = str(x['name']).strip()
                prefix = _prefix_from_name(raw_name) or str(x.get('prefix', '') or '')
                v = x.get('value', '')
                item = {'name': fflag_strip_prefix(raw_name), 'value': str(v).lower() if isinstance(v, bool) else str(v), 'type': x.get('type') or fflag_infer_type(v)}
                if prefix in FFLAG_PREFIXES:
                    item['prefix'] = prefix
                flags.append(item)
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
        return (True, UI_TEXT['g32'])
    n = len(payload) - (4 if payload[:4] == RBXH_MAGIC else 0)
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
    end = min(len(body), 131072)
    i = body.find(b'RIFF', 0, end)
    while i != -1 and i + 12 <= end:
        if body[i + 8:i + 12] == b'WEBP':
            return ('WEBP', i)
        i = body.find(b'RIFF', i + 1, end)
    sigs = [(b'\x89PNG\r\n\x1a\n', 'PNG'), (b'\xff\xd8\xff', 'JPEG'), (b'GIF8', 'GIF'), (b'DDS ', 'DDS'), (b'BM', 'BMP')]
    for sig, lbl in sigs:
        j = body.find(sig, 0, end)
        if j != -1:
            return (lbl, j)
    return ('', -1)
def _is_ogg_at(scan: bytes, j: int, end_limit=None) -> bool:
    limit = min(len(scan), int(end_limit)) if end_limit is not None else len(scan)
    if j < 0 or j + 27 > limit:
        return False
    if scan[j:j + 4] != b'OggS':
        return False
    if scan[j + 4] != 0:
        return False
    tail = scan[j:min(j + 4096, limit)]
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
    end = min(len(body), 131072)
    i = body.find(b'RIFF', 0, end)
    while i != -1 and i + 12 <= end:
        if body[i + 8:i + 12] == b'WAVE':
            return ('WAV', i)
        i = body.find(b'RIFF', i + 1, end)
    j = body.find(b'OggS', 0, end)
    if j != -1 and _is_ogg_at(body, j, end):
        return ('OGG', j)
    off = _find_mp3_two_frames(body)
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
    end = min(len(body), 131072)
    i1 = body.find(KTX1_MAGIC, 0, end)
    if i1 != -1:
        return ('Texture', _label_ktx1(body, i1))
    i2 = body.find(KTX2_MAGIC, 0, end)
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
    if payload.find(b'DRACO', 0, min(len(payload), 4096)) != -1 or payload.find(b'MESH', 0, min(len(payload), 16)) != -1:
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
    end = min(len(body), 262144)
    i = body.find(b'{', 0, end)
    if i != -1:
        try:
            return body[i:min(i + 8192, len(body))].decode('utf-8', 'ignore')
        except Exception:
            pass
    body_unz = _maybe_gunzip(body, headers)
    if body_unz is not body:
        end_unz = min(len(body_unz), 262144)
        j = body_unz.find(b'{', 0, end_unz)
        if j != -1:
            try:
                return body_unz[j:min(j + 8192, len(body_unz))].decode('utf-8', 'ignore')
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
_ROBLOX_TAG_RE = re.compile(b'<roblox', re.IGNORECASE)
_ANIMATION_MARKER_RE = re.compile(b'keyframesequence|animationclip', re.IGNORECASE)
def _leading_ws_offset(data: bytes) -> int:
    if not data or data[0] not in (32, 9, 10, 11, 12, 13):
        return 0
    position = 0
    length = len(data)
    while position < length and data[position] in (32, 9, 10, 11, 12, 13):
        position += 1
    return position
def detect_rbxm_binary(body: bytes) -> int:
    p = body.find(_RBXM_BIN_MAGIC, 0, min(len(body), _RBXM_SCAN_LIMIT))
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
        raw_start = _leading_ws_offset(raw)
        if raw.startswith(b'<roblox!', raw_start):
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
        elif raw.find(b'<roblox', 0, min(len(raw), 4096)) != -1:
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
        body_start = _leading_ws_offset(body)
        if body.startswith(b'<roblox!', body_start):
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
        elif body.find(b'<roblox', 0, min(len(body), 4096)) != -1:
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
    ct = _content_type(headers)
    is_decal_url = bool(url and ('tr.rbxcdn.com' in url.lower() or '/image/' in url.lower() or '/thumbnail/' in url.lower()))
    if body.startswith(KTX1_MAGIC):
        return ('Texture', _label_ktx1(body, 0), False)
    if body.startswith(KTX2_MAGIC):
        return ('Texture', _label_ktx2(body, 0), False)
    if body[:8] == b'\x89PNG\r\n\x1a\n':
        return ('Decal' if is_decal_url else 'Image', 'PNG', False)
    if body[:3] == b'GIF':
        return ('Decal' if is_decal_url else 'Image', 'GIF', False)
    if body[:2] == b'\xff\xd8':
        return ('Decal' if is_decal_url else 'Image', 'JPEG', False)
    if len(body) >= 12 and body[:4] == b'RIFF' and body[8:12] == b'WEBP':
        return ('Decal' if is_decal_url else 'Image', 'WEBP', False)
    if body[:4] == b'OTTO':
        return ('Font', 'OTF', False)
    if body[:4] == b'ttcf':
        return ('Font', 'TTC', False)
    if body[:4] == b'wOFF':
        return ('Font', 'WOFF', False)
    if body[:4] == b'wOF2':
        return ('Font', 'WOFF2', False)
    if body[:4] == b'\x00\x01\x00\x00':
        return ('Font', 'TTF', False)
    if body[:3] == b'ID3':
        return ('Sound', 'MP3', False)
    if len(body) >= 12 and body[:4] == b'RIFF' and body[8:12] == b'WAVE':
        return ('Sound', 'WAV', False)
    if _is_ogg_at(body, 0, min(len(body), 131072)):
        return ('Sound', 'OGG', False)
    if body[:4] == b'\x1aE\xdf\xa3':
        return ('Video', 'WebM', False)
    if len(body) >= 12 and body[4:8] == b'ftyp':
        return ('Video', 'MP4', False)
    if body.find(b'DRACO', 0, min(len(body), 4096)) != -1 or body.find(b'MESH', 0, min(len(body), 16)) != -1:
        m_cat, m_lbl = detect_mesh_kind(body)
        if m_cat:
            return (m_cat, m_lbl, False)
    if ct.startswith('font/'):
        f_cat, f_lbl = detect_font_kind(body, ct)
        if f_cat:
            return (f_cat, f_lbl, False)
    if ct.startswith('video/') and not body[:256].lstrip().lower().startswith(b'#extm3u'):
        subtype = ct.split('/', 1)[1].upper()
        if subtype in ('X-MATROSKA', 'MATROSKA'):
            subtype = 'WEBM'
        elif subtype in ('MP4', 'X-M4V'):
            subtype = 'MP4'
        elif subtype in ('M3U8', 'X-MPEGURL', 'VND.APPLE.MPEGURL'):
            subtype = 'M3U8'
        return ('Video', subtype, False)
    if body[:256].lstrip().lower().startswith(b'#extm3u'):
        return ('Video', 'M3U', False)
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
    scan_end = min(len(body), 131072)
    if _ROBLOX_TAG_RE.search(body, 0, scan_end):
        rcat, rlbl = _classify_rbxm_asset(body)
        if rcat:
            return (rcat, rlbl, False)
        if _ANIMATION_MARKER_RE.search(body, 0, scan_end):
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
    conn = sqlite3.connect(uri, uri=True, timeout=0.5, isolation_level=None)
    try:
        conn.execute('PRAGMA query_only=ON')
        conn.execute('PRAGMA cache_size=-32768')
        conn.execute('PRAGMA mmap_size=268435456')
    except sqlite3.Error:
        pass
    return conn
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
    size_text: str = ''
    search_text: str = field(repr=False, default='')
def scan_db_once(db_path: str, shard_root: str, seen: set, max_rows: Optional[int]=None, on_batch=None, batch_size: int=800) -> List[ScanItem]:
    out: List[ScanItem] = []
    try:
        conn = connect_ro(db_path)
    except Exception:
        return out
    try:
        cur = conn.cursor()
        content_cur = conn.cursor()
        row_count = 0
        ids_only = False
        if seen:
            try:
                row_count = int(conn.execute('SELECT COUNT(*) FROM files').fetchone()[0] or 0)
                ids_only = row_count > 0 and len(seen) >= int(row_count * 0.82)
            except Exception:
                ids_only = False
        cur.arraysize = 512
        cur.execute('SELECT id FROM files' if ids_only else 'SELECT id, content FROM files')
        cnt = 0
        scan_time = now_hms()
        for row in cur:
            cnt += 1
            if max_rows and cnt > max_rows:
                break
            id_b = row[0]
            content = None if ids_only else row[1]
            h = id_bytes_to_hex(id_b)
            if h in seen:
                continue
            if ids_only:
                try:
                    content_cur.execute('SELECT content FROM files WHERE id = ?', (id_b,))
                    content_row = content_cur.fetchone()
                    content = content_row[0] if content_row else None
                except sqlite3.Error:
                    content = None
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
            kind = f"{cat}{(' (' + lbl + ')' if lbl else '')}"
            if cnt & 255 == 0:
                scan_time = now_hms()
            size_text = human_size(size)
            search_text = ' '.join((scan_time, name, h, size_text, kind, 'inline' if content is not None else 'shard')).lower()
            item = ScanItem(time=scan_time, hash=h, size=size, kind=kind, src='inline' if content is not None else 'shard', url=url or '-', wrapped=bool(meta.get('wrapped', False)), header_text=meta.get('header_text'), content_type=_content_type(headers), is_ticket=is_ticket, name=name, id_bytes=id_b, size_text=size_text, search_text=search_text)
            out.append(item)
            seen.add(h)
            if on_batch is not None and len(out) >= max(1, int(batch_size)):
                on_batch(out)
                out = []
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
        text = re.sub('[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]', '', text)
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
            pname = pname_elem.text or ''
            cf_d = {}
            for comp in cf_elem:
                cf_d[comp.tag] = comp.text
            pos = _cf_position(cf_d)
            poses[pname] = {'pos': pos, 'cf': cf_d}
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
            if child.class_name in ('Pose', 'NumberPose'):
                name = child.properties.get('Name')
                cf = child.properties.get('CFrame')
                pos = _cf_position(cf)
                if name:
                    out[name] = {'pos': pos, 'cf': cf}
            _collect_poses(child, out)
    keyframes: List[Keyframe] = []
    for kf in sorted((i for i in instances.values() if i.class_name == 'Keyframe'), key=lambda i: _safe_number(i.properties.get('Time', 0.0))):
        poses: Dict[str, Dict] = {}
        _collect_poses(kf, poses)
        cf = kf.properties.get('CFrame')
        if not poses:
            poses['__frame__'] = {'pos': _cf_position(cf), 'cf': cf}
        keyframes.append(Keyframe(_safe_number(kf.properties.get('Time', 0.0)), poses))
    if not keyframes and _RbxmDeserializer is not None:
        def _props(d: dict) -> dict:
            out = {}
            for k, v in d.items():
                nm = k.name if hasattr(k, 'name') else str(k)
                out[nm] = v.value if hasattr(v, 'value') else v
            return out
        def _collect(node, out: dict):
            for child in node.children:
                if child.class_name in ('Pose', 'NumberPose'):
                    p = _props(child.properties)
                    name = p.get('Name')
                    if name:
                        out[name] = {'pos': _cf_position(p.get('CFrame')), 'cf': p.get('CFrame')}
                _collect(child, out)
        try:
            doc = _RbxmDeserializer().deserialize(data)
        except Exception:
            doc = None
        if doc is not None:
            for kf in sorted((i for i in doc.instances.values() if i.class_name == 'Keyframe'), key=lambda i: _safe_number(_props(i.properties).get('Time', 0.0))):
                p = _props(kf.properties)
                poses: Dict[str, Dict] = {}
                _collect(kf, poses)
                if not poses:
                    poses['__frame__'] = {'pos': _cf_position(p.get('CFrame')), 'cf': p.get('CFrame')}
                keyframes.append(Keyframe(_safe_number(p.get('Time', 0.0)), poses))
            keyframes.sort(key=lambda k: k.time)
    return keyframes
def parse_animation(data: bytes) -> List[Keyframe]:
    if not data:
        return []
    try:
        if b'CurveAnimation' in data:
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
    stripped = raw.lstrip(b'\xef\xbb\xbf \t\r\n')
    if stripped.startswith(b'<roblox!'):
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
    _b64 = base64
    _struct = struct
    TICKS = 14400.0
    bone_curves: Dict[str, dict] = {}
    def _empty_bc():
        return {'px': [], 'py': [], 'pz': [], 'rx': [], 'ry': [], 'rz': []}
    def _vat(raw_b: bytes):
        if len(raw_b) < 8:
            return []
        _, n = _struct.unpack_from('<II', raw_b)
        if not n:
            return []
        off_t = 8 + n * 14
        if off_t + 8 + n * 4 > len(raw_b):
            return []
        _, sn = _struct.unpack_from('<II', raw_b, off_t)
        out = []
        for i in range(min(n, sn)):
            v = _struct.unpack_from('<f', raw_b, 8 + i * 14 + 2)[0]
            tk = _struct.unpack_from('<I', raw_b, off_t + 8 + i * 4)[0]
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
    if anim_data.lstrip().startswith(b'<roblox!'):
        try:
            if _RbxmDeserializer is None:
                return []
            tree = _RbxmDeserializer().deserialize(_decompress_document(anim_data))
        except Exception:
            return []
        def _prop(inst, key):
            for k, v in inst.properties.items():
                pk = k.name if hasattr(k, 'name') else str(k)
                if pk == key:
                    return v.value if hasattr(v, 'value') else v
            return None
        def _vat_rbxm(inst):
            for k, v in inst.properties.items():
                pk = k.name if hasattr(k, 'name') else str(k)
                if pk == 'ValuesAndTimes':
                    raw = v.value if hasattr(v, 'value') else v
                    if raw:
                        rb = raw.encode('latin-1') if isinstance(raw, str) else bytes(raw)
                        return _vat(rb)
            return []
        def _walk_rbxm(inst):
            nonlocal bone_curves
            if inst.class_name == 'Folder':
                name = _prop(inst, 'Name') or ''
                if name:
                    bc = _empty_bc()
                    for child in inst.children:
                        ccls = child.class_name
                        if ccls == 'Vector3Curve':
                            for fc in child.children:
                                if fc.class_name != 'FloatCurve':
                                    continue
                                axis = (_prop(fc, 'Name') or '').upper()
                                tv = _vat_rbxm(fc)
                                if axis == 'X':
                                    bc['px'] = tv
                                elif axis == 'Y':
                                    bc['py'] = tv
                                elif axis == 'Z':
                                    bc['pz'] = tv
                        elif ccls == 'EulerRotationCurve':
                            for fc in child.children:
                                if fc.class_name != 'FloatCurve':
                                    continue
                                axis = (_prop(fc, 'Name') or '').upper()
                                tv = _vat_rbxm(fc)
                                if axis == 'X':
                                    bc['rx'] = tv
                                elif axis == 'Y':
                                    bc['ry'] = tv
                                elif axis == 'Z':
                                    bc['rz'] = tv
                        elif ccls == 'Folder':
                            _walk_rbxm(child)
                    if any((bc[k] for k in bc)):
                        bone_curves[name] = bc
            elif inst.class_name == 'CurveAnimation':
                for child in inst.children:
                    _walk_rbxm(child)
        for root_inst in getattr(tree, 'roots', []):
            _walk_rbxm(root_inst)
    else:
        try:
            text = anim_data.decode('utf-8-sig', errors='replace')
            text = re.sub('[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]', '', text)
            root = ET.fromstring(text)
        except Exception:
            return []
        def _vat_xml(fc_item):
            for bs in fc_item.iter('BinaryString'):
                if bs.get('name') == 'ValuesAndTimes' and bs.text:
                    try:
                        return _vat(_b64.b64decode(bs.text.strip()))
                    except Exception:
                        pass
            return []
        def _walk_xml(item):
            nonlocal bone_curves
            cls = item.get('class', '')
            if cls == 'Folder':
                props = item.find('Properties')
                name = ''
                if props is not None:
                    ne = props.find("string[@name='Name']")
                    if ne is not None:
                        name = ne.text or ''
                if name:
                    bc = _empty_bc()
                    for child in item:
                        ccls = child.get('class', '')
                        if ccls == 'Vector3Curve':
                            for fc in child:
                                if fc.get('class') != 'FloatCurve':
                                    continue
                                fcp = fc.find('Properties')
                                if fcp is None:
                                    continue
                                ae = fcp.find("string[@name='Name']")
                                axis = (ae.text or '').upper() if ae is not None else ''
                                bc['px' if axis == 'X' else 'py' if axis == 'Y' else 'pz' if axis == 'Z' else axis.lower()] = _vat_xml(fc)
                        elif ccls == 'EulerRotationCurve':
                            for fc in child:
                                if fc.get('class') != 'FloatCurve':
                                    continue
                                fcp = fc.find('Properties')
                                if fcp is None:
                                    continue
                                ae = fcp.find("string[@name='Name']")
                                axis = (ae.text or '').upper() if ae is not None else ''
                                bc['rx' if axis == 'X' else 'ry' if axis == 'Y' else 'rz' if axis == 'Z' else axis.lower()] = _vat_xml(fc)
                        elif ccls == 'Folder':
                            _walk_xml(child)
                    if any((bc[k] for k in bc)):
                        bone_curves[name] = bc
            elif cls == 'CurveAnimation':
                for child in item:
                    _walk_xml(child)
        for item in root.iter('Item'):
            if item.get('class') == 'CurveAnimation':
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
            poses[name] = {'pos': (_lerp(bc['px'], t), _lerp(bc['py'], t), _lerp(bc['pz'], t)), 'rot': (_lerp(bc['rx'], t), _lerp(bc['ry'], t), _lerp(bc['rz'], t))}
        keys.append(Keyframe(t, poses))
    return keys
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
            raise RuntimeError(UI_TEXT['o32'])
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
        raise ValueError(UI_TEXT['s29'])
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
        return ([], UI_TEXT['q29'])
    return (parts, f"{UI_TEXT['s32']}{len(parts)} parts")
class Viewport3DPanel(ttk.Frame):
    def __init__(self, master, title=UI_TEXT['j28']):
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
        self.mesh_info: str = ''
        self._mesh_bounds_cache = None
        self._resize_preview_mode = False
        self._resize_quiet_until = 0.0
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
        self.header.pack(fill='x', padx=4, pady=(3, 1))
        ttk.Label(self.header, text=UI_TEXT['j1'], font=('Segoe UI Semibold', 9)).pack(side='left')
        self.btn_close = ttk.Button(self.header, text=UI_TEXT['k1'], width=3, command=self.hide)
        self.btn_close.pack(side='right', padx=(4, 0))
        self.btn_play = ttk.Button(self.header, text=UI_TEXT['l1'], width=7, command=self.toggle_play, style='Preview.Play.TButton')
        try:
            ttk.Style(self).configure('Preview.Play.TButton', padding=(5, 2), font=('Segoe UI', 8))
        except Exception:
            pass
        self.btn_play.pack(side='right', padx=(4, 0), pady=0)
        self.controls = ttk.Frame(self)
        self.controls.pack(fill='x', padx=4, pady=(2, 2), side='top')
        self.controls.columnconfigure(0, weight=0)
        self.controls.columnconfigure(1, weight=1)
        self.controls.columnconfigure(2, weight=1)
        self.canvas = tk.Canvas(self, bg='#18181a', highlightthickness=0, height=150)
        self.canvas.pack(fill='both', expand=True, padx=4, pady=2)
        self.lbl_mode = ttk.Label(self.controls, text=UI_TEXT['m1'])
        self._model_controls_visible = False
        self.lbl_mode.grid(row=0, column=0, sticky='w', padx=3, pady=1)
        self.chk_wireframe = ttk.Checkbutton(self.controls, text=UI_TEXT['n1'], variable=self.show_wireframe, command=self.draw_frame)
        self.chk_wireframe.grid(row=0, column=1, sticky='w', padx=3, pady=1)
        self.chk_optimize = ttk.Checkbutton(self.controls, text=UI_TEXT['o1'], variable=self.reduce_polys, command=self.draw_frame)
        self.chk_optimize.grid(row=0, column=2, sticky='w', padx=3, pady=1)
        self.controls.bind('<Configure>', self._layout_controls, add='+')
        self.canvas.bind('<Configure>', self._on_canvas_configure, add='+')
        self._resize_draw_job = None
        self._controls_narrow = None
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
    def _layout_controls(self, event=None):
        width = event.width if event is not None else self.controls.winfo_width()
        if not getattr(self, '_model_controls_visible', False):
            return
        narrow = width < 520
        if narrow == self._controls_narrow:
            return
        try:
            if getattr(self.winfo_toplevel(), '_resize_active', False):
                self._controls_layout_pending = True
                return
        except Exception:
            pass
        self._controls_narrow = narrow
        if narrow:
            self.lbl_mode.grid_configure(row=0, column=0, columnspan=2, sticky='w', padx=3)
            self.chk_wireframe.grid_configure(row=1, column=0, columnspan=2, sticky='w', padx=3)
            self.chk_optimize.grid_configure(row=2, column=0, columnspan=2, sticky='w', padx=3)
        else:
            self.lbl_mode.grid_configure(row=0, column=0, sticky='w', padx=3)
            self.chk_wireframe.grid_configure(row=0, column=1, sticky='w', padx=3)
            self.chk_optimize.grid_configure(row=0, column=2, sticky='w', padx=3)
    def _on_canvas_configure(self, _event=None):
        self._resize_preview_mode = True
        self._resize_quiet_until = time.monotonic() + 0.48
        try:
            root = self.winfo_toplevel()
            if getattr(root, '_resize_active', False) or getattr(root, '_native_resize_in_progress', False):
                self._resize_draw_pending = True
                if self._resize_draw_job is not None:
                    try:
                        self.after_cancel(self._resize_draw_job)
                    except Exception:
                        pass
                    self._resize_draw_job = None
                return
        except Exception:
            pass
        if self._resize_draw_job is not None:
            try:
                self.after_cancel(self._resize_draw_job)
            except Exception:
                pass
        self._resize_draw_job = self.after(500, self._redraw_after_resize)
    def _redraw_after_resize(self):
        self._resize_draw_job = None
        try:
            root = self.winfo_toplevel()
            if getattr(root, '_resize_active', False) or getattr(root, '_native_resize_in_progress', False):
                self._resize_draw_pending = True
                return
        except Exception:
            pass
        self._resize_draw_pending = False
        self._resize_preview_mode = False
        self._resize_quiet_until = 0.0
        if not self.is_playing:
            self.draw_frame()
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
    def set_asset_data_from_temp(self, temp_file_path: str, is_anim=False, is_mesh=False, is_model=False, is_audio=False):
        self.keyframes = []
        self.mesh_vertices = []
        self.mesh_faces = []
        self._mesh_bounds_cache = None
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
        if is_anim:
            self.keyframes = parse_animation(data)
            self.mesh_info = f'{len(self.keyframes)} keyframes'
        elif is_mesh:
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
        _tf = tempfile
        self.audio_path = os.path.join(_tf.gettempdir(), f'routils_preview_{hashlib.sha256(payload).hexdigest()[:16]}.{ext}')
        try:
            with open(self.audio_path, 'wb') as f:
                f.write(payload)
        except Exception as e:
            self.audio_path = None
            self.mesh_info = f'Audio present, but could not write temp file ({e})'
            return
        try:
            stamp = datetime.now().strftime('%H:%M:%S')
        except Exception:
            stamp = ''
        self.mesh_info = f'Audio: {fmt} · {len(payload):,} bytes · {stamp} (▶ plays with system audio player)'
    def _toggle_audio_play(self):
        if not self.audio_path or not os.path.isfile(self.audio_path):
            return
        try:
            os.startfile(self.audio_path)
        except Exception as e:
            messagebox.showerror(UI_TEXT['p1'], UI_TEXT['q1'].format(p0=e))
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
            self.mesh_info = UI_TEXT['r29']
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
        self._mesh_bounds_cache = None
        self.mesh_info = f'Vertices: {len(verts):,} · Faces: {len(faces):,}'
    def show(self, is_anim=True, mode_label='Mesh'):
        self.lbl_mode.config(text=str(mode_label))
        if str(mode_label).lower().startswith('audio'):
            self.lbl_mode.grid_remove()
        else:
            self.lbl_mode.grid()
        model_preview = bool((self.mesh_vertices and self.mesh_faces) or self.model_parts)
        self._model_controls_visible = model_preview
        if model_preview:
            self.chk_wireframe.grid()
            self.chk_optimize.grid()
        else:
            self.chk_wireframe.grid_remove()
            self.chk_optimize.grid_remove()
        if self.is_own_host:
            self.pack(fill='both', expand=True)
        else:
            self.pack(fill='x', padx=8, pady=4)
        self.canvas.focus_set()
        self.is_playing = False
        playable = bool(self.keyframes) or bool(self.audio_path and os.path.isfile(self.audio_path))
        self.btn_play.config(text=UI_TEXT['l1'], state='normal' if playable else 'disabled', width=8)
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
        if not self.keyframes:
            self.is_playing = False
            self.btn_play.config(text=UI_TEXT['l1'], state='disabled', width=8)
            return
        self.is_playing = not self.is_playing
        self.btn_play.config(text=UI_TEXT['r1'] if self.is_playing else UI_TEXT['l1'])
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
        if not self.winfo_ismapped() or not self.is_playing or not self.keyframes:
            self.anim_job = None
            if not self.keyframes:
                self.is_playing = False
                try:
                    self.btn_play.config(text=UI_TEXT['l1'], state='disabled', width=8)
                except Exception:
                    pass
            return
        try:
            canvas_size = (self.canvas.winfo_width(), self.canvas.winfo_height())
            if canvas_size != getattr(self, '_animation_canvas_size', None):
                self._animation_canvas_size = canvas_size
                self._resize_preview_mode = True
                self._resize_quiet_until = time.monotonic() + 0.48
            if self._resize_preview_mode or time.monotonic() < getattr(self, '_resize_quiet_until', 0.0) or getattr(self.winfo_toplevel(), '_resize_active', False):
                self.anim_job = self.after(90, self._animate_loop)
                return
        except Exception:
            pass
        self.anim_time += 0.03
        self.draw_frame()
        self.anim_job = self.after(33, self._animate_loop)
    def draw_frame(self):
        self.canvas.delete('all')
        w = self.canvas.winfo_width() or 300
        h = self.canvas.winfo_height() or 220
        if self.mesh_vertices and self.mesh_faces:
            self._draw_mesh(w, h)
            if self.mesh_info:
                self.canvas.create_text(w / 2, 8, text=self.mesh_info, anchor='n', justify='center', width=max(80, w - 24), fill='#8ad0ff', font=('Consolas', 8))
            return
        if self.model_parts:
            self._draw_model(w, h)
            if self.mesh_info:
                self.canvas.create_text(w / 2, 8, text=self.mesh_info, anchor='n', justify='center', width=max(80, w - 24), fill='#8ad0ff', font=('Consolas', 8))
            return
        if self.keyframes:
            self._draw_skeleton(w, h)
        elif self.audio_path and self.mesh_info:
            self.canvas.create_text(w / 2, h / 2, text=self.mesh_info, fill='#8ad0ff', font=('Segoe UI', 10))
            self.canvas.create_text(w / 2, h / 2 + 26, text=UI_TEXT['s1'], fill='#c8c8c8', font=('Segoe UI', 9))
        else:
            self.canvas.create_text(w / 2, h / 2, text=UI_TEXT['t1'], fill='#007acc', font=('Segoe UI', 10))
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
        preview = bool(self._resize_preview_mode or getattr(self.winfo_toplevel(), '_resize_active', False))
        render_parts = self.model_parts
        if preview and len(render_parts) > 48:
            stride = max(1, (len(render_parts) + 47) // 48)
            render_parts = render_parts[::stride][:48]
        ax, ay = (self.angle_x, self.angle_y)
        cx, cy = (w / 2 + self.pan_x, h / 2 + self.pan_y)
        base = max(40.0, min(w, h) / 3) * self.zoom
        all_pos = [part['pos'] for part in self.model_parts]
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
        for part in render_parts:
            pos = part['pos']
            sx, sy, sz = part['size']
            sx = sx or 1.0
            sy = sy or 1.0
            sz = sz or 1.0
            depth_pts = []
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
        if not preview:
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
    def _draw_skeleton(self, w, h):
        n = len(self.keyframes)
        idx = int(self.anim_time * 30.0) % n if self.is_playing and n else 0
        kf = self.keyframes[idx]
        t = kf.time
        cx, cy = (w / 2 + self.pan_x, h / 2 + self.pan_y + 10)
        scale = max(0.05, min(w, h) / 4.0) * self.zoom
        default_r6 = {'Head': (0, 3.1, 0), 'Torso': (0, 1.8, 0), 'Left Arm': (-1.5, 1.8, 0), 'Right Arm': (1.5, 1.8, 0), 'Left Leg': (-0.55, 0.0, 0), 'Right Leg': (0.55, 0.0, 0)}
        default_r15 = {'Head': (0, 3.2, 0), 'UpperTorso': (0, 2.25, 0), 'LowerTorso': (0, 1.55, 0), 'LeftUpperArm': (-0.8, 2.25, 0), 'LeftLowerArm': (-1.35, 1.75, 0), 'LeftHand': (-1.65, 1.35, 0), 'RightUpperArm': (0.8, 2.25, 0), 'RightLowerArm': (1.35, 1.75, 0), 'RightHand': (1.65, 1.35, 0), 'LeftUpperLeg': (-0.45, 0.9, 0), 'LeftLowerLeg': (-0.45, 0.15, 0), 'LeftFoot': (-0.45, -0.55, 0), 'RightUpperLeg': (0.45, 0.9, 0), 'RightLowerLeg': (0.45, 0.15, 0), 'RightFoot': (0.45, -0.55, 0)}
        points = {}
        has_geo = False
        for name, pdata in kf.pose_by_part_name.items():
            pos = pdata.get('pos')
            if pos and any((abs(float(v)) > 1e-05 for v in pos)):
                points[name] = self._project_point(pos, cx, cy, scale)
                has_geo = True
            else:
                fallback = default_r15.get(name) or default_r6.get(name)
                if fallback:
                    points[name] = self._project_point(fallback, cx, cy, scale)
        bone_pts = set()
        for a, b in self.BONES:
            if a in points and b in points:
                self.canvas.create_line(points[a][0], points[a][1], points[b][0], points[b][1], fill='#9aa0a6', width=3)
                bone_pts.add(a)
                bone_pts.add(b)
        for name, (px, py) in points.items():
            fill = '#ffd54f' if name in bone_pts else '#90a4ae'
            self.canvas.create_oval(px - 4, py - 4, px + 4, py + 4, fill=fill, outline='')
        info = f'Animation: {n} keyframes @ t={t:.2f}s | joints: {len(points)}'
        self.canvas.create_text(w / 2, 8, text=info, anchor='n', justify='center', width=max(80, w - 24), fill='#8ad0ff', font=('Consolas', 8))
        if not has_geo:
            self.canvas.create_text(w / 2, h / 2, text=UI_TEXT['u1'], fill='#78909c', font=('Segoe UI', 9))
    def _draw_mesh(self, w, h):
        verts = self.mesh_vertices
        if not verts:
            return
        preview = bool(self._resize_preview_mode or getattr(self.winfo_toplevel(), '_resize_active', False))
        faces = self.mesh_faces
        if preview:
            max_faces = 48
        elif self.reduce_polys.get() and len(verts) > 500 and len(faces) > 128:
            max_faces = 128
        else:
            max_faces = len(faces)
        if max_faces > 0 and len(faces) > max_faces:
            stride = max(1, (len(faces) + max_faces - 1) // max_faces)
            faces = faces[::stride][:max_faces]
        if not faces:
            return
        try:
            if self._mesh_bounds_cache is None:
                mins = [float('inf'), float('inf'), float('inf')]
                maxs = [float('-inf'), float('-inf'), float('-inf')]
                for vertex in verts:
                    for axis in range(3):
                        value = float(vertex[axis])
                        if value < mins[axis]:
                            mins[axis] = value
                        if value > maxs[axis]:
                            maxs[axis] = value
                self._mesh_bounds_cache = (tuple(mins), tuple(maxs))
            mins, maxs = self._mesh_bounds_cache
        except Exception:
            mins = tuple(min(float(v[i]) for v in verts) for i in range(3))
            maxs = tuple(max(float(v[i]) for v in verts) for i in range(3))
        ax, ay = (self.angle_x, self.angle_y)
        cx, cy = (w / 2 + self.pan_x, h / 2 + self.pan_y)
        base = max(20.0, min(w, h) / 4) * self.zoom
        span = max(maxs[0] - mins[0], maxs[1] - mins[1], maxs[2] - mins[2], 1e-06)
        mx, my, mz = ((maxs[0] + mins[0]) / 2, (maxs[1] + mins[1]) / 2, (maxs[2] + mins[2]) / 2)
        scale = base / span
        cosx, sinx, cosy, siny = (math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay))
        valid_faces = []
        used_indices = set()
        vertex_count = len(verts)
        for face in faces:
            if len(face) < 3:
                continue
            normalized = tuple(int(index) % vertex_count for index in face)
            if len(normalized) < 3:
                continue
            valid_faces.append(normalized)
            used_indices.update(normalized)
        if not valid_faces:
            return
        pts2d = {}
        pts3d = {}
        for index in used_indices:
            x, y, z = verts[index]
            px, py, pz = (x - mx, y - my, z - mz)
            x1 = px * cosy + pz * siny
            z1 = -px * siny + pz * cosy
            y2 = py * cosx - z1 * sinx
            z2 = py * sinx + z1 * cosx
            pts2d[index] = (cx + x1 * scale, cy - y2 * scale)
            pts3d[index] = z2
        items = []
        for face in valid_faces:
            coords = [c for index in face for c in pts2d[index]]
            depth = sum(pts3d[index] for index in face) / len(face)
            items.append((depth, coords))
        if not preview:
            try:
                shadow_poly = []
                for index in used_indices:
                    x, _, z = verts[index]
                    px, pz = (x - mx, z - mz)
                    x1 = px * cosy + pz * siny
                    z1 = -px * siny + pz * cosy
                    y2 = -my * cosx - z1 * sinx
                    shadow_poly.append((cx + x1 * scale, cy - y2 * scale))
                self.canvas.create_polygon([c for pt in shadow_poly for c in pt], fill='#000000', outline='', stipple='gray12')
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
        ttk.Label(self.source_row, text=UI_TEXT['v1']).pack(side='left')
        self.source_var = tk.StringVar(value='Caches')
        for val in ('Caches', 'HashSaves', 'FileSaves'):
            ttk.Radiobutton(self.source_row, text=val, variable=self.source_var, value=val, command=self.refresh_view).pack(side='left', padx=5)
        self.search_row = ttk.Frame(self.container)
        self.search_row.pack(fill='x', pady=(0, 4))
        ttk.Label(self.search_row, text=UI_TEXT['w1']).pack(side='left')
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_row, textvariable=self.search_var)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(4, 0))
        self.search_entry.bind('<KeyRelease>', lambda e: self.refresh_view(True))
        self.btn_create = ttk.Button(self.action_bar, text=UI_TEXT['x1'], command=self.create_cache, width=13)
        self.btn_applycache = ttk.Button(self.action_bar, text=UI_TEXT['y1'], command=self.apply_caches, width=13)
        self.btn_savehash = ttk.Button(self.action_bar, text=UI_TEXT['z1'], command=self.save_hash, width=13)
        self.btn_savefile = ttk.Button(self.action_bar, text=UI_TEXT['a2'], command=self.save_file, width=13)
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
        self.ctx_menu.add_command(label=UI_TEXT['b2'], command=self.delete_selected, state=delete_state)
        rename_state = 'normal' if len(selected_objs) == 1 and selected_objs[0]['kind'] in ('item', 'hash', 'group_item', 'group') else 'disabled'
        self.ctx_menu.add_command(label=UI_TEXT['c2'], command=self.rename_selected, state=rename_state)
        self.ctx_menu.add_separator()
        self.ctx_menu.add_command(label=UI_TEXT['d2'], command=self.create_group_from_selection)
        if clicked_obj and clicked_obj.get('kind') == 'group':
            self.ctx_menu.add_separator()
            self.ctx_menu.add_command(label=UI_TEXT['e2'], command=self.delete_selected_groups)
            self.ctx_menu.add_command(label=UI_TEXT['f2'], command=self.ungroup_selected_groups)
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
        dialog.grab_set()
        theme_toplevel(dialog)
        dialog.geometry('620x230')
        dialog.minsize(500, 210)
        body = ttk.Frame(dialog, padding=0)
        body.pack(fill='both', expand=True)
        body.columnconfigure(1, weight=1)
        ttk.Label(body, text=UI_TEXT['g2']).grid(row=0, column=0, sticky='w', padx=10, pady=(12, 4))
        hash_status = tk.StringVar(value='Loading…')
        hash_combo = ttk.Combobox(body, textvariable=hash_status, values=(), state='readonly', width=38)
        hash_combo.grid(row=0, column=1, sticky='we', padx=10, pady=(12, 4))
        hs = []
        hash_names = []
        chosen_hash = {'hex': None}
        def ask_custom_hash():
            ch = simpledialog.askstring(UI_TEXT['h2'], UI_TEXT['i2'], parent=dialog)
            if ch and ch.strip():
                chosen_hash['hex'] = re.sub('[^0-9A-Fa-f]', '', ch.strip())
                messagebox.showinfo(UI_TEXT['j2'], UI_TEXT['k2'].format(p0=chosen_hash['hex']), parent=dialog)
            elif ch is not None:
                chosen_hash['hex'] = None
        ttk.Button(body, text=UI_TEXT['l2'], command=ask_custom_hash).grid(row=0, column=2, padx=10, pady=(12, 4))
        ttk.Label(body, text=UI_TEXT['m2']).grid(row=1, column=0, sticky='w', padx=10, pady=4)
        file_status = tk.StringVar(value='Loading…')
        file_combo = ttk.Combobox(body, textvariable=file_status, values=(), state='readonly', width=38)
        file_combo.grid(row=1, column=1, sticky='we', padx=10, pady=4)
        fs = []
        file_names = []
        chosen_file = {'path': None}
        def pick_custom_file():
            p = filedialog.askopenfilename(title=UI_TEXT['n2'])
            if p:
                chosen_file['path'] = p
                messagebox.showinfo(UI_TEXT['j2'], UI_TEXT['o2'].format(p0=p), parent=dialog)
        ttk.Button(body, text=UI_TEXT['p2'], command=pick_custom_file).grid(row=1, column=2, padx=10, pady=4)
        ttk.Label(body, text=UI_TEXT['q2']).grid(row=2, column=0, sticky='w', padx=10, pady=(8, 4))
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
                messagebox.showerror(UI_TEXT['x1'], UI_TEXT['r2'], parent=dialog)
                return
            final_hash = re.sub('[^0-9A-Fa-f]', '', final_hash)
            if len(final_hash) == 0:
                messagebox.showerror(UI_TEXT['x1'], UI_TEXT['s2'], parent=dialog)
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
                messagebox.showerror(UI_TEXT['x1'], UI_TEXT['t2'], parent=dialog)
                return
            if not os.path.isfile(src_path):
                messagebox.showerror(UI_TEXT['x1'], UI_TEXT['u2'], parent=dialog)
                return
            disp = entry_name.get().strip()
            if not disp:
                messagebox.showerror(UI_TEXT['x1'], UI_TEXT['v2'], parent=dialog)
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
                messagebox.showerror(UI_TEXT['x1'], UI_TEXT['w2'].format(p0=e), parent=dialog)
                return
            dialog.destroy()
            self.refresh_view()
            messagebox.showinfo(UI_TEXT['x2'], UI_TEXT['y2'].format(p0=os.path.basename(dest_path)), parent=self)
            self._console_log(UI_TEXT['z2'].format(p0=os.path.basename(dest_path)))
        ttk.Button(btnf, text=UI_TEXT['a3'], command=on_ok).pack(side='left', padx=6)
        ttk.Button(btnf, text=UI_TEXT['b3'], command=dialog.destroy).pack(side='left', padx=6)
        body.columnconfigure(1, weight=1)
        entry_name.focus_set()
        def load_sources():
            nonlocal hs, fs, hash_names, file_names
            if not dialog.winfo_exists():
                return
            hash_status.set(UI_TEXT['c3'])
            file_status.set(UI_TEXT['c3'])
            dialog.update_idletasks()
            def scan():
                try:
                    return self._scan_hash_saves(), self._scan_file_saves()
                except Exception:
                    return [], []
            def apply_results(results):
                nonlocal hs, fs, hash_names, file_names
                if not dialog.winfo_exists():
                    return
                hs, fs = results
                hash_names = [name for name, _h, _p in hs]
                file_names = [name for name, _p in fs]
                hash_combo.configure(values=hash_names)
                file_combo.configure(values=file_names)
                hash_status.set(hash_names[0] if hash_names else UI_TEXT['d3'])
                file_status.set(file_names[0] if file_names else UI_TEXT['e3'])
                if hash_names:
                    hash_combo.current(0)
                if file_names:
                    file_combo.current(0)
            result_queue = queue.Queue(maxsize=1)
            threading.Thread(target=lambda: result_queue.put(scan()), daemon=True).start()
            def poll_results():
                if not dialog.winfo_exists():
                    return
                try:
                    apply_results(result_queue.get_nowait())
                except queue.Empty:
                    dialog.after(35, poll_results)
            dialog.after(35, poll_results)
        dialog.after_idle(load_sources)
        dialog.wait_window()
    def save_hash(self):
        dialog = tk.Toplevel(self)
        dialog.title('Save Hash')
        dialog.transient(self)
        dialog.grab_set()
        theme_toplevel(dialog)
        ttk.Label(dialog, text=UI_TEXT['f3']).grid(row=0, column=0, padx=10, pady=(12, 4), sticky='w')
        entry_hash = ttk.Entry(dialog, width=40)
        entry_hash.grid(row=0, column=1, padx=10, pady=(12, 4), sticky='we')
        ttk.Label(dialog, text=UI_TEXT['g3']).grid(row=1, column=0, padx=10, pady=4, sticky='w')
        entry_name = ttk.Entry(dialog, width=40)
        entry_name.grid(row=1, column=1, padx=10, pady=4, sticky='we')
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=12)
        dialog.columnconfigure(1, weight=1)
        def on_ok():
            hv = entry_hash.get().strip()
            nv = entry_name.get().strip()
            if not hv or not nv:
                messagebox.showerror(UI_TEXT['h3'], UI_TEXT['i3'], parent=dialog)
                return
            filename = ' - '.join([re.sub('[^0-9A-Fa-f]', '', hv), nv])
            safe_filename = self._sanitize_filename(filename)
            if not safe_filename:
                messagebox.showerror(UI_TEXT['h3'], UI_TEXT['j3'], parent=dialog)
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
                messagebox.showerror(UI_TEXT['h3'], UI_TEXT['k3'].format(p0=e), parent=dialog)
                return
            dialog.destroy()
            self.refresh_view()
            messagebox.showinfo(UI_TEXT['x2'], UI_TEXT['l3'].format(p0=os.path.basename(dest)))
            self._console_log(UI_TEXT['m3'].format(p0=os.path.basename(dest)))
        ttk.Button(btn_frame, text=UI_TEXT['a3'], command=on_ok).pack(side='left', padx=6)
        ttk.Button(btn_frame, text=UI_TEXT['b3'], command=dialog.destroy).pack(side='left', padx=6)
        entry_hash.focus_set()
        dialog.wait_window()
    def save_file(self):
        dialog = tk.Toplevel(self)
        dialog.title('Save File')
        dialog.transient(self)
        dialog.grab_set()
        theme_toplevel(dialog)
        chosen = {'path': None}
        def pick_file():
            p = filedialog.askopenfilename(title=UI_TEXT['n3'])
            if p:
                chosen['path'] = p
                lbl_file.config(text=p)
        ttk.Label(dialog, text=UI_TEXT['o3']).grid(row=0, column=0, padx=10, pady=(12, 4), sticky='w')
        btn_pick = ttk.Button(dialog, text=UI_TEXT['p3'], command=pick_file)
        btn_pick.grid(row=0, column=1, padx=10, pady=(12, 4), sticky='w')
        lbl_file = ttk.Label(dialog, text=UI_TEXT['q3'])
        lbl_file.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 8), sticky='w')
        ttk.Label(dialog, text=UI_TEXT['g3']).grid(row=2, column=0, padx=10, pady=4, sticky='w')
        entry_name = ttk.Entry(dialog, width=40)
        entry_name.grid(row=2, column=1, padx=10, pady=4, sticky='we')
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=12)
        dialog.columnconfigure(1, weight=1)
        def on_ok():
            src = chosen['path']
            name = entry_name.get().strip()
            if not src:
                messagebox.showerror(UI_TEXT['h3'], UI_TEXT['r3'], parent=dialog)
                return
            if not name:
                messagebox.showerror(UI_TEXT['h3'], UI_TEXT['s3'], parent=dialog)
                return
            safe_name = self._sanitize_filename(name)
            if not safe_name:
                messagebox.showerror(UI_TEXT['h3'], UI_TEXT['j3'], parent=dialog)
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
                messagebox.showerror(UI_TEXT['h3'], UI_TEXT['t3'].format(p0=e), parent=dialog)
                return
            dialog.destroy()
            self.refresh_view()
            msg = UI_TEXT['z32'] if is_roblox_model else 'Saved'
            messagebox.showinfo(UI_TEXT['x2'], UI_TEXT['u3'].format(p0=msg, p1=os.path.basename(dest)))
            self._console_log(UI_TEXT['v3'].format(p0=msg, p1=os.path.basename(dest)))
        ttk.Button(btn_frame, text=UI_TEXT['a3'], command=on_ok).pack(side='left', padx=6)
        ttk.Button(btn_frame, text=UI_TEXT['b3'], command=dialog.destroy).pack(side='left', padx=6)
        entry_name.focus_set()
        dialog.wait_window()
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
            messagebox.showerror(UI_TEXT['y1'], UI_TEXT['w3'])
            return
        objs = self._get_selected_objs()
        if not objs:
            messagebox.showinfo(UI_TEXT['y1'], UI_TEXT['x3'])
            return
        targets: List[Tuple[bytes, str, str, str]] = []
        for o in objs:
            info = self._resolve_cache_file_for_item(o)
            if not info and o.get('kind') == 'hash':
                full = o.get('path')
                if full and os.path.isfile(full):
                    entered = simpledialog.askstring(UI_TEXT['y3'], UI_TEXT['z3'], parent=self)
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
            messagebox.showerror(UI_TEXT['y1'], UI_TEXT['a4'])
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
            messagebox.showerror(UI_TEXT['y1'], UI_TEXT['b4'].format(p0=e))
            return
        if ok:
            root = self.winfo_toplevel()
            recorder = getattr(root, '_cc_record_applied_caches', None)
            if callable(recorder):
                applied = []
                for id_b, _full, display, h_hex in targets:
                    applied.append({'name': display, 'hash': h_hex})
                recorder(applied)
        messagebox.showinfo(UI_TEXT['y1'], UI_TEXT['c4'].format(p0=ok, p1=len(targets)))
        self._console_log(UI_TEXT['d4'].format(p0=ok, p1=len(targets)))
    def rename_selected(self):
        objs = self._get_selected_objs()
        if len(objs) != 1:
            return
        o = objs[0]
        kind = o.get('kind')
        current = o.get('display') or o.get('name')
        new_name = simpledialog.askstring(UI_TEXT['c2'], UI_TEXT['e4'], initialvalue=current)
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
            messagebox.showerror(UI_TEXT['h3'], UI_TEXT['f4'].format(p0=e))
            return
        self.refresh_view()
    def delete_selected(self):
        objs = self._get_selected_objs()
        if not objs:
            messagebox.showerror(UI_TEXT['h3'], UI_TEXT['g4'])
            return
        prompt = UI_TEXT['h4'].format(p0=objs[0].get('name') or objs[0].get('display')) if len(objs) == 1 else UI_TEXT['i4'].format(p0=len(objs))
        if not messagebox.askyesno(UI_TEXT['j4'], prompt):
            return
        deleted_units = 0
        for o in objs:
            if o['kind'] == 'group':
                try:
                    shutil.rmtree(o['path'])
                    deleted_units += 1
                    self.group_states.pop(o['path'], None)
                except Exception as e:
                    messagebox.showerror(UI_TEXT['h3'], UI_TEXT['k4'].format(p0=e))
                    return
            elif o['kind'] == 'group_item':
                try:
                    os.remove(os.path.join(o['group_path'], o['filename']))
                    deleted_units += 1
                except Exception as e:
                    messagebox.showerror(UI_TEXT['h3'], UI_TEXT['l4'].format(p0=e))
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
                                messagebox.showerror(UI_TEXT['h3'], UI_TEXT['l4'].format(p0=e))
                                return
            elif o['kind'] == 'hash':
                try:
                    os.remove(o['path'])
                    deleted_units += 1
                except Exception as e:
                    messagebox.showerror(UI_TEXT['h3'], UI_TEXT['l4'].format(p0=e))
                    return
        self.refresh_view()
        messagebox.showinfo(UI_TEXT['x2'], UI_TEXT['m4'].format(p0=deleted_units))
        self._console_log(UI_TEXT['n4'].format(p0=deleted_units))
    def delete_selected_groups(self):
        objs = self._get_selected_objs()
        groups = [o for o in objs if o.get('kind') == 'group']
        if not groups:
            return
        prompt = UI_TEXT['o4'].format(p0=groups[0]['name']) if len(groups) == 1 else UI_TEXT['p4'].format(p0=len(groups))
        if not messagebox.askyesno(UI_TEXT['j4'], prompt):
            return
        deleted = 0
        for g in groups:
            try:
                shutil.rmtree(g['path'])
                deleted += 1
                self.group_states.pop(g['path'], None)
            except Exception as e:
                messagebox.showerror(UI_TEXT['h3'], UI_TEXT['k4'].format(p0=e))
                return
        self.refresh_view()
        messagebox.showinfo(UI_TEXT['x2'], UI_TEXT['q4'].format(p0=deleted))
        self._console_log(UI_TEXT['r4'].format(p0=deleted))
    def ungroup_selected_groups(self):
        objs = self._get_selected_objs()
        groups = [o for o in objs if o.get('kind') == 'group']
        if not groups:
            return
        prompt = UI_TEXT['s4'].format(p0=groups[0]['name']) if len(groups) == 1 else UI_TEXT['t4'].format(p0=len(groups))
        if not messagebox.askyesno(UI_TEXT['j4'], prompt):
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
                messagebox.showerror(UI_TEXT['h3'], UI_TEXT['u4'].format(p0=e))
                return
        self.refresh_view()
        messagebox.showinfo(UI_TEXT['x2'], UI_TEXT['v4'].format(p0=removed_groups, p1=moved_files))
        self._console_log(UI_TEXT['w4'].format(p0=removed_groups, p1=moved_files))
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
                messagebox.showerror(UI_TEXT['h3'], UI_TEXT['x4'])
                return
        name = simpledialog.askstring(UI_TEXT['d2'], UI_TEXT['y4'])
        if not name:
            return
        group_path = os.path.join(base, name)
        if os.path.exists(group_path):
            messagebox.showerror(UI_TEXT['h3'], UI_TEXT['z4'])
            return
        try:
            os.makedirs(group_path, exist_ok=False)
        except Exception as e:
            messagebox.showerror(UI_TEXT['h3'], UI_TEXT['a5'].format(p0=e))
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
            messagebox.showinfo(UI_TEXT['x2'], UI_TEXT['b5'].format(p0=name, p1=moved_count))
        else:
            messagebox.showinfo(UI_TEXT['x2'], UI_TEXT['c5'].format(p0=name))
        self._console_log(UI_TEXT['d5'].format(p0=name, p1=moved_count))
TYPE_FILTERS = [('All', lambda c: True), ('Mesh', lambda c: c == 'Mesh'), ('Audio', lambda c: c == 'Sound'), ('Animation', lambda c: c == 'Animation'), ('Image', lambda c: c in ('Image', 'Decal')), ('Video', lambda c: c == 'Video'), ('KTX Texture', lambda c: c == 'KTX Texture'), ('Model/RBXM', lambda c: c in ('Model', 'RBXM', 'rbxl (place)')), ('Font', lambda c: c == 'Font'), ('Text', lambda c: c in ('Text', 'Translations', 'Compressed', 'Ticket')), ('Unknown', lambda c: c == 'Unknown')]
TYPE_FILTER_MATCHERS = {label: matcher for label, matcher in TYPE_FILTERS}
FFLAG_PREFIXES = ['DFDouble', 'DFFloat', 'DFInt', 'DFString', 'DFFlag', 'DFLog', 'FDouble', 'FFloat', 'FInt', 'FString', 'FFlag', 'FLog', 'SFDouble', 'SFFloat', 'SFFlag', 'SFInt', 'SFString', 'SFLog']
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
                        self.module_size = max(int(me.modBaseSize), FFLAG_MODULE_SIZE)
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
    if not pid:
        return ''
    if sys.platform.startswith('linux'):
        try:
            return os.readlink(f'/proc/{int(pid)}/exe')
        except (OSError, TypeError, ValueError):
            return ''
    if sys.platform != 'win32':
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
    try:
        clients = list_roblox_clients()
        return int(clients[0]['pid']) if clients else 0
    except Exception:
        return 0

_NATIVE_MESSAGEBOX = messagebox
def _pady_pair(value):
    try:
        if isinstance(value, (tuple, list)):
            vals = list(value)
            if len(vals) == 1:
                return int(float(vals[0] or 0)), int(float(vals[0] or 0))
            return int(float(vals[0] or 0)), int(float(vals[1] or 0))
        n = int(float(value or 0))
        return n, n
    except Exception:
        return 0, 0
def _routils_center_popup(win):
    try:
        if not win.winfo_exists() or getattr(win, '_skip_popup_centering', False):
            return
        win.update_idletasks()
        width = max(1, int(win.winfo_width()), int(win.winfo_reqwidth()))
        height = max(1, int(win.winfo_height()), int(win.winfo_reqheight()))
        screen_width = int(win.winfo_screenwidth())
        screen_height = int(win.winfo_screenheight())
        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 2)
        win.geometry(f'+{x}+{y}')
    except Exception:
        pass
def _routils_clear_window_references(event, win):
    if getattr(event, 'widget', None) is not win:
        return
    try:
        root = tk._default_root
        if root is not None:
            for name, value in tuple(vars(root).items()):
                if value is win:
                    try:
                        setattr(root, name, None)
                    except Exception:
                        pass
            if 'Outdated' in str(win.title()):
                try:
                    root._outdated_dialog_shown = False
                except Exception:
                    pass
    except Exception:
        pass
def _routils_close_popup(win):
    try:
        if not win.winfo_exists():
            return
    except Exception:
        return
    callback = getattr(win, '_routils_close_callback', None)
    if callable(callback):
        try:
            callback()
            if not win.winfo_exists():
                return
        except Exception:
            pass
    try:
        protocol = win.protocol('WM_DELETE_WINDOW')
        if protocol:
            win.tk.call(protocol)
            try:
                if not win.winfo_exists():
                    return
            except Exception:
                return
    except Exception:
        pass
    try:
        win.grab_release()
    except Exception:
        pass
    try:
        win.destroy()
    except Exception:
        pass
def _routils_process_has_focus(root=None):
    try:
        if sys.platform == 'win32':
            foreground = ctypes.windll.user32.GetForegroundWindow()
            if not foreground:
                return False
            process_id = ctypes.wintypes.DWORD()
            ctypes.windll.user32.GetWindowThreadProcessId(foreground, ctypes.byref(process_id))
            return int(process_id.value) == os.getpid()
    except Exception:
        pass
    try:
        root = root or tk._default_root
        focus = root.focus_get() if root is not None and root.winfo_exists() else None
        return bool(focus and focus.winfo_toplevel())
    except Exception:
        return False
def _routils_sync_popup_topmost(root=None):
    try:
        root = root or tk._default_root
        if root is None or not root.winfo_exists():
            return False
        focused = _routils_process_has_focus(root)
        if sys.platform != 'win32':
            return focused
        windows = []
        pending = list(root.winfo_children())
        while pending:
            widget = pending.pop(0)
            try:
                pending.extend(widget.winfo_children())
                if isinstance(widget, tk.Toplevel) and widget.winfo_exists():
                    windows.append(widget)
            except Exception:
                pass
        for widget in windows:
            try:
                widget.attributes('-topmost', bool(focused))
            except Exception:
                pass
            try:
                if sys.platform == 'win32':
                    hwnd = _win32_root_hwnd(widget)
                    if hwnd:
                        insert_after = -1 if focused else -2
                        ctypes.windll.user32.SetWindowPos(hwnd, insert_after, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0010)
                if focused:
                    widget.lift()
            except Exception:
                pass
        if focused:
            try:
                root.lift()
            except Exception:
                pass
            for widget in windows:
                try:
                    if widget.winfo_exists():
                        widget.lift()
                except Exception:
                    pass
        return focused
    except Exception:
        return False
def _routils_popup_chrome(win):
    try:
        if not win.winfo_exists() or getattr(win, '_skip_custom_chrome', False) or getattr(win, '_routils_custom_chrome', False):
            return
        win._routils_custom_chrome = True
        try:
            title = str(win.title() or 'RoUtils')
        except Exception:
            title = 'RoUtils'
        palette = _CURRENT_PALETTE if isinstance(_CURRENT_PALETTE, dict) else THEMES[DEFAULT_THEME]
        bg = palette.get('bg_dark', '#111318')
        fg = palette.get('fg', '#e6e9ef')
        accent = palette.get('accent', '#8ab4f8')
        bar_bg = _routils_darken_color(bg, 0.20)
        height = 34
        children = list(win.winfo_children())
        pack_children = [child for child in children if child.winfo_manager() == 'pack']
        grid_children = [child for child in children if child.winfo_manager() == 'grid']
        place_children = [child for child in children if child.winfo_manager() == 'place']
        if pack_children:
            first = next((child for child in pack_children if str(child.pack_info().get('side', 'top')) == 'top'), pack_children[0])
            info = first.pack_info()
            top, bottom = _pady_pair(info.get('pady', 0))
            first.pack_configure(pady=(top + height, bottom))
        elif grid_children:
            minrow = min(int(child.grid_info().get('row', 0)) for child in grid_children)
            for child in grid_children:
                info = child.grid_info()
                if int(info.get('row', 0)) == minrow:
                    top, bottom = _pady_pair(info.get('pady', 0))
                    child.grid_configure(pady=(top + height, bottom))
        elif place_children:
            for child in place_children:
                info = child.place_info()
                try:
                    y = int(float(info.get('y', 0))) + height
                    child.place_configure(y=y)
                except Exception:
                    pass
        try:
            win.overrideredirect(True)
        except Exception:
            pass
        try:
            win.configure(bg=accent, highlightthickness=2, highlightbackground=accent, highlightcolor=accent, bd=0, relief='flat')
        except Exception:
            try:
                win.configure(bg=accent)
            except Exception:
                pass
        bar = tk.Frame(win, bg=bar_bg, height=height, bd=0, highlightthickness=0)
        bar.place(x=2, y=2, relwidth=1.0, width=-4, height=height)
        bar.pack_propagate(False)
        title_label = tk.Label(bar, text=title, bg=bar_bg, fg=fg, font=('Segoe UI Semibold', 9), anchor='w')
        title_label.pack(side='left', fill='both', expand=True, padx=(11, 4))
        close = tk.Label(bar, text=UI_TEXT['e5'], bg=bar_bg, fg='#ff777d', font=('Segoe UI', 13), width=2, cursor='hand2')
        close.pack(side='right', fill='y')
        close.bind('<Button-1>', lambda _e, w=win: _routils_close_popup(w))
        close.bind('<Enter>', lambda _e, w=close: w.configure(bg='#542a31'))
        close.bind('<Leave>', lambda _e, w=close, color=bar_bg: w.configure(bg=color))
        win._routils_chrome_bar = bar
        win._routils_chrome_title = title_label
        win._routils_chrome_close = close
        win._routils_chrome_colors = {'accent': accent, 'bar': bar_bg, 'fg': fg}
        drag = {'x': 0, 'y': 0, 'wx': 0, 'wy': 0, 'pending': None, 'job': None, 'last': None}
        def start_drag(event):
            drag.update(x=event.x_root, y=event.y_root, wx=win.winfo_x(), wy=win.winfo_y(), last=None)
        def apply_drag():
            drag['job'] = None
            position = drag.get('pending')
            if position is None or position == drag.get('last'):
                return
            drag['last'] = position
            try:
                if sys.platform == 'win32':
                    hwnd = _win32_root_hwnd(win)
                    if hwnd:
                        ctypes.windll.user32.SetWindowPos(hwnd, 0, int(position[0]), int(position[1]), 0, 0, 1 | 4 | 16)
                        return
                win.geometry(f'+{int(position[0])}+{int(position[1])}')
            except Exception:
                pass
        def move_drag(event):
            drag['pending'] = (int(drag['wx'] + event.x_root - drag['x']), int(drag['wy'] + event.y_root - drag['y']))
            if drag['job'] is None:
                try:
                    drag['job'] = win.after(16, apply_drag)
                except Exception:
                    drag['job'] = None
        def finish_drag(_event=None):
            job = drag.get('job')
            if job is not None:
                try:
                    win.after_cancel(job)
                except Exception:
                    pass
                drag['job'] = None
            apply_drag()
        for widget in (bar, title_label):
            widget.bind('<ButtonPress-1>', start_drag, add='+')
            widget.bind('<B1-Motion>', move_drag, add='+')
            widget.bind('<ButtonRelease-1>', finish_drag, add='+')
        def sync_topmost(_event=None):
            try:
                _routils_sync_popup_topmost(tk._default_root)
            except Exception:
                pass
        win.bind('<FocusIn>', sync_topmost, add='+')
        win.bind('<FocusOut>', lambda _e: win.after(180, sync_topmost), add='+')
        win.after_idle(lambda w=win, b=bar: (b.lift() if w.winfo_exists() and b.winfo_exists() else None))
        win.after_idle(lambda w=win: _routils_center_popup(w))
        win.after_idle(lambda w=win: _routils_refresh_popup_chrome(w))
        win.after(100, sync_topmost)
    except Exception:
        pass
def _routils_refresh_popup_chrome(win):
    try:
        if not win.winfo_exists() or not getattr(win, '_routils_custom_chrome', False):
            return
        palette = _CURRENT_PALETTE if isinstance(_CURRENT_PALETTE, dict) else THEMES[DEFAULT_THEME]
        accent = palette.get('accent', '#8ab4f8')
        bar_bg = _routils_darken_color(palette.get('bg_dark', '#111318'), 0.20)
        fg = palette.get('fg', '#e6e9ef')
        win.configure(bg=accent, highlightbackground=accent, highlightcolor=accent)
        bar = getattr(win, '_routils_chrome_bar', None)
        label = getattr(win, '_routils_chrome_title', None)
        close = getattr(win, '_routils_chrome_close', None)
        if bar is not None and bar.winfo_exists():
            bar.configure(bg=bar_bg)
        if label is not None and label.winfo_exists():
            label.configure(bg=bar_bg, fg=fg)
        if close is not None and close.winfo_exists():
            close.configure(bg=bar_bg)
        win._routils_chrome_colors = {'accent': accent, 'bar': bar_bg, 'fg': fg}
    except Exception:
        pass
_original_toplevel_init = tk.Toplevel.__init__
def _routils_toplevel_init(self, *args, **kwargs):
    skip_popup_chrome = bool(getattr(tk, '_routils_skip_next_popup_chrome', False))
    if skip_popup_chrome:
        tk._routils_skip_next_popup_chrome = False
    _original_toplevel_init(self, *args, **kwargs)
    try:
        master = self.master
        if master is not None and isinstance(master, (tk.Tk, tk.Toplevel)) and master.winfo_exists():
            self.transient(master)
        self.bind('<Destroy>', lambda event, w=self: _routils_clear_window_references(event, w), add='+')
        if not skip_popup_chrome:
            self.after_idle(lambda w=self: _routils_popup_chrome(w) if w.winfo_exists() else None)
    except Exception:
        pass
tk.Toplevel.__init__ = _routils_toplevel_init
def _routils_nonblocking_grab_set(self, *args, **kwargs):
    try:
        self.focus_set()
    except Exception:
        pass
    return None
tk.Toplevel.grab_set = _routils_nonblocking_grab_set
class _MacNotification:
    _active = []
    _pulse_jobs = {}
    @classmethod
    def _app_has_focus(cls, root):
        try:
            focus = root.focus_get()
            if focus is None:
                return False
            top = focus.winfo_toplevel()
            return top is root or str(top.transient()) == str(root)
        except Exception:
            return False
    @classmethod
    def _reposition(cls):
        live = []
        for win, height in cls._active:
            try:
                if win.winfo_exists():
                    live.append((win, height))
            except Exception:
                pass
        cls._active = live
        ordered = list(reversed(cls._active))
        for index, (win, height) in enumerate(ordered):
            try:
                width = 280
                root = getattr(win, '_routils_notification_parent', None)
                if root is not None and root.winfo_exists():
                    root.update_idletasks()
                    rx, ry = root.winfo_rootx(), root.winfo_rooty()
                    rw, rh = root.winfo_width(), root.winfo_height()
                    x = rx + rw - width - 14
                    y = ry + rh - height - 14 - sum(h + 10 for _, h in ordered[:index])
                else:
                    x = win.winfo_screenwidth() - width - 22
                    y = win.winfo_screenheight() - height - 58 - sum(h + 12 for _, h in ordered[:index])
                sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
                x = max(0, min(int(x), sw - width))
                y = max(0, min(int(y), sh - height))
                win.geometry(f'{width}x{height}+{x}+{y}')
            except Exception:
                pass
    @classmethod
    def show(cls, title, message, parent=None, kind='info'):
        try:
            parent = parent or tk._default_root
            if parent is None or not parent.winfo_exists():
                return
            root = parent.winfo_toplevel()
            if not cls._app_has_focus(root):
                return
            _record_notification(title, message, kind)
            accent = _CURRENT_PALETTE.get('accent', '#8ab4f8')
            if kind == 'error':
                accent = '#ff5f68'
            elif kind == 'warning':
                accent = '#ffc857'
            bg = _CURRENT_PALETTE.get('bg_dark', '#111318')
            panel = _CURRENT_PALETTE.get('bg_medium', '#1a1d24')
            fg = _CURRENT_PALETTE.get('fg', '#e6e9ef')
            lines = max(1, min(4, (len(str(message)) // 46) + 1))
            height = 46 + lines * 14
            toast = tk.Toplevel(root)
            toast._routils_notification_parent = root
            toast._skip_custom_chrome = True
            toast.overrideredirect(True)
            toast.configure(bg=accent)
            toast.attributes('-topmost', True)
            try:
                toast.transient(root)
            except Exception:
                pass
            outer = tk.Frame(toast, bg=accent, bd=0, highlightthickness=2, highlightbackground=accent)
            outer.pack(fill='both', expand=True, padx=0, pady=0)
            card = tk.Frame(outer, bg=panel, bd=0)
            card.pack(fill='both', expand=True, padx=2, pady=2)
            header = tk.Frame(card, bg=panel, height=25)
            header.pack(fill='x')
            header.pack_propagate(False)
            tk.Label(header, text=str(title), bg=panel, fg=fg, font=('Segoe UI Semibold', 8), anchor='w').pack(side='left', fill='both', expand=True, padx=(7, 2))
            close = tk.Label(header, text=UI_TEXT['e5'], bg=panel, fg='#ff8a90', font=('Segoe UI', 13), width=2, cursor='hand2')
            close.pack(side='right', fill='y')
            body = tk.Label(card, text=str(message), bg=panel, fg=fg, justify='left', anchor='w', wraplength=238, font=('Segoe UI', 8))
            body.pack(fill='both', expand=True, padx=9, pady=(1, 7))
            state = {'count': 0, 'closed': False}
            def close_toast():
                if state['closed']:
                    return
                state['closed'] = True
                try:
                    job = cls._pulse_jobs.pop(toast, None)
                    if job:
                        toast.after_cancel(job)
                except Exception:
                    pass
                cls._active = [(w, h) for w, h in cls._active if w is not toast]
                try:
                    toast.destroy()
                except Exception:
                    pass
                cls._reposition()
            close.bind('<Button-1>', lambda _e: close_toast())
            close.bind('<Enter>', lambda _e: close.configure(bg='#542a31'))
            close.bind('<Leave>', lambda _e: close.configure(bg=panel))
            def sync_topmost(_event=None):
                try:
                    toast.attributes('-topmost', True)
                    toast.lift()
                except Exception:
                    pass
            root.bind('<FocusIn>', sync_topmost, add='+')
            root.bind('<FocusOut>', lambda _e: toast.after(180, sync_topmost), add='+')
            toast.bind('<FocusIn>', sync_topmost, add='+')
            toast.bind('<FocusOut>', lambda _e: toast.after(180, sync_topmost), add='+')
            cls._active.append((toast, height))
            cls._reposition()
            try:
                toast.update_idletasks()
                toast.attributes('-topmost', True)
                toast.lift()
                toast.after(20, lambda w=toast: (w.attributes('-topmost', True), w.lift()) if w.winfo_exists() else None)
            except Exception:
                pass
            try:
                root.bind('<Configure>', lambda _e: cls._reposition(), add='+')
            except Exception:
                pass
            def pulse():
                if state['closed'] or not toast.winfo_exists():
                    return
                state['count'] += 1
                color = accent if state['count'] % 2 else '#ffffff'
                try:
                    outer.configure(highlightbackground=color, bg=color)
                except Exception:
                    pass
                if state['count'] < 8:
                    cls._pulse_jobs[toast] = toast.after(160, pulse)
                else:
                    outer.configure(highlightbackground=accent, bg=accent)
                    cls._pulse_jobs.pop(toast, None)
            cls._pulse_jobs[toast] = toast.after_idle(pulse)
            toast.after(4200, close_toast)
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
        root = parent or tk._default_root
        if root is None:
            return _NATIVE_MESSAGEBOX.askyesno(title, message, parent=parent, **kwargs)
        dialog = None
        result = {'value': False}
        try:
            dialog = tk.Toplevel(root)
            dialog.title(str(title or 'RoUtils'))
            dialog.transient(root)
            dialog.resizable(False, False)
            body = ttk.Frame(dialog, padding=(16, 15, 16, 12))
            body.pack(fill='both', expand=True)
            prompt = ttk.Label(body, text=str(message), justify='left', wraplength=460)
            prompt.pack(fill='x', anchor='w', pady=(3, 16))
            buttons = ttk.Frame(body)
            buttons.pack(fill='x')
            def finish(answer):
                result['value'] = bool(answer)
                try:
                    if dialog is not None and dialog.winfo_exists():
                        dialog.destroy()
                except Exception:
                    pass
            no_button = ttk.Button(buttons, text='No', command=lambda: finish(False))
            no_button.pack(side='right', padx=(7, 0))
            yes_button = ttk.Button(buttons, text='Yes', command=lambda: finish(True))
            yes_button.pack(side='right')
            dialog.protocol('WM_DELETE_WINDOW', lambda: finish(False))
            dialog.bind('<Escape>', lambda _event: finish(False))
            dialog.update_idletasks()
            width = max(390, min(560, int(dialog.winfo_reqwidth())))
            height = max(145, int(dialog.winfo_reqheight()))
            dialog.geometry(f'{width}x{height}')
            dialog.after_idle(lambda w=dialog: _routils_center_popup(w) if w.winfo_exists() else None)
            no_button.focus_set()
            dialog.wait_window()
            return bool(result['value'])
        except Exception:
            try:
                if dialog is not None and dialog.winfo_exists():
                    dialog.destroy()
            except Exception:
                pass
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
            return
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
        width = max(1, int(getattr(event, 'width', 0) or 0))
        if width == getattr(self, '_last_inner_width', -1):
            return
        self._last_inner_width = width
        try:
            root = self.winfo_toplevel()
            if getattr(root, '_resize_active', False) and hasattr(root, '_apply_or_defer_canvas_window_width'):
                root._apply_or_defer_canvas_window_width(self.canvas, self.window, width, f'_scrollable_width_{id(self.canvas)}')
                return
        except Exception:
            pass
        try:
            self.canvas.itemconfigure(self.window, width=width)
        except Exception:
            pass
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
class _RoUtilsDiscordRPC:
    def __init__(self, client_id, status_callback=None):
        self.client_id = str(client_id)
        self.status_callback = status_callback
        self._lock = threading.RLock()
        self._wake = threading.Event()
        self._stop_event = threading.Event()
        self._thread = None
        self._enabled = True
        self._reconnect_requested = False
        self._activity = ('Not playing Roblox', 'Sekme: Ana Sayfa')
    def _status(self, text):
        callback = self.status_callback
        if callback is not None:
            try:
                callback(str(text))
            except Exception:
                pass
    def set_enabled(self, enabled):
        with self._lock:
            self._enabled = bool(enabled)
        self._wake.set()
    def set_client_id(self, client_id):
        value = str(client_id or '').strip()
        if not value.isdigit():
            return False
        with self._lock:
            if value == self.client_id:
                return True
            self.client_id = value
            self._reconnect_requested = True
        self._wake.set()
        return True
    def set_activity(self, details, state):
        activity = (str(details)[:128], str(state)[:128])
        with self._lock:
            if activity == self._activity:
                return
            self._activity = activity
        self._wake.set()
    def start(self):
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True, name='RoUtils-DiscordRPC')
        self._thread.start()
    def stop(self):
        self._stop_event.set()
        self._wake.set()
        thread = self._thread
        if thread is not None and thread.is_alive() and thread is not threading.current_thread():
            thread.join(timeout=2.0)
    def _close_presence(self, presence):
        if presence is not None:
            try:
                presence.clear()
            except Exception:
                pass
            try:
                presence.close()
            except Exception:
                pass
    def _run(self):
        presence = None
        last_activity = None
        last_update = 0.0
        while not self._stop_event.is_set():
            with self._lock:
                enabled = self._enabled
                activity = self._activity
                reconnect_requested = self._reconnect_requested
                self._reconnect_requested = False
            if reconnect_requested:
                self._close_presence(presence)
                presence = None
                last_activity = None
                last_update = 0.0
            if not enabled:
                self._close_presence(presence)
                presence = None
                last_activity = None
                self._status('Discord RPC disabled')
                self._wake.wait(1.0)
                self._wake.clear()
                continue
            if _DiscordPresence is None:
                self._status('Discord RPC unavailable: install requirements.txt')
                self._wake.wait(10.0)
                self._wake.clear()
                continue
            if presence is None:
                try:
                    presence = _DiscordPresence(self.client_id)
                    presence.connect()
                    last_activity = None
                    last_update = 0.0
                    self._status('Discord RPC connected')
                except Exception:
                    self._close_presence(presence)
                    presence = None
                    self._status('Waiting for Discord desktop app')
                    self._wake.wait(10.0)
                    self._wake.clear()
                    continue
            now = time.monotonic()
            if activity != last_activity or now - last_update >= DISCORD_RPC_INTERVAL:
                details, state = activity
                try:
                    presence.update(name='RoUtils', details=details, state=state, large_image='routils', large_text='RoUtils', buttons=[{'label': 'RoUtils Github', 'url': 'https://github.com/offp001/routils'}, {'label': 'RoUtils Website', 'url': 'https://offp001.github.io/routilsw/'}])
                except Exception:
                    try:
                        presence.update(name='RoUtils', details=details, state=state)
                    except Exception:
                        self._close_presence(presence)
                        presence = None
                        last_activity = None
                        self._status('Reconnecting Discord RPC')
                        self._wake.wait(5.0)
                        self._wake.clear()
                        continue
                last_activity = activity
                last_update = time.monotonic()
                self._status('Discord RPC connected')
            timeout = max(0.2, min(DISCORD_RPC_INTERVAL, DISCORD_RPC_INTERVAL - (time.monotonic() - last_update)))
            self._wake.wait(timeout)
            self._wake.clear()
        self._close_presence(presence)
        self._status('Discord RPC stopped')
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
from autoupdate.autoupdate import AutoUpdateMixin
from ai.ai import AIMixin
from cache.cache import CacheMixin
from client.client import ClientMixin
from console.console import ConsoleMixin
from emote_manager.emote_manager import EmoteManagerMixin
from fflag.fflag import FFlagMixin
from history.history import HistoryMixin
from home.home import HomeMixin
from plugins.plugins import PluginsMixin
from release_notes.release_notes import ReleaseNotesMixin
from server_viewer.server_viewer import ServerViewerMixin
from settings.settings import SettingsMixin
from subplace.subplace import SubplaceMixin
from themes.themes import ThemesMixin
from viewer.viewer import ViewerMixin
class App(AutoUpdateMixin, AIMixin, CacheMixin, ClientMixin, ConsoleMixin, EmoteManagerMixin, FFlagMixin, HistoryMixin, HomeMixin, PluginsMixin, ReleaseNotesMixin, ServerViewerMixin, SettingsMixin, SubplaceMixin, ThemesMixin, ViewerMixin, _TkAppBase):
    def after(self, ms, func=None, *args):
        ui_thread = getattr(self, '_ui_thread_id', None)
        if func is not None and ui_thread is not None and threading.get_ident() != ui_thread:
            if getattr(self, '_ui_dispatch_closed', False):
                return None
            token = None
            key = self._thread_ui_coalesce_key(func, args)
            try:
                with self._thread_ui_counter_lock:
                    self._thread_ui_counter += 1
                    token = f'__routils_thread_after_{self._thread_ui_counter}'
                if key is not None:
                    with self._thread_ui_coalesce_lock:
                        previous = self._thread_ui_coalesce_tokens.get(key)
                        if previous is not None and not self._thread_token_cancelled(previous):
                            return previous
                        if previous is not None:
                            self._thread_ui_coalesce_tokens.pop(key, None)
                            self._thread_ui_token_coalesce_keys.pop(previous, None)
                        self._thread_ui_coalesce_tokens[key] = token
                        self._thread_ui_token_coalesce_keys[token] = key
                due = time.monotonic() + max(0, float(ms or 0)) / 1000.0
                with self._thread_ui_cancel_lock:
                    self._thread_ui_known_tokens.add(token)
                task = (due, token, func, args)
                try:
                    self._thread_ui_dispatch_queue.put_nowait(task)
                    return token
                except queue.Full:
                    with self._thread_ui_cancel_lock:
                        self._thread_ui_known_tokens.discard(token)
                        self._thread_ui_cancelled.discard(token)
                    stored = self._store_thread_ui_overflow(task)
                    if stored is None:
                        self._forget_thread_ui_token(token)
                    return stored
            except Exception:
                if token is not None:
                    self._forget_thread_ui_token(token)
                return None
        return super().after(ms, func, *args)
    def after_cancel(self, after_id):
        if isinstance(after_id, str) and after_id.startswith('__routils_thread_after_'):
            with self._thread_ui_cancel_lock:
                if after_id in self._thread_ui_known_tokens:
                    self._thread_ui_cancelled.add(after_id)
            self._forget_thread_ui_coalesce_key(after_id)
            return
        if after_id is None:
            return
        return super().after_cancel(after_id)
    def _forget_thread_ui_coalesce_key(self, token):
        lock = getattr(self, '_thread_ui_coalesce_lock', None)
        if lock is None:
            return
        with lock:
            key = self._thread_ui_token_coalesce_keys.pop(token, None)
            if key is not None and self._thread_ui_coalesce_tokens.get(key) == token:
                self._thread_ui_coalesce_tokens.pop(key, None)
    def _forget_thread_ui_token(self, token):
        with self._thread_ui_cancel_lock:
            self._thread_ui_cancelled.discard(token)
            self._thread_ui_known_tokens.discard(token)
        self._forget_thread_ui_coalesce_key(token)
    def _thread_token_cancelled(self, token, consume=False):
        with self._thread_ui_cancel_lock:
            cancelled = token in self._thread_ui_cancelled
            if cancelled and consume:
                self._thread_ui_cancelled.discard(token)
                self._thread_ui_known_tokens.discard(token)
            return cancelled
    def _store_thread_ui_overflow(self, task):
        due, token, func, args = task
        key = self._thread_ui_coalesce_key(func, args)
        with self._thread_ui_overflow_lock:
            if key is not None and key in self._thread_ui_overflow_keys:
                old_token = self._thread_ui_overflow_keys[key]
                if not self._thread_token_cancelled(old_token, consume=False):
                    self._forget_thread_ui_token(token)
                    return old_token
                self._thread_ui_overflow = [item for item in self._thread_ui_overflow if item[1] != old_token]
                heapq.heapify(self._thread_ui_overflow)
                self._thread_ui_overflow_keys.pop(key, None)
                self._forget_thread_ui_token(old_token)
            if len(self._thread_ui_overflow) >= 512:
                drop_index = next((i for i, item in enumerate(self._thread_ui_overflow) if item[4] is not None), None)
                if drop_index is None:
                    return None
                dropped = self._thread_ui_overflow.pop(drop_index)
                heapq.heapify(self._thread_ui_overflow)
                if dropped[4] is not None and self._thread_ui_overflow_keys.get(dropped[4]) == dropped[1]:
                    self._thread_ui_overflow_keys.pop(dropped[4], None)
                self._forget_thread_ui_token(dropped[1])
            with self._thread_ui_cancel_lock:
                self._thread_ui_known_tokens.add(token)
            heapq.heappush(self._thread_ui_overflow, (due, token, func, args, key))
            if key is not None:
                self._thread_ui_overflow_keys[key] = token
        return token
    def _take_thread_ui_overflow(self, limit):
        result = []
        with self._thread_ui_overflow_lock:
            count = min(max(0, int(limit)), len(self._thread_ui_overflow))
            for _ in range(count):
                item = heapq.heappop(self._thread_ui_overflow)
                result.append(item)
                key, token = item[4], item[1]
                if key is not None and self._thread_ui_overflow_keys.get(key) == token:
                    self._thread_ui_overflow_keys.pop(key, None)
        return result
    def _thread_ui_coalesce_key(self, func, args):
        target = getattr(func, '__func__', func)
        name = str(getattr(target, '__name__', '') or '')
        lower = name.lower()
        owner = id(getattr(func, '__self__', None))
        def part(value):
            if value is None or isinstance(value, (str, int, float, bool, bytes)):
                return (type(value).__name__, value)
            if isinstance(value, (tuple, list)) and len(value) <= 8:
                return (type(value).__name__, tuple(part(item) for item in value))
            return (type(value).__name__, id(value))
        try:
            args_key = tuple(part(value) for value in args)
        except Exception:
            args_key = (id(args),)
        if lower == '<lambda>':
            code = getattr(target, '__code__', None)
            if code is None:
                return None
            closure = []
            try:
                for cell in getattr(target, '__closure__', ()) or ():
                    try:
                        closure.append(part(cell.cell_contents))
                    except Exception:
                        closure.append(('empty',))
            except Exception:
                pass
            defaults = part(getattr(target, '__defaults__', None))
            return ('lambda', owner, id(code), tuple(closure), defaults, args_key)
        if not name:
            return None
        repeatable = lower.endswith(('_loop', '_poll', '_tick', '_watch')) or lower.startswith(('_update_status', '_refresh_status', '_poll_', '_scan_loop', '_drain_queue', '_responsive_', '_watch_loop', '_animate_loop'))
        if not repeatable:
            return None
        return (owner, id(target), args_key)
    def _pump_thread_ui_queue(self):
        resizing = bool(getattr(self, '_resize_active', False))
        max_pull = 96 if resizing else 24
        pending_limit = 384
        pulled = 0
        while pulled < max_pull and len(self._thread_ui_pending) < pending_limit:
            try:
                task = self._thread_ui_dispatch_queue.get_nowait()
            except queue.Empty:
                break
            due, token, func, args = task
            if self._thread_token_cancelled(token, consume=True):
                self._forget_thread_ui_coalesce_key(token)
                continue
            key = self._thread_ui_coalesce_key(func, args)
            if key is not None and key in self._thread_ui_pending_coalesce:
                self._forget_thread_ui_token(token)
                continue
            if key is not None:
                self._thread_ui_pending_coalesce.add(key)
            heapq.heappush(self._thread_ui_pending, (due, token, func, args, key))
            pulled += 1
        if pulled < max_pull and len(self._thread_ui_pending) < pending_limit:
            for due, token, func, args, overflow_key in self._take_thread_ui_overflow(max_pull - pulled):
                if self._thread_token_cancelled(token, consume=True):
                    self._forget_thread_ui_coalesce_key(token)
                    continue
                key = overflow_key or (self._thread_ui_coalesce_key(func, args) if resizing else None)
                if key is not None and key in self._thread_ui_pending_coalesce:
                    self._forget_thread_ui_token(token)
                    continue
                if key is not None:
                    self._thread_ui_pending_coalesce.add(key)
                heapq.heappush(self._thread_ui_pending, (due, token, func, args, key))
                pulled += 1
        if not resizing:
            now = time.monotonic()
            processed = 0
            started = time.perf_counter()
            while self._thread_ui_pending and processed < 6 and time.perf_counter() - started < 0.0045:
                due, token, func, args, key = self._thread_ui_pending[0]
                if self._thread_token_cancelled(token, consume=True):
                    heapq.heappop(self._thread_ui_pending)
                    if key is not None:
                        self._thread_ui_pending_coalesce.discard(key)
                    continue
                if due > now:
                    break
                heapq.heappop(self._thread_ui_pending)
                if key is not None:
                    self._thread_ui_pending_coalesce.discard(key)
                self._forget_thread_ui_token(token)
                processed += 1
                try:
                    func(*args)
                except Exception as exc:
                    try:
                        self.report_callback_exception(type(exc), exc, exc.__traceback__)
                    except Exception:
                        pass
        try:
            if self.winfo_exists():
                busy = self._thread_ui_dispatch_queue.qsize() or self._thread_ui_overflow or self._thread_ui_pending
                delay = 50 if resizing else 10 if busy else 35
                self.after(delay, self._pump_thread_ui_queue)
        except Exception:
            pass
    def report_callback_exception(self, exc_type, exc_value, exc_tb):
        _report_rotools_error(exc_type, exc_value, exc_tb, self)
    def __init__(self):
        self._ui_thread_id = threading.get_ident()
        self._ui_dispatch_closed = False
        self._thread_ui_dispatch_queue = queue.Queue(maxsize=256)
        self._thread_ui_overflow = []
        self._thread_ui_overflow_keys = {}
        self._thread_ui_overflow_lock = threading.Lock()
        self._thread_ui_coalesce_lock = threading.Lock()
        self._thread_ui_coalesce_tokens = {}
        self._thread_ui_token_coalesce_keys = {}
        self._thread_ui_pending = []
        self._thread_ui_pending_coalesce = set()
        self._thread_ui_cancelled = set()
        self._thread_ui_known_tokens = set()
        self._thread_ui_cancel_lock = threading.Lock()
        self._thread_ui_counter = 0
        self._thread_ui_counter_lock = threading.Lock()
        super().__init__()
        try:
            self.withdraw()
        except Exception:
            pass
        self.after(12, self._pump_thread_ui_queue)
        self._routils_splash = None
        self._routils_splash_canvas = None
        self._routils_splash_photo = None
        self._routils_splash_image_done = threading.Event()
        self._routils_splash_image_applied = False
        self._routils_splash_started_at = time.monotonic()
        self._create_startup_splash()
        self._console_history = self._load_console_history()
        self._console_undo_stack = []
        self._console_save_job = None
        self._console_original_stdout = sys.stdout
        sys.stdout = _ConsoleStream(self, self._console_original_stdout)
        self.settings = load_settings()
        self.settings.pop('multi_instance_enabled', None)
        self.settings.pop('discord_rpc_enabled', None)
        configured_discord_id = str(self.settings.get('discord_application_id') or DISCORD_APPLICATION_ID).strip()
        if not configured_discord_id.isdigit():
            configured_discord_id = DISCORD_APPLICATION_ID
        self.settings['discord_application_id'] = configured_discord_id
        self.discord_application_id_var = tk.StringVar(value=configured_discord_id)
        self.discord_rpc_status_var = tk.StringVar(value='Starting Discord RPC...')
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
        _initial_palette = dict(THEMES[DEFAULT_THEME] if _t == 'Custom' else THEMES.get(_t, THEMES[DEFAULT_THEME]))
        if _t == 'Custom':
            _saved_custom_palette = self.settings.get('custom_theme', {})
            if isinstance(_saved_custom_palette, dict):
                for _color_key, _fallback_color in THEMES[DEFAULT_THEME].items():
                    _saved_color = _saved_custom_palette.get(_color_key, _fallback_color)
                    _initial_palette[_color_key] = _saved_color if isinstance(_saved_color, str) and re.fullmatch(r'#[0-9a-fA-F]{6}', _saved_color) else _fallback_color
        apply_visual_polish(self, theme=UI_THEME, palette=_initial_palette)
        self.title('RoUtils')
        saved_geometry = str(self.settings.get('window_geometry', '') or '')
        screen_width = max(800, int(self.winfo_screenwidth() or 1920))
        screen_height = max(600, int(self.winfo_screenheight() or 1080))
        if re.match(r'^\d+x\d+(?:[+-]\d+[+-]\d+)?$', saved_geometry):
            match = re.match(r'^(\d+)x(\d+)(?:([+-]\d+)([+-]\d+))?$', saved_geometry)
            width = min(int(match.group(1)), max(700, screen_width - 40))
            height = min(int(match.group(2)), max(420, screen_height - 80))
            x, y = match.group(3), match.group(4)
            if x is None or y is None:
                x, y = str(max(0, (screen_width-width)//2)), str(max(0, (screen_height-height)//2))
            else:
                x = str(max(0, min(int(x), screen_width-width)))
                y = str(max(0, min(int(y), screen_height-height)))
            startup_geometry = f'{width}x{height}{int(x):+d}{int(y):+d}'
        else:
            width = min(1400, max(900, screen_width - 80))
            height = min(800, max(560, screen_height - 100))
            startup_geometry = f'{width}x{height}+{max(0,(screen_width-width)//2)}+{max(0,(screen_height-height)//2)}'
        self.geometry(startup_geometry)
        self._responsive_reference_width = max(1, int(width))
        self._responsive_reference_height = max(1, int(height))
        try:
            self._responsive_base_tk_scaling = float(self.tk.call('tk', 'scaling'))
        except Exception:
            self._responsive_base_tk_scaling = float(getattr(self, '_dpi_scale', 1.0) or 1.0)
        self._responsive_applied_ratio = 1.0
        self._responsive_scale_job = None
        self.minsize(620, 380)
        self.resizable(True, True)
        self._setup_custom_titlebar()
        self.after(120, self._restore_windows_taskbar_presence)
        if '--tray' in sys.argv:
            self.after(180, self._hide_to_tray)
        else:
            self.after(180, self._restore_windows_taskbar_presence)
        self.bind('<Map>', lambda _e: self.after_idle(self._restore_windows_taskbar_presence), add='+')
        self.bind('<Map>', lambda _e: self.after(250, self._apply_streamer_mode), add='+')
        self.after_idle(self._restore_windows_taskbar_presence)
        self.after(250, self._apply_streamer_mode)
        try:
            if os.name == 'nt':
                self.iconbitmap(ICON_PATH)
            elif os.path.isfile(ICON_PATH):
                self._routils_icon_image = tk.PhotoImage(file=ICON_PATH)
                self.iconphoto(True, self._routils_icon_image)
        except Exception:
            pass
        self.protocol('WM_DELETE_WINDOW', self._on_close)
        self._geometry_save_job = None
        self._geometry_configure_idle_job = None
        self._geometry_pending_key = None
        self._resize_idle_job = None
        self._resize_active = False
        self._native_resize_in_progress = False
        self._native_size_move_active = False
        self._resize_finish_pending = False
        self._deferred_canvas_widths = {}
        self._resize_deferred_jobs = {}
        self._resize_release_jobs = []
        self._resize_release_job = None
        self._resize_canvas_flush_job = None
        self._settings_save_deferred = False
        self._native_resize_hwnd = 0
        self._native_resize_proc = None
        self._native_resize_api = None
        self._native_resize_lib = None
        self._last_geometry_dimensions = None
        self._ui_jobs = {}
        self._global_scroll_support_installed = False
        self._history_render_signature = None
        self._client_tab_active = False
        self.bind('<Configure>', self._on_geometry_configure, add='+')
        self.bind('<FocusIn>', self._app_focus_changed, add='+')
        self.bind('<FocusOut>', lambda _e: self.after(180, self._app_focus_changed), add='+')
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
        self._emote_typing_lock = threading.Lock()
        self._emote_typing_active = False
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
        self._tab_nav_refresh_job = None
        self._tab_nav_layout_signature = None
        self._tab_nav.bind('<Configure>', self._schedule_tab_nav_refresh, add='+')
        self._setup_tab_nav_styles()
        self.nb = ttk.Notebook(self, style='RoUtils.Hidden.TNotebook')
        self.nb.pack(fill='both', expand=True, padx=8, pady=(0, 8))
        self.tab_viewer = ttk.Frame(self.nb)
        self.nb.add(self.tab_viewer, text=UI_TEXT['f5'])
        self.hpaned = ttk.PanedWindow(self.tab_viewer, orient='horizontal')
        self.hpaned.pack(fill='both', expand=True)
        self.viewer_root = ttk.Frame(self.hpaned)
        self.hpaned.add(self.viewer_root, weight=4)
        _set_pane_minsize(self.hpaned, self.viewer_root, VIEWER_MIN_WIDTH)
        self.replacer = ReplacerPane(self.hpaned)
        self.hpaned.add(self.replacer, weight=1)
        _set_pane_minsize(self.hpaned, self.replacer, REPLACER_MIN_WIDTH)
        self.hpaned.bind('<B1-Motion>', lambda e: self._clamp_hsash())
        self.hpaned.bind('<ButtonRelease-1>', self._on_hsash_release)
        self.viewer_collapsed = False
        self._restore_geom: Optional[Tuple[int, int, int, int]] = None
        self._saved_sash: Optional[int] = None
        self.collapse_btn = ttk.Button(self.replacer.top, text=UI_TEXT['g5'], width=2, command=self._toggle_viewer_pane)
        self.collapse_btn.pack(side='left', padx=(0, 4), before=self.replacer.action_bar)
        default_db, default_shards = default_paths()
        saved_db = str(self.settings.get('db_path') or '')
        saved_shards = str(self.settings.get('shard_root') or '')
        if os.name != 'nt':
            self.db_path, self.shard_root = resolve_storage_selection(saved_db, saved_shards, default_db, default_shards)
        else:
            self.db_path = saved_db or default_db
            self.shard_root = saved_shards or default_shards
        self.seen_hashes: set = set()
        self.items_by_iid: Dict[str, ScanItem] = {}
        self.items_by_hash: Dict[str, ScanItem] = {}
        self._tree_insert_pending = []
        self._tree_insert_pending_index = 0
        self._tree_insert_pending_job = None
        self._filter_render_job = None
        self._filter_render_generation = 0
        self._filter_render_phase = None
        self._filter_render_snapshot = []
        self._filter_render_index = 0
        self._filter_render_text = ''
        self._filter_clear_iids = []
        self._filter_clear_index = 0
        self._filter_render_last_iid = None
        self.new_items_q: 'queue.Queue[List[ScanItem]]' = queue.Queue()
        self.watching = False
        self.stop_event = threading.Event()
        self._watch_initial_scan_done = threading.Event()
        self._watch_loading_active = False
        self.scan_thread: Optional[threading.Thread] = None
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
        self._scan_max_rows_value = max(0, int(saved_max_rows))
        self.max_rows.trace_add('write', self._update_scan_max_rows_value)
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
        self.anti_afk_enabled = tk.BooleanVar(value=bool(self.settings.get('anti_afk_enabled', False)))
        self._anti_afk_last_action = time.monotonic()
        self._anti_afk_in_progress = False
        self.emote_names = ['/e dance1', '/e dance2', '/e dance3', '/e cheer', '/e laugh', '/e wave', '/e point']
        saved_emotes = self.settings.get('emote_binds', {})
        self.emote_binds = {name: str(saved_emotes.get(name, '') or '').upper() for name in self.emote_names} if isinstance(saved_emotes, dict) else {name: '' for name in self.emote_names}
        saved_nav_binds = self.settings.get('emote_nav_binds', {})
        self._emote_nav_binds = {action: str(saved_nav_binds.get(action, '') or '').upper() for action in ('previous', 'next', 'play')} if isinstance(saved_nav_binds, dict) else {'previous': '', 'next': '', 'play': ''}
        self._emote_hotkeys_enabled = bool(self.settings.get('emote_hotkeys_enabled', True))
        self._emote_hotkeys_toggle_key = str(self.settings.get('emote_hotkeys_toggle_key', '') or '').upper()
        self._emote_toggle_hotkey_capture_active = False
        self._emote_toggle_capture_dialog = None
        self._emote_current_index = 0
        self._emote_control_capture_action = None
        self._emote_controls_window = None
        self._emote_controls_labels = {}
        self._emote_hud = None
        self._emote_hud_canvas = None
        self._emote_hud_text = None
        self._emote_hud_position_job = None
        self._emote_capture_dialog = None
        self.launch_on_startup = tk.BooleanVar(value=self.settings.get('launch_on_startup', False))
        self.launch_on_tray = tk.BooleanVar(value=self.settings.get('launch_on_tray', False))
        self.hide_to_tray_on_close = tk.BooleanVar(value=self.settings.get('hide_to_tray_on_close', False))
        self.after_idle(self._update_kill_routils_visibility)
        if not self.settings.get('auto_update_v525_migrated', False):
            self.settings['auto_update'] = True
            self.settings['auto_update_v525_migrated'] = True
        self.auto_update = tk.BooleanVar(value=bool(self.settings.get('auto_update', True)))
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
        self._fflag_history_lock = threading.RLock()
        self._fflag_history_items = self._fflag_history_load()
        self._fflag_history_snapshot = self._fflag_history_snapshot_from_flags(self.fflag_flags)
        self._fflag_history_snapshot_ready = True
        self._fflag_apply_state_lock = threading.Lock()
        self._fflag_apply_in_progress = False
        self._fflag_apply_pending = False
        self._fflag_apply_pending_silent = True
        self._lazy_tabs = {}
        self._lazy_tab_ids = {}
        self.nb.bind('<<NotebookTabChanged>>', self._lazy_tab_changed, add='+')
        self._build_home_tab()
        lazy_builders = {UI_TEXT['f5']: self._lazy_build_cache, UI_TEXT['h5']: self._build_fflag_tab, UI_TEXT['i5']: self._build_emote_manager_tab, UI_TEXT['j5']: self._build_ai_tab, UI_TEXT['k5']: self._build_utils_tab, UI_TEXT['l5']: self._build_cconfigs_tab, UI_TEXT['m5']: self._build_subplace_joiner_tab, UI_TEXT['n5']: self._build_server_viewer_tab, UI_TEXT['o5']: self._build_history_tab, UI_TEXT['p5']: self._build_client_tab, UI_TEXT['q5']: self._build_themes_tab, UI_TEXT['r5']: self._build_settings_tab, UI_TEXT['s5']: self._build_plugins_tab, UI_TEXT['t5']: self._build_release_notes_tab, UI_TEXT['u5']: self._build_console_tab}
        for tab_name in (UI_TEXT['f5'], UI_TEXT['h5'], UI_TEXT['i5'], UI_TEXT['j5'], UI_TEXT['l5'], UI_TEXT['k5'], UI_TEXT['m5'], UI_TEXT['n5'], UI_TEXT['o5'], UI_TEXT['p5'], UI_TEXT['q5'], UI_TEXT['r5'], UI_TEXT['s5'], UI_TEXT['t5'], UI_TEXT['u5']):
            if tab_name == UI_TEXT['f5']:
                tab = self.tab_viewer
            else:
                tab = ttk.Frame(self.nb)
                self.nb.add(tab, text=tab_name)
            self._lazy_tab_ids[tab_name] = str(tab)
            self._lazy_tabs[str(tab)] = (tab_name, lazy_builders[tab_name], tab)
            if tab_name != UI_TEXT['f5']:
                ttk.Label(tab, text=UI_TEXT['v5'], foreground='#9aa0a6').pack(expand=True)
        self._reorder_tabs()
        self._refresh_tab_nav()
        self.after(80, self._initial_tab_order_post_map)
        if self.nb.tabs():
            preferred = str(self.settings.get('selected_tab', UI_TEXT['w5']))
            if preferred == 'Themes':
                preferred = UI_TEXT['q5']
            selected_id = next((tid for tid in self.nb.tabs() if self.nb.tab(tid, 'text') == preferred), None)
            if selected_id is None:
                selected_id = next((tid for tid in self.nb.tabs() if self.nb.tab(tid, 'text') == UI_TEXT['w5']), self.nb.tabs()[0])
            self.nb.select(selected_id)
        self.after_idle(self._lazy_tab_changed)
        self.after_idle(self._install_global_scroll_support)
        self._start_history_watcher()
        self._start_version_check()
        self._install_startup_shortcut()
        if '--tray' in sys.argv:
            self.after_idle(self._hide_to_tray)
        self._start_global_hotkeys()
        self.after(UI_HOTKEY_INTERVAL_MS, self._process_global_hotkeys)
        self.after(UI_QUICK_PANEL_INTERVAL_MS, self._quick_panel_tick)
        self.after(800, self._restore_enabled_plugins)
        if self.settings.get('viewer_collapsed'):
            self.after(250, self._apply_saved_viewer_state)
        self.after(UI_QUEUE_INTERVAL_MS, self._drain_queue)
        self.after(200, self._save_settings)
        self.after(15000, self._fflag_auto_apply_tick)
        self.after(15000, self._anti_afk_tick)
        self._discord_rpc = _RoUtilsDiscordRPC(self.discord_application_id_var.get(), self._discord_rpc_status_changed)
        self._discord_rpc.set_enabled(True)
        self._discord_rpc.start()
        self.after(150, self._refresh_discord_rpc_activity)
        self.after(int(DISCORD_RPC_INTERVAL * 1000), self._discord_rpc_poll_tick)
        if self._routils_splash is not None:
            self.after(90, self._startup_mint_theme_cycle)
            self.after(420, self._finish_startup_splash)
    def _startup_mint_theme_cycle(self):
        if getattr(self, '_startup_mint_theme_cycle_done', False):
            return
        self._startup_mint_theme_cycle_done = True
        try:
            theme_id = next((tab_id for tab_id in self.nb.tabs() if str(self.nb.tab(tab_id, 'text')) == UI_TEXT['q5']), None)
            if theme_id is not None and not hasattr(self, 'theme_var'):
                info = self._lazy_tabs.get(str(theme_id))
                if info is not None:
                    tab_name, builder, placeholder = info
                    try:
                        self.nb.forget(placeholder)
                    except Exception:
                        pass
                    try:
                        placeholder.destroy()
                    except Exception:
                        pass
                    self._lazy_tabs.pop(str(theme_id), None)
                    self._lazy_tab_ids.pop(tab_name, None)
                    builder()
                    self._reorder_tabs()
                    self._refresh_tab_nav()
            if not hasattr(self, 'theme_var'):
                return
            original_theme = str(self.settings.get('theme', self.theme_var.get()) or DEFAULT_THEME)
            if original_theme not in THEMES and original_theme != 'Custom':
                original_theme = DEFAULT_THEME
            theme_listbox = getattr(self, '_theme_listbox', None)
            def select_theme_item(name):
                try:
                    if theme_listbox is None or not theme_listbox.winfo_exists():
                        return
                    names = theme_listbox.get(0, 'end')
                    if name in names:
                        index = names.index(name)
                        theme_listbox.selection_clear(0, 'end')
                        theme_listbox.selection_set(index)
                        theme_listbox.see(index)
                except Exception:
                    pass
            try:
                self.theme_var.set('Mint')
                select_theme_item('Mint')
                self._apply_theme()
                self.update_idletasks()
            except Exception:
                pass
            finally:
                try:
                    self.theme_var.set(original_theme)
                    select_theme_item(original_theme)
                    self._apply_theme()
                except Exception:
                    self.settings['theme'] = original_theme
                    try:
                        _CURRENT_PALETTE.update(THEMES.get(original_theme, THEMES[DEFAULT_THEME]))
                    except Exception:
                        pass
        except Exception:
            pass
    def _create_startup_splash(self):
        if '--tray' in sys.argv:
            return
        self._routils_splash_started_at = time.monotonic()
        try:
            try:
                self.attributes('-alpha', 0.0)
                self.deiconify()
            except Exception:
                try:
                    self.withdraw()
                except Exception:
                    pass
            splash = tk.Toplevel(self)
            splash._skip_custom_chrome = True
            splash._skip_popup_centering = True
            splash.overrideredirect(True)
            palette = _CURRENT_PALETTE if isinstance(_CURRENT_PALETTE, dict) else THEMES[DEFAULT_THEME]
            accent = palette.get('accent', '#7f8cff')
            bg = palette.get('bg_dark', '#1b1b1c')
            width, height = 440, 176
            screen_w = int(splash.winfo_screenwidth() or 1920)
            screen_h = int(splash.winfo_screenheight() or 1080)
            x = max(0, (screen_w - width) // 2)
            y = max(0, (screen_h - height) // 2)
            splash.geometry(f'{width}x{height}+{x}+{y}')
            splash.configure(bg=accent, highlightthickness=2, highlightbackground=accent, bd=0)
            try:
                splash.attributes('-topmost', True)
            except Exception:
                pass
            canvas = tk.Canvas(splash, width=width - 4, height=height - 4, bg=bg, highlightthickness=0, bd=0)
            canvas.place(x=2, y=2, width=width - 4, height=height - 4)
            canvas.create_text((width - 4) // 2 + 1, 65, text=UI_TEXT['x5'], fill='#111111', font=('Segoe UI Semibold', 25))
            canvas.create_text((width - 4) // 2, 64, text=UI_TEXT['x5'], fill='#ffffff', font=('Segoe UI Semibold', 25))
            for glow_dx, glow_dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, -1), (-1, 1), (1, 1)):
                canvas.create_text((width - 4) // 2 + glow_dx, 108 + glow_dy, text=UI_TEXT['v5'], fill=accent, font=('Segoe UI Semibold', 11), tags=('loading_glow',))
            canvas.create_text((width - 4) // 2, 108, text=UI_TEXT['v5'], fill='#ffffff', font=('Segoe UI Semibold', 11), tags=('loading_text',))
            canvas.create_rectangle(110, 137, 330, 141, fill='#333338', outline='')
            canvas.create_rectangle(110, 137, 110, 141, fill=accent, outline='', tags=('loading_bar',))
            self._routils_splash = splash
            self._routils_splash_canvas = canvas
            self._routils_splash_photo = None
            self._routils_splash_image_applied = False
            splash.deiconify()
            splash.lift()
            try:
                splash.attributes('-topmost', True)
            except Exception:
                pass
            splash.update_idletasks()
            splash.update()
            self._routils_splash_animation_step = 0
            self.after(45, self._animate_startup_splash)
            if os.path.isfile(SPLASH_IMAGE_PATH):
                self._apply_startup_splash_image()
            threading.Thread(target=self._download_startup_splash_image, daemon=True, name='RoUtilsSplashDownload').start()
            self.after(100, self._poll_startup_splash_image)
        except Exception:
            self._routils_splash = None
            try:
                self.attributes('-alpha', 1.0)
                self.deiconify()
            except Exception:
                pass
    def _animate_startup_splash(self):
        splash = getattr(self, '_routils_splash', None)
        canvas = getattr(self, '_routils_splash_canvas', None)
        if splash is None or canvas is None:
            return
        try:
            if not splash.winfo_exists():
                return
            step = (getattr(self, '_routils_splash_animation_step', 0) + 11) % 221
            self._routils_splash_animation_step = step
            canvas.coords('loading_bar', 110, 137, 110 + step, 141)
            splash.lift()
            try:
                splash.attributes('-topmost', True)
            except Exception:
                pass
            self.after(45, self._animate_startup_splash)
        except Exception:
            pass
    def _download_startup_splash_image(self):
        try:
            _ensure_splash_image_file()
        finally:
            self._routils_splash_image_done.set()
    def _apply_startup_splash_image(self):
        try:
            splash = self._routils_splash
            canvas = self._routils_splash_canvas
            if splash is None or canvas is None or not splash.winfo_exists() or not os.path.isfile(SPLASH_IMAGE_PATH):
                return
            canvas.update_idletasks()
            target_width = max(1, int(canvas.winfo_width() or 436))
            target_height = max(1, int(canvas.winfo_height() or 172))
            with Image.open(SPLASH_IMAGE_PATH) as source:
                resampling_group = getattr(Image, 'Resampling', Image)
                resampling = getattr(resampling_group, 'LANCZOS', getattr(resampling_group, 'BICUBIC', 3))
                image = source.convert('RGB').resize((target_width, target_height), resampling)
            photo = ImageTk.PhotoImage(image, master=splash)
            canvas.delete('splash_background')
            canvas.create_image(0, 0, image=photo, anchor='nw', tags=('splash_background',))
            canvas.tag_lower('splash_background')
            self._routils_splash_photo = photo
            self._routils_splash_image_applied = True
        except Exception:
            pass
    def _poll_startup_splash_image(self):
        splash = getattr(self, '_routils_splash', None)
        if splash is None:
            return
        try:
            if not splash.winfo_exists():
                return
            if self._routils_splash_image_done.is_set() and not self._routils_splash_image_applied:
                self._apply_startup_splash_image()
            self.after(100, self._poll_startup_splash_image)
        except Exception:
            pass
    def _finish_startup_splash(self):
        splash = getattr(self, '_routils_splash', None)
        if splash is None:
            try:
                self.attributes('-alpha', 1.0)
                self.deiconify()
            except Exception:
                pass
            return
        try:
            if not splash.winfo_exists():
                self._routils_splash = None
                self.attributes('-alpha', 1.0)
                self._ensure_main_window_visible()
                return
            elapsed = time.monotonic() - self._routils_splash_started_at
            if elapsed < 1.35:
                self.after(70, self._finish_startup_splash)
                return
            if not self._routils_splash_image_done.is_set() and elapsed < 2.2:
                self.after(80, self._finish_startup_splash)
                return
            self._routils_splash = None
            try:
                splash.destroy()
            except Exception:
                pass
            try:
                self.attributes('-topmost', False)
            except Exception:
                pass
            try:
                self.attributes('-alpha', 1.0)
            except Exception:
                pass
            self._ensure_main_window_visible()
        except Exception:
            try:
                if splash.winfo_exists():
                    splash.destroy()
            except Exception:
                pass
            self._routils_splash = None
            try:
                self.attributes('-alpha', 1.0)
                self.deiconify()
            except Exception:
                pass
    def _is_resize_deferred_ui_key(self, key):
        return key in ('cache_toolbar', 'settings_region', 'history_region') or str(key).startswith(('ai_region_', 'settings_scrollbar_'))
    def _schedule_ui(self, key, delay_ms, callback):
        jobs = getattr(self, '_ui_jobs', None)
        if jobs is None:
            jobs = self._ui_jobs = {}
        if getattr(self, '_resize_active', False) and self._is_resize_deferred_ui_key(key):
            old = jobs.pop(key, None)
            if old:
                try:
                    self.after_cancel(old)
                except Exception:
                    pass
            self._resize_deferred_jobs[key] = (max(0, int(delay_ms or 0)), callback)
            return
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
        if getattr(self, '_resize_active', False) and self._is_resize_deferred_ui_key(key):
            self._resize_deferred_jobs[key] = (30, callback)
            return
        try:
            callback()
        except Exception:
            pass
    def _lazy_build_cache(self):
        if getattr(self, '_cache_built', False):
            return
        self._build_viewer_widgets()
        self._cache_built = True
        self._schedule_startup_layouts()
        self.after_idle(self._update_status)
    def _schedule_startup_layouts(self):
        for delay in (80, 220, 500, 900):
            try:
                self.after(delay, self._apply_startup_layouts)
            except Exception:
                pass
    def _lazy_tab_changed(self, _event=None):
        self._refresh_tab_nav()
        try:
            self._refresh_discord_rpc_activity()
        except Exception:
            pass
        try:
            tab_id = self.nb.select()
        except Exception:
            return
        if not tab_id:
            return
        info = self._lazy_tabs.get(str(tab_id))
        if not info:
            return
        tab_name, builder, placeholder = info
        target_name = tab_name
        try:
            self.nb.unbind('<<NotebookTabChanged>>')
            if tab_name in (UI_TEXT['s5'], UI_TEXT['t5'], UI_TEXT['h5']):
                builder(placeholder)
                self._reorder_tabs()
                self._refresh_tab_nav()
            elif tab_name != UI_TEXT['f5']:
                self.nb.forget(placeholder)
                placeholder.destroy()
                builder()
                self._reorder_tabs()
                self._refresh_tab_nav()
            else:
                builder()
        except Exception as exc:
            try:
                if tab_name in (UI_TEXT['s5'], UI_TEXT['t5'], UI_TEXT['h5']) and placeholder.winfo_exists():
                    for child in placeholder.winfo_children():
                        child.destroy()
                    ttk.Label(placeholder, text=UI_TEXT['y5'].format(p0=tab_name, p1=exc), foreground='#ff8a80').pack(expand=True, padx=16, pady=16)
                elif tab_name != UI_TEXT['f5'] and placeholder.winfo_exists():
                    placeholder.destroy()
            except Exception:
                pass
            try:
                self._console_log(UI_TEXT['y5'].format(p0=tab_name, p1=exc))
            except Exception:
                pass
        finally:
            try:
                self.nb.bind('<<NotebookTabChanged>>', self._lazy_tab_changed, add='+')
            except Exception:
                pass
        self._lazy_tabs.pop(str(tab_id), None)
        self._lazy_tab_ids.pop(tab_name, None)
        self._client_tab_active = target_name == UI_TEXT['p5']
        try:
            for current_id in self.nb.tabs():
                if self.nb.tab(current_id, 'text') == target_name:
                    self.nb.select(current_id)
                    break
        except Exception:
            pass
        try:
            self.after_idle(self._install_global_scroll_support)
        except Exception:
            pass
    def _apply_saved_viewer_state(self):
        if not getattr(self, '_cache_built', False):
            return
        try:
            if self.settings.get('viewer_collapsed'):
                self._toggle_viewer_pane()
        except Exception:
            pass
    def _start_linux_global_hotkeys(self):
        if getattr(self, '_linux_hotkey_starting', False):
            return
        self._linux_hotkey_starting = True
        def worker():
            try:
                from pynput import keyboard
                pressed = set()
                state = {'ctrl_f3': False}
                aliases = {'ENTER': 'RETURN', 'ESC': 'ESCAPE', 'CTRL_L': 'CTRL', 'CTRL_R': 'CTRL', 'CONTROL_L': 'CTRL', 'CONTROL_R': 'CTRL', 'SHIFT_L': 'SHIFT', 'SHIFT_R': 'SHIFT', 'ALT_L': 'ALT', 'ALT_R': 'ALT', 'ALT_GR': 'ALT'}
                def token_for(key):
                    try:
                        char = key.char
                    except Exception:
                        char = None
                    if char:
                        token = char.upper()
                    else:
                        token = str(key).split('.')[-1].replace('Key.', '').upper()
                    return aliases.get(token, token)
                def active_bindings():
                    bindings = [('quick_panel', 'F7', {})]
                    toggle_key = str(getattr(self, '_emote_hotkeys_toggle_key', '') or '').upper()
                    if toggle_key:
                        bindings.append(('emote_hotkeys_toggle', toggle_key, {'key': toggle_key}))
                    if bool(getattr(self, '_emote_hotkeys_enabled', True)):
                        for action, configured_key in getattr(self, '_emote_nav_binds', {}).items():
                            configured_key = str(configured_key or '').upper()
                            if configured_key:
                                bindings.append(('emote_nav', configured_key, {'key': configured_key, 'action': action}))
                        for dance, configured_key in getattr(self, 'emote_binds', {}).items():
                            configured_key = str(configured_key or '').upper()
                            if configured_key:
                                bindings.append(('emote', configured_key, {'key': configured_key, 'dance': dance}))
                    for binding in self.fflag_hotkeys:
                        configured_key = str(binding.get('key', '')).upper()
                        if configured_key:
                            bindings.append(('fflag', configured_key, binding.copy()))
                    for fps, configured_key in self.fps_hotkeys.items():
                        configured_key = str(configured_key or '').upper()
                        if configured_key:
                            bindings.append(('fps', configured_key, {'fps': int(fps), 'key': configured_key}))
                    return bindings
                def on_press(key):
                    token = token_for(key)
                    if not token or token in pressed:
                        return
                    pressed.add(token)
                    if 'F3' in pressed and 'CTRL' in pressed:
                        if not state['ctrl_f3']:
                            state['ctrl_f3'] = True
                            self._global_hotkey_q.put(('emote_controls_toggle', {}))
                        return
                    if getattr(self, '_emote_control_capture_action', None) or getattr(self, '_emote_toggle_hotkey_capture_active', False) or self._emote_typing_active:
                        return
                    if token in {'CTRL', 'SHIFT', 'ALT', 'CMD', 'SUPER'}:
                        return
                    for kind, configured_key, binding in active_bindings():
                        normalized = aliases.get(str(configured_key).upper(), str(configured_key).upper())
                        if token != normalized:
                            continue
                        if kind in ('emote', 'emote_nav') and not sober_is_focused(self.fflag_pid or _fflag_find_pid()):
                            continue
                        self._global_hotkey_q.put((kind, binding))
                        break
                def on_release(key):
                    token = token_for(key)
                    pressed.discard(token)
                    if 'F3' not in pressed or 'CTRL' not in pressed:
                        state['ctrl_f3'] = False
                listener = keyboard.Listener(on_press=on_press, on_release=on_release)
                self._linux_hotkey_listener = listener
                listener.start()
                while listener.is_alive() and not self._hotkey_stop.wait(0.25):
                    pass
                listener.stop()
            except Exception as error:
                try:
                    self._global_hotkey_q.put(('linux_hotkey_error', {'message': str(error)}))
                except Exception:
                    pass
            finally:
                self._linux_hotkey_starting = False
        self._hotkey_thread = threading.Thread(target=worker, name='RoUtilsLinuxGlobalHotkeys', daemon=True)
        self._hotkey_thread.start()
    def _start_global_hotkeys(self):
        if self._hotkey_thread and self._hotkey_thread.is_alive():
            return
        if sys.platform.startswith('linux'):
            self._start_linux_global_hotkeys()
            return
        if sys.platform != 'win32':
            return
        def worker():
            user32 = ctypes.windll.user32
            toggle_was_down = False
            while not self._hotkey_stop.is_set():
                try:
                    ctrl_down = bool(user32.GetAsyncKeyState(0x11) & 32768)
                    f3_vk = fflag_key_to_vk('F3') or 0x72
                    f3_down = bool(user32.GetAsyncKeyState(f3_vk) & 32768)
                    toggle_down = ctrl_down and f3_down
                    if toggle_down and not toggle_was_down:
                        self._global_hotkey_q.put(('emote_controls_toggle', {}))
                    if toggle_down:
                        self._hotkey_prev[f3_vk] = True
                    toggle_was_down = toggle_down
                    if toggle_down:
                        time.sleep(0.025)
                        continue
                    if getattr(self, '_emote_control_capture_action', None):
                        time.sleep(0.025)
                        continue
                    if getattr(self, '_emote_toggle_hotkey_capture_active', False):
                        time.sleep(0.025)
                        continue
                    bindings = [('quick_panel', 'F7', {})]
                    toggle_key = str(getattr(self, '_emote_hotkeys_toggle_key', '') or '').upper()
                    if toggle_key:
                        bindings.append(('emote_hotkeys_toggle', toggle_key, {'key': toggle_key}))
                    if bool(getattr(self, '_emote_hotkeys_enabled', True)):
                        nav_binds = getattr(self, '_emote_nav_binds', {})
                        for action, key in nav_binds.items():
                            key = str(key or '').upper()
                            if key:
                                bindings.append(('emote_nav', key, {'key': key, 'action': action}))
                        emote_binds = getattr(self, 'emote_binds', {})
                        for dance, key in emote_binds.items():
                            key = str(key or '').upper()
                            if key:
                                bindings.append(('emote', key, {'key': key, 'dance': dance}))
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
                        if self._emote_typing_active:
                            continue
                        if down and (not was_down):
                            if kind in ('emote', 'emote_nav'):
                                foreground = user32.GetForegroundWindow()
                                foreground_pid = ctypes.wintypes.DWORD()
                                if not foreground:
                                    continue
                                user32.GetWindowThreadProcessId(foreground, ctypes.byref(foreground_pid))
                                roblox_pid = self.fflag_pid or _fflag_find_pid()
                                if not roblox_pid or int(foreground_pid.value) != int(roblox_pid):
                                    continue
                            self._global_hotkey_q.put((kind, binding))
                except Exception:
                    pass
                time.sleep(0.025)
        self._hotkey_thread = threading.Thread(target=worker, name='RoUtilsGlobalHotkeys', daemon=True)
        self._hotkey_thread.start()
    def _process_global_hotkeys(self):
        if getattr(self, '_resize_active', False):
            if not self._hotkey_stop.is_set():
                self.after(100, self._process_global_hotkeys)
            return
        try:
            while True:
                kind, binding = self._global_hotkey_q.get_nowait()
                if kind == 'quick_panel':
                    self._toggle_quick_panel()
                elif kind == 'emote_controls_toggle':
                    self._toggle_emote_controls()
                elif kind == 'emote_hotkeys_toggle':
                    self._toggle_emote_hotkeys()
                elif kind == 'fps':
                    self._handle_fps_hotkey(binding)
                elif kind == 'emote':
                    if bool(getattr(self, '_emote_hotkeys_enabled', True)):
                        self._handle_emote_hotkey(binding)
                elif kind == 'emote_nav':
                    if bool(getattr(self, '_emote_hotkeys_enabled', True)):
                        self._handle_emote_nav_hotkey(binding)
                elif kind == 'linux_hotkey_error':
                    self._console_log('Linux global hotkeys are unavailable: ' + str(binding.get('message', 'unknown error')))
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
                self._hide_to_tray()
            else:
                self._emote_controls_detach_from_main(no_activate=True)
                self.iconify()
                try:
                    self.after(80, self._emote_controls_ensure_visible_after_hide)
                except Exception:
                    pass
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
                self.fps_value_label.config(text=UI_TEXT['z5'] if fps == 0 else UI_TEXT['a6'].format(p0=fps))
            if hasattr(self, '_fps_text_var'):
                self._fps_text_var.set(str(fps))
        except Exception:
            pass
    def _sync_fps_hotkey_slots(self):
        self.fps_hotkeys = {str(item.get('fps')): str(item.get('key', '')).upper() for item in getattr(self, 'fps_hotkey_slots', []) if int(item.get('fps', 0) or 0) > 0 and item.get('key')}
    def _fps_slot_editor(self, index):
        dlg = tk.Toplevel(self)
        dlg.title(f"{UI_TEXT['p32']}{index + 1}")
        dlg.geometry('430x250')
        dlg.transient(self)
        theme_toplevel(dlg)
        outer = ttk.Frame(dlg, padding=14)
        outer.pack(fill='both', expand=True)
        ttk.Label(outer, text=UI_TEXT['b6']).pack(anchor='w')
        item = self.fps_hotkey_slots[index]
        fps_var = tk.StringVar(value=str(item.get('fps', '') or ''))
        key_var = tk.StringVar(value=str(item.get('key', '') or ''))
        ttk.Entry(outer, textvariable=fps_var).pack(fill='x', pady=(4, 10))
        ttk.Label(outer, text=UI_TEXT['c6']).pack(anchor='w')
        key_entry = ttk.Entry(outer, textvariable=key_var)
        key_entry.pack(fill='x', pady=(4, 6))
        ttk.Label(outer, text=UI_TEXT['d6'], foreground='#9aa0a6').pack(anchor='w')
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
                messagebox.showerror(UI_TEXT['e6'], UI_TEXT['f6'], parent=dlg)
                return
            key = key_var.get().strip().upper()
            if not 1 <= fps <= 240 or not key or (not fflag_key_to_vk(key)):
                messagebox.showerror(UI_TEXT['e6'], UI_TEXT['g6'], parent=dlg)
                return
            for i, other in enumerate(self.fps_hotkey_slots):
                if i != index and other.get('key', '').upper() == key:
                    messagebox.showerror(UI_TEXT['e6'], UI_TEXT['h6'], parent=dlg)
                    return
            self.fps_hotkey_slots[index] = {'fps': fps, 'key': key}
            self._sync_fps_hotkey_slots()
            self._save_settings()
            self._refresh_fps_hotkey_buttons()
            dlg.destroy()
        btns = ttk.Frame(outer)
        btns.pack(fill='x', pady=(14, 0))
        ttk.Button(btns, text=UI_TEXT['i6'], command=save).pack(side='left')
        ttk.Button(btns, text=UI_TEXT['j6'], command=lambda: (self.fps_hotkey_slots.__setitem__(index, {'fps': 0, 'key': ''}), self._sync_fps_hotkey_slots(), self._save_settings(), self._refresh_fps_hotkey_buttons(), dlg.destroy())).pack(side='left', padx=6)
        ttk.Button(btns, text=UI_TEXT['b3'], command=dlg.destroy).pack(side='right')
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
            button.config(text=UI_TEXT['k6'].format(p0=fps, p1=key) if fps and key else UI_TEXT['l6'])
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
            button = ttk.Button(frame, text=UI_TEXT['l6'], width=9, command=lambda slot=index: self._fps_slot_editor(slot), padding=(3, 1))
            button.grid(row=index // 5, column=index % 5, padx=2, pady=2, sticky='ew')
            self._fps_hotkey_buttons[index] = button
        plus_col = len(self.fps_hotkey_slots) % 5
        plus_row = len(self.fps_hotkey_slots) // 5
        if len(self.fps_hotkey_slots) < 15:
            plus = ttk.Button(frame, text=UI_TEXT['m6'], width=3, command=self._add_fps_hotkey_slot, padding=(2, 1))
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
        if sys.platform.startswith('linux'):
            self.after(0, lambda: self._fflag_apply(silent=True))
            return
        if self.fflag_pid and self.fflag_engine.handle:
            pid = self.fflag_pid
            engine = self.fflag_engine
            def apply_hotkey_value():
                try:
                    started = time.perf_counter()
                    success = bool(self._fflag_write_offset(fflag_strip_prefix(flag_name), new_value, fflag_infer_type(new_value)))
                    elapsed = time.perf_counter() - started
                    if not success:
                        self.after(0, lambda: self._fflag_apply(silent=True))
                    else:
                        elapsed_text = f"{elapsed:.9f}".replace('.', ',')
                        status = f'{flag_name} = {new_value} (Applied in {elapsed_text} seconds)'
                        self.after(0, lambda text=status: self._fflag_status_text(text, '#65d98b'))
                except Exception:
                    try:
                        self.after(0, lambda: self._fflag_apply(silent=True))
                    except Exception:
                        pass
            threading.Thread(target=apply_hotkey_value, name='RoUtilsFFlagHotkeyApply', daemon=True).start()
    def _remove_fflag_hotkey(self, tree, refresh):
        sel = tree.selection()
        if not sel:
            return
        del self.fflag_hotkeys[int(sel[0])]
        self._save_settings()
        refresh()
    def _apply_streamer_mode(self, _retry=0):
        if sys.platform != 'win32' or not self.winfo_exists():
            return
        try:
            self.update_idletasks()
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
    def _ensure_main_window_visible(self):
        try:
            if not self.winfo_exists() or '--tray' in sys.argv:
                return
            self.deiconify()
            if self.state() in ('withdrawn', 'iconic'):
                self.state('normal')
            self.lift()
            self._layout_titlebar(force=True)
            self._restore_windows_taskbar_presence()
            try:
                self.focus_force()
            except Exception:
                pass
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
        self._titlebar = tk.Frame(self, bg=_CURRENT_PALETTE.get('bg_dark', '#1b1b1c'), height=38, bd=0, highlightthickness=0)
        self._titlebar.pack(fill='x', side='top')
        self._titlebar.pack_propagate(False)
        self._titlebar_canvas = tk.Canvas(self._titlebar, bg=_CURRENT_PALETTE.get('bg_dark', '#1b1b1c'), bd=0, highlightthickness=0, height=38)
        self._titlebar_canvas.pack(fill='both', expand=True)
        self._titlebar_canvas.create_text(0, 19, text=UI_TEXT['x5'], anchor='center', fill='#f2f2f2', font=('Segoe UI Semibold', 10), tags=('title',))
        self._titlebar_canvas.create_text(0, 19, text=UI_TEXT['b7'], anchor='w', fill='#b7c5df', font=('Segoe UI', 9), tags=('spotlight',))
        self._titlebar_canvas.tag_bind('spotlight', '<Button-1>', lambda _e: self._open_spotlight(), add='+')
        self.bind_all('<Control-k>', lambda _e: (self._open_spotlight(), 'break')[1], add='+')
        self.bind_all('<Control-K>', lambda _e: (self._open_spotlight(), 'break')[1], add='+')
        self._titlebar_canvas.tag_bind('spotlight', '<Enter>', lambda _e: self._titlebar_canvas.configure(cursor='hand2'), add='+')
        self._titlebar_canvas.tag_bind('spotlight', '<Leave>', lambda _e: self._titlebar_canvas.configure(cursor=''), add='+')
        self._titlebar_buttons = {}
        self._notification_button = self._titlebar_canvas.create_text(0, 19, text=UI_TEXT['c7'], fill='#d7dce5', font=('Segoe UI Emoji', 11), tags=('notification_button',))
        self._titlebar_canvas.tag_bind('notification_button', '<Button-1>', lambda _e: self._open_notification_center(), add='+')
        self._titlebar_canvas.tag_bind('notification_button', '<Enter>', lambda _e: self._titlebar_canvas.configure(cursor='hand2'), add='+')
        self._titlebar_canvas.tag_bind('notification_button', '<Leave>', lambda _e: self._titlebar_canvas.configure(cursor=''), add='+')
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
        saved_button_colors = self.settings.get('topbar_button_colors', {})
        legacy_button_color = self.settings.get('topbar_button_color')
        default_button_colors = {'close': '#ff5f57', 'max': '#28c840', 'min': '#febc2e'}
        if not isinstance(saved_button_colors, dict):
            saved_button_colors = {}
        for name, (item, command, old_color) in list(self._titlebar_buttons.items()):
            selected_color = saved_button_colors.get(name, legacy_button_color or default_button_colors.get(name, old_color))
            if not isinstance(selected_color, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', selected_color):
                selected_color = default_button_colors.get(name, old_color)
            self._titlebar_buttons[name] = (item, command, selected_color)
            self._titlebar_canvas.itemconfigure(item, fill=selected_color)
        self.after_idle(self._restore_windows_taskbar_presence)
    def _open_notification_center(self):
        panel = getattr(self, '_notification_center_panel', None)
        if panel is not None:
            try:
                if panel.winfo_exists():
                    if panel.winfo_ismapped():
                        panel.place_forget()
                    else:
                        self._refresh_notification_center()
                        panel.place(relx=1.0, x=-12, y=42, anchor='ne', width=390, height=430)
                        panel.lift()
                    return
            except Exception:
                pass
        bg = _CURRENT_PALETTE.get('bg_dark', '#111318')
        surface = _CURRENT_PALETTE.get('bg_medium', '#1a1d24')
        fg = _CURRENT_PALETTE.get('fg', '#e6e9ef')
        accent = _CURRENT_PALETTE.get('accent', '#8ab4f8')
        panel = tk.Frame(self, bg=bg, bd=0, highlightthickness=1, highlightbackground=accent)
        self._notification_center_panel = panel
        panel.place(relx=1.0, x=-12, y=42, anchor='ne', width=390, height=430)
        header = tk.Frame(panel, bg=bg)
        header.pack(fill='x', padx=10, pady=(8, 6))
        tk.Label(header, text=UI_TEXT['d7'], bg=bg, fg=fg, font=('Segoe UI Semibold', 11)).pack(side='left')
        ttk.Button(header, text=UI_TEXT['j6'], command=self._clear_notification_history).pack(side='right', padx=(4, 0))
        close = tk.Label(header, text=UI_TEXT['e5'], bg=bg, fg=fg, font=('Segoe UI', 16), cursor='hand2')
        close.pack(side='right', padx=(6, 4))
        close.bind('<Button-1>', lambda _e: panel.place_forget())
        listing = tk.Frame(panel, bg=surface)
        listing.pack(fill='both', expand=True, padx=10, pady=(0, 8))
        listbox = tk.Listbox(listing, bg=surface, fg=fg, selectbackground=accent, selectforeground='#ffffff', bd=0, highlightthickness=0, activestyle='none', font=('Segoe UI', 8), exportselection=False)
        scroll = ttk.Scrollbar(listing, orient='vertical', command=listbox.yview)
        listbox.configure(yscrollcommand=scroll.set)
        listbox.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        details = tk.Text(panel, height=5, wrap='word', bg=surface, fg=fg, bd=0, highlightthickness=0, font=('Segoe UI', 8), padx=8, pady=6)
        details.pack(fill='x', padx=10, pady=(0, 10))
        details.configure(state='disabled')
        self._notification_center_listbox = listbox
        self._notification_center_details = details
        listbox.bind('<<ListboxSelect>>', self._notification_center_show_selected)
        self._refresh_notification_center()
        panel.lift()
        return panel
    def _refresh_notification_center(self):
        panel = getattr(self, '_notification_center_panel', None)
        listbox = getattr(self, '_notification_center_listbox', None)
        details = getattr(self, '_notification_center_details', None)
        if panel is None or listbox is None or details is None:
            return
        try:
            if not panel.winfo_exists() or not listbox.winfo_exists() or not details.winfo_exists():
                return
            with _NOTIFICATION_HISTORY_LOCK:
                entries = list(reversed(_NOTIFICATION_HISTORY))
            self._notification_center_entries = entries
            listbox.delete(0, 'end')
            for entry in entries:
                title = str(entry.get('title', 'Notification')).strip() or 'Notification'
                listbox.insert('end', f"{entry.get('time', '')}  ·  {title}")
            if entries:
                listbox.selection_set(0)
                self._notification_center_show_selected()
            else:
                details.configure(state='normal')
                details.delete('1.0', 'end')
                details.insert('1.0', UI_TEXT['t27'])
                details.configure(state='disabled')
        except tk.TclError:
            pass
    def _notification_center_show_selected(self, _event=None):
        listbox = getattr(self, '_notification_center_listbox', None)
        details = getattr(self, '_notification_center_details', None)
        if listbox is None or details is None:
            return
        try:
            selection = listbox.curselection()
            entries = getattr(self, '_notification_center_entries', [])
            if not selection or selection[0] >= len(entries):
                return
            entry = entries[selection[0]]
            details.configure(state='normal')
            details.delete('1.0', 'end')
            details.insert('1.0', f"{entry.get('title', 'Notification')}\n{entry.get('date', '')} {entry.get('time', '')}\n\n{entry.get('message', '')}")
            details.configure(state='disabled')
        except tk.TclError:
            pass
    def _clear_notification_history(self):
        with _NOTIFICATION_HISTORY_LOCK:
            _NOTIFICATION_HISTORY.clear()
            _save_notification_history()
        self._refresh_notification_center()
    def _open_spotlight(self):
        existing = getattr(self, '_spotlight_window', None)
        if existing is not None:
            try:
                if existing.winfo_exists():
                    existing.deiconify()
                    existing.lift()
                    existing.focus_force()
                    existing._spotlight_entry.focus_set()
                    existing._spotlight_entry.selection_range(0, 'end')
                    return
            except Exception:
                pass
        win = tk.Toplevel(self)
        win._skip_custom_chrome = True
        win._skip_popup_centering = True
        win.title('RoUtils Command Search')
        win.overrideredirect(True)
        accent = _CURRENT_PALETTE.get('accent', '#8ab4f8')
        bg = _CURRENT_PALETTE.get('bg_dark', '#111318')
        surface = _CURRENT_PALETTE.get('bg_medium', '#1a1d24')
        foreground = _CURRENT_PALETTE.get('fg', '#e6e9ef')
        win.configure(bg=accent)
        width, height = 740, 470
        x = max(0, (self.winfo_screenwidth() - width) // 2)
        y = max(0, (self.winfo_screenheight() - height) // 2 - 35)
        win.geometry(f'{width}x{height}+{x}+{y}')
        try:
            win.attributes('-topmost', True)
        except Exception:
            pass
        card = tk.Frame(win, bg=bg, highlightthickness=1, highlightbackground=accent)
        card.pack(fill='both', expand=True, padx=2, pady=2)
        header = tk.Frame(card, bg=surface)
        header.pack(fill='x', padx=12, pady=(12, 7))
        var = tk.StringVar()
        entry = ttk.Entry(header, textvariable=var, font=('Segoe UI', 12))
        entry.pack(side='left', fill='x', expand=True, padx=(0, 8), ipady=5)
        ttk.Button(header, text='×', width=3, command=win.destroy).pack(side='right')
        hint = tk.Label(card, text='Search tabs, actions, settings, and FFlag commands', bg=bg, fg='#9aa0a6', anchor='w', font=('Segoe UI', 9))
        hint.pack(fill='x', padx=15, pady=(0, 7))
        results = tk.Listbox(card, bg=surface, fg=foreground, selectbackground=accent, selectforeground='#ffffff', bd=0, highlightthickness=0, activestyle='none', font=('Segoe UI', 10), height=16, selectborderwidth=0)
        results.pack(fill='both', expand=True, padx=12, pady=(0, 7))
        footer = tk.Label(card, text='↑ ↓ Navigate     Enter Open     Esc Close     Ctrl+K Search', bg=bg, fg='#9aa0a6', anchor='w', font=('Segoe UI', 9))
        footer.pack(fill='x', padx=15, pady=(0, 10))
        matches = []
        action_order = {}
        def widget_text(widget):
            values = []
            for option in ('text', 'label', 'title'):
                try:
                    value = str(widget.cget(option) or '').strip()
                    if value:
                        values.append(value)
                except Exception:
                    pass
            return ' '.join(values).strip()
        def is_searchable_text(value):
            value = re.sub(r'\s+', ' ', str(value or '')).strip()
            if len(value) < 2 or not re.search(r'[A-Za-zÇĞİÖŞÜçğıöşü]', value):
                return False
            if re.search(r'\b[A-Z]{1,8}\s+VAR\s*\d+\b', value, re.I):
                return False
            if re.search(r'\bversion\s*:?\s*v?\d+(?:\.\d+){1,4}\b', value, re.I):
                return False
            if re.fullmatch(r'[vV]?\d+(?:\.\d+){1,4}', value):
                return False
            return True
        def find_tab(tab_name):
            for tab_id in self.nb.tabs():
                try:
                    if self.nb.tab(tab_id, 'text').casefold() == str(tab_name).casefold():
                        return tab_id
                except Exception:
                    pass
            return None
        action_specs = [
            ('Open FFlags History', UI_TEXT['h5'], 'fflag_history', ('fflag history', 'flag change history', 'history of flags', 'changes history')),
            ('Apply FFlags', UI_TEXT['h5'], 'fflag_apply', ('apply flags', 'inject fflags', 'apply fastflags')),
            ('Add FFlag', UI_TEXT['h5'], 'fflag_add', ('new flag', 'create fflag', 'add fastflag')),
            ('Save FFlags', UI_TEXT['h5'], 'fflag_save', ('save flags', 'save fastflags')),
            ('Toggle FFlag Auto Apply', UI_TEXT['h5'], 'fflag_auto', ('auto apply', 'automatic fflag apply')),
            ('Open FFlag JSON Editor', UI_TEXT['h5'], 'fflag_json', ('edit flag json', 'json editor')),
            ('Import FFlags', UI_TEXT['h5'], 'fflag_import', ('import flags', 'load flags json')),
            ('Export FFlags', UI_TEXT['h5'], 'fflag_export', ('export flags', 'save flags json')),
            ('Refresh Roblox Process', UI_TEXT['h5'], 'fflag_process', ('detect roblox', 'refresh pid', 'find roblox process')),
            ('Open Console', UI_TEXT['u5'], 'console', ('terminal', 'commands', 'console commands')),
            ('Open Cache', UI_TEXT['f5'], 'cache', ('cache viewer', 'cache files')),
            ('Open Themes', UI_TEXT['q5'], 'themes', ('appearance', 'colors', 'change theme')),
            ('Open Settings', UI_TEXT['r5'], 'settings', ('preferences', 'app settings'))
        ]
        def collect():
            found = []
            tab_aliases = {
                UI_TEXT['f5']: ('Cache Viewer', 'Cache Editor', 'Browse Roblox cache', 'Find cached assets', 'Replace cache assets', 'Delete cache entries', 'Watch cache changes', 'Export caches'),
                UI_TEXT['h5']: ('FastFlags', 'Fast Flag Manager', 'FFlag values', 'FFlag offsets', 'Edit Roblox flags', 'FFlag History', 'Change History', 'FastFlag Settings'),
                UI_TEXT['l5']: ('Roblox configs', 'CConfig manager', 'Save config', 'Load config', 'Import config', 'Export config'),
                UI_TEXT['k5']: ('Mesh tools', 'Convert mesh', 'Replace Roblox meshes', 'Asset modifications'),
                UI_TEXT['m5']: ('Join Roblox game', 'Join subplace', 'Place ID', 'Server deeplink'),
                UI_TEXT['n5']: ('View Roblox server', 'Server deeplink', 'Job ID'),
                UI_TEXT['o5']: ('Recent games', 'Recent servers', 'Join history', 'Copy deeplink'),
                UI_TEXT['p5']: ('Roblox client info', 'CPU usage', 'RAM usage', 'Refresh client info'),
                UI_TEXT['q5']: ('Appearance', 'Change theme', 'Customize colors', 'Topbar button colors'),
                UI_TEXT['j5']: ('Ask AI', 'Gemini chat', 'RoUtils help'),
                UI_TEXT['s5']: ('Manage plugins', 'Enable plugins', 'Disable plugins'),
                UI_TEXT['u5']: ('Commands', 'Command console', 'Cache commands', 'FFlag commands'),
                UI_TEXT['r5']: ('Preferences', 'Performance settings', 'Startup settings', 'Hotkeys', 'Update settings')
            }
            for tab_id in self.nb.tabs():
                try:
                    tab_name = str(self.nb.tab(tab_id, 'text')).strip()
                except Exception:
                    continue
                if not tab_name or tab_name.casefold() == 'home':
                    continue
                found.append((tab_name, tab_name, tab_id, None))
                for alias in tab_aliases.get(tab_name, ()):
                    found.append((alias, tab_name, tab_id, None))
                try:
                    root = self.nametowidget(tab_id)
                except Exception:
                    continue
                stack = [root]
                while stack:
                    widget = stack.pop()
                    try:
                        stack.extend(widget.winfo_children())
                    except Exception:
                        pass
                    if isinstance(widget, (ttk.Button, tk.Button, ttk.Checkbutton, tk.Checkbutton, ttk.Radiobutton, tk.Radiobutton)):
                        label = widget_text(widget)
                        if is_searchable_text(label):
                            found.append((label, tab_name, tab_id, widget))
            for index, (label, tab_name, action, aliases) in enumerate(action_specs):
                tab_id = find_tab(tab_name)
                if tab_id is None:
                    continue
                action_order[action] = index
                found.append((label, tab_name, tab_id, '__action__:' + action))
                for alias in aliases:
                    found.append((alias, tab_name, tab_id, '__action__:' + action))
            unique = []
            seen = set()
            for item in found:
                label, tab_name = item[0], item[1]
                key = (label.casefold(), tab_name.casefold())
                if key not in seen:
                    seen.add(key)
                    unique.append(item)
            return unique
        all_items = collect()
        def score_item(item, query, terms):
            label, tab_name, _tab_id, widget = item
            label_norm = re.sub(r'\s+', ' ', str(label)).casefold().strip()
            tab_norm = str(tab_name).casefold()
            haystack = f'{label_norm} {tab_norm}'
            is_action = isinstance(widget, str) and widget.startswith('__action__:')
            action_name = widget.partition(':')[2] if is_action else ''
            if not query:
                if is_action:
                    return 250 - action_order.get(action_name, 99)
                if label_norm == tab_norm:
                    return 120
                return 65
            if label_norm == query:
                return 300
            if label_norm.startswith(query):
                return 240 - len(label_norm) * 0.02
            if all(term in haystack for term in terms):
                return 190 - len(label_norm) * 0.015 + sum(10 for term in terms if label_norm.startswith(term))
            tokens = re.findall(r'[a-z0-9çğıöşü]+', label_norm)
            token_scores = []
            for term in terms:
                token_scores.append(max([difflib.SequenceMatcher(None, term, token).ratio() for token in tokens] + [0.0]))
            fuzzy = sum(token_scores) / max(1, len(token_scores))
            full_fuzzy = difflib.SequenceMatcher(None, query, label_norm).ratio()
            score = max(fuzzy * 150, full_fuzzy * 135)
            return score if score >= 72 else -1
        def render(*_):
            query = var.get().strip().casefold()
            terms = [part for part in re.split(r'\s+', query) if part]
            matches.clear()
            results.delete(0, 'end')
            ranked = []
            for item in all_items:
                score = score_item(item, query, terms)
                if score >= 0:
                    ranked.append((score, item))
            ai_tab_id = find_tab(UI_TEXT['j5'])
            if query and ai_tab_id is not None and (query in ('ai', 'ask', 'ask ai', 'ro', 'help') or query.startswith('ask ')):
                ranked.append((55, ('Ask to AI', UI_TEXT['j5'], ai_tab_id, '__action__:ask_ai')))
            ranked.sort(key=lambda pair: pair[0], reverse=True)
            for _score, item in ranked[:70]:
                matches.append(item)
                prefix = '↪  ' if isinstance(item[3], str) and item[3].startswith('__action__:') else '›  '
                results.insert('end', f'{prefix}{item[0]}  ·  {item[1]}')
            if matches:
                results.selection_clear(0, 'end')
                results.selection_set(0)
                results.activate(0)
                footer.configure(text=f'{len(matches)} result(s)     ↑ ↓ Navigate     Enter Open     Esc Close')
            else:
                results.insert('end', 'No matching commands or controls')
                footer.configure(text='Try a shorter phrase or search by tab, action, setting, or FFlag name')
        def dispatch_action(action):
            callbacks = {
                'fflag_history': self._open_fflag_history_panel,
                'fflag_apply': self._fflag_apply,
                'fflag_add': self._fflag_add_dialog,
                'fflag_save': self._save_fflag_flags,
                'fflag_auto': self._toggle_fflag_auto_apply,
                'fflag_json': self._fflag_json_editor,
                'fflag_import': self._fflag_import,
                'fflag_export': self._fflag_export,
                'fflag_process': self._fflag_refresh_process
            }
            callback = callbacks.get(action)
            if callback:
                callback()
        def activate(_event=None):
            selection = results.curselection()
            if not selection or selection[0] >= len(matches):
                return 'break'
            _label, _tab_name, tab_id, widget = matches[selection[0]]
            if isinstance(widget, str) and widget.startswith('__action__:'):
                action = widget.partition(':')[2]
                try:
                    self.nb.select(tab_id)
                    self._lazy_tab_changed()
                except Exception:
                    pass
                try:
                    win.destroy()
                except Exception:
                    pass
                if action == 'ask_ai':
                    self.after_idle(lambda: self._open_ai_chat(var.get().strip() or None))
                else:
                    self.after_idle(lambda a=action: dispatch_action(a))
                return 'break'
            try:
                self.nb.select(tab_id)
                self._lazy_tab_changed()
                if widget is not None and widget.winfo_exists():
                    try:
                        widget.focus_set()
                    except Exception:
                        pass
                    try:
                        if isinstance(widget, ttk.Button):
                            old_style = widget.cget('style')
                            style = ttk.Style(self)
                            style.configure('RoUtils.Spotlight.TButton', background='#f8d84a', foreground='#161616')
                            widget.configure(style='RoUtils.Spotlight.TButton')
                            widget.after(1800, lambda w=widget, st=old_style: w.configure(style=st) if w.winfo_exists() else None)
                        elif isinstance(widget, (tk.Label, ttk.Label)):
                            old_fg = widget.cget('foreground') if isinstance(widget, ttk.Label) else widget.cget('fg')
                            if isinstance(widget, ttk.Label):
                                widget.configure(foreground='#ffd84a')
                                widget.after(1800, lambda w=widget, c=old_fg: w.configure(foreground=c) if w.winfo_exists() else None)
                            else:
                                widget.configure(fg='#ffd84a')
                                widget.after(1800, lambda w=widget, c=old_fg: w.configure(fg=c) if w.winfo_exists() else None)
                    except Exception:
                        pass
                win.destroy()
            except Exception as exc:
                self._console_log(UI_TEXT['e7'].format(p0=exc))
            return 'break'
        def move_selection(delta):
            if not matches:
                return 'break'
            current = results.curselection()
            index = current[0] if current else 0
            index = max(0, min(len(matches) - 1, index + delta))
            results.selection_clear(0, 'end')
            results.selection_set(index)
            results.activate(index)
            results.see(index)
            return 'break'
        render_job = {'id': None}
        def schedule_render(*_):
            previous_job = render_job.get('id')
            if previous_job:
                try:
                    win.after_cancel(previous_job)
                except Exception:
                    pass
            def run_render():
                render_job['id'] = None
                render()
            render_job['id'] = win.after(45, run_render)
        var.trace_add('write', schedule_render)
        results.bind('<Double-1>', activate)
        results.bind('<Return>', activate)
        results.bind('<Up>', lambda _e: move_selection(-1))
        results.bind('<Down>', lambda _e: move_selection(1))
        entry.bind('<Return>', activate)
        entry.bind('<Escape>', lambda _e: (win.destroy(), 'break')[1])
        entry.bind('<Down>', lambda _e: (results.focus_set(), move_selection(1))[1])
        entry.bind('<Up>', lambda _e: (results.focus_set(), move_selection(-1))[1])
        win.bind('<Escape>', lambda _e: win.destroy())
        win.bind('<Control-k>', lambda _e: (entry.focus_set(), entry.selection_range(0, 'end'), 'break')[2])
        self._spotlight_window = win
        win._spotlight_entry = entry
        render()
        entry.focus_set()
    def _update_kill_routils_visibility(self):
        try:
            enabled = bool(self.hide_to_tray_on_close.get())
        except Exception:
            enabled = bool(self.settings.get('hide_to_tray_on_close', False))
        try:
            if enabled and (not getattr(self, '_kill_ro_utils_items', None)):
                dot = self._titlebar_canvas.create_oval(0, 0, 14, 14, fill='#ff3b30', outline='', tags=('kill_ro_utils',))
                label = self._titlebar_canvas.create_text(0, 19, text=UI_TEXT['f7'], anchor='w', fill='#f2f2f2', font=('Segoe UI Semibold', 9), tags=('kill_ro_utils',))
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
            self._titlebar_canvas.coords('title', w / 2 - 86, 19)
            self._titlebar_canvas.coords('spotlight', w / 2 - 18, 19)
            kill_items = getattr(self, '_kill_ro_utils_items', None)
            if kill_items:
                self._titlebar_canvas.coords(kill_items[0], 10, 12, 24, 26)
                self._titlebar_canvas.coords(kill_items[1], 31, 19)
            self._titlebar_canvas.coords(self._notification_button, w - 103, 19)
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
        try:
            box = self._titlebar_canvas.bbox('notification_button')
            if box and box[0] - 5 <= x <= box[2] + 5 and box[1] - 5 <= y <= box[3] + 5:
                return ('notifications', self._open_notification_center)
        except Exception:
            pass
        try:
            box = self._titlebar_canvas.bbox('spotlight')
            if box and box[0] <= x <= box[2] and box[1] <= y <= box[3]:
                return ('spotlight', self._open_spotlight)
        except Exception:
            pass
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
        self._titlebar_pending_xy = (int(ox + event.x_root - sx), int(oy + event.y_root - sy))
        if self._titlebar_drag_job is None:
            def apply_drag():
                self._titlebar_drag_job = None
                xy = getattr(self, '_titlebar_pending_xy', None)
                if not xy or xy == self._titlebar_last_xy:
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
            self._titlebar_drag_job = self.after(16, apply_drag)
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
            if xy and xy != getattr(self, '_titlebar_last_xy', None):
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
            elif name == 'spotlight':
                self._open_spotlight()
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
    def _schedule_tab_nav_refresh(self, _event=None):
        try:
            if self._tab_nav_refresh_job is not None:
                self.after_cancel(self._tab_nav_refresh_job)
            self._tab_nav_refresh_job = self.after(220, self._run_tab_nav_refresh)
        except Exception:
            self._tab_nav_refresh_job = None
    def _run_tab_nav_refresh(self):
        self._tab_nav_refresh_job = None
        if getattr(self, '_resize_active', False):
            try:
                self._tab_nav_refresh_job = self.after(260, self._run_tab_nav_refresh)
            except Exception:
                self._tab_nav_refresh_job = None
            return
        self._refresh_tab_nav()
    def _refresh_tab_nav(self):
        if not hasattr(self, '_tab_nav_inner') or not hasattr(self, 'nb'):
            return
        try:
            active_id = str(self.nb.select()) if self.nb.select() else ''
            current_tabs = list(self.nb.tabs())
            buttons = getattr(self, '_tab_nav_buttons', {})
            grips = getattr(self, '_tab_grips', {})
            for tab_id in tuple(buttons):
                if tab_id not in current_tabs:
                    for widget in (buttons.get(tab_id), grips.get(tab_id)):
                        try:
                            widget.destroy()
                        except Exception:
                            pass
                    buttons.pop(tab_id, None)
                    grips.pop(tab_id, None)
            try:
                nav_width = max(self.winfo_width(), self._tab_nav.winfo_width())
            except Exception:
                nav_width = 1200
            if nav_width < 760:
                compact_names = {UI_TEXT['k5']: 'Mods', UI_TEXT['m5']: 'Subpl.', UI_TEXT['n5']: 'Server', UI_TEXT['r5']: 'Set.'}
            elif nav_width < 1080:
                compact_names = {UI_TEXT['k5']: 'Mods', UI_TEXT['m5']: 'Subplace', UI_TEXT['n5']: 'Server', UI_TEXT['r5']: UI_TEXT['r5']}
            else:
                compact_names = {}
            display_rows = []
            for tab_id in current_tabs:
                name = str(self.nb.tab(tab_id, 'text'))
                display_name = compact_names.get(name, name)
                display_rows.append((tab_id, display_name))
                button = buttons.get(tab_id)
                if button is None or not button.winfo_exists():
                    button = ttk.Button(self._tab_nav_inner, text=display_name, takefocus=False, style='RoUtils.Nav.TButton', command=lambda tid=tab_id: self.nb.select(tid))
                    buttons[tab_id] = button
                elif str(button.cget('text')) != display_name:
                    button.configure(text=display_name)
                grip = grips.get(tab_id)
                if grip is None or not grip.winfo_exists():
                    grip = tk.Label(self._tab_nav_inner, text=UI_TEXT['g7'], bg=_CURRENT_PALETTE.get('bg_dark', '#111318'), fg='#8490a6', font=('Segoe UI Symbol', 10), cursor='hand2', padx=1)
                    grip.bind('<ButtonPress-1>', lambda event, tid=tab_id: self._tab_drag_start(event, tid))
                    grip.bind('<B1-Motion>', self._tab_drag_motion)
                    grip.bind('<ButtonRelease-1>', self._tab_drag_release)
                    grips[tab_id] = grip
                else:
                    grip.configure(bg=_CURRENT_PALETTE.get('bg_dark', '#111318'))
            self._tab_nav_buttons = buttons
            self._tab_grips = grips
            signature = tuple(display_rows)
            if signature != getattr(self, '_tab_nav_layout_signature', None):
                for tab_id, _display_name in display_rows:
                    grip = grips[tab_id]
                    button = buttons[tab_id]
                    grip.pack_forget()
                    button.pack_forget()
                    grip.pack(side='left', padx=(3, 0), pady=0)
                    button.pack(side='left', padx=(0, 2), pady=0)
                self._tab_nav_layout_signature = signature
            for tab_id in current_tabs:
                button = buttons[tab_id]
                selected_style = 'RoUtils.ActiveNav.TButton' if tab_id == active_id else 'RoUtils.Nav.TButton'
                if str(button.cget('style')) != selected_style:
                    button.configure(style=selected_style)
        except Exception:
            pass
    def _tab_drag_start(self, event, tab_id):
        self._tab_drag_state = {'tab_id': str(tab_id), 'x': event.x_root, 'y': event.y_root, 'moved': False}
        return 'break'
    def _tab_drag_motion(self, event):
        state = getattr(self, '_tab_drag_state', None)
        if not state:
            return 'break'
        if abs(event.x_root - state['x']) + abs(event.y_root - state['y']) > 8:
            state['moved'] = True
            try:
                self.configure(cursor='fleur')
            except Exception:
                pass
        return 'break'
    def _tab_drag_release(self, event):
        state = getattr(self, '_tab_drag_state', None)
        self._tab_drag_state = None
        try:
            self.configure(cursor='')
        except Exception:
            pass
        if not state or not state.get('moved'):
            return 'break'
        tab_id = state.get('tab_id')
        if tab_id not in self.nb.tabs():
            return 'break'
        try:
            left, top = self.winfo_rootx(), self.winfo_rooty()
            right, bottom = left + self.winfo_width(), top + self.winfo_height()
            if event.x_root < left or event.x_root > right or event.y_root < top or event.y_root > bottom:
                return 'break'
            entries = []
            for current_id in self.nb.tabs():
                widget = self._tab_grips.get(current_id) or self._tab_nav_buttons.get(current_id)
                if widget is None or current_id == tab_id:
                    continue
                try:
                    center = widget.winfo_rootx() + widget.winfo_width() // 2
                    entries.append((abs(event.x_root - center), center, current_id))
                except Exception:
                    pass
            if entries:
                target = min(entries)[2]
                order = list(self.nb.tabs())
                order.remove(tab_id)
                index = order.index(target)
                target_center = next(item[1] for item in entries if item[2] == target)
                if event.x_root > target_center:
                    index += 1
                order.insert(index, tab_id)
                for position, item in enumerate(order):
                    self.nb.insert(position, item)
                self._refresh_tab_nav()
                self._save_settings()
        except Exception as exc:
            self._console_log(UI_TEXT['h7'].format(p0=exc))
        return 'break'
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
                    if isinstance(w, tk.Canvas):
                        try:
                            if w.cget('yscrollcommand'):
                                target = w
                                break
                        except Exception:
                            pass
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
    def _add_json_editor_value(self, txt, dlg):
        try:
            data = json.loads(txt.get('1.0', 'end'))
            if not isinstance(data, (dict, list)):
                raise ValueError('JSON must be an object or an array.')
        except Exception as e:
            messagebox.showerror(UI_TEXT['t10'], UI_TEXT['u10'].format(p0=e), parent=dlg)
            return
        candidate = [dict(flag) for flag in self.fflag_flags if isinstance(flag, dict)]
        if isinstance(data, dict):
            for n, v in data.items():
                candidate.append({'name': fflag_strip_prefix(str(n)), 'value': str(v).lower() if isinstance(v, bool) else str(v), 'type': fflag_infer_type(v)})
        else:
            for item in data:
                if isinstance(item, dict) and item.get('name') is not None:
                    candidate.append({'name': fflag_strip_prefix(str(item['name'])), 'value': str(item.get('value', '')), 'type': item.get('type') or fflag_infer_type(item.get('value', ''))})
        if not self._fflag_confirm_large_values(candidate, dlg):
            return
        self.fflag_flags = candidate
        self._save_fflag_flags()
        self._refresh_fflag_list()
        self._fflag_check_source_flags()
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
                flags = [{'name': fflag_strip_prefix(str(key)), 'value': str(value).lower() if isinstance(value, bool) else str(value), 'type': fflag_infer_type(value)} for key, value in data.items()]
            elif isinstance(data, list):
                flags = [{'name': fflag_strip_prefix(str(item['name'])), 'value': str(item.get('value', '')), 'type': item.get('type') or fflag_infer_type(item.get('value', ''))} for item in data if isinstance(item, dict) and item.get('name') is not None]
            else:
                raise ValueError('JSON must be an object or array.')
            if not self._fflag_confirm_large_values(flags, self):
                return
            self.fflag_flags = flags
            self._save_fflag_flags()
            self._refresh_fflag_list()
            self._fflag_check_source_flags()
            messagebox.showinfo(UI_TEXT['h5'], UI_TEXT['v10'].format(p0=len(flags), p1=os.path.basename(path)), parent=self)
        except Exception as e:
            messagebox.showerror(UI_TEXT['h5'], UI_TEXT['w10'].format(p0=e), parent=self)

    def _choose_roblox_path(self):
        path = filedialog.askopenfilename(parent=self, title=UI_TEXT['x10'], filetypes=[(UI_TEXT['y10'], 'RobloxPlayerBeta.exe'), (UI_TEXT['z10'], '*.exe')])
        if path and os.path.basename(path).lower() == 'robloxplayerbeta.exe':
            self.roblox_path_var.set(path)
            self.settings['roblox_path'] = path
            self._save_settings()
    def _resolve_history_game_name(self, place_id):
        place_id = str(place_id or '').strip()
        if not place_id.isdigit():
            return None
        for url in (f'https://games.roblox.com/v1/games/multiget-place-details?placeIds={place_id}', f'https://develop.roblox.com/v1/places/{place_id}'):
            try:
                with _routils_request(url, timeout=8) as r:
                    data = json.load(r)
                if isinstance(data, list):
                    data = data[0] if data else {}
                name = str(data.get('name') or data.get('universeName') or '').strip()
                if name and (not name.isdigit()):
                    return name
            except Exception:
                pass
        try:
            with _routils_request(f'https://apis.roblox.com/universes/v1/places/{place_id}/universe', timeout=8) as r:
                universe_id = json.load(r).get('universeId')
            if universe_id:
                with _routils_request(f'https://games.roblox.com/v1/games?universeIds={universe_id}', timeout=8) as r:
                    data = json.load(r)
                rows = data.get('data', []) if isinstance(data, dict) else []
                if rows:
                    name = str(rows[0].get('name') or '').strip()
                    if name and (not name.isdigit()):
                        return name
        except Exception:
            pass
        return None
    def _build_emote_manager_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.add(tab, text=UI_TEXT['i5'])
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)
        head = ttk.Frame(tab)
        head.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(head, text=UI_TEXT['i5'], font=('Segoe UI Semibold', 15)).pack(side='left')
        self.emote_status = ttk.Label(head, text=UI_TEXT['q13'], foreground='#9aa0a6')
        self.emote_status.pack(side='right', padx=(8, 0))
        bar = ttk.Frame(tab)
        bar.grid(row=1, column=0, sticky='ew', pady=(0, 8))
        ttk.Button(bar, text=UI_TEXT['r13'], command=self._emote_remove_bind).pack(side='left', padx=(0, 6))
        ttk.Button(bar, text=UI_TEXT['s13'], command=self._emote_add_bind).pack(side='left')
        self.emote_tree = ttk.Treeview(tab, columns=('hotkey', 'dance'), show='headings', selectmode='browse')
        self.emote_tree.heading('hotkey', text=UI_TEXT['t13'])
        self.emote_tree.heading('dance', text=UI_TEXT['u13'])
        self.emote_tree.column('hotkey', width=150, anchor='center', stretch=True)
        self.emote_tree.column('dance', width=300, anchor='w', stretch=True)
        self.emote_tree.grid(row=2, column=0, sticky='nsew')
        scroll = ttk.Scrollbar(tab, orient='vertical', command=self.emote_tree.yview)
        scroll.grid(row=2, column=1, sticky='ns')
        self.emote_tree.configure(yscrollcommand=scroll.set)
        bottom = ttk.Frame(tab)
        bottom.grid(row=3, column=0, sticky='ew', pady=(8, 0))
        self.emote_action_status = ttk.Label(bottom, text=UI_TEXT['v13'], foreground='#9aa0a6')
        self.emote_action_status.pack(side='left', fill='x', expand=True)
        self._emote_hotkeys_button = ttk.Button(bottom, text=UI_TEXT['w13'], command=self._toggle_emote_hotkeys)
        self._emote_hotkeys_button.pack(side='left', padx=(4, 4))
        self._emote_toggle_hotkey_button = ttk.Button(bottom, text=self._emote_toggle_hotkey_button_text(), command=self._emote_assign_toggle_hotkey)
        self._emote_toggle_hotkey_button.pack(side='left', padx=(4, 4))
        self._emote_controls_button = ttk.Button(bottom, text=UI_TEXT['x13'], command=self._toggle_emote_controls)
        self._emote_controls_button.pack(side='left', padx=(4, 4))
        ttk.Button(bottom, text=UI_TEXT['i6'], command=self._emote_save_binds).pack(side='right')
        self._emote_refresh_list()
        self._emote_update_control_button_states()
        self.after(100, self._emote_status_tick)
    def _open_default_fflag_values(self):
        self._show_fflag_reference_panel()
    def _open_latest_fflag_list(self):
        self._show_fflag_reference_panel()
    def _fps_apply_tick(self):
        return
    def _load_console_history(self):
        try:
            with open(CONSOLE_HISTORY_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [_routils_visible_text(str(x)) for x in data][-1000:] if isinstance(data, list) else []
        except Exception:
            return []
    def _save_console_history(self):
        self._console_save_job = None
        if getattr(self, '_resize_active', False):
            try:
                self._console_save_job = self.after(500, self._save_console_history)
            except Exception:
                self._console_save_job = None
            return
        try:
            os.makedirs(os.path.dirname(CONSOLE_HISTORY_PATH), exist_ok=True)
            temp = CONSOLE_HISTORY_PATH + '.tmp'
            with open(temp, 'w', encoding='utf-8') as f:
                json.dump(self._console_history[-1000:], f, ensure_ascii=False, indent=2)
            os.replace(temp, CONSOLE_HISTORY_PATH)
        except Exception:
            pass
    def _apply_or_defer_canvas_window_width(self, canvas, window_id, width, state_key):
        try:
            width = max(1, int(width))
            if not canvas.winfo_exists():
                return
            if getattr(self, '_resize_active', False):
                self._deferred_canvas_widths[id(canvas)] = (canvas, window_id, width, state_key)
                return
            if width == getattr(self, state_key, -1):
                return
            canvas.itemconfigure(window_id, width=width)
            setattr(self, state_key, width)
        except Exception:
            pass
    def _discord_rpc_status_changed(self, status):
        if threading.get_ident() != getattr(self, '_ui_thread_id', threading.get_ident()):
            try:
                self.after(0, self._discord_rpc_status_changed, status)
            except Exception:
                pass
            return
        try:
            if hasattr(self, 'discord_rpc_status_var'):
                self.discord_rpc_status_var.set(str(status))
        except Exception:
            pass
    def _prompt_change_discord_application_id(self):
        if getattr(self, '_discord_id_prompt_open', False):
            return
        self._discord_id_prompt_open = True
        win = tk.Toplevel(self)
        win.title('Discord Rich Presence')
        win.transient(self)
        win.resizable(False, False)
        try:
            theme_toplevel(win)
        except Exception:
            pass
        body = tk.Frame(win, bg=_CURRENT_PALETTE['bg_dark'], padx=22, pady=18)
        body.pack(fill='both', expand=True)
        tk.Label(body, text='Do you want to change Application ID?\n(Not suggested most users)', bg=_CURRENT_PALETTE['bg_dark'], fg=_CURRENT_PALETTE['fg'], justify='center', font=('Segoe UI', 10)).pack(pady=(2, 18))
        buttons = tk.Frame(body, bg=_CURRENT_PALETTE['bg_dark'])
        buttons.pack()
        continue_button = ttk.Button(buttons, text='Continue (3s)', state='disabled')
        continue_button.pack(side='left', padx=6)
        cancel_button = ttk.Button(buttons, text="I don't want to", command=win.destroy)
        cancel_button.pack(side='left', padx=6)
        entry_area = tk.Frame(body, bg=_CURRENT_PALETTE['bg_dark'])
        def finish_prompt():
            self._discord_id_prompt_open = False
            try:
                win.destroy()
            except Exception:
                pass
        def continue_to_edit():
            finish_prompt()
            edit = tk.Toplevel(self)
            edit.title('Application ID')
            edit.transient(self)
            edit.resizable(False, False)
            try:
                theme_toplevel(edit)
            except Exception:
                pass
            panel = tk.Frame(edit, bg=_CURRENT_PALETTE['bg_dark'], padx=18, pady=16)
            panel.pack(fill='both', expand=True)
            value = tk.StringVar(value=self.discord_application_id_var.get())
            tk.Label(panel, text='Application ID', bg=_CURRENT_PALETTE['bg_dark'], fg=_CURRENT_PALETTE['fg']).pack(anchor='w', pady=(0, 6))
            field = ttk.Entry(panel, textvariable=value, width=34)
            field.pack(fill='x', pady=(0, 12))
            def save_value():
                candidate = value.get().strip()
                if not candidate.isdigit():
                    messagebox.showwarning('Discord Rich Presence', 'Application ID must contain digits only.', parent=edit)
                    return
                self.discord_application_id_var.set(candidate)
                self._save_discord_application_id()
                edit.destroy()
            ttk.Button(panel, text='Save', command=save_value).pack(anchor='e')
            edit.after(80, field.focus_set)
            edit.update_idletasks()
            edit.geometry(f'+{self.winfo_rootx() + 80}+{self.winfo_rooty() + 80}')
        continue_button.configure(command=continue_to_edit)
        state = {'left': 3}
        def tick():
            if not win.winfo_exists():
                self._discord_id_prompt_open = False
                return
            if state['left'] > 0:
                continue_button.configure(text=f"Continue ({state['left']}s)", state='disabled')
                state['left'] -= 1
                win.after(1000, tick)
            else:
                continue_button.configure(text='Continue', state='normal')
        win.protocol('WM_DELETE_WINDOW', finish_prompt)
        win.update_idletasks()
        win.geometry(f'+{self.winfo_rootx() + 60}+{self.winfo_rooty() + 60}')
        win.after(1000, tick)
    def _save_discord_application_id(self):
        application_id = str(self.discord_application_id_var.get() or '').strip()
        if not application_id.isdigit():
            messagebox.showwarning('Discord Rich Presence', 'Application ID must contain digits only.', parent=self)
            return
        self.discord_application_id_var.set(application_id)
        self.settings['discord_application_id'] = application_id
        try:
            self._save_settings()
        except Exception:
            save_settings(self.settings)
        rpc = getattr(self, '_discord_rpc', None)
        if rpc is not None:
            rpc.set_client_id(application_id)
            self._discord_rpc_status_changed('Reconnecting Discord RPC...')
            self._refresh_discord_rpc_activity()
    def _refresh_discord_rpc_activity(self):
        rpc = getattr(self, '_discord_rpc', None)
        if rpc is None:
            return
        rpc.set_enabled(True)
        tab_name = 'Home'
        try:
            selected = self.nb.select()
            if selected:
                tab_name = str(self.nb.tab(selected, 'text') or 'Home')
        except Exception:
            pass
        rpc.set_activity('Using RoUtils', f'Tab: {tab_name}')
    def _discord_rpc_poll_tick(self):
        try:
            if not self.winfo_exists():
                return
            self._refresh_discord_rpc_activity()
            self.after(int(DISCORD_RPC_INTERVAL * 1000), self._discord_rpc_poll_tick)
        except Exception:
            pass
    def _save_settings(self):
        if getattr(self, '_resize_active', False):
            self._settings_save_deferred = True
            self._geometry_save_job = None
            return
        data = dict(self.settings)
        data.pop('multi_instance_enabled', None)
        data.pop('discord_rpc_enabled', None)
        data['emote_hotkeys_enabled'] = bool(getattr(self, '_emote_hotkeys_enabled', self.settings.get('emote_hotkeys_enabled', True)))
        data['emote_hotkeys_toggle_key'] = str(getattr(self, '_emote_hotkeys_toggle_key', self.settings.get('emote_hotkeys_toggle_key', '')) or '').upper()
        data.update({'autoscroll': self.autoscroll.get(), 'hide_tickets': self.hide_tickets.get(), 'stay_on_top': self.stay_on_top.get(), 'show_lines': self.show_lines.get(), 'preview_optimize_vertices': self.viewport_3d.reduce_polys.get() if hasattr(self, 'viewport_3d') else self.settings.get('preview_optimize_vertices', True), 'streamer_mode': self.streamer_mode.get() if hasattr(self, 'streamer_mode') else self.settings.get('streamer_mode', False), 'fps_limit': self.fps_limit.get() if hasattr(self, 'fps_limit') else self.settings.get('fps_limit', 0), 'autostart_watch': self.autostart_watch.get() if hasattr(self, 'autostart_watch') else self.settings.get('autostart_watch', False), 'max_rows': self.max_rows.get() if hasattr(self, 'max_rows') else self.settings.get('max_rows', 0), 'type_filter': self.type_filter.get(), 'columns': {c: var.get() for c, var in getattr(self, '_col_vars', {}).items()}, 'viewer_collapsed': self.viewer_collapsed, 'theme': self.theme_var.get() if hasattr(self, 'theme_var') else self.settings.get('theme', DEFAULT_THEME), 'fflag_hotkeys': self.fflag_hotkeys, 'fps_hotkeys': self.fps_hotkeys, 'fps_hotkey_slots': self.fps_hotkey_slots, 'fflag_auto_apply': self.fflag_auto_apply.get() if hasattr(self, 'fflag_auto_apply') else self.settings.get('fflag_auto_apply', False), 'launch_on_tray': self.launch_on_tray.get() if hasattr(self, 'launch_on_tray') else self.settings.get('launch_on_tray', False), 'launch_on_startup': self.launch_on_startup.get() if hasattr(self, 'launch_on_startup') else self.settings.get('launch_on_startup', False), 'hide_to_tray_on_close': self.hide_to_tray_on_close.get() if hasattr(self, 'hide_to_tray_on_close') else self.settings.get('hide_to_tray_on_close', False), 'auto_update': self.auto_update.get() if hasattr(self, 'auto_update') else self.settings.get('auto_update', False), 'dpi_percent': int(self.dpi_percent.get()) if hasattr(self, 'dpi_percent') else int(getattr(self, '_dpi_scale', 1.0) * 100), 'plugin_enabled': getattr(self, '_plugin_enabled', self.settings.get('plugin_enabled', {})), 'emote_nav_binds': dict(getattr(self, '_emote_nav_binds', self.settings.get('emote_nav_binds', {}))), 'emote_hud_enabled': False, 'hpaned_sash_v2': self.hpaned.sashpos(0) if hasattr(self, 'hpaned') and self.hpaned.winfo_width() > 0 and self.hpaned.sashpos(0) > 0 else self.settings.get('hpaned_sash_v2', None), 'roblox_path': self.settings.get('roblox_path', ''), 'roblox_username': self.settings.get('roblox_username', ''), 'roblox_user_id': self.settings.get('roblox_user_id', ''), 'gemini_api_key': self.gemini_api_key.get().strip() if hasattr(self, 'gemini_api_key') else self.settings.get('gemini_api_key', ''), 'custom_theme': self.settings.get('custom_theme', {}), 'db_path': getattr(self, 'db_path', self.settings.get('db_path', '')), 'shard_root': getattr(self, 'shard_root', self.settings.get('shard_root', '')), 'window_geometry': self.geometry() if self.winfo_exists() else self.settings.get('window_geometry', STARTUP_GEOMETRY), 'include_cconfigs': self.include_cconfigs.get() if hasattr(self, 'include_cconfigs') else self.settings.get('include_cconfigs', False), 'include_cache_dumps': self.include_cache_dumps.get() if hasattr(self, 'include_cache_dumps') else self.settings.get('include_cache_dumps', False), 'tab_order': [self.nb.tab(t, 'text') for t in self.nb.tabs()] if hasattr(self, 'nb') else self.settings.get('tab_order', []), 'selected_tab': self.nb.tab(self.nb.select(), 'text') if hasattr(self, 'nb') and self.nb.select() else self.settings.get('selected_tab', UI_TEXT['w5']), 'hpaned_sash': self.hpaned.sashpos(0) if hasattr(self, 'hpaned') else self.settings.get('hpaned_sash', None), 'vpaned_sash': self.vpaned.sashpos(0) if hasattr(self, 'vpaned') else self.settings.get('vpaned_sash', None)})
        data['discord_application_id'] = str(self.discord_application_id_var.get()).strip() if hasattr(self, 'discord_application_id_var') else str(self.settings.get('discord_application_id') or DISCORD_APPLICATION_ID)
        save_settings(data)
        self.settings = data
    def _apply_startup_layouts(self):
        if not getattr(self, '_cache_built', False):
            return
        try:
            self.update_idletasks()
        except Exception:
            pass
        try:
            total = self.vpaned.winfo_height()
            if total > 160 and len(self.vpaned.panes()) >= 2:
                saved = self.settings.get('vpaned_sash')
                target = int(saved) if saved is not None else int(total * PANED_TOP_FRACTION)
                self.vpaned.sashpos(0, max(80, min(total - 80, target)))
        except Exception:
            pass
        try:
            total = self.hpaned.winfo_width()
            if total > VIEWER_MIN_WIDTH + REPLACER_MIN_WIDTH and len(self.hpaned.panes()) >= 2:
                saved = self.settings.get('hpaned_sash_v2')
                scale = max(0.62, min(1.0, float(getattr(self, '_responsive_last_scale', 1.0) or 1.0)))
                min_left = max(260, int(VIEWER_MIN_WIDTH * scale))
                min_right = max(190, int(REPLACER_MIN_WIDTH * scale))
                target = int(saved) if saved is not None and int(saved) > 0 else int(total * HPANED_LEFT_FRACTION)
                target = max(min_left, min(total - min_right, target))
                self.hpaned.sashpos(0, target)
                self._clamp_hsash()
        except Exception:
            pass
        self._autosize_columns_once()
    def _start_dump_all_caches(self, include_videos=False):
        dump_root = os.path.abspath(os.path.join(DATA_DIR, 'Dump'))
        self._last_dump_folder = dump_root
        os.makedirs(dump_root, exist_ok=True)
        self._console_log(UI_TEXT['b24'] if include_videos else UI_TEXT['c24'])
        self._console_log(UI_TEXT['d24'])
        def log(message):
            try:
                self.after(0, lambda m=str(message): self._console_log(m))
            except Exception:
                pass
        def worker():
            try:
                db_path, shard_root = default_paths()
                if not os.path.isfile(db_path):
                    log('ERROR: rbx-storage.db was not found.')
                    return
                try:
                    items = scan_db_once(db_path, shard_root, set(), None)
                except Exception as e:
                    log(f'ERROR while scanning: {e}')
                    return
                videos = [it for it in items if str(getattr(it, 'kind', '')).split(' ', 1)[0].lower() == 'video']
                items_to_dump = items if include_videos else [it for it in items if str(getattr(it, 'kind', '')).split(' ', 1)[0].lower() != 'video']
                helper = object.__new__(App)
                helper.db_path = db_path
                helper.shard_root = shard_root
                helper._video_ticket_entries = None
                dumped = failed = 0
                total = len(items_to_dump)
                log(f"Found {len(items)} cache(s), including {len(videos)}{UI_TEXT['t32']}")
                if not include_videos and videos:
                    log(f"Skipping {len(videos)}{UI_TEXT['t32']}")
                for index, it in enumerate(items_to_dump, 1):
                    try:
                        if App._dump_one_cache(helper, it, dump_root, include_video=include_videos):
                            dumped += 1
                        else:
                            failed += 1
                    except Exception as e:
                        failed += 1
                        log(f'Failed {getattr(it, "hash", "unknown")}: {e}')
                    if index % 10 == 0 or index == total:
                        log(f'Processed {index}/{total} | dumped={dumped} failed={failed}')
                log(f'Finished. Dumped: {dumped} | Failed: {failed}')
                log(f'Output folder: {dump_root}')
            except Exception as e:
                log(f'ERROR while dumping caches: {e}')
            finally:
                try:
                    self.after(0, lambda: setattr(self, '_dump_caches_running', False))
                except Exception:
                    self._dump_caches_running = False
        threading.Thread(target=worker, daemon=True, name='RoUtils-DumpCaches').start()
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
            print(UI_TEXT['e24'], flush=True)
            return 1
        print(UI_TEXT['f24'], flush=True)
        print(UI_TEXT['z23'].format(p0=db_path), flush=True)
        print(UI_TEXT['a24'].format(p0=dump_root), flush=True)
        while True:
            try:
                answer = input(UI_TEXT['c28']).strip().lower()
            except (EOFError, KeyboardInterrupt):
                answer = 'n'
            if answer in ('y', 'yes', 'n', 'no'):
                break
            print(UI_TEXT['p19'], flush=True)
        include_videos = answer in ('y', 'yes')
        helper = object.__new__(App)
        helper.db_path = db_path
        helper.shard_root = shard_root
        helper._video_ticket_entries = None
        try:
            items = scan_db_once(db_path, shard_root, set(), None)
        except Exception as e:
            print(UI_TEXT['g24'].format(p0=e), flush=True)
            return 1
        videos = [it for it in items if str(getattr(it, 'kind', '')).split(' ', 1)[0].lower() == 'video']
        items_to_dump = items if include_videos else [it for it in items if str(getattr(it, 'kind', '')).split(' ', 1)[0].lower() != 'video']
        dumped = 0
        failed = 0
        total = len(items_to_dump)
        print(UI_TEXT['h24'].format(p0=len(items), p1=len(videos)), flush=True)
        if not include_videos and videos:
            print(UI_TEXT['i24'].format(p0=len(videos)), flush=True)
        print(UI_TEXT['d24'], flush=True)
        for index, it in enumerate(items_to_dump, 1):
            try:
                if App._dump_one_cache(helper, it, dump_root, include_video=include_videos):
                    dumped += 1
                else:
                    failed += 1
            except Exception as e:
                failed += 1
                print(UI_TEXT['j24'].format(p0=getattr(it, "hash", "unknown"), p1=e), flush=True)
            if index % 10 == 0 or index == total:
                print(UI_TEXT['k24'].format(p0=index, p1=total, p2=dumped, p3=failed), flush=True)
        print()
        print(UI_TEXT['l24'].format(p0=dumped, p1=failed), flush=True)
        print(UI_TEXT['m24'].format(p0=dump_root), flush=True)
        return 0
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
        if os.name != 'nt':
            self._tray_hidden = False
            try:
                self.iconify()
            except Exception:
                pass
            return
        self._start_tray()
        self._tray_hidden = True
        try:
            self._emote_controls_detach_from_main(no_activate=True)
        except Exception:
            pass
        try:
            self.withdraw()
        except Exception:
            pass
        try:
            self.after(80, self._emote_controls_ensure_visible_after_hide)
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
        try:
            self.after(100, self._emote_controls_restore_activation)
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
        self._emote_hud_closing_from_app = True
        try:
            rpc = getattr(self, '_discord_rpc', None)
            if rpc is not None:
                rpc.stop()
        except Exception:
            pass
        self.watching = False
        self.stop_event.set()
        self._hotkey_stop.set()
        try:
            listener = getattr(self, '_linux_hotkey_listener', None)
            if listener is not None:
                listener.stop()
        except Exception:
            pass
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
        self._ui_dispatch_closed = True
        self._resize_active = False
        self._settings_save_deferred = False
        self.destroy()
def _routils_visible_text(value):
    if not isinstance(value, str) or not value:
        return value
    lowered_value = value.lower()
    if _routils_is_network_error(value):
        return 'could not reach the server check your internet connection and try again'
    special_phrases = (
        UI_TEXT['i5'], 'Gemini AI', 'RoUtils AI', 'Roblox File Converter',
        UI_TEXT['m5'], UI_TEXT['n5'], 'Global FFlag Hotkeys',
        'R6 Animation → R15', 'Mesh to OBJ'
    )
    saved_phrases = []
    for index, phrase in enumerate(special_phrases):
        marker = chr(0xE000 + index)
        if re.search(re.escape(phrase), value, re.IGNORECASE):
            value = re.sub(re.escape(phrase), marker, value, flags=re.IGNORECASE)
            saved_phrases.append((marker, phrase))
    def clean_line(line):
        if not line.strip():
            return line
        abbreviation_tokens = ('e.g.', 'i.e.', 'mr.', 'mrs.', 'dr.', 'vs.')
        protected = []
        for index, token in enumerate(abbreviation_tokens):
            marker = chr(0xE100 + index)
            if re.search(re.escape(token), line, re.IGNORECASE):
                line = re.sub(re.escape(token), marker, line, flags=re.IGNORECASE)
                protected.append((marker, token))
        parts = re.split(r'(?<!\.)\.(?!\.)(?=\s+)', line)
        if len(parts) > 1:
            leading = line[:len(line) - len(line.lstrip())]
            result = '\n'.join((leading if index == 0 else '') + clean_line(part.strip()) for index, part in enumerate(parts) if part.strip())
            for marker, token in protected:
                result = result.replace(marker, token)
            return result
        line = re.sub(r'(?<!\.)\.(?!\.)(?=\s|$)', '', line)
        for marker, token in protected:
            line = line.replace(marker, token)
        plain = line.strip()
        if not plain or any(token in plain for token in ('://', '\\', '/e ', '{', '}', '```')):
            return line
        words = re.findall(r"[A-Za-z][A-Za-z0-9]*", plain)
        special = {'routils', 'roblox', 'fflag', 'fflags', 'ai', 'api', 'pid', 'fps', 'json', 'xml', 'csv', 'url', 'cpu', 'ram', 'http', 'https', 'obj', 'rbxm', 'rbxmx', 'rbxl', 'ctrl', 'shift', 'alt', 'esc', 'enter', 'tab', 'ui', 'hashsaves', 'filesaves', 'cconfigs', 'id', 'dpi', 'gpu', 'ram', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'}
        def title_like(word):
            low = word.lower()
            if low in special or word.isupper() or re.fullmatch(r'[A-Z]+\d+', word) or re.fullmatch(r'\d+', word):
                return True
            return len(word) > 0 and word[0].isupper() and word[1:].islower()
        if len(words) >= 2 and all(title_like(word) for word in words):
            first_alpha = True
            def convert_title_case_match(match):
                nonlocal first_alpha
                word = match.group(0)
                low = word.lower()
                if low in special:
                    mapping = {'routils':'RoUtils','roblox':'Roblox','fflag':'FFlag','fflags':UI_TEXT['h5'],'ai':UI_TEXT['j5'],'api':'API','pid':'PID','fps':'FPS','json':'JSON','xml':'XML','csv':'CSV','url':'URL','cpu':'CPU','ram':'RAM','http':'HTTP','https':'HTTPS','obj':'OBJ','rbxm':'RBXM','rbxmx':'RBXMX','rbxl':'RBXL','ctrl':'Ctrl','shift':'Shift','alt':'Alt','esc':'Esc','enter':'Enter','tab':'Tab','ui':'UI','hashsaves':'HashSaves','filesaves':'FileSaves','cconfigs':'CConfigs','id':'ID','dpi':'DPI','gpu':'GPU'}
                    return mapping.get(low, word)
                if word.isupper() or re.fullmatch(r'[A-Z]+\d+', word) or re.fullmatch(r'\d+', word):
                    return word
                if first_alpha:
                    first_alpha = False
                    return word[:1].upper() + word[1:].lower()
                first_alpha = False
                return word.lower()
            plain = re.sub(r'[A-Za-z][A-Za-z0-9]*', convert_title_case_match, plain)
            leading = line[:len(line) - len(line.lstrip())]
            trailing = line[len(line.rstrip()):]
            line = leading + plain + trailing
        return line
    value = '\n'.join(clean_line(line) for line in value.split('\n'))
    for marker, phrase in saved_phrases:
        value = value.replace(marker, phrase)
    return value
def _routils_install_text_rules():
    widget_classes = (
        (tk.Label, False, False), (tk.Button, False, False), (tk.Checkbutton, True, False),
        (tk.Radiobutton, False, False), (tk.LabelFrame, False, False),
        (ttk.Label, False, False), (ttk.Button, False, False), (ttk.Checkbutton, True, True),
        (ttk.Radiobutton, False, False), (ttk.LabelFrame, False, False)
    )
    for widget_class, is_checkbutton, is_ttk_checkbutton in widget_classes:
        if getattr(widget_class, '_routils_text_rules_installed', False):
            continue
        original_init = widget_class.__init__
        original_configure = widget_class.configure
        def wrapped_init(self, *args, __original=original_init, __is_check=is_checkbutton, __ttk_check=is_ttk_checkbutton, __widget_class=widget_class, **kwargs):
            if 'text' in kwargs:
                kwargs['text'] = _routils_visible_text(kwargs['text'])
            if __ttk_check and ttkbootstrap is not None and kwargs.get('style') in (None, '', 'TCheckbutton'):
                kwargs['style'] = 'primary.TCheckbutton'
            if __is_check and __widget_class is tk.Checkbutton:
                kwargs.setdefault('selectcolor', '#1688e8')
            __original(self, *args, **kwargs)
        def wrapped_configure(self, cnf=None, __original=original_configure, __is_check=is_checkbutton, __ttk_check=is_ttk_checkbutton, **kwargs):
            if isinstance(cnf, dict):
                cnf = dict(cnf)
                if 'text' in cnf:
                    cnf['text'] = _routils_visible_text(cnf['text'])
            if 'text' in kwargs:
                kwargs['text'] = _routils_visible_text(kwargs['text'])
            if __ttk_check and ttkbootstrap is not None and kwargs.get('style') == 'TCheckbutton':
                kwargs['style'] = 'primary.TCheckbutton'
            return __original(self, cnf, **kwargs)
        widget_class.__init__ = wrapped_init
        widget_class.configure = wrapped_configure
        widget_class.config = wrapped_configure
        widget_class._routils_text_rules_installed = True
    for widget_class in (tk.Tk, tk.Toplevel):
        original_title = widget_class.title
        def wrapped_title(self, text=None, __original=original_title):
            if text is None:
                return __original(self)
            return __original(self, _routils_visible_text(text))
        widget_class.title = wrapped_title
    original_create_text = tk.Canvas.create_text
    def wrapped_create_text(self, *args, **kwargs):
        if 'text' in kwargs:
            kwargs['text'] = _routils_visible_text(kwargs['text'])
        return original_create_text(self, *args, **kwargs)
    tk.Canvas.create_text = wrapped_create_text
    original_itemconfigure = tk.Canvas.itemconfigure
    def wrapped_itemconfigure(self, *args, **kwargs):
        if isinstance(kwargs.get('text'), str):
            kwargs['text'] = _routils_visible_text(kwargs['text'])
        return original_itemconfigure(self, *args, **kwargs)
    tk.Canvas.itemconfigure = wrapped_itemconfigure
    tk.Canvas.itemconfig = wrapped_itemconfigure
    for method_name in ('add_command', 'add_cascade', 'add_radiobutton', 'add_checkbutton'):
        original_menu_method = getattr(tk.Menu, method_name)
        def wrapped_menu_method(self, *args, __original=original_menu_method, **kwargs):
            if 'label' in kwargs:
                kwargs['label'] = _routils_visible_text(kwargs['label'])
            if 'text' in kwargs:
                kwargs['text'] = _routils_visible_text(kwargs['text'])
            return __original(self, *args, **kwargs)
        setattr(tk.Menu, method_name, wrapped_menu_method)
    original_heading = ttk.Treeview.heading
    def wrapped_heading(self, column, option=None, **kwargs):
        if isinstance(kwargs.get('text'), str):
            kwargs['text'] = _routils_visible_text(kwargs['text'])
        return original_heading(self, column, option, **kwargs)
    ttk.Treeview.heading = wrapped_heading
    original_notebook_add = ttk.Notebook.add
    def wrapped_notebook_add(self, child, **kwargs):
        if isinstance(kwargs.get('text'), str):
            kwargs['text'] = _routils_visible_text(kwargs['text'])
        return original_notebook_add(self, child, **kwargs)
    ttk.Notebook.add = wrapped_notebook_add
    with _NOTIFICATION_HISTORY_LOCK:
        for entry in _NOTIFICATION_HISTORY:
            if isinstance(entry, dict):
                entry['title'] = _routils_visible_text(str(entry.get('title', 'Notification')))
                entry['message'] = _routils_visible_text(str(entry.get('message', '')))
    for name in ('showinfo', 'showwarning', 'showerror', 'askquestion', 'askokcancel', 'askyesno', 'askretrycancel'):
        original_messagebox = getattr(messagebox, name, None)
        if not callable(original_messagebox):
            continue
        def wrapped_messagebox(title, text, *args, __original=original_messagebox, __name=name, **kwargs):
            title = _routils_visible_text(title)
            text = _routils_visible_text(text)
            if __name == 'showerror' and isinstance(text, str) and re.search(r'(Traceback|AttributeError|TclError|WinError|RuntimeError|FileNotFoundError|No module named)', text, re.IGNORECASE):
                text = 'RoUtils could not complete this action\n\nTry again and check the error log if it keeps happening'
            return __original(title, text, *args, **kwargs)
        setattr(messagebox, name, wrapped_messagebox)
_routils_shared_module_names = ('autoupdate.autoupdate', 'ai.ai', 'cache.cache', 'client.client', 'console.console', 'emote_manager.emote_manager', 'fflag.fflag', 'history.history', 'home.home', 'plugins.plugins', 'release_notes.release_notes', 'server_viewer.server_viewer', 'settings.settings', 'subplace.subplace', 'themes.themes', 'viewer.viewer')
for _routils_module_name in _routils_shared_module_names:
    _routils_module = sys.modules.get(_routils_module_name)
    if _routils_module is not None:
        _routils_module.__dict__.update({k: v for k, v in globals().items() if not k.startswith('__') and k not in {'_host'}})
        _routils_module.__dict__['__file__'] = __file__
del _routils_shared_module_names, _routils_module_name, _routils_module
def main():
    global _ACTIVE_APP
    _routils_install_text_rules()
    _install_error_hooks()
    if '--webview2' in sys.argv:
        try:
            idx = sys.argv.index('--webview2')
            url = sys.argv[idx + 1]
            title = sys.argv[idx + 2] if len(sys.argv) > idx + 2 else 'RoUtils w2'
            _launch_webview2(url, title)
        except Exception as e:
            try:
                messagebox.showerror(UI_TEXT['f1'], str(e))
            except Exception:
                pass
        return
    if '--dump-caches' in sys.argv:
        try:
            helper = object.__new__(App)
            code = App._run_dump_caches_cli(helper)
        except Exception as e:
            print(UI_TEXT['p27'].format(p0=e), flush=True)
            code = 1
        input(UI_TEXT['d28'])
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
