# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import pathlib

from collections.abc import Sequence

from no_vtf.io.io import IO


class BytesIO(IO[bytes]):
    def write_sequence(self, path: pathlib.Path, sequence: Sequence[bytes]) -> None:
        with open(path, "wb") as file:
            for data in sequence:
                file.write(data)

    def readback_sequence(self, path: pathlib.Path, sequence: Sequence[bytes]) -> None:
        with open(path, "rb") as file:
            for data in sequence:
                read_data = file.read(len(data))
                if data != read_data:
                    raise RuntimeError(f"{path!r}: Data differs from what is in the file")

            if file.read():
                raise RuntimeError(f"{path!r}: Data differs from what is in the file")
