# Nadir Patcher

## In one sentence

Takes logo file, converts to equirectangular image, transforms to desired size, and overlays on-top of an equirectangular photo to create a new equirectangular photo with the nadir in.

## Why we built this

Adding a nadir to 360 photos is a great way to show off your brand or watermark your imagery.

Lot's of proprietry software offers this functionality already, but we wanted an easy way to create a batch script that could add a nadir to multiple files in one command.

Nadir patcher is the result. 

## How it works

1. You create a 500px x 500px image you want to use as the nadir
2. You have one of more equirectangular panoramic photo files that you want to add the nadir to
3. You define the size of the nadir as a % of the photo height
4. The script flips the nadir image 180 degrees and converts the nadir image into an equirectangular image
5. The script resizes the nadir image to match the width of the panoramic photo(s) and overlays the nadir on the bottom of the panroamic photo
6. The script outputs the new panoramic photo with the new nadir in the output directory defined

## Requirements

### Software Requirements

* Python version 3.6+
* [Imagemagick](https://imagemagick.org/script/download.php)
* [ffmpeg / ffprobe](https://www.ffmpeg.org/download.html)

### Image Requirements

**For panoramic photo**

* Must be [XMP] ProjectionType=equirectangular. 

**For nadir**

* Must be a minimum of 500 pixels x 500 pixels

## Quick start guide

Using the script is simple. Arguments can be provided in the following format:

` python nadir-patcher.py "[PANOROAMIC PHOTO FILE OR FOLDER PATH]" "[NADIR FILE PATH]" [PERCENTAGE SIZE]"`

`[PERCENTAGE SIZE]` refers to the height of the nadir as a percentage of total image height. This must be specified as whole number between 1 (smallest) and 100 (covers entire image). Somewhere between 5% to 15% is what most other software tools use to generate a nadir.

![Nadir as percentage of panoramic image height](/example-nadir-percentage-of-pano.jpg) "Nadir as percentage of panoramic image height")

The naming convention for outputted images is as follows: [ORIGINAL FILE NAME]_nadir_[PERCENTAGE SIZE OF NADIR]pc.[ORIGINAL FILE EXTENSION]. For example; MULTISHOT_9698_000001.jpg > MULTISHOT_9698_000001_nadir_12pc.jpg

To help you get started here's some examples. You'll find the files used in the [`samples/`](/samples) directory of this repository.

**Take single panoramic image and add a nadir covering 12% of the image:**

` python nadir-patcher.py "samples/input/MULTISHOT_9698_000001.jpg" "samples/input/my_custom_nadir.png" 12`

**Take a directory of panoramic images and add a nadir covering 8% of every image in the directory:**

` python nadir-patcher.py "samples/input/" "samples/input/my_custom_nadir.png" 8`

## Branding guidelines

If you plan to upload your photos to products like Google Street View, be aware of the branding guidelines for nadirs, otherwise your images could be rejected.

[Street View branding guidelines can be viewed here](https://www.google.co.uk/streetview/sales/).

## Support 

We offer community support for all our software on our Campfire forum. [Ask a question or make a suggestion here](https://campfire.trekview.org/c/support/8).

## License

Nadir Patcher is licensed under an [MIT License](https://github.com/trek-view/nadir-patcher/blob/master/LICENSE.txt).