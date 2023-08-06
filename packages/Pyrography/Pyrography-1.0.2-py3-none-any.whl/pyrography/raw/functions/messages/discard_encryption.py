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


class DiscardEncryption(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``F393AEA0``

    Parameters:
        chat_id (``int`` ``32-bit``):
            N/A

        delete_history (``bool``, *optional*):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["chat_id", "delete_history"]

    ID = 0xf393aea0
    QUALNAME = "functions.messages.DiscardEncryption"

    def __init__(self, *, chat_id: int, delete_history: Optional[bool] = None) -> None:
        self.chat_id = chat_id  # int
        self.delete_history = delete_history  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DiscardEncryption":
        
        flags = Int.read(b)
        
        delete_history = True if flags & (1 << 0) else False
        chat_id = Int.read(b)
        
        return DiscardEncryption(chat_id=chat_id, delete_history=delete_history)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.delete_history else 0
        b.write(Int(flags))
        
        b.write(Int(self.chat_id))
        
        return b.getvalue()
