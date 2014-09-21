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
        return self.model

    def check_magic_number(self):
        if self.infile.read(4) != b'MDLX':
            raise LoadError("not a MDX file")

    def load_version(self):
        buf = self.infile.read(4)
        if buf != b'VERS':
            raise LoadError("expected VERS, not %s" % buf.decode("ascii"))

        buf = self.load_block()
        self.model.version, = struct.unpack('<i', buf)

    def load_block(self):
        n, = struct.unpack('<i', self.infile.read(4))
        if n < 0:
            raise LoadError("expected a positive integer")
        return self.infile.read(n)

    def load_modelinfo(self):
        buf = self.infile.read(4)
        if buf != b'MODL':
            raise LoadError("expected MODL, not %s" % buf.decode("ascii"))

        buf = self.load_block()
        name, = struct.unpack_from('<80s', buf)
        name = name.rstrip(b'\x00').decode("ascii")
        bounds_radius, = struct.unpack_from('<f', buf, 80)
        min_extent = struct.unpack_from('<3f', buf, 84)
        max_extent = struct.unpack_from('<3f', buf, 96)
        blend_time, = struct.unpack_from('<i', buf, 108)

        self.model.model = ModelInfo(name, bounds_radius,
                                     min_extent, max_extent, blend_time)


def load(infile):
    if isinstance(infile, str):
        infile = open(infile, 'rb')
    return Loader(infile).load()
