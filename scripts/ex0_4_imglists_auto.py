# -*- coding: utf-8 -*-
#
# Pyplis is a Python library for the analysis of UV SO2 camera data
# Copyright (C) 2017 Jonas Gliß (jonasgliss@gmail.com)
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License a
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
Pyplis introduction script 4 - Automatic creation of image lists

The previous script gave an introduction into the manual creation of ``ImgList``
objects and some basic image preparation features. 
In this script, a number of ImgList objects (on, off, dark low gain, 
dark high gain, offset low gain, offset high gain) is created automatically 
using the Camera class created in example script ex0_2_camera_setup.py (ECII
camera)

Based on the information stored in the Camera class, a MeasSetup class is 
created. The latter class collects all meta information relevant for an 
emission rate analysis. Apart from the camera specs, this may include source
definitions  contains information about the camera specs a the
image base directory (note that in this example, start / stop acq. time stamps
are ignored, i.e. all images available in the specified directory are imported)
"""
from SETTINGS import check_version
# Raises Exception if conflict occurs
check_version()

import pyplis

### IMPORT GLOBAL SETTINGS
from SETTINGS import IMG_DIR

### IMPORTS FROM OTHER EXAMPLE SCRIPTS
from ex0_2_camera_setup import create_ecII_cam_new_filters


if __name__ == "__main__":
    # create the camera which was 
    cam = create_ecII_cam_new_filters()
    
    #now throw all this stuff into the BaseSetup objec
    stp = pyplis.setupclasses.MeasSetup(IMG_DIR, camera = cam)
    
    # Create a Dataset which creates separate ImgLists for all types (dark,
    # offset, etc.)
    ds = pyplis.dataset.Dataset(stp)
    
    # The image lists can be accessed in different ways for instance using
    # the method "all_lists", which returns a Python list containing all 
    # ImgList objects that were created within the Dataset
    all_imglists = ds.all_lists() 
     
    # print some information about each of the lists
    for lst in all_imglists:
        print ("list_id: %s, list_type: %s, number_of_files: %s"
                %(lst.list_id, lst.list_type, lst.nof))
                
    # single lists can be accessed using "get_list(<id>)" using a valid ID,
    # e.g.:
    on_list = ds.get_list("on")
    off_list = ds.get_list("off")
    
    on_list.goto_img(50) #this also changes the index in the off band list ...
    
    # ... because it is linked to the on band list (automatically set in 
    # Dataset)
    print ("\nImgLists linked to ImgList on: %s" %on_list.linked_lists.keys())
    print ("Current file number on / off list: %d / %d\n" %(on_list.cfn,
                                                          off_list.cfn))
                                                    
    # Detected dark and offset image lists are also automatically linked to the
    # on and off band image list, such that dark image correction can be 
    # applied 
    on_list.darkcorr_mode = True
    off_list.darkcorr_mode = True
    
    # the current image preparation settings can be accessed via the 
    # edit_info method
    on_list.edit_info()
    
    
