#!/usr/bin/env python

# Copyright  2020, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
#
# The DELTA (Deep Earth Learning, Tools, and Analysis) platform is
# licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Script to correct bad nodata values
"""
import sys
import os
import argparse


#------------------------------------------------------------------------------

def main(argsIn):

    try:

        usage  = "usage: fix_nodata [options]"
        parser = argparse.ArgumentParser(usage=usage)

        parser.add_argument("--input-folder", dest="input_folder", required=True,
                            help="Folder containing input images.")

        parser.add_argument("--output-folder", dest="output_folder", required=True,
                            help="Folder to write output images in.")

        options = parser.parse_args(argsIn)

    except argparse.ArgumentError:
        print(usage)
        return -1

    if not os.path.exists(options.output_folder):
        os.mkdir(options.output_folder)

    input_files = os.listdir(options.input_folder)
    for f in input_files:
        input_path  = os.path.join(options.input_folder,  f)
        output_path = os.path.join(options.output_folder, f)
        cmd = ('image_calc ' + input_path + ' -o ' + output_path
               + ' -d uint8 --output-nodata-value 0 --calc "eq(var_0, 255, 0, var_0)" ')
        print(cmd)
        os.system(cmd)
        #raise Exception('DEBUG')

    print('Landsat TOA conversion is finished.')
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
