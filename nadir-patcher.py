# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Author: hq@trekview.org
# Created: 2020-0602
# Copyright: Trek View
# Licence: MIT
# -------------------------------------------------------------------------------

import subprocess
import shlex
import os
import shutil
import sys

folder_name="nadir_patcher_temp"
output1="nadir_patcher_temp\\temp_result1.png"
output2="nadir_patcher_temp\\temp_result2.png"
output3="nadir_patcher_temp\\temp_result3.png"
def main(argv):


    main_file = sys.argv[1]
    overlay_file = sys.argv[2]
    d_size = float(int(sys.argv[3])/100)
    output = sys.argv[4]
    print('staring...')  
    if not os.path.exists(folder_name):
               os.makedirs(folder_name)
               
    main_file1="\""+main_file+"\"" 
    comd1="convert "+"\""+overlay_file+"\""+" -distort DePolar 0  "+output1
    subprocess.call(comd1,shell=True)
    print('process 1 done') 
    
    comd2="convert {} -rotate 180 -strip {}".format(output1,output2)
    subprocess.call(comd2,shell=True)
    print('process 2 done') 
    
    cmd = 'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv="s=x:p=0"'
    args = shlex.split(cmd)
    args.append(main_file)

    ffprobe_output = subprocess.check_output(args).decode('utf-8')
    wh_values = ffprobe_output.split("x")
    width_str = wh_values[0]
    height_float = float(wh_values[1])
    overlay_height_temp=int(float(height_float*d_size))
    overlay_position=str(int(height_float)-overlay_height_temp)
 
    overlay_height= str(overlay_height_temp)
 
    overlay_scale ="{}:{}".format(width_str,overlay_height)
    comd3 ="ffmpeg -y -i {} -vf scale={} {}".format(output2,overlay_scale,output3)
    subprocess.call(comd3,shell=True)
    print('process 3 done') 
    comd4 ="convert "+main_file1+" "+output3+"  -geometry +0+"+overlay_position+" -composite "+"\""+output+"\"" 
    subprocess.call(comd4,shell=True)
    print('process 4 done') 
    shutil.rmtree(folder_name)
    print('Done Successfully') 

if __name__ == '__main__':
    main(sys.argv[1:])