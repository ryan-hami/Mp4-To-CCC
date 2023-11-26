# Info
Fork of [Mp4-To-Srt](https://github.com/Nachtwind1/Mp4-To-Srt). This adds color from the video into the closed captions.

Originally I exported the closed captions as json because looking at how YouTube stores subtitles internally they are json files. Specifically I used this video as reference: [rainbow caption video](https://youtu.be/Cc2nkx77U24). You can get the subtitles by opening the Network tab of Inspect, and filtering for the `youtube.com/api/timedtext` request. Having done some research, they now export as `.ytt`, but it is a little buggier.

To test the subtitles I used the popular strategy of capturing requests with Telerik Fiddler and overriding the response with my generated caption file. This technique is described in the README of [this repo](https://github.com/arcusmaximus/YTSubConverter) under `Testing on PC`.

The wobble video is a recording of the famous gif then I just used ffmpeg to crop it.

[Demo of result](https://youtu.be/9-oYx9Scd7g)

# Mp4-To-CCC
A Python Programm That Converts Mp4 files to Colored Closed Captions for YouTube

# How to use

## Requirements

python3, opencv-python, pillow, numpy

### How to install

#### [Python](https://www.python.org/downloads/)

if you have python setup do

#### python3 -m pip install \<dependency\>

## Example
```
python3 main.py --file "./wobble.mp4" --inputfps 30 --collums 40 --msoffset 0 --idoffset 0
```
## What do The Arguments mean

|Argument|Rquired|Description|
|----|-----|-------|
|--file|Yes|Your input mp4 file|
|--inputfps|Yes|The fps of your input Video (it only works for 30, 60, 90...)|
|--collums|Yes|How many characters Per Row|
|--msoffset|No|After How many milliseconds should the animation start|
|--idoffset|No|At which subtitle id should it start|
