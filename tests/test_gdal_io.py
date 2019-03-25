#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __BEGIN_LICENSE__
#  Copyright (c) 2009-2013, United States Government as represented by the
#  Administrator of the National Aeronautics and Space Administration. All
#  rights reserved.
#
#  The NGT platform is licensed under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance with the
#  License. You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# __END_LICENSE__

"""
Test for GDAL I/O classes.
"""
import sys, os
import string, argparse#, threading, time
#import copy
#import psutil
#import math

# TODO: Clean this up
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../delta')))


from image_reader import *
from image_writer import *

#from osgeo import gdal
#import numpy as np

#from utilities import Rectangle




#------------------------------------------------------------------------------

# TODO: Make unit tests!

def main(argsIn):

    try:

        # Use parser that ignores unknown options
        usage  = "usage: image_reader [options]"
        parser = argparse.ArgumentParser(usage=usage)

        parser.add_argument('input_paths', metavar='N', type=str, nargs='+',
                            help='Input files')

        #parser.add_argument("--input-path", dest="inputPath", default=None,
        #                                      help="Input path")

        parser.add_argument("--output-path", dest="outputPath", default=None,
                                              help="Output path.")


        # This call handles all the parallel_mapproject specific options.
        options = parser.parse_args(argsIn)

        # Check the required positional arguments.

    except argparse.ArgumentError as msg:
        raise Usage(msg)

    #image = TiffReader()
    #image.open_image(options.inputPath)

    #band = 1
    #(nCols, nRows) = image.image_size()
    #(bSize, (numBlocksX, numBlocksY)) = image.get_block_info(band)
    #noData = image.nodata_value()

    #print('nBands = %d, nRows = %d, nCols = %d' % (nBands, nRows, nCols))
    #print('noData = %s, dType = %d, bSize = %d, %d' % (str(noData), dType, bSize[0], bSize[1]))

    
    band = 1
    input_reader = MultiTiffFileReader()
    input_reader.load_images(options.input_paths)
    (nCols, nRows) = input_reader.image_size()
    noData = input_reader.nodata_value()
    (bSize, (numBlocksX, numBlocksY)) = input_reader.get_block_info(band)

    #print('Num blocks = %f, %f' % (numBlocksX, numBlocksY))

    # TODO: Will we be faster using this method? Or ReadAsArray? Or ReadRaster?
    #data = band.ReadBlock(0,0) # Reads in as 'bytes' or raw data
    #print(type(data))
    #print('len(data) = ' + str(len(data)))
    
    #data = band.ReadAsArray(0, 0, bSize[0], bSize[1]) # Reads as numpy array
    ##np.array()
    #print(type(data))
    ##print('len(data) = ' + str(len(data)))
    #print('data.shape = ' + str(data.shape))
    
    # TODO: Need a more flexible test here!
    output_tile_width  = bSize[0]
    output_tile_height = 32

    # Make a list of output ROIs
    numBlocksX = int(nCols / output_tile_width)
    numBlocksY = int(nRows / output_tile_height)

    #stuff = dir(band)
    #for s in stuff:
    #    print(s)

    print('Testing image duplication!')
    writer = TiffWriter()
    writer.init_output_geotiff(options.outputPath, nRows, nCols, noData,
                             tileWidth=output_tile_width, tileHeight=output_tile_height)

    # Setting up output ROIs
    output_rois = []
    for r in range(0,numBlocksY):
        for c in range(0,numBlocksX):
            
            roi = Rectangle(c*output_tile_width, r*output_tile_height,
                            width=output_tile_width, height=output_tile_height)
            output_rois.append(roi)
            #print(roi)
            #print(band)
            #data = image.read_pixels(roi, band)
            #writer.write_geotiff_block(data, c, r)
            
    
    def callback_function(output_roi, read_roi, data_vec):
      
        print('For output roi: ' + str(output_roi) +' got read_roi ' + str(read_roi))
        print(data_vec[0].shape)
        
        col = output_roi.min_x / output_tile_width # Hack for testing!
        row = output_roi.min_y / output_tile_height
        writer.write_geotiff_block(data_vec[0], col, row)
        
            
    print('Writing TIFF blocks...')
    input_reader.process_rois(output_rois, callback_function)



    print('Done sending in blocks!')
    writer.finish_writing_geotiff()
    print('Done duplicating the image!')

    time.sleep(2)
    print('Cleaning up the writer!')
    writer.cleanup()

    image = None # Close the image

    print('Script is finished.')

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
    
    
    
    
    
    
    
    
    
    
    
    