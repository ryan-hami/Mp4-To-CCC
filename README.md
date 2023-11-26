# Info
This fork of [Mp4-To-Srt](https://github.com/Nachtwind1/Mp4-To-Srt) adds color from the video into the closed captions.

I am unfamiliar with the standard techniques for creating closed captions, so I just went to a [rainbow caption video](https://youtu.be/Cc2nkx77U24), opened the Network tab of Inspect, pulled the `youtube.com/api/timedtext` request, and wrote the script to construct a subtitle payload in that format.

To test the subtitles I used the popular strategy of capturing requests with Telerik Fiddler and overriding the response with my generated json caption file instead of the intended captions for any video.

The wobble video is a recording of the famous gif then I just used ffmpeg to crop it.

[Demo of result](https://youtu.be/9-oYx9Scd7g)

# Mp4-To-CCC
A Python Programm That Converts Mp4 files to Colored Closed Captions for YouTube

# How to use

## Requirements

python3, opencv-python, PIL, numpy

### How to install

#### [Python](https://www.python.org/downloads/)

if you have python setup do

#### python3 -m pip install \<dependency\>

## Example
```
python3 main.py --file "./Bad Apple.mp4" --inputfps 30 --collums 40 --msoffset 0 --idoffset 0
```
## What do The Arguments mean

|Argument|Rquired|Description|
|----|-----|-------|
|--file|Yes|Your input mp4 file|
|--inputfps|Yes|The fps of your input Video (it only works for 30, 60, 90...)|
|--collums|Yes|How many characters Per Row|
|--msoffset|No|After How many milliseconds should the animation start|
|--idoffset|No|At which subtitle id should it start|
