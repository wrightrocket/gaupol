# -*- coding: utf-8 -*-

# Copyright (C) 2013 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Enumerations for orientation types."""

import aeidon

from gi.repository import Gtk

__all__ = ("orientation",)


class Horizontal(aeidon.EnumerationItem):

    value = Gtk.Orientation.HORIZONTAL


class Vertical(aeidon.EnumerationItem):

    value = Gtk.Orientation.VERTICAL


orientation = aeidon.Enumeration()
orientation.HORIZONTAL = Horizontal()
orientation.VERTICAL = Vertical()
