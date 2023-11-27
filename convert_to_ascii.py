# Python code to convert an image to ASCII image. AI comment?
import numpy as np

from PIL import Image

events = []
pens = [ "#FFFFFF" ]
pen_map = { "#FFFFFF": 0 }

def color_to_id(color):
    if color in pen_map: return pen_map[color]

    # tail of list
    id = len(pens)

    # map unique color to tail
    pen_map[color] = id

    # add new color as pen
    pens.append(f'<pen id="{id}" fc="{color}"/>')

    return id

# append a subtitle to the events list
def add_event(start_ms, duration_ms, segs): events.append(f'<p t="{start_ms}" d="{duration_ms}">{segs}</p>')

# return a segment
def segment(color, utf8_text): return f'<s p="{color_to_id(color)}">{utf8_text}</s>'

# export the subtitles as .ytt
def export(): open("output/subtitles.ytt", "w").write(f'<?xml version="1.0" encoding="utf-8" ?><timedtext format="3"><head>{"".join(pens[1:])}</head><body>{"".join(events)}</body></timedtext>')

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

            # convert rgb tuple to hex string
            hex_string = '#{:02X}{:02X}{:02X}'.format(*pixel)

            # append segment as char and color
            segs.append(segment(hex_string, gsval))
        # end of line, append new line character
        if (j != rows - 1): segs.append('&#xA;')

    # return txt image
    return "".join(segs)

# converts an image to colored ascii characters then adds event to result
def convert(imgFile, frm, duration_ms, cols):
	# set scale default as 0.43 which suits
	# a Courier font
	scale = 0.43

	segs = convertImageToAscii(imgFile, cols, scale)
	add_event(frm, duration_ms, segs)
