#  Pyrography - A wonderful Pyrogram fork inspired by Pyromod & AmanoTeam/Pyrogram.
#  Copyright (C) 2023-present Lelzin λ <https://github.com/d3cryptofc>
#
#  Forked from Pyrogram <https://github.com/pyrogram/pyrogram>,
#  originally copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrography.
#
#  Pyrography is is free software: you can redistribute it and/or modify it under
#  the terms of the GNU Lesser General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Pyrography is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
#  for more details.
#
#  You should have received a copy of the GNU Lesser General Public License along
#  with Pyrography. If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrography.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrography.raw.core import TLObject
from pyrography import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class TmpPassword(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.account.TmpPassword`.

    Details:
        - Layer: ``158``
        - ID: ``DB64FD34``

    Parameters:
        tmp_password (``bytes``):
            N/A

        valid_until (``int`` ``32-bit``):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrography.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetTmpPassword
    """

    __slots__: List[str] = ["tmp_password", "valid_until"]

    ID = 0xdb64fd34
    QUALNAME = "types.account.TmpPassword"

    def __init__(self, *, tmp_password: bytes, valid_until: int) -> None:
        self.tmp_password = tmp_password  # bytes
        self.valid_until = valid_until  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TmpPassword":
        # No flags
        
        tmp_password = Bytes.read(b)
        
        valid_until = Int.read(b)
        
        return TmpPassword(tmp_password=tmp_password, valid_until=valid_until)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.tmp_password))
        
        b.write(Int(self.valid_until))
        
        return b.getvalue()
