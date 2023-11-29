# Mp4-To-CCC - Convert .mp4's to Colored Closed Captions for YouTube

## Info
> Fork of [Mp4-To-Srt](https://github.com/Nachtwind1/Mp4-To-Srt). This adds color from the video into the closed captions.
>
> Initially I just wanted to add *color support* then make a **pull request**, but at this point I don't think there's a line of code I haven't rewritten, so it has been detached. Also the original version *constructs and renders the captions much faster, so it would be a disservice to implement these changes. Furthermore, this script is written for a different file format entirely which changes how it is used.
>
> Originally I exported the closed captions as json because looking at how YouTube stores subtitles internally they are json files. Specifically I used this video as reference: [rainbow caption video](https://youtu.be/Cc2nkx77U24). You can get the subtitles by opening the Network tab of Inspect, and filtering for the `youtube.com/api/timedtext` request. Having done some research, they now export as `.ytt`, but it is a little buggier.
>
> To test the subtitles I used the popular strategy of capturing requests with [Telerik Fiddler Classic](https://www.telerik.com/download/fiddler/fiddler4) and overriding the response with my generated caption file. This technique is described in the README of [this repo](https://github.com/arcusmaximus/YTSubConverter#testing-on-pc) under `Testing on PC`.
>
> The wobble video is a recording of the [famous gif](https://media.tenor.com/rj8goiLxkZoAAAAi/discord-blob.gif) then I just used [ffmpeg](https://ffmpeg.org/) to crop it.

### [Demo of result](https://youtu.be/9-oYx9Scd7g)

## Requirements

* opencv-python
* pillow
* numpy

### How to install
1. Setup python3

2. If you have python3 setup, paste this into terminal.

```bash
python3 -m pip install opencv-python pillow numpy
```

## Usage
> Run main.py with *python3 and pass in your desired arguments.
>
> The video will be processed and a `.ytt` captions file will be generated in `/output/{name}.ytt`
>
> This file can be uploaded directly to a youtube video as closed captions.

### Example:

```bash
python3 main.py --file "./wobble.mp4" --columns 40
```

## What do The Arguments mean

|Argument|Rquired|Description|
|----|-----|-------|
|--file|:white_check_mark:|mp4 file to process|
|--columns|:white_check_mark:|number of characters per row|
|--startms|:x:|how far in ms into the video to start|
