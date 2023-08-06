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


class UpdateDialogUnreadMark(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.Update`.

    Details:
        - Layer: ``158``
        - ID: ``E16459C3``

    Parameters:
        peer (:obj:`DialogPeer <pyrography.raw.base.DialogPeer>`):
            N/A

        unread (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["peer", "unread"]

    ID = 0xe16459c3
    QUALNAME = "types.UpdateDialogUnreadMark"

    def __init__(self, *, peer: "raw.base.DialogPeer", unread: Optional[bool] = None) -> None:
        self.peer = peer  # DialogPeer
        self.unread = unread  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateDialogUnreadMark":
        
        flags = Int.read(b)
        
        unread = True if flags & (1 << 0) else False
        peer = TLObject.read(b)
        
        return UpdateDialogUnreadMark(peer=peer, unread=unread)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.unread else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        return b.getvalue()
