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

import aeidon
import gaupol

from gi.repository import Gtk


class TestHelpAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()

    def test__on_browse_wiki_documentation_activate(self):
        self.application.get_action("browse_wiki_documentation").activate()

    def test__on_report_a_bug_activate(self):
        self.application.get_action("report_a_bug").activate()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__on_view_about_dialog_activate(self):
        respond = lambda *args: Gtk.ResponseType.DELETE_EVENT
        gaupol.util.flash_dialog = respond
        self.application.get_action("view_about_dialog").activate()
