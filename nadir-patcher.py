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
import traceback

# Global Variables for temp folder and files that will be automatically deleted when process complete.
temp_folder_name = "nadir_patcher_temp"
temp_output1 = ""
temp_output2 = ""
temp_output3 = ""
temp_output4 = ""
temp_output5 = ""


def main(argv):
    # Create nadir_patcher_temp folder
    if not os.path.exists(temp_folder_name):
        os.makedirs(temp_folder_name)

    # get parameter values from command line arguments
    main_file_dir = os.path.abspath(sys.argv[1])
    overlay_file = sys.argv[2]
    nadir_percentage = float(int(sys.argv[3]) / 100)

    # Check operating system

    if platform.system() == "Linux":
        print("Linux")
        os_path_set = "/"
    elif platform.system() == "Windows":
        os_path_set = "\\"
    else:
        os_path_set = "/"

    # Check input path is file or directory
    check_file_dir = os.path.isdir(main_file_dir)
    print(check_file_dir)

    if check_file_dir:
        # process one by one image or video from directory
        print('staring...')
        for r, d, f in os.walk(main_file_dir):
            for file in f:
                file_path = os.path.join(r, file)

                main_process(file_path, overlay_file, nadir_percentage)
        shutil.rmtree(temp_folder_name)
        print('Done Successfully')

    else:
        print('staring...')
        # Process image or video from file path
        main_process(main_file_dir, overlay_file, nadir_percentage)
        shutil.rmtree(temp_folder_name)
        print('Done Successfully')


def run_command(*args):
    try:
        out = subprocess.Popen(list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        return stdout.decode('utf8')
    except:
        print(traceback.format_exc())
        return ''


def main_process(main_file_dir, overlay_file, nadir_percentage):
    input_file_name = (os.path.splitext(os.path.basename(main_file_dir))[0])
    input_path_name, input_file_extension = os.path.splitext(main_file_dir)

    nadir_file_name = (os.path.splitext(os.path.basename(overlay_file))[0])
    nadir_path_name, nadir_file_extension = os.path.splitext(overlay_file)
    output_file = input_file_name + "_" + nadir_file_name + "_" + str(sys.argv[3]) + "pc" + input_file_extension

    output_directory = os.path.abspath(sys.argv[4])
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    output_file = os.path.join(output_directory, output_file)

    temp_output1 = os.path.join(temp_folder_name, "temp_result1" + nadir_file_extension)
    temp_output2 = os.path.join(temp_folder_name, "temp_result2" + nadir_file_extension)
    temp_output3 = os.path.join(temp_folder_name, "temp_result3" + nadir_file_extension)
    temp_output4 = os.path.join(temp_folder_name, "temp_result4" + nadir_file_extension)
    temp_output5 = os.path.join(temp_folder_name, "temp_result5" + nadir_file_extension)

    # Rotate nadir file 180 degrees and strip any metadata (https://imagemagick.org/script/command-line-options.php#rotate
    # https://imagemagick.org/script/command-line-options.php#strip)
    comd1 = "magick " + "\"" + overlay_file + "\"" + " -rotate 180 -strip {}".format(temp_output1)
    subprocess.call(comd1, shell=True)
    print('process 1 done')

    # Turn nadir file into equirectangular projection (https://imagemagick.org/script/command-line-options.php#distort)
    comd2 = "magick " + "\"" + temp_output1 + "\"" + " -distort DePolar 0  " + temp_output2
    subprocess.call(comd2, shell=True)
    print('process 2 done')

    # Flip nadir file vertically (https://imagemagick.org/script/command-line-options.php#flip)
    comd3 = "magick " + "\"" + temp_output2 + "\"" + " -flip  " + temp_output3
    subprocess.call(comd3, shell=True)
    print('process 3 done')

    # Flip nadir file horizontally (https://imagemagick.org/script/command-line-options.php#flop)
    comd4 = "magick " + "\"" + temp_output3 + "\"" + " -flop  " + temp_output4
    subprocess.call(comd4, shell=True)
    print('process 4 done')

    cmd = 'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv="s=x:p=0"'
    args = shlex.split(cmd)
    args.append(main_file_dir)

    # Calculate the nadir dimensions for overlay
    ffprobe_output = subprocess.check_output(args).decode('utf-8')
    wh_values = ffprobe_output.split("x")
    width_str = wh_values[0]
    height_float = float(wh_values[1])
    overlay_height_temp = int(float(height_float * nadir_percentage))
    overlay_position = str(int(height_float) - overlay_height_temp)

    overlay_height = str(overlay_height_temp)

    # Overlay the nadir and output the new file into specified directory
    overlay_scale = "{}:{}".format(width_str, overlay_height)
    comd5 = "ffmpeg -y -i {} -vf scale={} {}".format(temp_output4, overlay_scale, temp_output5)
    subprocess.call(comd5, shell=True)
    print('process 5 done')
    if (main_file_dir.endswith(".MP4") or main_file_dir.endswith(".mp4")):
        comd6 = "ffmpeg -y -i " + "\"" + main_file_dir + "\"" + " -i " + temp_output5 + " -filter_complex  \"[0:v][1:v]overlay=x=0:y=(main_h)-overlay_h\" -strict -2 " + "\"" + output_file + "\""
        res1 = subprocess.call(comd6, shell=True)

    else:
        comd6 = "magick " + "\"" + main_file_dir + "\"" + " " + temp_output5 + "  -geometry +0+" + overlay_position + " -composite" + "\"" + output_file + "\""
        subprocess.call(comd6, shell=True)
    print('process 6 done')
    print(' ----------------- Start updating metadata ------------------- ')
    res = run_command('exiftool', '-tagsfromfile', main_file_dir, '-all:all'
                      , os.path.abspath(output_file), '-overwrite_original', '-api', 'largefilesupport=1', '-ee')
    print(' ----------------- End updating metadata ------------------- '
          '\n\nExiftool output result:\n\n{}'.format(res))


if __name__ == '__main__':
    main(sys.argv[1:])
