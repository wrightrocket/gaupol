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


"""Text formatting actions."""


import gaupol.gtk
import gtk
_ = gaupol.i18n._

from .action import Action, MenuAction


class ShowCaseMenuAction(MenuAction):

    """Show the case format menu."""

    def __init__(self):

        Action.__init__(self, "show_case_menu")
        self.props.label = _("Ca_se")

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        assert gaupol.gtk.util.is_text_column(col)


class ToggleDialogLinesAction(Action):

    """Toggle dialogue lines on the selected texts."""

    def __init__(self):

        Action.__init__(self, "toggle_dialogue_lines")
        self.props.label = _("_Dialogue")
        tooltip = _("Add or remove dialogue lines on the selected texts")
        self.props.tooltip = tooltip
        self.accelerator = "D"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        assert gaupol.gtk.util.is_text_column(col)


class ToggleItalicizationAction(Action):

    """Toggle italicization of the selected texts."""

    def __init__(self):

        Action.__init__(self, "toggle_italicization")
        self.props.label = _("_Italic")
        self.props.stock_id = gtk.STOCK_ITALIC
        self.props.tooltip = _("Italicize or unitalicize the selected texts")
        self.accelerator = "I"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        assert gaupol.gtk.util.is_text_column(col)
        doc = gaupol.gtk.util.text_column_to_document(col)
        taglib = page.project.get_tag_library(doc)
        assert taglib is not None
        assert taglib.italic_tag is not None


class UseLowerCaseAction(Action):

    """Change the selected texts to lower case."""

    def __init__(self):

        Action.__init__(self, "use_lower_case")
        self.props.label = _("_Lower")
        self.props.tooltip = _("Change the selected texts to lower case")

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        assert gaupol.gtk.util.is_text_column(col)


class UseSentenceCaseAction(Action):

    """Change the selected texts to sentence case."""

    def __init__(self):

        Action.__init__(self, "use_sentence_case")
        self.props.label = _("_Sentence")
        self.props.tooltip = _("Change the selected texts to sentence case")

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        assert gaupol.gtk.util.is_text_column(col)


class UseTitleCaseAction(Action):

    """Change the selected texts to title case."""

    def __init__(self):

        Action.__init__(self, "use_title_case")
        self.props.label = _("_Title")
        self.props.tooltip = _("Change the selected texts to title case")

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        assert gaupol.gtk.util.is_text_column(col)


class UseUpperCaseAction(Action):

    def __init__(self):

        Action.__init__(self, "use_upper_case")
        self.props.label = _("_Upper")
        self.props.tooltip = _("Change the selected texts to upper case")

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        assert gaupol.gtk.util.is_text_column(col)