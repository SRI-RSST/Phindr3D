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

import os
import json
import numpy as np
import pandas as pd
import tifffile as tf
from scipy import ndimage
from .SegmentationFunctions import *

class Segmentation:
    """This class ...
       Static methods that draw closely from transliterations of the MATLAB functions
       can be found in the SegmentationFunctions class."""

    def __init__(self):
        """Segmentation class constructor"""
        self.defaultSettings = {
            'min_area_spheroid':200.0,
            'intensity_threshold':1000.0,
            'radius_spheroid':75.0,
            'smoothin_param':0.01,
            'scale_spheroid':1.0,
            'entropy_threshold':1.0,
            'max_img_fraction':0.25,
            'seg_Channel':'allChannels'
            }
        self.settings = self.defaultSettings
        self.metadata = None
        self.outputDir = None
        self.labDir = None
        self.segDir = None
        # end constructor
    
    def saveSettings(self, outputpath):
        with open(outputpath, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=4)

    def loadSettings(self, settingJsonPath):
        with open(settingJsonPath, 'r') as f:
            newsettings = json.load(f)
        self.settings = newsettings
    
    def createSubfolders(self):
        self.labDir = os.path.join(self.outputDir, 'LabelledImages')
        self.segDir = os.path.join(self.outputDir, 'SegmentedImages')
        os.makedirs(self.labDir, exist_ok=True)
        os.makedirs(self.segDir, exist_ok=True)

    def RunSegmentation(self, mdata):
        for id in mdata.images:
            imstack = mdata.images[id]
            if self.settings['seg_Channel'] == 'allChannels':
                IM, focusIndex = getfsimage_multichannel(imstack)
            else:
                IM, focusIndex = getfsimage(imstack, self.settings['seg_channel'])
            L = getSegmentedOverlayImage(IM, self.settings)
            uLabels = np.unique(L)
            uLabels = uLabels[uLabels != 0]
            numObjects = len(uLabels)
            ll = []
            for iObjects in range(numObjects):
                nL = (L == uLabels[iObjects]) #nL is a binary map
                if np.sum(nL) > (L.size * self.settings['max_img_fraction']):
                    L[L == uLabels[iObjects]] = 0
                else:
                    ll.append( getFocusplanesPerObjectMod(nL, focusIndex) )
            ll = np.array(ll)
            numObjects = len(ll)
            if numObjects > 0:
                zVals = list(imstack.stackLayers.keys())
                channels = list(imstack.stackLayers[zVals[0]].channels.keys())
                SEdil = morph.disk(25) # this structuring element can be made larger if needed.
                L = cv.dilate(L, SEdil)
                fstruct = ndimage.find_objects(L.astype(int))
                for iObjects in range(numObjects):
                    for iPlanes in range(int(ll[iObjects, 0]), int(ll[iObjects, 1]+1)):
                        for chan in channels:
                            IM1 = io.imread( imstack.stackLayers[iPlanes].channels[chan].channelpath )
                            IM2 = IM1[fstruct[iObjects]]
                            filenameParts = []
                            for dfcol in filenameData:
                                part = f'{dfcol[0]}{imageData.loc[imageData["Stack"]==zVals[0], dfcol].values[0]}'
                                filenameParts.append(part)
                            filenameParts.append(f'Z{iPlanes}')
                            filenameParts.append(f'CH{kChannels+1}')
                            filenameParts.append(f'ID{id}')
                            filenameParts.append(f'OB{iObjects+1}')
                            obFileName = '__'.join(filenameParts)
                            obFileName = obFileName + '.tiff'
                            tf.imwrite(os.path.join(self.segDir, obFileName), IM2)
                    filenameParts = []
                    for dfcol in filenameData:
                        part = f'{dfcol[0]}{imageData.loc[imageData["Stack"]==zVals[0], dfcol].values[0]}'
                        filenameParts.append(part)
                    filenameParts.append('Z1')
                    filenameParts.append(f'CH{kChannels+1}')
                    filenameParts.append(f'ID{id}')
                    filenameParts.append(f'OB{iObjects+1}')
                    obFileName = '__'.join(filenameParts)
                    obFileName = obFileName + '.tiff'
                    IML = L[fstruct[iObjects]]
                    tf.imwrite(os.path.join(self.labDir, obFileName), IML)
            filenameParts = []
            for dfcol in filenameData:
                part = f'{dfcol[0]}{imageData.loc[imageData["Stack"]==zVals[0], dfcol].values[0]}'
                filenameParts.append(part)
            filenameParts.append(f'ID{id}')
            allobsname = filenameParts.copy()
            focusname = filenameParts.copy()
            allobsname.append(f'All_{numObjects}_Objects')
            obFileName = '__'.join(allobsname) + '.tiff'
            focusname = '__'.join(focusname) + '.tiff'
            IML = L
            tf.imwrite(os.path.join(self.labDir, obFileName), IML)
            tf.imwrite(os.path.join(self.labDir, focusname), IM)



        else:
            pass
            #nothing here yet, need to add channel selection option.




# end class Segmentation



if __name__ == '__main__':
    """Tests of the Segmentation class that can be run directly."""


# end main