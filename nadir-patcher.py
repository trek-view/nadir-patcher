# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Author: hq@trekview.org
# Created: 2020-06-02
# Copyright: Trek View
# Licence: GNU AGPLv3
# -------------------------------------------------------------------------------

import subprocess
import shlex
import os
import shutil
import sys
import platform

#Global Variables for temp folder and files that will be automatically deleted when process complete. 
temp_folder_name_s="nadir_patcher_temp_s"
temp_folder_name_d="nadir_patcher_temp_d"
temp_output1=""
temp_output2=""
temp_output3=""
temp_output4=""
temp_output5=""

def main(argv):
    
    file_list=[]
    firt_img_s_h=""    
    #Create nadir_patcher_temp folder 
    if not os.path.exists(temp_folder_name_s):
               os.makedirs(temp_folder_name_s)
    
    if not os.path.exists(temp_folder_name_d):
               os.makedirs(temp_folder_name_d)    
    #get parameter values from command line arguments           
    main_file_dir = sys.argv[1]
    overlay_file = sys.argv[2]
    nadir_percentage = float(int(sys.argv[3])/100)

    #Check operating system
    
    if platform.system() =="Linux":
        print("Linux")
        os_path_set="/"
    elif platform.system() =="Windows":
        os_path_set="\\"
    else:
        os_path_set="/"
             
    #Check input path is file or directory     
    check_file_dir=os.path.isdir(main_file_dir)
    print(check_file_dir)  
    
    if check_file_dir:
        #process one by one image or video from directory
        print('staring...')             
        for r, d, f in os.walk(main_file_dir):
            for file in f:            
                file_path = os.path.join(r, file)
                file_list.append(file_path)
   
        
        
        
        flag=False
        first_s=get_res(file_list[0])
        for file_p in file_list:
            get_rs=get_res(file_p)
            if (get_rs!=first_s):
                flag=True
                break
            
            
        
        if flag:

               text = input ("All Resolution is not the same, But Do you want to Continue(YES/NO: ") 
               if (text.upper()=="YES"):
                    res=get_resolution(file_list[0])
                    overlay_pos=overlay_p(res[1],nadir_percentage)
                    main_process(file_list[0],overlay_file,nadir_percentage,os_path_set,temp_folder_name_s)
                    
                    for file_path in file_list:
                        res_temp=get_resolution(file_path)
                        if(res_temp[1]==res[1]):
                            main_process1(file_path,overlay_file,os_path_set,overlay_pos,temp_folder_name_s)
                        else:
                            main_process(file_path,overlay_file,nadir_percentage,os_path_set,temp_folder_name_d)
                            
                    shutil.rmtree(temp_folder_name_s)
                    shutil.rmtree(temp_folder_name_d)            
               else:
                    print("Please use all same resolutional images")
                    shutil.rmtree(temp_folder_name_s)
                    shutil.rmtree(temp_folder_name_d)                     
        

        else:

                res=get_resolution(file_list[0])
                overlay_pos=overlay_p(res[1],nadir_percentage)
                main_process(file_list[0],overlay_file,nadir_percentage,os_path_set,temp_folder_name_s)
                
                for file_path in file_list:
                    res_temp=get_resolution(file_path)
                    main_process1(file_path,overlay_file,os_path_set,overlay_pos,temp_folder_name_s)
                        
                shutil.rmtree(temp_folder_name_s)
                shutil.rmtree(temp_folder_name_d)
                

        
       
    else:
        print('staring...')  
        #Process image or video from file path
        main_process(main_file_dir,overlay_file,nadir_percentage,os_path_set,temp_folder_name_s)
        shutil.rmtree(temp_folder_name_s)
        shutil.rmtree(temp_folder_name_d) 
        print('Done Successfully') 

def main_process(main_file_dir,overlay_file,nadir_percentage,os_path_set,temp_folder_name):
        input_file_name=(os.path.splitext(os.path.basename(main_file_dir))[0])
        input_path_name, input_file_extension = os.path.splitext(main_file_dir)

        nadir_file_name=(os.path.splitext(os.path.basename(overlay_file))[0])
        nadir_path_name, nadir_file_extension = os.path.splitext(overlay_file)
        output_file=input_file_name+"_"+nadir_file_name+"_"+str(sys.argv[3])+"pc"+input_file_extension

        output_directory = sys.argv[4]
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        output_file=output_directory+os_path_set+output_file

        temp_output1=temp_folder_name+os_path_set+"temp_result1"+nadir_file_extension
        temp_output2=temp_folder_name+os_path_set+"temp_result2"+nadir_file_extension
        temp_output3=temp_folder_name+os_path_set+"temp_result3"+nadir_file_extension
        temp_output4=temp_folder_name+os_path_set+"temp_result4"+nadir_file_extension
        temp_output5=temp_folder_name+os_path_set+"temp_result5"+nadir_file_extension
    
        #Rotate nadir file 180 degrees and strip any metadata (https://imagemagick.org/script/command-line-options.php#rotate 
        # https://imagemagick.org/script/command-line-options.php#strip)
        comd1="magick "+"\""+overlay_file+"\""+" -rotate 180 -strip {}".format(temp_output1)
        subprocess.call(comd1,shell=True)
        print('process 1 done')
        
        #Turn nadir file into equirectangular projection (https://imagemagick.org/script/command-line-options.php#distort)
        comd2="magick "+"\""+temp_output1+"\""+" -distort DePolar 0  "+temp_output2
        subprocess.call(comd2,shell=True)
        print('process 2 done') 

        #Flip nadir file vertically (https://imagemagick.org/script/command-line-options.php#flip)
        comd3="magick "+"\""+temp_output2+"\""+" -flip  "+temp_output3
        subprocess.call(comd3,shell=True)
        print('process 3 done')

        #Flip nadir file horizontally (https://imagemagick.org/script/command-line-options.php#flop)
        comd4="magick "+"\""+temp_output3+"\""+" -flop  "+temp_output4
        subprocess.call(comd4,shell=True)
        print('process 4 done')        
                
        res=get_resolution(main_file_dir)
        overlay_position=overlay_p(res[1],nadir_percentage)
        overlay_scale=overlay_scale_cal(res[1],res[0],nadir_percentage)
        
        
        comd5 ="ffmpeg -y -i {} -vf scale={} {}".format(temp_output4,overlay_scale,temp_output5)
        subprocess.call(comd5,shell=True)
        
        print('process 5 done')
        img_video_process(main_file_dir,temp_output5,output_file,overlay_position)
        print('process done')




    
def main_process1(main_file_dir,overlay_file,os_path_set,overlay_position,temp_folder_name):
        input_file_name=(os.path.splitext(os.path.basename(main_file_dir))[0])
        input_path_name, input_file_extension = os.path.splitext(main_file_dir)

        nadir_file_name=(os.path.splitext(os.path.basename(overlay_file))[0])
        nadir_file_extension = os.path.splitext(overlay_file)[1]        
        output_file=input_file_name+"_"+nadir_file_name+"_"+str(sys.argv[3])+"pc"+input_file_extension

        output_directory = sys.argv[4]
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        output_file=output_directory+os_path_set+output_file
        temp_output5=temp_folder_name+os_path_set+"temp_result5"+nadir_file_extension
        
        
        img_video_process(main_file_dir,temp_output5,output_file,overlay_position)


def get_resolution(main_file_dir):
        w_h=[]
        cmd = 'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv="s=x:p=0"'
        args = shlex.split(cmd)
        args.append(main_file_dir)

        #Calculate the nadir dimensions for overlay
        ffprobe_output = subprocess.check_output(args).decode('utf-8')
        wh_values = ffprobe_output.split("x")
        w_h.append(wh_values[0])
        w_h.append(wh_values[1])
        return w_h 


def get_res(main_file_dir):
        
        cmd = 'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv="s=x:p=0"'
        args = shlex.split(cmd)
        args.append(main_file_dir)

        #Calculate the nadir dimensions for overlay
        ffprobe_output = subprocess.check_output(args).decode('utf-8')
        return ffprobe_output 


def overlay_p(height_val,nadir_percentage):
        height_float = float(height_val)
        overlay_height_temp=int(float(height_float*nadir_percentage))
        overlay_position=str(int(height_float)-overlay_height_temp)
        return overlay_position
        
def overlay_scale_cal(height_val,width_val,nadir_percentage):
        height_float = float(height_val)
        overlay_height_temp=int(float(height_float*nadir_percentage)) 
        
        overlay_height= str(overlay_height_temp)
        overlay_scale ="{}:{}".format(width_val,overlay_height) 
        return overlay_scale  

def img_video_process(main_file_dir,temp_output5,output_file,overlay_position):

        if(main_file_dir.endswith(".MP4") or main_file_dir.endswith(".mp4")):
            comd6="ffmpeg -y -i "+"\""+main_file_dir+"\""+" -i "+temp_output5+" -filter_complex  \"[0:v][1:v]overlay=x=0:y=(main_h)-overlay_h\" "+"\""+output_file+"\""  
            subprocess.call(comd6,shell=True)
        else:
            comd6 ="magick "+"\""+main_file_dir+"\""+" "+temp_output5+"  -geometry +0+"+overlay_position+" -composite "+"\""+output_file+"\"" 
            subprocess.call(comd6,shell=True)
        
if __name__ == '__main__':
    main(sys.argv[1:])