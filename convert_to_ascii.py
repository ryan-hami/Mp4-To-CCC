import numpy as np
from PIL import Image
from random import shuffle

avg_to_char = ['$', '8', 'o', 'b', 'd', 'p', 'q', '0', 'L', 'u', 'n', '1', '+', '" ', '` ']

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

def avg_color(img):
    width, height = img.size
    pixels = img.load()

    total_r, total_g, total_b = 0, 0, 0

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            total_r += r
            total_g += g
            total_b += b

    num_pixels = width * height
    avg_r = total_r // num_pixels
    avg_g = total_g // num_pixels
    avg_b = total_b // num_pixels

    return (avg_r, avg_g, avg_b)

# converts an image to colored ascii characters then adds event to result
def convert(index, pil_image, mspf, num_columns, num_rows, dw, dh):
    # characters (with color / segments) in the subtitle event (frame as ascii)
    segs = []

    # traverse image as quads
    for row in range(num_rows):
        y1 = row * dh
        y2 = y1 + dh

        for col in range(num_columns):
            x1 = col * dw
            x2 = x1 + dw

            # extract tile
            tile = pil_image.crop((x1, y1, x2, y2))
            tile_greyscale = tile.convert('L')

            # max bright minus average luminescence
            luminosity = 255 - int(np.average(tile_greyscale))

            # look up ascii char from avg of greyscaled image
            char = avg_to_char[luminosity * 14 // 255]

            # convert rgb tuple to hex string
            hex_string = '#{:02X}{:02X}{:02X}'.format(*avg_color(tile))

            segs.append(segment(hex_string, char))

        # end of line, append new line character
        if (row != num_rows - 1): segs.append('&#xA;')

    add_event(index * mspf, mspf, "".join(segs))
