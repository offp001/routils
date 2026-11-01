import math
import struct
import threading
import time
import tkinter as tk
from tkinter import ttk

_host = __import__('sys').modules.get('main') or __import__('sys').modules.get('__main__')
if _host is not None:
    globals().update({k: v for k, v in vars(_host).items() if not k.startswith('__') and k not in {'_host'}})
_FFLAG_COLOR_MUTED = globals().get('_FFLAG_COLOR_MUTED', '#9aa0a6')
_FFLAG_COLOR_SUCCESS = globals().get('_FFLAG_COLOR_SUCCESS', '#65d98b')
_FFLAG_COLOR_ERROR = globals().get('_FFLAG_COLOR_ERROR', '#ff6b6b')
_FFLAG_COLOR_WARNING = globals().get('_FFLAG_COLOR_WARNING', '#f2c94c')

PROPERTY_GROUPS = ['Physics', 'Character', 'Character Parts', 'Camera', 'Lighting', 'World', 'GUI', 'Game Info']
PROPERTY_DEFINITIONS = []


def _register(group, title, target, section, rows, classes=None, root='dm'):
    for row in rows:
        field, value_type = row[0], row[1]
        options = row[2] if len(row) > 2 else {}
        target_name = target if target != 'scan' else classes[0]
        PROPERTY_DEFINITIONS.append({'key': f'{target_name}.{section}.{field}', 'group': group, 'title': title, 'label': options.get('label', field), 'type': value_type, 'target': target, 'classes': tuple(classes) if classes else None, 'root': root, 'at': options.get('at', (section, field)), 'plus': options.get('plus'), 'mask': options.get('mask'), 'conv': options.get('conv'), 'also': options.get('also', []), 'ro': options.get('ro', False)})


_READ_ONLY = {'ro': True}
_register('Physics', 'World', 'world', 'World', [('Gravity', 'float'), ('worldStepsPerSec', 'float', {'label': 'Physics FPS', 'conv': 'div4'}), ('FallenPartsDestroyHeight', 'float')])
_register('Physics', 'Air Properties', 'airprops', 'AirProperties', [('AirDensity', 'float'), ('GlobalWind', 'vec3')])
_register('Physics', 'Workspace', 'workspace', 'Workspace', [('ReadOnlyGravity', 'float', _READ_ONLY), ('DistributedGameTime', 'double', _READ_ONLY), ('StreamingEnabled', 'bool', _READ_ONLY)])
_register('Physics', 'Task Scheduler', 'scheduler', 'TaskScheduler', [('MaxFPS', 'double', {'label': 'FPS cap', 'conv': 'inv'})])
_register('Character', 'Humanoid', 'humanoid', 'Humanoid', [('Health', 'float'), ('MaxHealth', 'float'), ('Walkspeed', 'float', {'label': 'WalkSpeed', 'also': [('Humanoid', 'WalkspeedCheck')]}), ('JumpPower', 'float'), ('JumpHeight', 'float'), ('HipHeight', 'float'), ('MaxSlopeAngle', 'float'), ('HealthDisplayDistance', 'float'), ('NameDisplayDistance', 'float'), ('CameraOffset', 'vec3'), ('Jump', 'bool'), ('Sit', 'bool'), ('PlatformStand', 'bool'), ('UseJumpPower', 'bool'), ('AutomaticScalingEnabled', 'bool'), ('BreakJointsOnDeath', 'bool'), ('EvaluateStateMachine', 'bool'), ('AutoJumpEnabled', 'bool'), ('AutoRotate', 'bool'), ('DisplayDistanceType', 'int'), ('HealthDisplayType', 'int'), ('NameOcclusion', 'int'), ('RigType', 'int'), ('MoveDirection', 'vec3', _READ_ONLY), ('FloorMaterial', 'int', _READ_ONLY), ('IsWalking', 'bool', _READ_ONLY)])
_register('Character', 'Player', 'player', 'Player', [('MinZoomDistance', 'float'), ('MaxZoomDistance', 'float'), ('CameraMode', 'int'), ('HealthDisplayDistance', 'float'), ('NameDisplayDistance', 'float'), ('SimulationRadius', 'float', _READ_ONLY), ('MaxSimulationRadius', 'float', _READ_ONLY), ('UserId', 'i64', _READ_ONLY), ('AccountAge', 'int', _READ_ONLY)])
_register('Character', 'Character Model', 'character', 'Model', [('Scale', 'float')])
_register('Character', 'Root Part (BasePart)', 'part', 'BasePart', [('Transparency', 'float'), ('Reflectance', 'float'), ('Massless', 'bool'), ('CastShadow', 'bool'), ('Locked', 'bool'), ('Color3', 'u8x3'), ('Material', 'int')])
_register('Character', 'Root Part (Primitive)', 'primitive', 'Primitive', [('Position', 'vec3'), ('Size', 'vec3'), ('AssemblyLinearVelocity', 'vec3'), ('AssemblyAngularVelocity', 'vec3')])
_register('Character', 'Root Part Flags', 'primitive', 'PrimitiveFlags', [(name, 'flag', {'at': ('Primitive', 'Flags'), 'mask': ('PrimitiveFlags', name)}) for name in ('Anchored', 'CanCollide', 'CanTouch', 'CanQuery')])
_BODY_PARTS = [('Head', 'head'), ('Torso', 'torso'), ('UpperTorso', 'uppertorso'), ('LowerTorso', 'lowertorso'), ('LeftUpperArm', 'leftupperarm'), ('LeftLowerArm', 'leftlowerarm'), ('LeftHand', 'lefthand'), ('RightUpperArm', 'rightupperarm'), ('RightLowerArm', 'rightlowerarm'), ('RightHand', 'righthand'), ('LeftUpperLeg', 'leftupperleg'), ('LeftLowerLeg', 'leftlowerleg'), ('LeftFoot', 'leftfoot'), ('RightUpperLeg', 'rightupperleg'), ('RightLowerLeg', 'rightlowerleg'), ('RightFoot', 'rightfoot')]
for _label, _target in _BODY_PARTS:
    _register('Character Parts', f'{_label} (BasePart)', _target, 'BasePart', [('Transparency', 'float'), ('Reflectance', 'float'), ('Massless', 'bool'), ('CastShadow', 'bool'), ('Locked', 'bool'), ('Color3', 'u8x3'), ('Material', 'int')])
    _register('Character Parts', f'{_label} (Primitive)', _target, 'Primitive', [('Position', 'vec3'), ('Size', 'vec3'), ('AssemblyLinearVelocity', 'vec3'), ('AssemblyAngularVelocity', 'vec3')])
    _register('Character Parts', f'{_label} Flags', _target, 'PrimitiveFlags', [(name, 'flag', {'at': ('Primitive', 'Flags'), 'mask': ('PrimitiveFlags', name)}) for name in ('Anchored', 'CanCollide', 'CanTouch', 'CanQuery')])
_register('Camera', 'Camera', 'camera', 'Camera', [('FieldOfView', 'float', {'label': 'FieldOfView (degrees)', 'conv': 'deg'}), ('CameraType', 'int'), ('Position', 'vec3'), ('Focus', 'vec3'), ('ImagePlaneDepth', 'float', _READ_ONLY), ('NearPlaneZ', 'float', _READ_ONLY)])
_register('Lighting', 'Lighting', 'lighting', 'Lighting', [('ClockTime', 'double'), ('Brightness', 'float'), ('EnvironmentDiffuseScale', 'float'), ('EnvironmentSpecularScale', 'float'), ('ExposureCompensation', 'float'), ('GeographicLatitude', 'float'), ('FogStart', 'float'), ('FogEnd', 'float'), ('FogColor', 'color3'), ('Ambient', 'color3'), ('OutdoorAmbient', 'color3'), ('ColorShift_Top', 'color3'), ('ColorShift_Bottom', 'color3'), ('GlobalShadows', 'bool'), ('LightColor', 'color3'), ('GradientTop', 'color3'), ('GradientBottom', 'color3'), ('Technology', 'int'), ('ShadowSoftness', 'float'), ('LightDirection', 'vec3', _READ_ONLY), ('SunPosition', 'vec3', _READ_ONLY), ('MoonPosition', 'vec3', _READ_ONLY)])
_register('Lighting', 'Atmosphere', 'scan', 'Atmosphere', [('Density', 'float'), ('Offset', 'float'), ('Glare', 'float'), ('Haze', 'float'), ('Color', 'color3'), ('Decay', 'color3')], classes=['Atmosphere'], root='lighting')
_register('Lighting', 'Sky (sun / moon / stars)', 'scan', 'Sky', [('SunAngularSize', 'float'), ('MoonAngularSize', 'float'), ('StarCount', 'int')], classes=['Sky'], root='lighting')
_register('Lighting', 'BloomEffect', 'scan', 'BloomEffect', [('Intensity', 'float'), ('Size', 'float'), ('Threshold', 'float'), ('Enabled', 'bool')], classes=['BloomEffect'], root='lighting')
_register('Lighting', 'DepthOfFieldEffect', 'scan', 'DepthOfFieldEffect', [('FocusDistance', 'float'), ('FarIntensity', 'float'), ('NearIntensity', 'float'), ('InFocusRadius', 'float'), ('Enabled', 'bool')], classes=['DepthOfFieldEffect'], root='lighting')
_register('Lighting', 'SunRaysEffect', 'scan', 'SunRaysEffect', [('Intensity', 'float'), ('Spread', 'float'), ('Enabled', 'bool')], classes=['SunRaysEffect'])
_register('Lighting', 'ColorCorrectionEffect', 'scan', 'ColorCorrectionEffect', [('Brightness', 'float'), ('Contrast', 'float'), ('TintColor', 'color3'), ('Enabled', 'bool')], classes=['ColorCorrectionEffect'])
_register('Lighting', 'ColorGradingEffect', 'scan', 'ColorGradingEffect', [('TonemapperPreset', 'int'), ('Enabled', 'bool')], classes=['ColorGradingEffect'])
_register('Lighting', 'BlurEffect', 'scan', 'BlurEffect', [('Size', 'float'), ('Enabled', 'bool')], classes=['BlurEffect'])
_register('Lighting', 'Dynamic Lights', 'scan', 'Light', [('Brightness', 'float'), ('Color', 'color3'), ('Range', 'float'), ('Enabled', 'bool'), ('Shadows', 'bool')], classes=['PointLight', 'SpotLight', 'SurfaceLight'])
_register('World', 'Terrain', 'terrain', 'Terrain', [('GrassLength', 'float'), ('WaterReflectance', 'float'), ('WaterTransparency', 'float'), ('WaterWaveSize', 'float'), ('WaterWaveSpeed', 'float'), ('WaterColor', 'color3')])
_register('World', 'Terrain Material Colors', 'terrain', 'MaterialColors', [(name, 'u8x3', {'at': ('Terrain', 'MaterialColors'), 'plus': ('MaterialColors', name)}) for name in ('Asphalt', 'Basalt', 'Brick', 'Cobblestone', 'Concrete', 'CrackedLava', 'Glacier', 'Grass', 'Ground', 'Ice', 'LeafyGrass', 'Limestone', 'Mud', 'Pavement', 'Rock', 'Salt', 'Sand', 'Sandstone', 'Slate', 'Snow', 'WoodPlanks')])
_register('World', 'Highlight (ESP)', 'scan', 'Highlight', [('FillColor', 'color3'), ('OutlineColor', 'color3'), ('FillTransparency', 'float'), ('OutlineTransparency', 'float'), ('Enabled', 'bool'), ('DepthMode', 'int')], classes=['Highlight'])
_register('World', 'ProximityPrompt', 'scan', 'ProximityPrompt', [('HoldDuration', 'float'), ('MaxActivationDistance', 'float'), ('Enabled', 'bool'), ('RequiresLineOfSight', 'bool'), ('KeyCode', 'int'), ('GamepadKeyCode', 'int')], classes=['ProximityPrompt'])
_register('World', 'ClickDetector', 'scan', 'ClickDetector', [('MaxActivationDistance', 'float')], classes=['ClickDetector'])
_register('World', 'DragDetector', 'scan', 'DragDetector', [('MaxActivationDistance', 'float'), ('MaxForce', 'float'), ('MaxTorque', 'float'), ('Responsiveness', 'float'), ('MaxDragAngle', 'float'), ('MinDragAngle', 'float'), ('MaxDragTranslation', 'vec3'), ('MinDragTranslation', 'vec3')], classes=['DragDetector'])
_register('World', 'Sound', 'scan', 'Sound', [('Volume', 'float'), ('PlaybackSpeed', 'float'), ('RollOffMinDistance', 'float'), ('RollOffMaxDistance', 'float'), ('Looped', 'bool'), ('IsPlaying', 'bool'), ('TimePosition', 'double')], classes=['Sound'])
_register('World', 'SpawnLocation', 'scan', 'SpawnLocation', [('Enabled', 'bool'), ('Neutral', 'bool'), ('AllowTeamChangeOnTouch', 'bool'), ('ForcefieldDuration', 'float'), ('TeamColor', 'int')], classes=['SpawnLocation'])
_register('World', 'VehicleSeat', 'scan', 'VehicleSeat', [('MaxSpeed', 'float'), ('Torque', 'float'), ('TurnSpeed', 'float'), ('SteerFloat', 'float'), ('ThrottleFloat', 'float')], classes=['VehicleSeat'])
_register('World', 'Tool', 'scan', 'Tool', [('Enabled', 'bool'), ('CanBeDropped', 'bool'), ('ManualActivationOnly', 'bool'), ('RequiresHandle', 'bool')], classes=['Tool'])
_register('World', 'ParticleEmitter', 'scan', 'ParticleEmitter', [('Rate', 'float'), ('Brightness', 'float'), ('LightEmission', 'float'), ('LightInfluence', 'float'), ('ZOffset', 'float'), ('Drag', 'float'), ('TimeScale', 'float'), ('VelocityInheritance', 'float'), ('Lifetime', 'range'), ('Speed', 'range'), ('Rotation', 'range'), ('RotSpeed', 'range'), ('SpreadAngle', 'vec2'), ('Acceleration', 'vec3')], classes=['ParticleEmitter'])
_register('World', 'Beam', 'scan', 'Beam', [('Brightness', 'float'), ('LightEmission', 'float'), ('LightInfluence', 'float'), ('TextureLength', 'float'), ('TextureSpeed', 'float'), ('ZOffset', 'float'), ('CurveSize0', 'float'), ('CurveSize1', 'float'), ('Width0', 'float'), ('Width1', 'float')], classes=['Beam'])
_register('World', 'SurfaceAppearance', 'scan', 'SurfaceAppearance', [('Color', 'color3'), ('EmissiveTint', 'color3'), ('EmissiveStrength', 'float'), ('AlphaMode', 'int')], classes=['SurfaceAppearance'])
_register('World', 'Fire & Smoke', 'scan', 'ParticleEffect', [('Enabled', 'bool'), ('Size', 'float'), ('Heat', 'float')], classes=['Fire', 'Smoke'])
_register('World', 'Shirt / Pants Color', 'scan', 'Clothing', [('Color3', 'color3')], classes=['Shirt', 'Pants', 'ShirtGraphic'])
_register('World', 'CharacterMesh', 'scan', 'CharacterMesh', [('BodyPart', 'int')], classes=['CharacterMesh'])
_register('World', 'Attachment', 'scan', 'Attachment', [('Position', 'vec3')], classes=['Attachment'])
_register('World', 'SpecialMesh', 'scan', 'SpecialMesh', [('Scale', 'vec3')], classes=['SpecialMesh'])
_GUI_CLASSES = ['Frame', 'TextLabel', 'TextButton', 'TextBox', 'ImageLabel', 'ImageButton', 'ScrollingFrame', 'ViewportFrame', 'CanvasGroup']
_register('GUI', 'ScreenGui', 'scan', 'GuiObject', [('ScreenGui_Enabled', 'bool', {'label': 'Enabled'}), ('ResetOnSpawn', 'bool')], classes=['ScreenGui'], root='playergui')
_register('GUI', 'GuiObject (all frames / labels / buttons)', 'scan', 'GuiObject', [('Visible', 'bool'), ('BackgroundColor3', 'color3'), ('BackgroundTransparency', 'float'), ('BorderColor3', 'color3'), ('TextColor3', 'color3'), ('TextTransparency', 'float'), ('ImageTransparency', 'float'), ('Rotation', 'float'), ('ZIndex', 'int'), ('LayoutOrder', 'int'), ('ClipsDescendants', 'bool'), ('Active', 'bool')], classes=_GUI_CLASSES, root='playergui')
_register('Game Info', 'Game / Session', 'dm', 'DataModel', [('PlaceId', 'i64', _READ_ONLY), ('GameId', 'i64', _READ_ONLY), ('CreatorId', 'i64', _READ_ONLY), ('PlaceVersion', 'int', _READ_ONLY), ('GameLoaded', 'bool', _READ_ONLY), ('PrimitiveCount', 'int', _READ_ONLY)])
PROPERTY_BY_KEY = {item['key']: item for item in PROPERTY_DEFINITIONS}
PROPERTY_TYPES = {'float': '<f', 'int': '<i', 'double': '<d', 'byte': '<B', 'bool': '<B', 'flag': '<B', 'i64': '<q', 'vec2': '<2f', 'range': '<2f', 'vec3': '<3f', 'color3': '<3f', 'u8x3': '<3B'}
PART_ALIASES = {'head': ('Head',), 'torso': ('UpperTorso', 'Torso', 'LowerTorso'), 'uppertorso': ('UpperTorso', 'Torso'), 'lowertorso': ('LowerTorso', 'Torso'), 'leftupperarm': ('LeftUpperArm', 'Left Arm'), 'leftlowerarm': ('LeftLowerArm', 'Left Arm'), 'lefthand': ('LeftHand', 'Left Arm'), 'rightupperarm': ('RightUpperArm', 'Right Arm'), 'rightlowerarm': ('RightLowerArm', 'Right Arm'), 'righthand': ('RightHand', 'Right Arm'), 'leftupperleg': ('LeftUpperLeg', 'Left Leg'), 'leftlowerleg': ('LeftLowerLeg', 'Left Leg'), 'leftfoot': ('LeftFoot', 'Left Leg'), 'rightupperleg': ('RightUpperLeg', 'Right Leg'), 'rightlowerleg': ('RightLowerLeg', 'Right Leg'), 'rightfoot': ('RightFoot', 'Right Leg')}


class _ExternalPropertyContext:
    def __init__(self, app, offsets_data=None):
        self.app = app
        self.engine = app.fflag_engine
        source = offsets_data if isinstance(offsets_data, dict) else getattr(app, '_external_offsets_data', {})
        self.offsets = source.get('offsets', {})
        self.targets = {}
        self.scans = {}
        self.class_cache = {}

    def off(self, section, name):
        key = f'{section}::{name}'
        item = self.offsets.get(key)
        if not isinstance(item, dict) or item.get('value') is None:
            raise RuntimeError(f'Missing offset: {key}')
        return int(str(item['value']), 0)

    def sane(self, value):
        return value is not None and 65536 <= int(value) <= 140737488355327

    def read_pointer(self, address):
        return self.engine._read_u64(int(address))

    def read_bytes(self, address, size):
        data = self.engine._read(int(address), int(size))
        if data is None or len(data) != size:
            raise RuntimeError('Could not read the selected property from the Roblox client.')
        return data

    def read_string(self, address, max_len=128):
        length = struct.unpack('<Q', self.read_bytes(address + self.off('Misc', 'StringLength'), 8))[0]
        if length == 0 or length > max_len:
            return ''
        data_address = self.read_pointer(address) if length >= 16 else address
        if length >= 16 and not self.sane(data_address):
            return ''
        return self.read_bytes(data_address, length).decode('utf-8', 'ignore')

    def _read_cstr(self, address):
        return self.read_bytes(address, 64).split(b'\x00')[0].decode('utf-8', 'ignore')

    @staticmethod
    def _printable(value):
        return 0 < len(value) <= 64 and all(31 < ord(char) < 127 for char in value)

    def class_name(self, instance):
        descriptor = self.read_pointer(instance + self.off('Instance', 'ClassDescriptor'))
        if descriptor in self.class_cache:
            return self.class_cache[descriptor]
        name_pointer = self.read_pointer(descriptor + self.off('Instance', 'ClassName'))
        name = ''
        for reader in (self.read_string, self._read_cstr):
            try:
                candidate = reader(name_pointer)
                if self._printable(candidate):
                    name = candidate
                    break
            except Exception:
                continue
        if name:
            self.class_cache[descriptor] = name
        return name

    def children(self, instance):
        try:
            container = self.read_pointer(instance + self.off('Instance', 'ChildrenStart'))
            if not self.sane(container):
                return []
            start = self.read_pointer(container)
            end = self.read_pointer(container + self.off('Instance', 'ChildrenEnd'))
            if not self.sane(start) or end <= start:
                return []
            count = (end - start) // 16
            if count <= 0 or count > 200000:
                return []
            raw = self.read_bytes(start, count * 16)
            return [value for value in struct.unpack(f'<{2 * count}Q', raw)[0::2] if self.sane(value)]
        except Exception:
            return []

    def child_by_class(self, parent, wanted):
        for child in self.children(parent):
            try:
                if self.class_name(child) == wanted:
                    return child
            except Exception:
                continue
        raise RuntimeError(f'No {wanted} instance found')

    def instance_name(self, instance):
        if not self.sane(instance):
            return ''
        try:
            container = self.read_pointer(instance + self.off('Instance', 'NameContainer'))
            if not self.sane(container):
                return ''
            name_pointer = self.read_pointer(container + self.off('Instance', 'Name'))
            if self.sane(name_pointer):
                for reader in (self.read_string, self._read_cstr):
                    try:
                        value = reader(name_pointer)
                        if self._printable(value):
                            return value
                    except Exception:
                        continue
            for reader in (self.read_string, self._read_cstr):
                try:
                    value = reader(container)
                    if self._printable(value):
                        return value
                except Exception:
                    continue
        except Exception:
            return ''
        return ''

    def child_by_name_any(self, parent, names):
        wanted = {str(name).casefold() for name in names}
        for child in self.children(parent):
            try:
                if self.instance_name(child).casefold() in wanted:
                    return child
            except Exception:
                continue
        raise RuntimeError('Required character part was not found')

    def scan_classes(self, root, wanted, budget=4.0, node_cap=50000):
        found = {name: [] for name in wanted}
        stack = [root]
        started = time.monotonic()
        visited = 0
        while stack:
            if visited >= node_cap or time.monotonic() - started > budget:
                break
            node = stack.pop()
            visited += 1
            try:
                name = self.class_name(node)
            except Exception:
                continue
            if name in found:
                found[name].append(node)
            stack.extend(self.children(node))
        return found

    def scan(self, root, classes):
        have = self.scans.get(root)
        wanted = set(classes)
        if have is None or not wanted.issubset(have):
            combined = wanted | (set(have) if have else set())
            result = self.scan_classes(self.target(root), combined)
            self.scans[root] = result
        return [item for name in classes for item in self.scans[root].get(name, [])]

    def target(self, name):
        if name in self.targets:
            return self.targets[name]
        engine = self.engine
        if not engine.handle or not engine.module_base:
            raise RuntimeError('Open Roblox and select a client in Clients first.')
        if name == 'dm':
            fake = self.read_pointer(engine.module_base + self.off('FakeDataModel', 'Pointer'))
            result = self.read_pointer(fake + self.off('FakeDataModel', 'RealDataModel')) if self.sane(fake) else 0
        elif name == 'workspace':
            result = self.read_pointer(self.target('dm') + self.off('DataModel', 'Workspace'))
        elif name == 'world':
            result = self.read_pointer(self.target('workspace') + self.off('Workspace', 'World'))
        elif name == 'airprops':
            result = self.read_pointer(self.target('world') + self.off('World', 'AirProperties'))
        elif name == 'lighting':
            result = self.child_by_class(self.target('dm'), 'Lighting')
        elif name == 'terrain':
            result = self.child_by_class(self.target('workspace'), 'Terrain')
        elif name == 'camera':
            result = self.read_pointer(self.target('workspace') + self.off('Workspace', 'CurrentCamera'))
        elif name == 'player':
            players = self.child_by_class(self.target('dm'), 'Players')
            result = self.read_pointer(players + self.off('Player', 'LocalPlayer'))
        elif name == 'character':
            result = self.read_pointer(self.target('player') + self.off('Player', 'ModelInstance'))
        elif name == 'humanoid':
            character = self.target('character')
            try:
                result = self.child_by_class(character, 'Humanoid')
            except Exception:
                result = self.child_by_name_any(character, ('Humanoid',))
        elif name == 'part':
            character = self.target('character')
            humanoid = self.target('humanoid')
            result = self.read_pointer(humanoid + self.off('Humanoid', 'HumanoidRootPart'))
            if not self.sane(result):
                result = self.child_by_name_any(character, ('HumanoidRootPart',))
        elif name == 'primitive':
            result = self.read_pointer(self.target('part') + self.off('BasePart', 'Primitive'))
        elif name in PART_ALIASES:
            result = self.child_by_name_any(self.target('character'), PART_ALIASES[name])
        elif name == 'scheduler':
            result = self.read_pointer(engine.module_base + self.off('TaskScheduler', 'Pointer'))
        elif name == 'playergui':
            result = self.child_by_class(self.target('player'), 'PlayerGui')
        else:
            raise RuntimeError(f'Unknown property target: {name}')
        if not self.sane(result):
            raise RuntimeError(f'{name} is not available in the current Roblox session.')
        self.targets[name] = result
        return result


def _property_address(prop, obj, context):
    address = obj + context.off(*prop['at'])
    if prop.get('plus'):
        address += context.off(*prop['plus'])
    return address


def _read_property_value(prop, address, context):
    value_type = prop['type']
    fmt = PROPERTY_TYPES[value_type]
    raw = struct.unpack(fmt, context.read_bytes(address, struct.calcsize(fmt)))
    if value_type == 'flag':
        return bool(raw[0] & context.off(*prop['mask']))
    if value_type == 'bool':
        return raw[0] != 0
    value = raw[0] if len(raw) == 1 else list(raw)
    conversion = prop.get('conv')
    if conversion == 'deg':
        value = math.degrees(value)
    elif conversion == 'inv':
        value = 1.0 / value if value else 0.0
    elif conversion == 'div4':
        value = value / 4.0
    if isinstance(value, float):
        return round(value, 4)
    if isinstance(value, list) and value_type in ('vec2', 'range', 'vec3', 'color3'):
        return [round(item, 4) for item in value]
    return value


def _property_objects(prop, context):
    if prop['target'] == 'scan':
        objects = context.scan(prop['root'], prop['classes'])
        if not objects:
            raise RuntimeError('No matching Roblox objects were found.')
        return objects
    return [context.target(prop['target'])]


def _read_property(prop, context):
    objects = _property_objects(prop, context)
    return {'value': _read_property_value(prop, _property_address(prop, objects[0], context), context), 'count': len(objects)}


class ExternalPropertiesMixin:
    def _external_build_property_panel(self, tab):
        self._external_property_values = {}
        self._external_property_selected = None
        self._external_property_load_active = False
        self._external_property_trees = {}
        self._external_property_refresh_job = None
        self._external_property_last_pid = 0
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        header = ttk.Frame(tab)
        header.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        ttk.Label(header, text='Offsets', font=('Segoe UI Semibold', 10)).pack(side='left')
        self.external_property_status = ttk.Label(header, text='Waiting for a Roblox client', foreground=_FFLAG_COLOR_MUTED)
        self.external_property_status.pack(side='right')
        self.external_property_notebook = ttk.Notebook(tab)
        self.external_property_notebook.grid(row=1, column=0, sticky='nsew')
        for group in PROPERTY_GROUPS:
            page = ttk.Frame(self.external_property_notebook, padding=7)
            page.rowconfigure(0, weight=1)
            page.columnconfigure(0, weight=1)
            tree = ttk.Treeview(page, columns=('property', 'value', 'type'), show='headings', selectmode='browse')
            tree.heading('property', text='Property')
            tree.heading('value', text='Current Value')
            tree.heading('type', text='Type')
            tree.column('property', width=230, anchor='w', stretch=True)
            tree.column('value', width=170, anchor='w', stretch=True)
            tree.column('type', width=80, anchor='center', stretch=False)
            tree.tag_configure('readonly', foreground=_FFLAG_COLOR_MUTED)
            scrollbar = ttk.Scrollbar(page, orient='vertical', command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            tree.grid(row=0, column=0, sticky='nsew')
            scrollbar.grid(row=0, column=1, sticky='ns')
            tree.bind('<<TreeviewSelect>>', lambda event, selected_group=group: self._external_property_select(event, selected_group))
            self.external_property_notebook.add(page, text=group)
            self._external_property_trees[group] = tree
            for prop in (item for item in PROPERTY_DEFINITIONS if item['group'] == group):
                tree.insert('', 'end', iid=prop['key'], values=(prop['label'], '—', prop['type']), tags=('readonly',))
        footer = ttk.Frame(tab)
        footer.grid(row=2, column=0, sticky='ew', pady=(8, 0))
        footer.columnconfigure(0, weight=1)
        self.external_property_status_detail = ttk.Label(footer, text='Live values refresh automatically when the client or game changes.', foreground=_FFLAG_COLOR_MUTED)
        self.external_property_status_detail.grid(row=0, column=0, sticky='w')
        gravity_tree = self._external_property_trees.get('Physics')
        if gravity_tree is not None and gravity_tree.exists('world.World.Gravity'):
            gravity_tree.selection_set('world.World.Gravity')
            gravity_tree.focus('world.World.Gravity')
            self._external_property_select(None, 'Physics')
        self._external_property_schedule_refresh()

    def _external_property_select(self, event, group):
        tree = self._external_property_trees.get(group)
        if tree is None:
            return
        selection = tree.selection()
        if not selection:
            return
        prop = PROPERTY_BY_KEY.get(selection[0])
        if not prop:
            return
        self._external_property_selected = prop
        result = self._external_property_values.get(prop['key'])
        if result is None:
            self.external_property_status_detail.configure(text=f"{prop['title']} · {prop['label']} · waiting for live value", foreground=_FFLAG_COLOR_MUTED)
        else:
            count = result.get('count', 1)
            self.external_property_status_detail.configure(text=f"{prop['title']} · {prop['label']} · {result.get('display', 'N/A')} · {count} object(s)", foreground=_FFLAG_COLOR_SUCCESS)
        self._external_property_refresh_selected(silent=True)

    def _external_properties_offsets_ready(self):
        engine = getattr(self, 'fflag_engine', None)
        pid = int(getattr(self, 'fflag_pid', 0) or 0)
        state = 'Offsets ready'
        if pid and engine and engine.handle:
            state += f' · Client {pid}'
        self.external_property_status.configure(text=state, foreground=_FFLAG_COLOR_SUCCESS)
        self._external_property_refresh_all(silent=True)
        if hasattr(self, '_external_explorer_refresh') and pid and engine and engine.handle:
            self.after(250, self._external_explorer_refresh)
        self._external_property_schedule_refresh()

    def _external_property_refresh_all(self, silent=True):
        if getattr(self, '_external_property_load_active', False):
            return
        engine = getattr(self, 'fflag_engine', None)
        pid = int(getattr(self, 'fflag_pid', 0) or 0)
        if not engine or not engine.handle or not pid:
            if not silent:
                self.external_property_status_detail.configure(text='Attach a Roblox client to load current values.', foreground=_FFLAG_COLOR_WARNING)
            return
        self._external_property_load_active = True
        self.external_property_status_detail.configure(text='Reading current values…', foreground=_FFLAG_COLOR_MUTED)

        def worker():
            values = {}
            offsets_data = None
            fatal_error = ''
            try:
                if int(getattr(engine, 'pid', 0)) != pid:
                    raise RuntimeError('The selected Roblox client changed.')
                offsets_data = self._external_offsets_for_client(pid)
                context = _ExternalPropertyContext(self, offsets_data)
                scan_targets = {}
                for item in PROPERTY_DEFINITIONS:
                    if item.get('target') == 'scan':
                        scan_targets.setdefault(item.get('root', 'dm'), set()).update(item.get('classes') or ())
                for root_name, classes in scan_targets.items():
                    try:
                        target = context.target(root_name)
                        context.scans[root_name] = context.scan_classes(target, classes)
                    except Exception:
                        context.scans[root_name] = {name: [] for name in classes}
                for item in PROPERTY_DEFINITIONS:
                    try:
                        result = _read_property(item, context)
                        value = result.get('value')
                        display = ', '.join(str(part) for part in value) if isinstance(value, list) else str(value)
                        values[item['key']] = {'ok': True, 'value': value, 'display': display, 'count': int(result.get('count', 1))}
                    except Exception:
                        values[item['key']] = {'ok': False, 'display': 'N/A', 'count': 0}
            except Exception as error:
                fatal_error = str(error)
            try:
                self.after(0, self._external_property_refresh_all_finished, pid, values, offsets_data, fatal_error)
            except Exception:
                self._external_property_load_active = False

        threading.Thread(target=worker, daemon=True, name='RoUtilsExternalReadAll').start()

    def _external_property_refresh_all_finished(self, pid, values, offsets_data, fatal_error=''):
        self._external_property_load_active = False
        engine = getattr(self, 'fflag_engine', None)
        current_pid = int(getattr(self, 'fflag_pid', 0) or 0)
        if current_pid != int(pid) or not engine or not engine.handle:
            if current_pid and engine and engine.handle:
                self.after(100, lambda: self._external_property_refresh_all(silent=True))
            return
        self._external_property_last_pid = int(pid)
        if isinstance(offsets_data, dict):
            self._external_offsets_data = offsets_data
            version = str(offsets_data.get('version') or 'selected client')
            self.external_property_status.configure(text=f'Offsets · {version}', foreground=_FFLAG_COLOR_SUCCESS)
        loaded = 0
        unavailable = 0
        for item in PROPERTY_DEFINITIONS:
            result = values.get(item['key'], {})
            tree = self._external_property_trees.get(item['group'])
            if result.get('ok'):
                loaded += 1
                display = result.get('display', 'N/A')
                self._external_property_values[item['key']] = result
            else:
                unavailable += 1
                display = 'N/A'
                self._external_property_values[item['key']] = {'display': 'N/A', 'count': 0}
            if tree is not None and tree.exists(item['key']):
                tree.set(item['key'], 'value', display)
        if fatal_error:
            self.external_property_status_detail.configure(text=fatal_error, foreground=_FFLAG_COLOR_WARNING)
        else:
            self.external_property_status_detail.configure(text=f'Loaded {loaded}/{len(PROPERTY_DEFINITIONS)} live values · {unavailable} unavailable.', foreground=_FFLAG_COLOR_SUCCESS if loaded else _FFLAG_COLOR_WARNING)
        selected = self._external_property_selected
        if selected:
            self._external_property_select(None, selected['group'])

    def _external_property_refresh_selected(self, silent=False):
        prop = self._external_property_selected
        engine = getattr(self, 'fflag_engine', None)
        pid = int(getattr(self, 'fflag_pid', 0) or 0)
        if not prop or not engine or not engine.handle or not pid or getattr(self, '_external_property_load_active', False):
            return
        def worker():
            try:
                if int(getattr(engine, 'pid', 0)) != pid:
                    raise RuntimeError('Select the Roblox client again before reading properties.')
                offsets_data = self._external_offsets_for_client(pid)
                context = _ExternalPropertyContext(self, offsets_data)
                result = _read_property(prop, context)
                value = result['value']
                display = ', '.join(str(item) for item in value) if isinstance(value, list) else str(value)
                outcome = {'ok': True, 'value': value, 'display': display, 'count': result['count'], 'offsets_data': offsets_data}
            except Exception as error:
                outcome = {'ok': False, 'error': str(error)}
            try:
                self.after(0, self._external_property_refresh_finished, prop['key'], outcome, bool(silent))
            except Exception:
                pass
        threading.Thread(target=worker, daemon=True, name='RoUtilsExternalRead').start()

    def _external_property_refresh_finished(self, key, result, silent=False):
        prop = self._external_property_selected
        if not prop or prop['key'] != key:
            return
        if not result.get('ok'):
            self.external_property_status_detail.configure(text=str(result.get('error', 'Could not read property')), foreground=_FFLAG_COLOR_WARNING)
            return
        offsets_data = result.get('offsets_data')
        if isinstance(offsets_data, dict):
            self._external_offsets_data = offsets_data
            version = str(offsets_data.get('version') or 'selected client')
            self.external_property_status.configure(text=f'Offsets · {version}', foreground=_FFLAG_COLOR_SUCCESS)
        self._external_property_values[key] = result
        tree = self._external_property_trees.get(prop['group'])
        if tree is not None and tree.exists(key):
            tree.set(key, 'value', result['display'])
        self.external_property_status_detail.configure(text=f"{prop['title']} · {prop['label']} · {result['display']} · {result['count']} object(s)", foreground=_FFLAG_COLOR_SUCCESS)

    def _external_property_schedule_refresh(self):
        try:
            if self._external_property_refresh_job:
                self.after_cancel(self._external_property_refresh_job)
        except Exception:
            pass
        try:
            self._external_property_refresh_job = self.after(15000, self._external_property_auto_refresh)
        except Exception:
            self._external_property_refresh_job = None

    def _external_property_auto_refresh(self):
        self._external_property_refresh_job = None
        engine = getattr(self, 'fflag_engine', None)
        pid = int(getattr(self, 'fflag_pid', 0) or 0)
        if engine and engine.handle and pid and int(getattr(engine, 'pid', 0) or 0) == pid:
            self._external_property_refresh_selected(silent=True)
        self._external_property_schedule_refresh()


__all__ = ['ExternalPropertiesMixin', 'PROPERTY_DEFINITIONS', 'PROPERTY_GROUPS']
