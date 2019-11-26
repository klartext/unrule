#! /usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class Antikaro:
    def __init__(self, image):
        pass

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




def bar( ins, outs, width, height, image_array ):

    outpicarray = image_array.copy()

    for xval in range(outs, width - outs):
        for yval in range(outs, height - outs):

            left = image_array[yval,  xval - outs : xval - 1]
            right = image_array[yval,  xval +1 : xval + outs]

            lav = left.sum()/(outs-1)
            rav = right.sum()/(outs-1)

            avdiff = abs(lav - rav)

            # Standardabweichung noch checken -> wenn zu groß, dann nicht verändern

            if avdiff > 0 and avdiff < 8:
                outpicarray[yval][xval] = (lav + rav) / 2
            else:
                outpicarray[yval][xval] = image_array[yval][xval]

    return outpicarray



bwpicarr = readimage_as_grayval_to_array("lemma.png")

print(type(bwpicarr))
print(bwpicarr.ndim)
print(bwpicarr.shape)
print(bwpicarr.dtype)
print(bwpicarr.size)

height, width = bwpicarr.shape

print("width:", width)
print("height:", height)

ins = 3
stretch  = 2
outs = 2 * stretch + ins


print("ins =", ins)
print("outs =", outs)
print("stretch =", stretch)
print("height:", height)


outpicarray = bar(ins, outs, width, height, bwpicarr)
save_nparray_as_pic(outpicarray, "out.png")
