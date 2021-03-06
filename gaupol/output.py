# -*- coding: utf-8 -*-

# Copyright (C) 2005-2007,2010 Osmo Salomaa
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

"""Window for standard output from external applications."""

import aeidon
import gaupol
_ = aeidon.i18n._

from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("OutputWindow",)


class OutputWindow(Gtk.Window):

    """Window for standard output from external applications."""

    def __init__(self):
        """Initialize an :class:`OutputWindow` object."""
        GObject.GObject.__init__(self)
        self._close_button = None
        self._text_view = None
        self.set_border_width(12)
        self.set_title(_("Output"))
        self._init_widgets()
        self._init_sizes()
        self._init_signal_handlers()
        self._init_keys()

    def _init_keys(self):
        """Initialize keyboard shortcuts."""
        accel_group = Gtk.AccelGroup()
        accel_group.connect(Gdk.KEY_w,
                            Gdk.ModifierType.CONTROL_MASK,
                            Gtk.AccelFlags.MASK,
                            self._on_close_key_pressed)

        self.add_accel_group(accel_group)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""
        aeidon.util.connect(self, "_close_button", "clicked")
        aeidon.util.connect(self, self, "delete-event")
        aeidon.util.connect(self, self, "notify::visible")
        aeidon.util.connect(self, self, "window-state-event")

    def _init_sizes(self):
        """Initialize widget sizes."""
        self.resize(*gaupol.conf.output_window.size)
        self.move(*gaupol.conf.output_window.position)
        if gaupol.conf.output_window.maximized:
            self.maximize()

    def _init_widgets(self):
        """Initialize all contained widgets."""
        self._text_view = Gtk.TextView()
        self._text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self._text_view.set_cursor_visible(False)
        self._text_view.set_editable(False)
        self._text_view.set_left_margin(6)
        self._text_view.set_right_margin(6)
        self._text_view.set_pixels_below_lines(1)
        gaupol.util.set_widget_font(self._text_view, "monospace")
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(*((Gtk.PolicyType.AUTOMATIC,) * 2))
        scroller.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        scroller.add(self._text_view)
        self._close_button = Gtk.Button(stock=Gtk.STOCK_CLOSE)
        button_box = Gtk.HButtonBox()
        button_box.set_layout(Gtk.ButtonBoxStyle.END)
        button_box.pack_start(self._close_button,
                              expand=False,
                              fill=False,
                              padding=0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                       spacing=12)

        vbox.pack_start(scroller,
                        expand=True,
                        fill=True,
                        padding=0)

        vbox.pack_start(button_box,
                        expand=False,
                        fill=False,
                        padding=0)

        vbox.show_all()
        self.add(vbox)

    def _on_close_button_clicked(self, *args):
        """Hide window."""
        self._save_geometry()
        self.hide()

    def _on_close_key_pressed(self, *args):
        """Hide window."""
        self._save_geometry()
        self.hide()

    def _on_delete_event(self, *args):
        """Hide window."""
        self._save_geometry()
        self.hide()
        return True

    def _on_notify_visible(self, *args):
        """Save window visibility."""
        gaupol.conf.output_window.show = self.props.visible

    def _on_window_state_event(self, window, event):
        """Save window maximization."""
        state = event.new_window_state
        maximized = bool(state & Gdk.WindowState.MAXIMIZED)
        gaupol.conf.output_window.maximized = maximized

    def _save_geometry(self):
        """Save window size and position."""
        if gaupol.conf.output_window.maximized: return
        gaupol.conf.output_window.size = list(self.get_size())
        gaupol.conf.output_window.position = list(self.get_position())

    def set_output(self, output):
        """Display `output` in text view."""
        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(output)
        mark = text_buffer.get_insert()
        self._text_view.scroll_to_mark(mark=mark,
                                       within_margin=0,
                                       use_align=False,
                                       xalign=0.5,
                                       yalign=0.5)
