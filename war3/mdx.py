"""This module contains an importer for the MDX format."""


import struct
from .model import *

__all__ = ["LoadError", "Loader", "load"]


class LoadError(Exception):
    pass


class Loader:
    def __init__(self, infile):
        self.infile = infile
        self.model = Model()

    def load(self):
        self.check_magic_number()
        self.load_version()
        self.load_modelinfo()
        self.load_sequences()
        self.load_global_sequences()
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


def load(infile):
    if isinstance(infile, str):
        infile = open(infile, 'rb')
    return Loader(infile).load()
