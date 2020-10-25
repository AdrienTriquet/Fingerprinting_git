import numpy as np
import cv2
import os
import sys
from time import time
from base64 import b64encode
from binascii import unhexlify

# fonction ravif : crée la fingerprint
# arguements : x et y pour la position du centre du calcul (px)
def ravif(path, x,y):
    print("RAViF : RApid Video Fingerprinter")
    print("---------------------------------------------")

    bits = 7
    blocks = 1 << bits
    mbunit = 1048576

    f = open(path,"r")
    liststr = []
    filesizes = []
    netfilesize = 0
    while True:
        path = f.readline()
        if not path: break
        liststr.append(path.rstrip())
        filesize = os.path.getsize(path.rstrip())
        netfilesize += filesize
        filesizes.append(filesize)
    f.close()

    print("processing " + str(len(liststr)) + " files (" + str(netfilesize / mbunit) + " Mb)")
    print("hash depth: " + str(bits) + " bits\n")

    speed = []

    for c in range(len(liststr)):

        file_start = time()
        cap = cv2.VideoCapture(liststr[c])

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        unit_pos = frame_count * 1.0 / blocks
        st = np.array((),np.dtype(np.uint8))
        fp_R = ""
        fp_G = ""
        fp_B = ""

        msg = "[" + str(c) + "/" + str(len(liststr)) + "] " + liststr[c] + " (" + str(filesizes[c]/mbunit) + " Mb)"

        for i in range(blocks):
            pos = int(i * unit_pos)
            cap.set(cv2.CAP_PROP_POS_FRAMES,pos)
            ret, frame = cap.read()
            small = cv2.resize(frame,(256,256))
            small = cv2.blur(small,(16,16))
            px = small[x,y]
            fp_R = fp_R + ("%0.2x" % px[0])
            fp_G = fp_G + ("%0.2x" % px[1])
            fp_B = fp_B + ("%0.2x" % px[2])

            sys.stdout.write(msg + " %d%%    \r" % ((i+1)*100/blocks))
            sys.stdout.flush()
        sys.stdout.write("\n")
        cap.release()
        fp_hex = fp_R + fp_G + fp_B
        fp_b64 = b64encode(unhexlify(fp_hex))

        file_done = time()
        speed.append(file_done - file_start)

        return fp_b64
