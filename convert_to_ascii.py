import numpy as np

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

# return a segment
def segment(color, utf8_text): return f'<s p="{color_to_id(color)}">{utf8_text}</s>'

# export the subtitles as .ytt
def export(name): open(f"output/{name}.ytt", "w").write(f'<?xml version="1.0" encoding="utf-8" ?><timedtext format="3"><head>{"".join(pens[1:])}</head><body>{"".join(events)}</body></timedtext>')

# converts an image to colored ascii characters then adds event to result
def convert(index, pil_image, mspf, num_columns, num_rows, dw, dh):
    # characters (with color / segments) in the subtitle event (frame as ascii)
    segs = []

    cur_color = ''
    utf8 = []

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

            # average color
            avg = tile.resize((1, 1)).getpixel((0, 0))

            # convert rgb tuple to hex string
            hex_string = '#{:02X}{:02X}{:02X}'.format(*avg)

            if cur_color != hex_string:
                if len(utf8): segs.append(segment(cur_color, "".join(utf8)))
                cur_color = hex_string
                utf8.clear()

            utf8.append(char)

        # end of line, append new line character
        if (row != num_rows - 1): utf8.append('&#xA;')

    start_ms = round(index * mspf)
    duration = round(mspf)

    if len(segs):
        segs.append(segment(cur_color, "".join(utf8)))
        text = "".join(segs)
        events.append(f'<p t="{start_ms}" d="{duration}">{text}</p>')
    else:
        id = color_to_id(cur_color)
        text = "".join(utf8)
        events.append(f'<p t="{start_ms}" d="{duration}" p="{id}">{text}</p>')
