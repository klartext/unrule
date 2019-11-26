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

ins = 3
stretch  = 2
outs = 2 * stretch + ins

outpicarray = bwpicarr.copy()

def foo():
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
            allav = outersum/(outs*outs)

            avdiff = frameav - innerav

            #print("avdiff:", avdiff)

    #        if abs(avdiff) > 5 and abs(avdiff) < 10:
    #            for yo in range(0,outs):
    #                for xo in range(0,outs):
    #                    outpicarray[yval+xo][xval+xo] = frameav
            if avdiff > -10 and avdiff < 10:
                outpicarray[yval][xval] = frameav
            else:
                outpicarray[yval][xval] = bwpicarr[yval][xval]

def bar():
    # das geht schon mal sehr gut!
    for xval in range(20,750):
        for yval in range(20,240):
            left = bwpicarr[yval,  xval - outs : xval - 1]
            right = bwpicarr[yval,  xval +1 : xval + outs]

            lav = left.sum()/(outs-1)
            rav = right.sum()/(outs-1)

            avdiff = abs(lav - rav)


            #print(left, right)
            #print("lav / rav:", lav, rav)
            #print(avdiff)



            # Standardabweichung noch checken -> wenn zu groß, dann nicht verändern

            if avdiff > 0 and avdiff < 8:
                outpicarray[yval][xval] = (lav + rav) / 2
            else:
                outpicarray[yval][xval] = bwpicarr[yval][xval]

    # Das hier funktioniert noch nicht
    for xval in range(20,750):
        for yval in range(20,240):
            above = bwpicarr[yval - outs : yval - 1, xval]
            below = bwpicarr[yval +1 : yval + outs, xval]

            aav = above.sum()/(outs-1)
            bav = below.sum()/(outs-1)

            avdiff = abs(aav - bav)


            #print(above, below)
            #print("aav / bav:", aav, bav)
            #print(avdiff)



            # Standardabweichung noch checken -> wenn zu groß, dann nicht verändern

            if avdiff > 0 and avdiff < 8:
                outpicarray[yval][xval] = (aav + bav) / 2
            else:
                outpicarray[yval][xval] = bwpicarr[yval][xval]


bar()
save_nparray_as_pic(outpicarray, "out.png")
