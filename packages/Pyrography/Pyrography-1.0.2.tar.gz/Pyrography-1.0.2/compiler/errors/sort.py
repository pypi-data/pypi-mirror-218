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

import csv
from pathlib import Path

for p in Path("source").glob("*.tsv"):
    with open(p) as f:
        reader = csv.reader(f, delimiter="\t")
        dct = {k: v for k, v in reader if k != "id"}
        keys = sorted(dct)

    with open(p, "w") as f:
        f.write("id\tmessage\n")

        for i, item in enumerate(keys, start=1):
            f.write(f"{item}\t{dct[item]}")

            if i != len(keys):
                f.write("\n")
