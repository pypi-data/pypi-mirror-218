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


class GetAdminLog(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``33DDF480``

    Parameters:
        channel (:obj:`InputChannel <pyrography.raw.base.InputChannel>`):
            N/A

        q (``str``):
            N/A

        max_id (``int`` ``64-bit``):
            N/A

        min_id (``int`` ``64-bit``):
            N/A

        limit (``int`` ``32-bit``):
            N/A

        events_filter (:obj:`ChannelAdminLogEventsFilter <pyrography.raw.base.ChannelAdminLogEventsFilter>`, *optional*):
            N/A

        admins (List of :obj:`InputUser <pyrography.raw.base.InputUser>`, *optional*):
            N/A

    Returns:
        :obj:`channels.AdminLogResults <pyrography.raw.base.channels.AdminLogResults>`
    """

    __slots__: List[str] = ["channel", "q", "max_id", "min_id", "limit", "events_filter", "admins"]

    ID = 0x33ddf480
    QUALNAME = "functions.channels.GetAdminLog"

    def __init__(self, *, channel: "raw.base.InputChannel", q: str, max_id: int, min_id: int, limit: int, events_filter: "raw.base.ChannelAdminLogEventsFilter" = None, admins: Optional[List["raw.base.InputUser"]] = None) -> None:
        self.channel = channel  # InputChannel
        self.q = q  # string
        self.max_id = max_id  # long
        self.min_id = min_id  # long
        self.limit = limit  # int
        self.events_filter = events_filter  # flags.0?ChannelAdminLogEventsFilter
        self.admins = admins  # flags.1?Vector<InputUser>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetAdminLog":
        
        flags = Int.read(b)
        
        channel = TLObject.read(b)
        
        q = String.read(b)
        
        events_filter = TLObject.read(b) if flags & (1 << 0) else None
        
        admins = TLObject.read(b) if flags & (1 << 1) else []
        
        max_id = Long.read(b)
        
        min_id = Long.read(b)
        
        limit = Int.read(b)
        
        return GetAdminLog(channel=channel, q=q, max_id=max_id, min_id=min_id, limit=limit, events_filter=events_filter, admins=admins)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.events_filter is not None else 0
        flags |= (1 << 1) if self.admins else 0
        b.write(Int(flags))
        
        b.write(self.channel.write())
        
        b.write(String(self.q))
        
        if self.events_filter is not None:
            b.write(self.events_filter.write())
        
        if self.admins is not None:
            b.write(Vector(self.admins))
        
        b.write(Long(self.max_id))
        
        b.write(Long(self.min_id))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
