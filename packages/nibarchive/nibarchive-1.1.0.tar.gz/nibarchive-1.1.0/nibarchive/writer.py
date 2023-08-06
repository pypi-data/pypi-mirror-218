# Copyright (C) 2023 MatrixEditor

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from __future__ import annotations

import struct
import io

from nibarchive import (
    NIBArchive,
    NIBArchiveHeader,
    NIBObject,
    NIBKey,
    NIBValue,
    ClassName,
    MAGIC_BYTES,
)


def dump(archive: NIBArchive, fp: io.IOBase) -> None:
    if not fp or not fp.writable():
        raise ValueError("Invalid input file pointer - not writable!")

    encoder = NIBArchiveEncoder()
    fp.write(MAGIC_BYTES)
    fp.write(encoder.encode_header(archive.header))
    for obj in archive.objects:
        fp.write(encoder.encode_object(obj))

    for key in archive.keys:
        fp.write(encoder.encode_key(key))

    for value in archive.values:
        fp.write(encoder.encode_value(value))

    for class_name in archive.class_names:
        fp.write(encoder.encode_class_name(class_name))


class NIBArchiveEncoder:
    def encode_archive(self, archive: NIBArchive) -> bytes:
        objects = bytes()
        for obj in archive.objects:
            objects += self.encode_object(obj)

        keys = bytes()
        for key in archive.keys:
            keys += self.encode_key(key)

        values = bytes()
        for value in archive.values:
            values += self.encode_value(value)

        class_names = bytes()
        for class_name in archive.class_names:
            class_names += self.encode_class_name(class_name)

        return (
            MAGIC_BYTES
            + self.encode_header(archive.header)
            + objects
            + keys
            + values
            + class_names
        )

    def encode_varint(self, value: int) -> bytes:
        if value < 128:
            return bytes([value])

        first = (value & 0xFF00) >> 8
        second = (value & 0x00FF) ^ 128
        return bytes([first, second])

    def encode_object(self, obj: NIBObject) -> bytes:
        return (
            self.encode_varint(obj.class_name_index)
            + self.encode_varint(obj.values_index)
            + self.encode_varint(obj.value_count)
        )

    def encode_class_name(self, class_name: ClassName) -> bytes:
        if len(class_name.extras) > 0:
            extras = struct.pack(
                "<%s" % "i" * len(class_name.extras), class_name.extras
            )
        else:
            extras = bytes()

        return (
            self.encode_varint(class_name.length)
            + self.encode_varint(class_name.extras_count)
            + extras
            + class_name.name.encode()
        )

    def encode_key(self, key: NIBKey) -> bytes:
        return self.encode_varint(key.length) + key.name.encode()

    def encode_value(self, value: NIBValue) -> bytes:
        return (
            self.encode_varint(value.key_index)
            + bytes([value.type.value])
            + getattr(self, f"_encode_{value.type.name.lower()}")(value.data)
        )

    def encode_header(self, header: NIBArchiveHeader) -> bytes:
        return struct.pack(
            "<%s" % "i" * 10,
            bytes([header.__dict__[key] for key in header.__dict__])
        )

    def _encode_int8(self, data) -> bytes:
        return bytes([data])

    def _encode_int16(self, data) -> bytes:
        return struct.pack("<h", data)

    def _encode_int32(self, data) -> bytes:
        return struct.pack("<i", data)

    def _encode_int64(self, data) -> bytes:
        return struct.pack("<q", data)

    def _encode_nil(self, data) -> bytes:
        return bytes()

    def _encode_bool_true(self, data) -> bytes:
        return self._encode_nil(data)

    def _encode_bool_false(self, data) -> bytes:
        return self._encode_nil(data)

    def _encode_float(self, data) -> bytes:
        return struct.pack("<f", data)

    def _encode_double(self, data) -> bytes:
        return struct.pack("<d", data)

    def _encode_object_ref(self, data) -> bytes:
        return self._encode_int32(data)

    def _encode_data(self, data) -> bytes:
        return self.encode_varint(len(data)) + data
