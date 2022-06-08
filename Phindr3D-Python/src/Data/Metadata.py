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

# Static functions for data and metadata handling
import DataFunctions

class Metadata:
    """This class handles groups of image files and the associated metadata.
       Individual file objects are handled by the ImageFile class.
       Static methods that draw closely from transliterations of the MATLAB functions
       can be found in the DataFunctions class."""

    def __init__(self):
        """Metadata class constructor"""
        # These are the default values from Teo's code
        # Use them until I understand them
        self.ID_pos = 'start'
        self.ID_mark = None
        self.ID_markextra = None
        self.slice_mark = 'z'
        self.chan_mark = 'ch'
        self.treat_mark = None
        self.treat_endmark = None
        self.training_folder_path = r"FILE_name"
        self.analysis_folder_path = self.training_folder_path
        # The various marks are associated with reading a regex string.
        # This is an operation performed by the MATLAB version


        # Set default values for member variables
        self.metadataFilename = ""


    # end constructor


    def fillMetadataFile(self):
        """Use regular expression and file name to fill the metadata file with
            image file information."""

        # DataFunctions.createMetadata


    # end fillMetadataFile


    def SetMetadataFilename(self, omf):
        """Set method to check the type of the filename string
            and set the member variable. Returns True if successful,
            False on error."""
        if not isinstance(omf, str):
            return False
        # else

    # end SetMetadataFilename

    def GetMetadataFilename(self):
        """Get method to return the metadata filename string."""

    # end GetMetadataFilename


    def metadataFileExists(self, omf):
        """Check whether the filename specified already exists.
            Returns True if the file exists, False if it does not, or if the given
            argument is not a string."""
        if not isinstance(omf, str):
            return False
        # else

    # end metadataFileExists


# end class Metadata



if __name__ == '__main__':
    """Tests of the Metadata class that can be run directly."""

    pass





# end main
