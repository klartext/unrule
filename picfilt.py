#! /usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# plt.imshow(pic)

def readimage_to_array(filename):
    pic = Image.open(filename)
    return np.array(pic)

def readimage_as_grayval_to_array(filename):
    pic = Image.open(filename)
    pic_grayval = pic.convert('L') # Stimmt "L" überhaupt?
    return np.array(pic_grayval)




# Wie dann wider Bild aus dem Array machen?
# picBW.putdata(picarr) # zurück schreiben
# Image.fromarray(pix) # neues Bild

def save_nparray_as_pic(nparr, filename):
    newimage = Image.fromarray(nparr)
    newimage.save(filename)




#####################################################


bwpicarr = readimage_as_grayval_to_array("lemma.png")

print(type(bwpicarr))
print(bwpicarr.ndim)
print(bwpicarr.shape)
print(bwpicarr.dtype)
print(bwpicarr.size)

ins = 4
stretch    = 1
outs = 2 * stretch + ins

outpicarray = bwpicarr.copy()

for xval in range(50,600):
    for yval in range(40,200):
        outer = bwpicarr[yval : yval + outs,   xval : xval + outs]
        inner = outer[stretch : ins + stretch, stretch : ins + stretch]
        #print("outer shape:", outer.shape)
        #print("inner shape:", inner.shape)

        outersum = outer.sum()
        innersum = inner.sum()
        framesum = outersum - innersum

        frameav = framesum / (outs*outs - ins*ins)
        innerav = innersum / (ins*ins)

        #print("frameav | innerav | diff", frameav, innerav, frameav - innerav)
        #arithmittel = outer.sum()/outer.size

        #print(outer)
        #print("Mittelwert:", arithmittel)
        for yo in range(0,outs):
            for xo in range(0,outs):
                outpicarray[yval+xo][xval+xo] = frameav


save_nparray_as_pic(outpicarray, "out.png")
