# Nadir Patcher

## In one sentence

Command line Python script that 1) takes logo file, 2) converts to equirectangular image, 3) transforms to desired size, and 4) overlays on-top of an equirectangular photo or video as a nadir.

## Why we built this

Adding a nadir to 360 imagery is a great way to show off your brand or watermark your imagery.

Lot's of propriety software offers this functionality already, but we wanted an easy way to create a batch script that could add a nadir to multiple files in one command.

Nadir Patcher is the result. 

## How it works

1. You create a 500px x 500px image you want to use as the nadir
2. You have one of more equirectangular panoramic photo or video files that you want to add the nadir to
3. You define the size of the nadir as a % of the photo or video height
4. The script converts the nadir image into an equirectangular image, and then flips the nadir image vertically and horizontally 
5. The script resizes the nadir image to match the width of the panoramic photo(s) and overlays the nadir on the bottom of the panoramic photo or video
6. The script outputs the new panoramic photo or video with the new nadir in the output directory defined

## Requirements

### Software Requirements

* Python version 3.6+
* [Imagemagick](https://imagemagick.org/script/download.php)
* [ffmpeg / ffprobe](https://www.ffmpeg.org/download.html)

### Image Requirements

**For panoramic photo / video**

* Must be [XMP] ProjectionType=equirectangular. 

**For nadir**

* Must be a minimum of 500 pixels x 500 pixels

## Quick start guide

Using the script is simple. Arguments can be provided in the following format:

`python nadir-patcher.py "[PANORAMIC PHOTO / VIDEO FILE OR FOLDER PATH]" "[NADIR FILE PATH]" [PERCENTAGE SIZE] "[OUTPUT_FOLDER_PATH]"`

In the images below I'll use [this panoramic photo](samples/input/MULTISHOT_9698_000001.jpg) and [this nadir](samples/input/my_custom_nadir.png).

`[PERCENTAGE SIZE]` refers to the height of the nadir as a percentage of total image height. This must be specified as whole number between 1 (smallest) and 100 (covers entire image). Somewhere between 5% to 15% is what most other software tools use to generate a nadir.

![Nadir as percentage of panoramic image height](/example-nadir-percentage-of-pano.jpg)

The naming convention for outputted images is as follows: [ORIGINAL FILE NAME] _ [NADIR FILE NAME] _ [PERCENTAGE SIZE OF NADIR] pc. [ORIGINAL FILE EXTENSION]. For example; MULTISHOT_9698_000001.jpg > MULTISHOT_9698_000001_nadir_12pc.jpg

And here's what the outputted file looks like looking down when rendered in a panoramic viewer:

![Example cropped output from Nadir Patcher](/example-nadir-pano-result.jpg)

To help you get started here's some examples. You'll find the files used in the [`samples/`](/samples) directory of this repository.

**Take a single panoramic image and add a nadir covering 12% of the image:**

_MacOS / Linux:_

`python nadir-patcher.py samples/input/MULTISHOT_9698_000001.jpg samples/input/my_custom_nadir.png 12 samples/demo/`

_Windows:_

`python nadir-patcher.py "samples\input\MULTISHOT_9698_000001.jpg" "samples\input\my_custom_nadir.png" 12 "samples\demo"`

**Take a directory of panoramic images and add a nadir covering 8% of every image in the directory:**

_MacOS / Linux:_

`python nadir-patcher.py samples/input/ samples/input/my_custom_nadir.png 8 samples/demo/`

_Windows:_

`python nadir-patcher.py "samples\input\" "samples\input\my_custom_nadir.png" 8 "samples\demo\"`

**Take a single panoramic video and add a nadir covering 12% of the video:**

_MacOS / Linux:_

`python nadir-patcher.py samples/input/VIDEO_7152.mp4 samples/input/my_custom_nadir.png 12 samples/demo/`

_Windows:_

`python nadir-patcher.py "samples\input\VIDEO_7152.mp4" "samples\input\my_custom_nadir.png" 12 "samples\demo"`


## Nadir library

We've included some stock nadirs you can use in the [`nadir-libary/`](/nadir-library) directory of this repository.

Submit you own logos (via pull request or email) to us and we'll add them to the library.

### Branding guidelines

If you plan to upload your photos to products like Google Street View, be aware of the branding guidelines for nadirs, otherwise your images could be rejected.

[Street View branding guidelines can be viewed here](https://www.google.co.uk/streetview/sales/).

## Support 

We offer community support for all our software on our Campfire forum. [Ask a question or make a suggestion here](https://campfire.trekview.org/c/support/8).

## License

Nadir Patcher is licensed under an [GNU AGPLv3 License](https://github.com/trek-view/nadir-patcher/blob/master/LICENSE.txt).