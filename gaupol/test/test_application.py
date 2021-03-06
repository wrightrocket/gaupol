# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

import gaupol

from gi.repository import Gtk


class TestApplication(gaupol.TestCase):

    def run__application(self):
        Gtk.main()

    def setup_method(self, method):
        self.application = self.new_application()

    def test___init__(self):
        conf = gaupol.conf.application_window
        conf.toolbar_style = gaupol.toolbar_styles.ICONS
        conf.maximized = True
        self.application = gaupol.Application()
