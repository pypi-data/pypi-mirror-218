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


class RpcAnswerDropped(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.RpcDropAnswer`.

    Details:
        - Layer: ``158``
        - ID: ``A43AD8B7``

    Parameters:
        msg_id (``int`` ``64-bit``):
            N/A

        seq_no (``int`` ``32-bit``):
            N/A

        bytes (``int`` ``32-bit``):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrography.raw.functions

        .. autosummary::
            :nosignatures:

            RpcDropAnswer
    """

    __slots__: List[str] = ["msg_id", "seq_no", "bytes"]

    ID = 0xa43ad8b7
    QUALNAME = "types.RpcAnswerDropped"

    def __init__(self, *, msg_id: int, seq_no: int, bytes: int) -> None:
        self.msg_id = msg_id  # long
        self.seq_no = seq_no  # int
        self.bytes = bytes  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RpcAnswerDropped":
        # No flags
        
        msg_id = Long.read(b)
        
        seq_no = Int.read(b)
        
        bytes = Int.read(b)
        
        return RpcAnswerDropped(msg_id=msg_id, seq_no=seq_no, bytes=bytes)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.msg_id))
        
        b.write(Int(self.seq_no))
        
        b.write(Int(self.bytes))
        
        return b.getvalue()
