import numpy as np
import cv2
import os
import sys
from time import time
from base64 import b64encode
from binascii import unhexlify

bits = 7
blocks = 1 << bits
mbunit = 1048576

def ravif(video, X, Y):
    cap = cv2.VideoCapture(video)

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    unit_pos = frame_count * 1.0 / blocks

    fp_R = ""
    fp_G = ""
    fp_B = ""

    for i in range(blocks):
        pos = int(i * unit_pos)
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, frame = cap.read()
        small = cv2.resize(frame, (256, 256))
        small = cv2.blur(small, (16, 16))
        px = small[X, Y]
        fp_R = fp_R + ("%0.2x" % px[0])
        fp_G = fp_G + ("%0.2x" % px[1])
        fp_B = fp_B + ("%0.2x" % px[2])

    fp_hex = fp_R + fp_G + fp_B
    fp_b64 = b64encode(unhexlify(fp_hex))
    return (fp_b64)

# print(main(video_1))
