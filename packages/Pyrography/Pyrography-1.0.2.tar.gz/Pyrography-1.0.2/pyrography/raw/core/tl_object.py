"""
Pyrography - A wonderful Pyrogram fork inspired by Pyromod & AmanoTeam/Pyrogram.
Copyright (C) 2023-present Lelzin λ <https://github.com/d3cryptofc>

Forked from Pyrogram <https://github.com/pyrogram/pyrogram>,
originally copyright (C) 2017-present Dan <https://github.com/delivrance>

This file is part of Pyrography.

Pyrography is is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

Pyrography is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
for more details.

You should have received a copy of the GNU Lesser General Public License along
with Pyrography. If not, see <http://www.gnu.org/licenses/>.
"""

from io import BytesIO
from json import dumps
from typing import cast, List, Any, Union, Dict

from ..all import objects


class TLObject:
    __slots__: List[str] = []

    QUALNAME = "Base"

    @classmethod
    def read(cls, b: BytesIO, *args: Any) -> Any:
        return cast(TLObject, objects[int.from_bytes(b.read(4), "little")]).read(b, *args)

    def write(self, *args: Any) -> bytes:
        pass

    @staticmethod
    def default(obj: "TLObject") -> Union[str, Dict[str, str]]:
        if isinstance(obj, bytes):
            return repr(obj)

        return {
            "_": obj.QUALNAME,
            **{
                attr: getattr(obj, attr)
                for attr in obj.__slots__
                if getattr(obj, attr) is not None
            }
        }

    def __str__(self) -> str:
        return dumps(self, indent=4, default=TLObject.default, ensure_ascii=False)

    def __repr__(self) -> str:
        if not hasattr(self, "QUALNAME"):
            return repr(self)

        return "pyrography.raw.{}({})".format(
            self.QUALNAME,
            ", ".join(
                f"{attr}={repr(getattr(self, attr))}"
                for attr in self.__slots__
                if getattr(self, attr) is not None
            )
        )

    def __eq__(self, other: Any) -> bool:
        for attr in self.__slots__:
            try:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False

        return True

    def __len__(self) -> int:
        return len(self.write())

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        pass
