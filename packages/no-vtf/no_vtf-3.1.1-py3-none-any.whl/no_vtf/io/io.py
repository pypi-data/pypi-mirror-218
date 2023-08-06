# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import pathlib

from abc import abstractmethod
from collections.abc import Sequence
from typing import Generic, TypeVar

import no_vtf.io  # noqa: F401  # define all task runners for IO.initialize()

_A_contra = TypeVar("_A_contra", contravariant=True)


class IO(Generic[_A_contra]):
    @classmethod
    def initialize(cls, *, _recursive: bool = True) -> None:
        if _recursive:
            for subclass in cls.__subclasses__():
                subclass.initialize()

    def write(self, path: pathlib.Path, data: _A_contra, /) -> None:
        self.write_sequence(path, [data])

    def readback(self, path: pathlib.Path, data: _A_contra, /) -> None:
        self.readback_sequence(path, [data])

    @abstractmethod
    def write_sequence(self, path: pathlib.Path, sequence: Sequence[_A_contra], /) -> None:
        ...

    @abstractmethod
    def readback_sequence(self, path: pathlib.Path, sequence: Sequence[_A_contra], /) -> None:
        ...
