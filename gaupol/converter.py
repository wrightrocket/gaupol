# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.


"""Subtitle text tag converter."""


import gaupol

__all__ = ["TagConverter"]


class TagConverter(object):

    """Subtitle text tag converter.

    Instance variables:
     * _from: TagLibrary instance for the 'from' format
     * _to: TagLibrary instance for the 'to' format
    """

    def __init__(self, from_format, to_format):
        """Initialize a TagConverter instance.

        from_format and to_format should be FORMAT constants.
        """
        self._from = gaupol.tags.get_class(from_format)()
        self._to = gaupol.tags.get_class(to_format)()

    def convert(self, text):
        """Return text with tags converted."""

        return self._to.encode(self._from.decode(text))