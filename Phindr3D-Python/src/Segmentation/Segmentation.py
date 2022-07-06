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


from .SegmentationFunctions import *
import os
import json
import numpy as np
import pandas as pd

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
            'max_img_fraction':0.25
            }
        self.settings = self.defaultSettings
        self.metadata = None
        self.outputDir = None
        self.labDir = None
        self.segDir = None
    
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

    # end constructor




# end class Segmentation



if __name__ == '__main__':
    """Tests of the Segmentation class that can be run directly."""


# end main