from PIL import Image
import struct


im = Image.open('bg.png')
out = open('bg.raw', "wb")
isSWAP = True

image_height = im.size[1]
image_width = im.size[0]
#load pixel array
pix = im.load()
for h in range(image_height):
    for w in range(image_width):
        if w < im.size[0]:
            R = pix[w, h][0] >> 3
            G = pix[w, h][1] >> 2
            B = pix[w, h][2] >> 3

            rgb = (R << 11) | (G << 5) | B

            if isSWAP:
                swap_string_low = rgb >> 8
                swap_string_high = (rgb & 0x00FF) << 8
                swap_string = swap_string_low | swap_string_high
                out.write(struct.pack('H', swap_string))
            else:
                out.write(struct.pack('H', rgb))
        else:
            rgb = 0
