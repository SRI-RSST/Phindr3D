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

from pandas import *
from ImageStack import *

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
        self.images = {}


    # end constructor


    # Teo uses a function get_files
    # files, imageIDs, treatmentids, idstreatment
    #    = phi.get_files(training_folder_path, ID_pos=ID_pos, ID_mark=ID_mark,
    #        treat_mark=treat_mark, treat_endmark=treat_endmark, ID_markextra=ID_markextra,
    #            slice_mark=slice_mark, chan_mark=chan_mark)
    # Then he stores the list of files, allImageID, treatmentIDs, idstreatment
    # tmpslices = list(files[imageIDs[0]].keys())
    # param.numChannels = len(files[imageIDs[0]][tmpslices[0]])

    # This class should also include
    # rescale intensities
    # threshold images

    # class attributes
    # output metadata file name



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

    def loadMetadataFile(self):
        filepath = self.metadataFilename
        metadata = read_table('C:/Users/fyi/Desktop/metaout_metadatafile.txt', usecols=lambda c: not c.startswith('Unnamed:'), delimiter='\t')
        numrows = metadata.shape[0]
        rows = []
        # takes input metadata and stores in a list of tuples of each row
        for i in range(numrows):
            c1 = metadata.at[i, 'Channel_1']
            c2 = metadata.at[i, 'Channel_2']
            c3 = metadata.at[i, 'Channel_3']
            well = metadata.at[i, 'Well']
            field = metadata.at[i, 'Field']
            stack = metadata.at[i, 'Stack']
            metadatafile = metadata.at[i, 'MetadataFile']
            imageid = metadata.at[i,'ImageID']
            row = (c1, c2, c3, well, field, stack, metadatafile, imageid)
            rows.append(row)

        # puts each row into a dictionary, sorted by image ids
        dict = {}
        for row in rows:
            if row[7] in dict:
                dict[row[7]].append(row)
            else:
                dict[row[7]] = []
                dict[row[7]].append(row)

        # create list of stacks
        stacks = {}
        for image in dict:
            stack = ImageStack()
            stack.setStackNumber(image)
            stack.addLayers(dict[image])
            stacks[image] = stack
        self.images = stacks


    # end metadataFileExists


# end class Metadata


# Things I know:
# In matlab version, can enter a regular expression and get back a metadata set
# Set training folder path, analysis folder path, output file name
# file name key? Regex simplification?
#


if __name__ == '__main__':
    """Tests of the Metadata class that can be run directly."""

    pass


test = Metadata()
test.loadMetadataFile()
print(test.images[4.0].layers[11].channels[2].channelpath)


# end main