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


"""Warning dialog displayed when trying to close multiple documents."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk

from gaupol.constants import TYPE
from gaupol.gui.util import gui


SAVE, PROJ = 0, 1


class MultiCloseWarningDialog(object):
    
    """
    Warning dialog displayed when trying to close multiple documents.

    Will be displayed when quitting or closing a tab with at least two
    documents open with unsaved changes.
    """
    
    def __init__(self, parent, projects):
        """
        Initialize a MultiCloseWarningDialog object.
        
        All projects or only a subset list can be given. Changed-ness will
        be checked in this class.
        """
        self._projects   = projects

        glade_xml = gui.get_glade_xml('multiclose-dialog.glade')
        get_widget = glade_xml.get_widget

        # Widgets
        self._dialog         = get_widget('dialog')
        self._main_tree_view = get_widget('main_tree_view')
        self._tran_tree_view = get_widget('translation_tree_view')

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_YES)

        self._build_main_tree_view(glade_xml)
        self._build_translation_tree_view(glade_xml)

        self._main_tree_view.grab_focus()
        self._dialog.show()

    def _build_main_tree_view(self, glade_xml):
        """Build the list of main documents."""
        
        tree_view = self._main_tree_view
        label = glade_xml.get_widget('main_label')
        label.set_mnemonic_widget(tree_view)
        tree_view, model = self._build_tree_view(tree_view, TYPE.MAIN)

        # Insert data.
        for project in self._projects:
            if project.main_changed:
                model.append([True, project])

        # Set sensible size for TreeView. 24 pixels are added to account for
        # possible scroll bar.
        width, height = tree_view.size_request()
        width  = min(150, width  + 24)
        height = min(126, height + 24)
        tree_view.set_size_request(width, height)
        
        if len(model) == 0:
            glade_xml.get_widget('main_label').hide()
            glade_xml.get_widget('main_scrolled_window').hide()

    def _build_translation_tree_view(self, glade_xml):
        """Build the list of translation documents."""
        
        tree_view = self._tran_tree_view
        label = glade_xml.get_widget('translation_label')
        label.set_mnemonic_widget(tree_view)
        tree_view, model = self._build_tree_view(tree_view, TYPE.TRAN)

        # Insert data.
        for project in self._projects:
            if project.tran_active and project.tran_changed:
                model.append([True, project])

        # Set sensible size for TreeView. 24 pixels are added to account for
        # possible scroll bar.
        width, height = tree_view.size_request()
        width  = min(150, width  + 24)
        height = min(126, height + 24)
        tree_view.set_size_request(width, height)

        if len(model) == 0:
            glade_xml.get_widget('translation_label').hide()
            glade_xml.get_widget('translation_scrolled_window').hide()

    def _build_tree_view(self, tree_view, file_type):
        """
        Build properties for tree_view.
        
        file_type: TYPE.MAIN or TYPE.TRAN
        Return: TreeView, TreeModel
        """
        # This method adaptively copied from Gazpacho by Lorenzo Gil Sanchez.
        # Gazpacho has a similar dialog made without using Glade.
    
        model = gtk.ListStore(gobject.TYPE_BOOLEAN, object)

        tree_view.set_model(model)
        tree_view.set_headers_visible(False)
        
        # Check-box column
        cell_renderer_0 = gtk.CellRendererToggle()
        cell_renderer_0.set_property('activatable', True)

        method = self._on_tree_view_cell_toggled
        cell_renderer_0.connect('toggled', method, model)

        tree_view_column_0 = gtk.TreeViewColumn('', cell_renderer_0)
        tree_view_column_0.add_attribute(cell_renderer_0, 'active', 0)
        tree_view.append_column(tree_view_column_0)

        # File basename column
        def render_basename(tree_view_column, cell_renderer, model, tree_iter):
            """Render text in file basename column."""

            project = model.get_value(tree_iter, PROJ)

            if file_type == TYPE.MAIN:
                basename = project.get_main_basename()
            elif file_type == TYPE.TRAN:
                basename = project.get_translation_basename()

            cell_renderer.set_property('text', basename)

        cell_renderer_1 = gtk.CellRendererText()
             
        tree_view_column_1 = gtk.TreeViewColumn('', cell_renderer_1)
        tree_view_column_1.set_cell_data_func(cell_renderer_1, render_basename)
        tree_view.append_column(tree_view_column_1)

        return tree_view, model

    def destroy(self):
        """Destroy the dialog."""
        
        self._dialog.destroy()

    def get_main_projects_to_save(self):
        """Get projects, whose main files were chosen to be saved."""
        
        model = self._main_tree_view.get_model()
        projects = []
        
        for i in range(len(model)):
            if model[i][SAVE]:
                projects.append(model[i][PROJ])
                
        return projects

    def get_translation_projects_to_save(self):
        """Get projects, whose translation files were chosen to be saved."""
        
        model = self._tran_tree_view.get_model()
        projects = []
        
        for i in range(len(model)):
            if model[i][SAVE]:
                projects.append(model[i][PROJ])
                
        return projects

    def _on_tree_view_cell_toggled(self, cell_rend, row, model):
        """Toggle the value on the CheckButton column."""

        model[row][SAVE] = not model[row][SAVE]

        mains       = self.get_main_projects_to_save()
        tranlations = self.get_translation_projects_to_save()

        sensitive = bool(mains or tranlations)
        self._dialog.set_response_sensitive(gtk.RESPONSE_YES, sensitive)

    def run(self):
        """Run the dialog."""
        
        return self._dialog.run()