# Nadir Patcher

## In one sentence

Command line Python script that 1) takes logo file, 2) converts to equirectangular image, 3) transforms to desired size, and 4) overlays on-top of an equirectangular photo or video.

## Why we built this

Adding a nadir to 360 imagery is a great way to show off your brand or watermark your imagery.

Lots of propriety software offers this functionality already, but we wanted an easy way to create a batch script that could add a nadir to multiple files in one command.

Nadir Patcher is the result.

## READ BEFORE YOU BEGIN

Nadir Patcher is designed as a simple tool to add a nadir to a series images. We have some other tools that might be better suited to what you need;

* [gopro2gsv](https://github.com/trek-view/gopro2frames) that takes a series of GoPro timelapse images, converts to a video (with nadir) and uploads to Street View. If your ultimate goal is to upload to Street View, we recommend using gopro2frames.
* if you need to break a GoPro video into frames (and optionally add a nadir) use our tool [gopro2frames](https://github.com/trek-view/gopro2frames). This will work with GoPro videos, including unprocessed GoPro Fusion (2x fisheye mp4) and GoPro MAX (.360) videos.

## How it works

1. You create a 500px x 500px image you want to use as the nadir
2. You have one of more equirectangular panoramic photo or video files that you want to add the nadir to
3. You define the size of the nadir as a % of the photo or video height
4. The script converts the nadir image into an equirectangular image, and then flips the nadir image vertically and horizontally 
5. The script resizes the nadir image to match the width of the panoramic photo(s) and overlays the nadir on the bottom of the panoramic photo or video
6. The script outputs the new panoramic photo or video with the new nadir in the output directory defined

If you are keen to learn more, these supporting blog posts will be of interest;

* How to Add a Custom Nadir to a 360 Photo using GIMP: https://www.trekview.org/blog/adding-a-custom-nadir-to-360-video-photo/
* How to Add a Custom Nadir to a 360 Photo Programmatically (using ImageMagick): https://www.trekview.org/blog/adding-a-custom-nadir-to-360-video-photo/
* Using ffmpeg to overlay a custom nadir or watermark on GoPro videos: https://www.trekview.org/blog/overlay-nadir-watermark-video-using-ffmpeg/

## Requirements

### Software Requirements

* Python version 3.6+
* [Imagemagick](https://imagemagick.org/script/download.php)
* [ffmpeg / ffprobe](https://www.ffmpeg.org/download.html)

These must be installed in the path. You can check this by running `magick` and `ffmpeg` in the CLI. If it returns information about the tools, they are correctly installed.

### Image Requirements

**For panoramic photo**

* Must be `[XMP] ProjectionType=equirectangular`. 

**For nadir**

* Must be a circle with a diameter of 500px.

## Quick start guide

There are two versions of the script:

* `nadir-patcher.py`: this calculates the resolution of the first image once, and thus the nadir once. It then overlays the nadir on all images supplied. Use when images are all the same resolution.
* `nadir-patcher.py`: this calculates the resolution of every image, and thus the nadir everytime. This is useful when directory has photo files with multiple resolutions.

```shell
# clone the latest code
git clone https://github.com/trek-view/nadir-patcher
cd nadir-patcher
# create a venv
python3 -m venv nadir-patcher-venv
source nadir-patcher-venv/bin/activate
```

Using the script is simple. Arguments can be provided in the following format:

```shell
python nadir-patcher.py "[PANORAMIC PHOTO / VIDEO FILE OR FOLDER PATH]" "[NADIR FILE PATH]" [PERCENTAGE SIZE] "[OUTPUT_FOLDER_PATH]"
```

Where:

* `[PANORAMIC PHOTO / FOLDER PATH]`: is the photo or directory of photos you want to add the nadir too
* `[NADIR FILE PATH]` is the path to the nadir file
* `[PERCENTAGE SIZE]` refers to the height of the nadir as a percentage of total image height. This must be specified as whole number between 1 (smallest) and 100 (covers entire image). Somewhere between 5% to 15% is what most other software tools use to generate a nadir.
* `[OUTPUT_FOLDER_PATH]`: directory where outputted photo(s) with nadir should be stored.

### Examples

**Take a single panoramic image and add a nadir covering 35% of the image and output to directory `/output`:**

```shell
python3 nadir-patcher.py \
	samples/input/GSAA7468.JPG \
	nadir-library/trek_view_full_nadir.png \
	25 \
	samples/output/GSAA7468/
```

**Take a directory of panoramic images and add a nadir covering 15% of every image in the directory:**

```shell
python3 nadir-patcher.py \
	samples/input/timelapse_images/ \
	nadir-library/trek_view_full_nadir.png \
	15 \
	samples/output/timelapse_images/
```

## License

[Apache 2.0](/LICENSE).