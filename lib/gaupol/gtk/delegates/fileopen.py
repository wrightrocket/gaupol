# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Opening and creating new projects."""


try:
    from psyco.classes import *
except ImportError:
    pass

import os
import urllib
import urlparse

import gtk

from gaupol.base.error              import FileFormatError
from gaupol.base.util               import encodinglib, listlib
from gaupol.constants               import Document
from gaupol.gtk.colconstants        import *
from gaupol.gtk.delegates           import Delegate, UIMAction
from gaupol.gtk.dialogs.filechooser import OpenFileDialog
from gaupol.gtk.dialogs.message     import ErrorDialog, WarningDialog
from gaupol.gtk.error               import Cancelled
from gaupol.gtk.page                import Page
from gaupol.gtk.util                import config, gtklib


class NewProjectAction(UIMAction):

    """Creating a new project."""

    uim_action_item = (
        'new_project',
        gtk.STOCK_NEW,
        _('_New'),
        '<control>N',
        _('Create a new project'),
        'on_new_project_activated'
    )

    uim_paths = ['/ui/menubar/file/new']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return True


class OpenMainFileAction(UIMAction):

    """Opening main files."""

    uim_action_item = (
        'open_main_file',
        gtk.STOCK_OPEN,
        _('_Open...'),
        '<control>O',
        _('Open main files'),
        'on_open_main_file_activated'
    )

    uim_paths = ['/ui/menubar/file/open']
    widgets   = ['open_button']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return True


class OpenTranslationFileAction(UIMAction):

    """Opening translation files."""

    uim_action_item = (
        'open_translation_file',
        gtk.STOCK_OPEN,
        _('O_pen Translation...'),
        '',
        _('Open a translation file'),
        'on_open_translation_file_activated'
    )

    uim_paths = ['/ui/menubar/file/open_translation']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False
        elif page.project.main_file is None:
            return False
        else:
            return True


class SelectVideoAction(UIMAction):

    """Selecting a video file."""

    uim_action_item = (
        'select_video_file',
        None,
        _('Se_lect Video...'),
        None,
        _('Select a video file'),
        'on_select_video_file_activated'
    )

    uim_paths = ['/ui/menubar/file/select_video']
    widgets   = ['video_file_button']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        return not page is None


class FileFormatErrorDialog(ErrorDialog):

    """Dialog to inform that filetype is not supported."""

    def __init__(self, parent, basename):

        title   = _('Failed to recognize format of file "%s"') % basename
        message = _('Please check that the file you are trying to open is a '
                    'subtitle file of a format supported by Gaupol.')

        ErrorDialog.__init__(self, parent, title, message)


class OpenBigFileWarningDialog(WarningDialog):

    """Dialog to warn when opening a file over 1 MB."""

    def __init__(self, parent, basename, size):

        title   = _('Open abnormally large file "%s"?') % basename
        message = _('Size of the file is %.1f MB, which is abnormally large '
                    'for a text-based subtitle file. Please, check that you '
                    'are not trying to open a binary file.') % size

        WarningDialog.__init__(self, parent, title, message)

        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NO )
        self.add_button(gtk.STOCK_OPEN  , gtk.RESPONSE_YES)
        self.set_default_response(gtk.RESPONSE_NO)


class OpenFileErrorDialog(ErrorDialog):

    """Dialog to inform that IOError occured while opening file."""

    def __init__(self, parent, basename, message):

        title   = _('Failed to open file "%s"') % basename
        message = _('Attempt to read file returned error: %s.') % message

        ErrorDialog.__init__(self, parent, title, message)


class OpenTranslationWarningDialog(WarningDialog):

    """Dialog to warn when opening a translation file."""

    def __init__(self, parent, basename):

        title   = _('Save changes to translation document "%s" before opening '
                    'a new one?') % basename
        message = _('If you don\'t save, changes will be permanently lost.')

        WarningDialog.__init__(self, parent, title, message)

        self.add_button(_('Open _Without Saving'), gtk.RESPONSE_NO    )
        self.add_button(gtk.STOCK_CANCEL         , gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_SAVE           , gtk.RESPONSE_YES   )
        self.set_default_response(gtk.RESPONSE_YES)


class UnicodeDecodeErrorDialog(ErrorDialog):

    """Dialog to inform that UnicodeError occured while opening file."""

    def __init__(self, parent, basename):

        title   = _('Failed to decode file "%s" with all attempted codecs') \
                  % basename
        message = _('Please try to open the file with a different character '
                    'encoding.')

        ErrorDialog.__init__(self, parent, title, message)


class FileOpenDelegate(Delegate):

    """Opening and creating new projects."""

    def _add_new_project(self, page):
        """Add a new project and a page for it."""

        self.pages.append(page)
        self._connect_page_signals(page)
        self.connect_view_signals(page)

        try:
            self.add_to_recent_files(page.project.main_file.path)
        except AttributeError:
            pass

        # Put the view in a scrolled window.
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.add(page.view)

        # Put the scrolled window in the notebook.
        tab_widget = page.init_tab_widget()
        label = page.tab_menu_label
        self.notebook.append_page_menu(scrolled_window, tab_widget, label)
        self.notebook.show_all()
        self.notebook.set_current_page(self.pages.index(page))

        page.reload_all()

    def add_to_recent_files(self, path):
        """Add path to list of recent files."""

        recent_files = config.file.recent_files

        try:
            recent_files.remove(path)
        except ValueError:
            pass

        recent_files.insert(0, path)

        while len(recent_files) > config.file.maximum_recent_files:
            recent_files.pop()

    def _check_file_open(self, path):
        """
        Check if file is already open.

        If the file is already open, select that page in the notebook.
        Return True if file is open, otherwise False.
        """
        for i in range(len(self.pages)):

            project = self.pages[i].project
            for sub_file in (project.main_file, project.tran_file):

                if sub_file is None or sub_file.path != path:
                    continue

                self.notebook.set_current_page(i)

                basename = os.path.basename(path)
                message = _('File "%s" is already open') % basename
                self.set_status_message(message)

                return True

        return False

    def _connect_page_signals(self, page):
        """Connect GObject signals emitted by page view."""

        # Project
        page.project.connect('action_done'  , self.on_project_action_done  )
        page.project.connect('action_redone', self.on_project_action_redone)
        page.project.connect('action_undone', self.on_project_action_undone)

        # Page
        page.connect('close-button-clicked', self.on_close_button_clicked)

    def connect_view_signals(self, page):
        """Connect GObject signals emitted by view."""

        view = page.view

        # View
        view.connect_after('move-cursor', self.on_view_move_cursor_event)
        view.connect('button-press-event', self.on_view_button_press_event)

        # Selection
        selection = view.get_selection()
        selection.connect('changed', self.on_view_selection_changed_event)

        # Cell renderers and column header widgets
        signals = (
            'editing-started',
            'editing-canceled',
            'edited'
        )
        methods = (
            self.on_view_cell_editing_started,
            self.on_view_cell_editing_canceled,
            self.on_view_cell_edited
        )
        for col in range(6):

            tree_view_column = view.get_column(col)
            for cell_renderer in tree_view_column.get_cell_renderers():
                for i in range(len(signals)):
                    cell_renderer.connect(signals[i], methods[i], col)

            widget = tree_view_column.get_widget()
            button = gtklib.get_parent_widget(widget, gtk.Button)
            button.connect('button-press-event', self.on_view_headers_clicked)

    def _get_tryable_encodings(self, first_encoding=None):
        """Get a list of encodings to try."""

        encodings = config.file.fallback_encodings[:]

        # Add locale encoding.
        if config.file.try_locale_encoding:
            try:
                encodings.insert(0, encodinglib.get_locale_encoding()[0])
            except TypeError:
                pass

        # Add desired first-try encoding.
        if first_encoding is not None:
            encodings.insert(0, first_encoding)

        # If encodings list is empty, add UTF-8.
        if not encodings:
            encodings.append('utf_8')

        encodings = listlib.remove_duplicates(encodings)
        return encodings

    def on_new_project_activated(self, *args):
        """Start a new project."""

        gtklib.set_cursor_busy(self.window)
        self.counter += 1
        page = Page(self.counter)

        # Start with a single blank subtitle.
        page.project.times      = [['00:00:00,000'] * 3]
        page.project.frames     = [[0, 0, 0]]
        page.project.main_texts = [u'']
        page.project.tran_texts = [u'']

        self._add_new_project(page)
        gtklib.set_cursor_normal(self.window)
        self.set_status_message(_('Created a new project'))

    def on_notebook_drag_data_received(self, notebook, context, x, y,
                                       selection_data, info, time):
        """Open drag-dropped files."""

        uris  = selection_data.get_uris()
        paths = []

        # Get paths from uris.
        for uri in uris:
            unquoted_uri = urllib.unquote(uri)
            path = urlparse.urlsplit(unquoted_uri)[2]
            if os.path.isfile(path):
                paths.append(path)

        self.open_main_files(paths)

    def on_open_main_file_activated(self, *args):
        """Open a main file."""

        gtklib.set_cursor_busy(self.window)

        try:
            paths, encoding = self._select_files(Document.MAIN)
        except Cancelled:
            gtklib.set_cursor_normal(self.window)
            return

        self.open_main_files(paths, encoding)
        gtklib.set_cursor_normal(self.window)

    def on_open_recent_file_activated(self, action):
        """Open a recent main file."""

        index = int(action.get_name().split('_')[-1])
        path = config.file.recent_files[index]
        self.open_main_files([path])

    def on_open_translation_file_activated(self, *args):
        """Open a translation file."""

        page = self.get_current_page()

        # Warn if current translation is unsaved.
        if page.project.tran_active and page.project.tran_changed:

            basename = page.get_translation_basename()
            dialog = OpenTranslationWarningDialog(self.window, basename)
            response = dialog.run()
            dialog.destroy()

            if response == gtk.RESPONSE_YES:
                self.save_translation_document(page)
                self.set_sensitivities()
            elif response != gtk.RESPONSE_NO:
                return

        gtklib.set_cursor_busy(self.window)

        try:
            paths, encoding = self._select_files(Document.TRAN)
        except Cancelled:
            gtklib.set_cursor_normal(self.window)
            return

        encodings = self._get_tryable_encodings(encoding)
        page = self._open_file(self.window, Document.TRAN, paths[0], encodings)

        if page is None:
            gtklib.set_cursor_normal(self.window)
            return

        # Show the translation column.
        if not page.view.get_column(TTXT).get_visible():
            path = '/ui/menubar/view/columns/%s' % Column.id_names[TTXT]
            self.uim.get_action(path).activate()

        self.set_sensitivities()
        page.reload_all()

        basename = page.get_translation_basename()
        message = _('Opened translation file "%s"') % basename
        self.set_status_message(message)

        gtklib.set_cursor_normal(self.window)

    def on_select_video_file_activated(self, *args):
        """Select video file."""

        self.video_file_dialog.run()

    def on_video_file_button_drag_data_received(self, notebook, context, x, y,
                                                selection_data, info, time):
        """Set video  file."""

        page = self.get_current_page()

        uri = selection_data.get_uris()[0]
        unquoted_uri = urllib.unquote(uri)
        path = urlparse.urlsplit(unquoted_uri)[2]
        if os.path.isfile(path):
            page.project.video_path = path
            self.set_sensitivities(page)

    def open_main_files(self, paths, encoding=None):
        """Open main files."""

        gtklib.set_cursor_busy(self.window)
        paths.sort()
        encodings = self._get_tryable_encodings(encoding)

        for path in paths:

            page = self._open_file(self.window, Document.MAIN, path, encodings)
            if page is None:
                continue

            # Guess video file path.
            extensions = config.preview.extensions
            video_path = page.project.guess_video_file_path(extensions)

            self._add_new_project(page)

            basename = page.get_main_basename()
            message = _('Opened main file "%s"') % basename
            self.set_status_message(message)

            # Show the new notebook page right away.
            while gtk.events_pending():
                gtk.main_iteration()

        gtklib.set_cursor_normal(self.window)

    def _open_file(self, parent, document_type, path, encodings):
        """
        Open file.

        Return Page or None if unsuccessful.
        """
        # Make sure file is not already open.
        if self._check_file_open(path):
            return None

        basename = os.path.basename(path)
        size_bytes = os.stat(path)[6]
        size_megabytes = float(size_bytes) / 1048576.0

        # Show a warning dialog if filesize is over 1 MB.
        if size_megabytes > 1:
            dialog = OpenBigFileWarningDialog(parent, basename, size_megabytes)
            gtklib.set_cursor_normal(self.window)
            response = dialog.run()
            dialog.destroy()
            if response != gtk.RESPONSE_YES:
                return None

        for encoding in encodings:

            try:
                if document_type == Document.MAIN:
                    page = Page()
                    page.project.open_main_file(path, encoding)
                elif document_type == Document.TRAN:
                    page = self.get_current_page()
                    page.project.open_translation_file(path, encoding)
                return page

            except UnicodeError:
                continue

            except IOError, (no, message):
                dialog = OpenFileErrorDialog(parent, basename, message)
                gtklib.set_cursor_normal(self.window)
                response = dialog.run()
                dialog.destroy()
                gtklib.set_cursor_busy(self.window)
                return None

            except FileFormatError:
                dialog = FileFormatErrorDialog(parent, basename)
                gtklib.set_cursor_normal(self.window)
                response = dialog.run()
                dialog.destroy()
                gtklib.set_cursor_busy(self.window)
                return None

        dialog = UnicodeDecodeErrorDialog(parent, basename)
        gtklib.set_cursor_normal(self.window)
        response = dialog.run()
        dialog.destroy()
        gtklib.set_cursor_busy(self.window)
        return None

    def _select_files(self, document_type):
        """
        Select files with a filechooser.

        Raise Cancelled if cancelled.
        Return paths, encoding.
        """
        if document_type == Document.MAIN:
            title = _('Open')
        elif document_type == Document.TRAN:
            title = _('Open Translation')

        chooser = OpenFileDialog(title, self.window)
        chooser.set_select_multiple(document_type == Document.MAIN)
        gtklib.set_cursor_normal(self.window)
        response = chooser.run()
        gtklib.set_cursor_busy(self.window)

        if response != gtk.RESPONSE_OK:
            gtklib.destroy_gobject(chooser)
            gtklib.set_cursor_normal(self.window)
            raise Cancelled

        filepaths = chooser.get_filenames()
        dirpath   = chooser.get_current_folder()
        encoding  = chooser.get_encoding()

        config.file.encoding = encoding
        config.file.directory = dirpath

        gtklib.destroy_gobject(chooser)
        return filepaths, encoding