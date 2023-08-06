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


class ChannelMessagesFilter(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.ChannelMessagesFilter`.

    Details:
        - Layer: ``158``
        - ID: ``CD77D957``

    Parameters:
        ranges (List of :obj:`MessageRange <pyrography.raw.base.MessageRange>`):
            N/A

        exclude_new_messages (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["ranges", "exclude_new_messages"]

    ID = 0xcd77d957
    QUALNAME = "types.ChannelMessagesFilter"

    def __init__(self, *, ranges: List["raw.base.MessageRange"], exclude_new_messages: Optional[bool] = None) -> None:
        self.ranges = ranges  # Vector<MessageRange>
        self.exclude_new_messages = exclude_new_messages  # flags.1?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelMessagesFilter":
        
        flags = Int.read(b)
        
        exclude_new_messages = True if flags & (1 << 1) else False
        ranges = TLObject.read(b)
        
        return ChannelMessagesFilter(ranges=ranges, exclude_new_messages=exclude_new_messages)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.exclude_new_messages else 0
        b.write(Int(flags))
        
        b.write(Vector(self.ranges))
        
        return b.getvalue()
