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

import tifffile as tf
import numpy as np

class SegmentationFunctions:
    """Static methods for segmentation. Referenced from
    https://github.com/DWALab/Phindr3D/tree/9b95aebbd2a62c41d3c87a36f1122a78a21019c8/Lib
    and
    https://github.com/SRI-RSST/Phindr3D-python/blob/ba588bc925ef72c72103738d17ea922d20771064/phindr_functions.py
    No constructor. All parameters and methods are static.
    """

    @staticmethod
    def getsomefiles():
        pass

    @staticmethod
    def imfinfo(filename):
        class info:
            pass
        info = info()
        tif = tf.TiffFile(filename)
        file = tif.pages[0]
        immetadata = {}
        for tag in file.tags.values():
            immetadata[tag.name] = tag.value
        info.Height = immetadata['ImageLength']
        info.Width = immetadata['ImageWidth']
        info.Format = 'tif'
        return info 
    
    @staticmethod
    def getImageThreshold(IM):
        maxBins = 256
        freq, binEdges = np.histogram(IM.flatten(), bins=maxBins)
        binCenters = binEdges[:-1] + np.diff(binEdges)/2
        meanIntensity = np.mean(IM.flatten())
        numThresholdParam = len(freq)
        binCenters -= meanIntensity
        den1 = np.sqrt((binCenters**2) @ freq.T)
        numAllPixels = np.sum(freq) #freq should hopefully be a 1D vector so summ of all elements should be right.
        covarMat = np.zeros(numThresholdParam)
        for iThreshold in range(numThresholdParam):
            numThreshPixels = np.sum(freq[binCenters > binCenters[iThreshold]])
            den2 = np.sqrt( (((numAllPixels - numThreshPixels)*(numThreshPixels))/numAllPixels) )
            if den2 == 0:
                covarMat[iThreshold] = 0 #dont want to select these, also want to avoid nans
            else:
                covarMat[iThreshold] = (binCenters @ (freq * (binCenters > binCenters[iThreshold])).T) / (den1*den2) #i hope this is the right mix of matrix multiplication and element-wise stuff.
        imThreshold = np.argmax(covarMat) #index makes sense here.
        imThreshold = binCenters[imThreshold] + meanIntensity
        return imThreshold



# end SegmentationFunctions


