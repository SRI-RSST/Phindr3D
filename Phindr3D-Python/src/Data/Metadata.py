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

#libraries used by createMetadata
import os
import re
import pandas as pd
import numpy as np

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
    
    # 
    def createMetadata(folder_path, regex, mdatafilename='metadata_python.txt'):
    """
    This function creates a metadata txt file in the same format as used in the matlab Phindr implementation

    folder_path: path to iamge folder (full or relative)
    regex: regular expression matching image file names. must include named groups for all required image attributes (wellID, field, treatment, channel, stack, etc.)
    Matlab style regex can be adapted by adding P before group names. ex. : "(?P<WellID>\w+)__(?P<Treatment>\w+)__z(?P<Stack>\d+)__ch(?P<Channel>\d)__example.tiff"
    mdatafilename: filename for metadatafile that will be written.

    regex groups MUST INCLUDE Channel and Stack and at least one other image identification group
    regex groups CANNOT include ImageID or _file.
    """
    
    f = os.listdir(folder_path)
    metadatafilename = f'{os.path.abspath(folder_path)}\\{mdatafilename}'
    #read images in folder
    rows = []
    for i, file in enumerate(f):
        m = re.fullmatch(regex, file)
        if m != None:
            d = m.groupdict()
            d['_file'] = os.path.abspath(f'{folder_path}\\{file}')
            rows.append(d)
    #make sure rows is not empty and that Channel and Stack are in the groups.
    if len(rows) == 0:
        print('\nFailed to create metadata. No regex matches found in folder.\n')
        return None
    if ('Channel' not in rows[0].keys()) or ('Stack' not in rows[0].keys()):
        print('\nFailed to create metadata. regex must contain "Channel" and "Stack" groups.')
        return None
    tmpdf = pd.DataFrame(rows)  
    #make new dataframe with desired colummns
    tags = tmpdf.columns
    channels = np.unique(tmpdf['Channel'])
    cols = []
    for chan in channels:
        cols.append(f'Channel_{chan}')
    for tag in tags:
        if tag not in ['Channel', 'Stack', '_file']:
            cols.append(tag)
    cols.append('Stack')
    cols.append('MetadataFile')
    df = pd.DataFrame(columns=cols)
    #add data to the new dataframe
    stacksubset = [tag for tag in tags if tag not in ['Channel', '_file']]
    idsubset = [tag for tag in tags if tag not in ['Channel', '_file', 'Stack']]
    df[stacksubset] = tmpdf.drop_duplicates(subset = stacksubset)[stacksubset]
    df.reset_index(inplace=True, drop=True)
    #add unique image ids based on the "other tags"
    idtmp = tmpdf.drop_duplicates(subset = idsubset)[idsubset].reset_index(drop=True)
    idtmp.reset_index(inplace=True)
    idtmp.rename(columns={'index':'ImageID'}, inplace=True)
    idtmp['ImageID'] = idtmp['ImageID'] + 1
    df = pd.merge(df, idtmp, left_on=idsubset, right_on=idsubset)
    #give metadatafilename
    df['MetadataFile'] = metadatafilename
    # fill in file paths for each channel
    for chan in channels:
        chandf = tmpdf[tmpdf['Channel']==chan].reset_index(drop=True)
        df[f'Channel_{chan}'] = chandf['_file']
    df.to_csv(metadatafilename, sep='\t', index=False)
    print(f'Metadata file created at \n{metadatafilename}')


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


# Things I know:
# In matlab version, can enter a regular expression and get back a metadata set
# Set training folder path, analysis folder path, output file name
# file name key? Regex simplification?
#


if __name__ == '__main__':
    """Tests of the Metadata class that can be run directly."""

    pass





# end main
