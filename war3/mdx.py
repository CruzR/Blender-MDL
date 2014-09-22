"""This module contains an importer for the MDX format."""


import struct
import sys
from .model import *

__all__ = ["LoadError", "Loader", "load"]


class LoadError(Exception):
    pass


class _ReadonlyBytesIO:
    def __init__(self, buf, idx=0):
        self.buf = buf
        self.idx = idx

    def read(self, n=-1):
        idx = self.idx
        if n < 0 or len(self.buf) - idx < n:
            self.idx = len(self.buf)
            return self.buf[self.idx:]
        else:
            self.idx += n
            return self.buf[idx:self.idx]


class Loader:
    def __init__(self, infile):
        self.infile = infile
        self.infile_stack = []
        self.model = Model()

    def load(self):
        self.check_magic_number()
        self.load_version()
        self.load_modelinfo()
        self.load_sequences()
        self.load_global_sequences()
        self.load_materials()
        self.load_textures()
        return self.model

    def check_magic_number(self):
        if self.infile.read(4) != b'MDLX':
            raise LoadError("not a MDX file")

    def check_block_magic(self, magic):
        buf = self.infile.read(4)
        if buf != magic:
            raise LoadError("expected %s, not %s"
                            % (magic.decode("ascii"), buf.decode("ascii")))

    def load_version(self):
        self.check_block_magic(b'VERS')
        buf = self.load_block()
        self.model.version, = struct.unpack('<i', buf)

    def load_block(self):
        n, = struct.unpack('<i', self.infile.read(4))
        if n < 0:
            raise LoadError("expected a positive integer")
        return self.infile.read(n)

    def load_modelinfo(self):
        self.check_block_magic(b'MODL')
        buf = self.load_block()

        name, = struct.unpack_from('<80s', buf)
        name = name.rstrip(b'\x00').decode("ascii")
        bounds_radius, = struct.unpack_from('<f', buf, 80)
        min_extent = struct.unpack_from('<3f', buf, 84)
        max_extent = struct.unpack_from('<3f', buf, 96)
        blend_time, = struct.unpack_from('<i', buf, 108)

        self.model.model = ModelInfo(name, bounds_radius,
                                     min_extent, max_extent, blend_time)

    def load_sequences(self):
        self.check_block_magic(b'SEQS')
        buf = self.load_block()
        fmt = '<80s 2i f i f 4x f 3f 3f'

        for i in range(0, len(buf), struct.calcsize(fmt)):
            t = struct.unpack_from(fmt, buf, i)

            name = t[0].rstrip(b'\x00').decode("ascii")
            interval = t[1:3]
            move_speed = t[4]
            non_looping = bool(t[5])
            rarity = t[6]
            bounds_radius = t[7]
            min_extent = t[8:11]
            max_extent = t[11:]

            self.model.sequences.append(
                Animation(name, interval, move_speed, non_looping, rarity,
                          bounds_radius, min_extent, max_extent)
            )

    def load_global_sequences(self):
        self.check_block_magic(b'GLBS')
        buf = self.load_block()
        i, n = 0, len(buf)
        while i < n:
            duration, = struct.unpack_from('<i', buf, i)
            self.model.global_sequences.append(duration)
            i += 4

    def load_materials(self):
        self.check_block_magic(b'MTLS')
        buf = self.load_block()
        i, n = 0, len(buf)

        while i < n:
            t = struct.unpack_from('<i i i', buf, i)
            mat = Material(t[1], bool(t[2] & 0x01),
                           bool(t[2] & 0x10), bool(t[2] & 0x20))

            # HACK: let load_layers() read from existing data
            self.push_infile(_ReadonlyBytesIO(buf, i + 12))
            mat.layers = self.load_layers()
            self.pop_infile()

            self.model.materials.append(mat)
            i += t[0]

    def push_infile(self, infile):
        self.infile_stack.append(self.infile)
        self.infile = infile

    def pop_infile(self):
        infile = self.infile
        self.infile = self.infile_stack.pop()
        return infile

    def load_layers(self):
        self.check_block_magic(b'LAYS')
        nlays, = struct.unpack('<i', self.infile.read(4))
        fmt = '<5i f'
        lays = []

        for i in range(nlays):
            n, = struct.unpack('<i', self.infile.read(4))
            buf = self.infile.read(n - 4)

            t = struct.unpack_from(fmt, buf)
            layer = Layer(t[0], bool(t[1] & 0x01), bool(t[1] & 0x02),
                          bool(t[1] & 0x10), bool(t[1] & 0x20),
                          bool(t[1] & 0x40), bool(t[1] & 0x80),
                          t[2], t[3], t[4], t[5])

            j, n = struct.calcsize(fmt), len(buf)
            while j < n:
                j, anim = self.load_material_keyframe(buf, j)
                layer.animations.append(anim)

            lays.append(layer)

        return lays

    def load_material_keyframe(self, buf, j):
        magic = buf[j:j+4]
        if magic == b'KMTA':
            target = KF.MaterialAlpha
            fmt0 = '<i f'
            fmt1 = '<2f'
        elif magic == b'KMTF':
            target = KF.MaterialTexture
            fmt0 = fmt1 = '<2i'
        else:
            raise LoadError("exptected KMT{A,F}, not %s"
                            % buf[j:j+4].decode("ascii"))

        t = struct.unpack_from('<3i', buf, j + 4)
        numkeys = t[0]
        linetype = LineType(t[1])
        gsid = t[2]
        j += 16

        anim = KeyframeAnimation(target, linetype, gsid)
        for k in range(numkeys):
            print(k)
            frame, value = struct.unpack_from(fmt0, buf, j)
            j += 8

            if linetype in (LineType.Hermite, LineType.Bezier):
                tin, tout = struct.unpack_from(fmt1, buf, j)
                j += 8
            else:
                tin = tout = None

            anim.keyframes.append(Keyframe(frame, value, tin, tout))

        return j, anim

    def load_textures(self):
        self.check_block_magic(b'TEXS')
        buf = self.load_block()
        fmt = '<i 256s 4x i'

        for i in range(0, len(buf), struct.calcsize(fmt)):
            t = struct.unpack_from(fmt, buf, i)
            rid = t[0]
            path = t[1].rstrip(b'\x00').decode("ascii")
            wrap_w = bool(t[2] & 1)
            wrap_h = bool(t[2] & 2)
            self.model.textures.append(Texture(rid, path, wrap_w, wrap_h))


def load(infile):
    if isinstance(infile, str):
        infile = open(infile, 'rb')
    return Loader(infile).load()
