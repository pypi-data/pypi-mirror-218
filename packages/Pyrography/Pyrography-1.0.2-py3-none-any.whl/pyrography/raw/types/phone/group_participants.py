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


class GroupParticipants(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.phone.GroupParticipants`.

    Details:
        - Layer: ``158``
        - ID: ``F47751B6``

    Parameters:
        count (``int`` ``32-bit``):
            N/A

        participants (List of :obj:`GroupCallParticipant <pyrography.raw.base.GroupCallParticipant>`):
            N/A

        next_offset (``str``):
            N/A

        chats (List of :obj:`Chat <pyrography.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <pyrography.raw.base.User>`):
            N/A

        version (``int`` ``32-bit``):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrography.raw.functions

        .. autosummary::
            :nosignatures:

            phone.GetGroupParticipants
    """

    __slots__: List[str] = ["count", "participants", "next_offset", "chats", "users", "version"]

    ID = 0xf47751b6
    QUALNAME = "types.phone.GroupParticipants"

    def __init__(self, *, count: int, participants: List["raw.base.GroupCallParticipant"], next_offset: str, chats: List["raw.base.Chat"], users: List["raw.base.User"], version: int) -> None:
        self.count = count  # int
        self.participants = participants  # Vector<GroupCallParticipant>
        self.next_offset = next_offset  # string
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.version = version  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GroupParticipants":
        # No flags
        
        count = Int.read(b)
        
        participants = TLObject.read(b)
        
        next_offset = String.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        version = Int.read(b)
        
        return GroupParticipants(count=count, participants=participants, next_offset=next_offset, chats=chats, users=users, version=version)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        b.write(Vector(self.participants))
        
        b.write(String(self.next_offset))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        b.write(Int(self.version))
        
        return b.getvalue()
