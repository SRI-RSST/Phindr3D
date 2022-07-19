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

try:
    from .VoxelBaseClass import *
    from .PixelImage import *
    from .SuperVoxelImage import *
    from .MegaVoxelImage import *
    from .VoxelGroupsFunctions import *
except ImportError:
    from VoxelBaseClass import *
    from PixelImage import *
    from SuperVoxelImage import *
    from MegaVoxelImage import *
    from VoxelGroupsFunctions import *

try:
    from ..PhindConfig.PhindConfig import *
    from ..Data.Metadata import *
except ImportError:
    from src.PhindConfig.PhindConfig import *
    from src.Data.Metadata import *

class VoxelGroups:
    """From pixels to supervoxels to megavoxels"""

    def __init__(self):
        """Constructor"""
        # PhindConfig is a static class. Reference members with PhindConfig.member
        #initial_params = PhindConfig()
        self.tilex = None
        self.tiley = None
        self.tilez = None
        self.megaVoxelTileX = None
        self.megaVoxelTileY = None
        self.megaVoxelTileZ = None
        self.numSuperVoxelZ = None
        self.numMegaVoxelsXY = None
        self.numMegaVoxels = None
        self.pixelBinCenters = None
        self.pixelBinCenterDifferences = None
        self.superVoxelBinCenters = None
        self.xOffsetStart = None
        self.xOffsetEnd = None
        self.yOffsetStart = None
        self.yOffsetEnd = None
        self.zOffsetStart = None
        self.zOffsetEnd = None
        self.croppedX = None
        self.croppedY = None
        self.croppedZ = None
        self.origX = None
        self.origY = None
        self.origZ = None
        self.superVoxelXOffsetStart = None
        self.superVoxelXOffsetEnd = None
        self.superVoxelXAddStart = None
        self.superVoxelXAddEnd = None
        self.superVoxelYAddStart = None
        self.superVoxelYAddEnd = None
        self.superVoxelZAddStart = None
        self.superVoxelZAddEnd = None
        self.superVoxelYOffsetStart = None
        self.superVoxelYOffsetEnd = None
        self.superVoxelZOffsetStart = None
        self.superVoxelZOffsetEnd = None
        self.numSuperVoxels = None
        self.numSuperVoxelsXY = None

    # end constructor

    def action(self, theMetadata):
        """Method run from MainGUI when the Phind button is pressed"""
        print("Running the VoxelGroups action method")
        # Redirect to a method with a descriptive name
        self.getBinCentersAndGroupVoxels(theMetadata)
    # end action

    def getBinCentersAndGroupVoxels(self, theMetadata):
        """Main action to be performed on the images after metadata loading, scaling, and thresholding."""

        # getPixelBinCenters
        # output of getPixelBinCenters is a 3D numpy array
        # this is param.pixelBinCenters in Jupyter notebooks/MATLAB versions
        # The PixelImage object holds the numpy array

        # temporary:
        thePixelArray = np.zeros((30000,3))





    # end getBinCentersAndGroupVoxels



# end class VoxelGroups




if __name__ == '__main__':
    """Unit testing"""

    pass





# end main