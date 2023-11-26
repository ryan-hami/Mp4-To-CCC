# Python code to convert an image to ASCII image. AI comment?
import numpy as np
import json

from PIL import Image

# subtitle file to export
out = { "pens": [{}], "events": [] }

# maps colors to its index in the pens list
pen_map = { 16777215: 0 }

def color_to_id(color):
    if color in pen_map: return pen_map[color]

    # tail of list
    id = len(out["pens"])

    # map unique color to tail
    pen_map[color] = id

    # add new color as pen
    out["pens"].append({ "fcForeColor": color })

    return id

# add caption segments for the given time slot
def add(start_ms, duration_ms, segs): out["events"].append({ "tStartMs": start_ms, "dDurationMs": duration_ms, "segs": segs })

# export result
def export(): open("output/subtitles.json", "w").write(json.dumps(out))

# 10 levels of grey
gscale2 = '$8obdpq0Lun1+"`'

def getAverageL(image):

	"""
	Given PIL Image, return average value of grayscale value
	"""
	# get image as numpy array
	im = np.array(image)

	# get shape
	w,h = im.shape

	# get average
	return np.average(im.reshape(w*h))

def getEqualWidthScale(scale, width):
    equal_width_scale = ""
    for char in scale:
        equal_width_scale += char + " " * (width - 1)
    return equal_width_scale

def convertImageToAscii(fileName, cols, scale):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images 
    """
    # declare globals
    global gscale2

    pil_image = Image.open(fileName)

    # open image and convert to grayscale
    image = pil_image.convert('L')

    # store dimensions
    W, H = image.size[0], image.size[1]
    #print("input image dims: %d x %d" % (W, H))

    # compute width of tile
    w = W / cols

    # compute tile height based on aspect ratio and scale
    h = w / scale

    # compute number of rows
    rows = int(H / h)

    #print("cols: %d, rows: %d" % (cols, rows))
    #print("tile dims: %d x %d" % (w, h))

    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    # ascii image is a list of character strings
    segs = []

    # j outer, i inner for loop ... you are a monster...
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)

        # correct last tile
        if j == rows - 1:
            y2 = H

        for i in range(cols):
            # crop image to tile
            x1 = int(i * w)
            x2 = int((i + 1) * w)

            # correct last tile
            if i == cols - 1:
                x2 = W

            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))

            # get average luminance
            avg = int(getAverageL(img))

            # look up ascii char
            gsval = gscale2[int(((255-avg) * 14) / 255)]
            if gsval == '"':
                gsval = '" '
            elif gsval == "`":
                gsval = "` "

            # get center pixel of segment
            mx = x1 + (x2 - x1) // 2
            my = y1 + (y2 - y1) // 2
            pixel = pil_image.getpixel((mx, my))

            # convert rgb into integer representation
            r, g, b = pixel
            color = r * 65536 + g * 256 + b

            # append segment as char and color
            segs.append({ "utf8": gsval, "pPenId": color_to_id(color) })
        # end of line, append new line character
        if (j != rows - 1): segs.append({ "utf8": "\n", "pPenId": 0 })

    # return txt image
    return segs

# converts an image to colored ascii characters then adds event to result
def convert(imgFile, frm, tfrm, clms):
	# set scale default as 0.43 which suits
	# a Courier font
	scale = 0.43

	# set cols
	#cols = 40 # 3:30 vids (Bad apple) if you upload your srt file and the subtitle doesn't appear its because the file is too big (5.5 i think is the max)
	#cols = 56 # 2:00 vids so use less columms if your file is too big
    #cols = 64 #max res
	if clms:
		cols = int(clms)
	else:
		print("ERROR"*1000)

	if tfrm == 2:
		frm -= 1
		duration_ms = 34
	else:
		duration_ms = 33

	segs = convertImageToAscii(imgFile, cols, scale)
	add(frm, duration_ms, segs)
