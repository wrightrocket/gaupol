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


"""Subtitle file reading."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.constants import FORMAT, MODE
from gaupol.base.colcons import *
from gaupol.base.delegates.delegate import Delegate
from gaupol.base.files.classes import *
from gaupol.base.files.determiner import FileFormatDeterminer


class FileReader(Delegate):
    
    """Subtitle file reading."""
    
    def read_main_file(self, path=None, encoding=None):
        """
        Read times/frames and texts from main file.
        
        path and encoding can be omitted if main file is already open.
        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise UnknownFileFormatError if unable to detect file format.
        """
        path     = path     or self.main_file.path
        encoding = encoding or self.main_file.encoding
        
        # Get format.
        determiner = FileFormatDeterminer(path, encoding)
        format = determiner.determine_file_format()
        format_name = FORMAT.CLASS_NAMES[format]

        # Read file.
        main_file = eval(format_name)(path, encoding)
        shows, hides, texts = main_file.read()
        shows, hides, texts = self._sort_data(shows, hides, texts)

        # After successful reading, instance variable can be set.
        self.main_file = main_file

        # Blank possible existing data.
        self.times  = []
        self.frames = []
        self.texts  = []

        self_times  = self.times
        self_frames = self.frames
        self_texts  = self.texts

        calc = self.calc

        if self.main_file.MODE == MODE.TIME:
            
            for i in range(len(shows)):

                show_time = shows[i]
                hide_time = hides[i]
                text      = texts[i]
                
                durn_time  = calc.get_time_duration(show_time, hide_time)
                show_frame = calc.time_to_frame(show_time)
                hide_frame = calc.time_to_frame(hide_time)
                durn_frame = calc.get_frame_duration(show_frame, hide_frame)
                            
                self_times.append([show_time, hide_time, durn_time])
                self_frames.append([show_frame, hide_frame, durn_frame])
                self_texts.append([text, u''])

        elif self.main_file.MODE == MODE.FRAME:
            
            for i in range(len(shows)):

                show_frame = shows[i]
                hide_frame = hides[i]
                text       = texts[i]

                durn_frame = calc.get_frame_duration(show_frame, hide_frame)
                show_time  = calc.frame_to_time(show_frame)
                hide_time  = calc.frame_to_time(hide_frame)
                durn_time  = calc.get_time_duration(show_time, hide_time)

                self_times.append([show_time, hide_time, durn_time])
                self_frames.append([show_frame, hide_frame, durn_frame])
                self_both_texts.append([text, u''])

    def read_translation_file(self, path=None, encoding=None):
        """
        Read texts from translation file.
        
        path and encoding can be omitted if translation file is already open.
        Main file should always exist before reading translation file.
        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FileFormatError if unable to detect file format.
        """
        path     = path     or self.tran_file.path
        encoding = encoding or self.tran_file.encoding
        
        # Get format
        determiner = FileFormatDeterminer(path, encoding)
        format = determiner.determine_file_format()
        format_name = FORMAT.CLASS_NAMES[format]

        # Read file.
        tran_file = eval(format_name)(path, encoding)
        shows, hides, trans = tran_file.read()
        shows, hides, trans = self._sort_data(shows, hides, trans)
        
        # After successful reading, instance variable can be set.
        self.tran_file = tran_file

        # Blank possible existing translations.
        for i in range(len(self.texts)):
            self.texts[i][TRAN] = u''

        # If translation file is longer than main file, new subtitles need to
        # be added.
        if len(trans) > len(self.times):
            start_row = len(self.times)
            amount = len(trans) - len(self.times)
            self.insert_subtitles(start_row, amount)

        for i in range(len(trans)):
            self.texts[i][TRAN] = trans[i]

    def _sort_data(self, shows, hides, texts):
        """
        Sort data based on show times/frames.

        Return shows, hides, texts.
        """
        data = [[shows[i], hides[i], texts[i]] for i in range(len(shows))]
        data.sort(lambda x, y: cmp(x[0], y[0]))

        shows = []
        hides = []
        texts = []
        
        for i in range(len(data)):
            shows.append(data[i][0])
            hides.append(data[i][1])
            texts.append(data[i][2])

        return shows, hides, texts