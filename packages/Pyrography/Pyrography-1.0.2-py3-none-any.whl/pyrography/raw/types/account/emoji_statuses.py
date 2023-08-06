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


class EmojiStatuses(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.account.EmojiStatuses`.

    Details:
        - Layer: ``158``
        - ID: ``90C467D1``

    Parameters:
        hash (``int`` ``64-bit``):
            N/A

        statuses (List of :obj:`EmojiStatus <pyrography.raw.base.EmojiStatus>`):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: pyrography.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetDefaultEmojiStatuses
            account.GetRecentEmojiStatuses
    """

    __slots__: List[str] = ["hash", "statuses"]

    ID = 0x90c467d1
    QUALNAME = "types.account.EmojiStatuses"

    def __init__(self, *, hash: int, statuses: List["raw.base.EmojiStatus"]) -> None:
        self.hash = hash  # long
        self.statuses = statuses  # Vector<EmojiStatus>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EmojiStatuses":
        # No flags
        
        hash = Long.read(b)
        
        statuses = TLObject.read(b)
        
        return EmojiStatuses(hash=hash, statuses=statuses)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.hash))
        
        b.write(Vector(self.statuses))
        
        return b.getvalue()
