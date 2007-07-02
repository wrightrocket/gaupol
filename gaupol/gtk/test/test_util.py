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


import gaupol.gtk
import gtk.glade

from gaupol.gtk import unittest
from .. import util


class TestModule(unittest.TestCase):

    def test_document_to_text_column(self):

        doc = gaupol.gtk.DOCUMENT.MAIN
        col = util.document_to_text_column(doc)
        assert col == gaupol.gtk.COLUMN.MAIN_TEXT
        doc = gaupol.gtk.DOCUMENT.TRAN
        col = util.document_to_text_column(doc)
        assert col == gaupol.gtk.COLUMN.TRAN_TEXT

    def test_get_font(self):

        assert util.get_font() == ""
        gaupol.gtk.conf.editor.use_custom_font = True
        gaupol.gtk.conf.editor.custom_font = "Serif 12"
        assert util.get_font() == "Serif 12"

    def test_get_glade_xml(self):

        glade_xml = util.get_glade_xml("debug-dialog")
        glade_xml = util.get_glade_xml("debug-dialog", "text_view")

    def test_get_text_view_size(self):

        text_view = gtk.TextView(gtk.TextBuffer())
        width, height = util.get_text_view_size(text_view)

    def test_get_tree_view_size(self):

        tree_view = gtk.TreeView()
        scroller = gtk.ScrolledWindow()
        scroller.add(tree_view)
        width, height = util.get_tree_view_size(tree_view)

    def test_is_position_column(self):

        assert not util.is_position_column(gaupol.gtk.COLUMN.NUMBER)
        assert util.is_position_column(gaupol.gtk.COLUMN.START)
        assert util.is_position_column(gaupol.gtk.COLUMN.END)
        assert util.is_position_column(gaupol.gtk.COLUMN.DURATION)
        assert not util.is_position_column(gaupol.gtk.COLUMN.MAIN_TEXT)
        assert not util.is_position_column(gaupol.gtk.COLUMN.TRAN_TEXT)

    def test_is_text_column(self):

        assert not util.is_text_column(gaupol.gtk.COLUMN.NUMBER)
        assert not util.is_text_column(gaupol.gtk.COLUMN.START)
        assert not util.is_text_column(gaupol.gtk.COLUMN.END)
        assert not util.is_text_column(gaupol.gtk.COLUMN.DURATION)
        assert util.is_text_column(gaupol.gtk.COLUMN.MAIN_TEXT)
        assert util.is_text_column(gaupol.gtk.COLUMN.TRAN_TEXT)

    def test_prepare_text_view(self):

        util.prepare_text_view(gtk.TextView())
        gaupol.gtk.conf.editor.show_lengths_edit = True
        gaupol.gtk.conf.editor.use_custom_font = False
        gaupol.gtk.conf.editor.custom_font = ""

        util.prepare_text_view(gtk.TextView())
        gaupol.gtk.conf.editor.show_lengths_edit = False
        gaupol.gtk.conf.editor.use_custom_font = True
        gaupol.gtk.conf.editor.custom_font = "Serif 12"

    def test_raise_default(self):

        error = gaupol.gtk.Default
        self.raises(error, util.raise_default, True)
        util.raise_default(False)

    def test_resize_dialog(self):

        dialog = gtk.Dialog()
        util.resize_dialog(dialog, 200, 200)
        assert dialog.get_size() == (200, 200)
        util.resize_dialog(dialog, 2000, 2000, 0.3)
        size = dialog.get_size()
        assert size[0] == 0.3 * gtk.gdk.screen_width()
        assert size[1] == 0.3 * gtk.gdk.screen_height()

    def test_resize_message_dialog(self):

        dialog = gtk.Dialog()
        util.resize_message_dialog(dialog, 200, 200)
        assert dialog.get_size() == (200, 200)
        util.resize_message_dialog(dialog, 2000, 2000, 0.3)
        size = dialog.get_size()
        assert size[0] == 0.3 * gtk.gdk.screen_width()
        assert size[1] == 0.3 * gtk.gdk.screen_height()

    def test_separate_combo(self):

        combo_box = gtk.ComboBox()
        combo_box.set_row_separator_func(util.separate_combo)

    def test_set_button(self):

        button = gtk.Button(gtk.STOCK_CLOSE)
        util.set_button(button, "test")
        util.set_button(button, "test", gtk.STOCK_QUIT)
        button = gtk.Button(gtk.STOCK_CLOSE)
        util.set_button(button, "test", gtk.STOCK_QUIT)
        util.set_button(button, "test")

    def test_set_cursor_busy(self):

        window = gtk.Window()
        window.show_all()
        util.set_cursor_normal(window)
        util.set_cursor_busy(window)
        window.destroy()

    def test_set_cursor_normal(self):

        window = gtk.Window()
        window.show_all()
        util.set_cursor_busy(window)
        util.set_cursor_normal(window)
        window.destroy()

    def test_set_label_font(self):

        util.set_label_font(gtk.Label(""), "Serif 12")

    def test_set_widget_font(self):

        util.set_label_font(gtk.Label(""), "Serif 12")

    def test_text_column_to_document(self):

        col = gaupol.gtk.COLUMN.MAIN_TEXT
        doc = util.text_column_to_document(col)
        assert doc == gaupol.gtk.DOCUMENT.MAIN
        col = gaupol.gtk.COLUMN.TRAN_TEXT
        doc = util.text_column_to_document(col)
        assert doc == gaupol.gtk.DOCUMENT.TRAN