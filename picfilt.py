#! /usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class Antikaro:
    def __init__(self, bwpicarray, ins, stretch):
        #self.bwpicarray = bwpicarr
        self.height, self.width = bwpicarr.shape

        self.ins     = ins
        self.stretch = stretch
        self.outs    = 2 * stretch + ins

        outpicarray = self.bar(bwpicarray)
        if False:
            outpicarray = np.transpose(outpicarray)
            outpicarray = self.bar(outpicarray)
            outpicarray = np.transpose(outpicarray)
        save_nparray_as_pic(outpicarray, "out.png")


    def bar(self, bwpicarray):
    #ins, outs, width, height, image_array ):

        height, width = bwpicarray.shape

        outs = self.outs
        outpicarray = bwpicarray.copy()

        avdiff_low = 0
        avdiff_high = 15


        for xval in range(outs, width - outs):
            for yval in range(outs, height - outs):

                left = bwpicarray[yval,  xval - outs : xval - 1]
                right = bwpicarray[yval,  xval +1 : xval + outs]

                lav = left.sum()/stretch
                rav = right.sum()/stretch

                avdiff = abs(lav - rav)

                # Standardabweichung noch checken -> wenn zu groß, dann nicht verändern

                if avdiff > avdiff_low and avdiff < avdiff_high:
                    outpicarray[yval][xval] = (lav + rav) / 2
                else:
                    outpicarray[yval][xval] = bwpicarray[yval][xval]

        return outpicarray


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








#print(type(bwpicarr))
#print(bwpicarr.ndim)
#print(bwpicarr.shape)
#print(bwpicarr.dtype)
#print(bwpicarr.size)

#print("width:", width)
#print("height:", height)


#print("ins =", ins)
#print("outs =", outs)
#print("stretch =", stretch)
#print("height:", height)

# plt.imshow(pic)

ins = 1
stretch  = 2
bwpicarr = readimage_as_grayval_to_array("lemma.png")
foo = Antikaro(bwpicarr, ins, stretch)
