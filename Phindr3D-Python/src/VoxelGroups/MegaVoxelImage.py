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
    from .VoxelBase import VoxelBase
except ImportError:
    from VoxelBase import VoxelBase

class MegaVoxelImage(VoxelBase):
    def __init__(self):
        super().__init__()
        self.megaVoxelBinCenters = None # np array

    def getMegaVoxelBinCenters(self, x, metadata):
        # Same as getSuperVoxelBinCenters, but mega
        # required: randFieldID, metadata, supervoxels, image params (tileinfo)
        megaVoxelsforTraining = []

        # megaVoxelBinCenters is an np array that represents the megavoxels
        self.megaVoxelBinCenters = self.getPixelBins(megaVoxelsforTraining)


# end class MegaVoxelImage