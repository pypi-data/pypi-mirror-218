# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol, TypeVar

_T = TypeVar("_T")


class TextureFilter(Protocol[_T]):
    @abstractmethod
    def __call__(self, textures: Sequence[_T]) -> Sequence[_T]:
        ...


class TextureCombinedFilter(TextureFilter[_T]):
    def __init__(self, filters: Sequence[TextureFilter[_T]]) -> None:
        self._filters = filters

    def __call__(self, textures: Sequence[_T]) -> Sequence[_T]:
        for texture_filter in self._filters:
            textures = texture_filter(textures)

        return textures
