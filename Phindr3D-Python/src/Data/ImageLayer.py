# Copyright (C) 2022 Sunnybrook Research Institute
# This file is part of src <https://github.com/DWALab/Phindr3D>.
#
# src is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# src is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with src.  If not, see <http://www.gnu.org/licenses/>.

from ImageChannel import *

class ImageLayer:
    """This class handles groups of image files and the associated metadata.
       Static methods that draw closely from transliterations of the MATLAB functions
       can be found in the DataFunctions class."""

    def __init__(self):
        """ImageChannel class constructor"""
        self.well = None
        self.field = None
        self.channels = {}
        pass

    def setWell(self, well):
        self.well = well

    def setField(self, field):
        self.field = field

    def addChannels(self, channels): # channels is a tuple/line of metadata
        count = 1
        for index in range(3):
            newChannel = ImageChannel()
            newChannel.setPath(channels[index])
            self.channels[count] = newChannel
            count += 1






# end class ImageChannel



if __name__ == '__main__':
    """Tests of the ImageChannel class that can be run directly."""

    pass


# end main