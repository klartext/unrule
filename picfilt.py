#! /usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class Antikaro:
    def __init__(self, filename):

        self.filename = filename
        self.bwpa = readimage_as_grayval_to_array(filename)
        bwpicarray = self.bwpa
        #self.bwpicarray = bwpicarr
        self.height, self.width = bwpicarray.shape

        # set defaults
        self.ins = 1
        self.stretch = 2
        self.calc_outs()

        #self.outpicarray = self.remove_lineature()
        if False:
            outpicarray = np.transpose(outpicarray)
            outpicarray = self.remove_lineature(outpicarray)
            outpicarray = np.transpose(outpicarray)


    def calc_outs(self):
        self.outs = 2 * self.stretch + self.ins

    def set_stretch(self, stretch):
        self.stretch = stretch
        self.calc_outs()

    def set_ins(self, ins):
        self.ins = ins
        self.calc_outs()

    def set_avdiff_lower(self, lowval):
        self.avdiff_lower = lowval

    def set_avdiff_higher(self, highval):
        self.avdiff_higher = highval

    def save(self, outfilename):
        save_nparray_as_pic(self.outpicarray, outfilename)

    def save2(self, outfilename):
        if not hasattr(self, outpicarray):
            print("No output array was created. Using the original picture")
            save_nparray_as_pic(self.bwpa, outfilename)
        else:
            save_nparray_as_pic(self.outpicarray, outfilename)

    def transpose(self):
        self.bwpa = np.transpose(self.bwpa)
        self.outpicarray = np.transpose(self.outpicarray)



    def remove_lineature(self):
    #ins, outs, width, height, image_array ):

        bwpicarray = self.bwpa
        height, width = bwpicarray.shape

        outs = self.outs
        outpicarray = bwpicarray.copy()

        avdiff_low = 0
        avdiff_high = 15


        for xval in range(outs, width - outs):
            for yval in range(outs, height - outs):

                left = bwpicarray[yval,  xval - outs : xval - 1]
                right = bwpicarray[yval,  xval +1 : xval + outs]

                lav = left.sum()/self.stretch
                rav = right.sum()/self.stretch

                avdiff = abs(lav - rav)

                # Standardabweichung noch checken -> wenn zu groß, dann nicht verändern

                if avdiff > avdiff_low and avdiff < avdiff_high:
                    outpicarray[yval][xval] = (lav + rav) / 2
                else:
                    outpicarray[yval][xval] = bwpicarray[yval][xval]

        #self.outpicarray = outpicarray
        #return outpicarray

        for yval in range(outs, height - outs):
            for xval in range(outs, width - outs):

                above = bwpicarray[yval - outs : yval - 1, xval]
                below = bwpicarray[yval +1 : yval + outs, xval]

                aav = above.sum()/self.stretch
                bav = below.sum()/self.stretch

                avdiff = abs(aav - bav)

                # Standardabweichung noch checken -> wenn zu groß, dann nicht verändern

                if avdiff > avdiff_low and avdiff < avdiff_high:
                    outpicarray[yval][xval] = (aav + bav) / 2
                else:
                    outpicarray[yval][xval] = bwpicarray[yval][xval]

        self.outpicarray = outpicarray
        return outpicarray



def readimage_to_array(filename):
    pic = Image.open(filename)
    return np.array(pic)

def readimage_as_grayval_to_array(filename):
    pic = Image.open(filename)
    pic_grayval = pic.convert('L') # Stimmt "L" überhaupt?
    return np.array(pic_grayval)

def save_nparray_as_pic(nparr, filename):
    newimage = Image.fromarray(nparr)
    newimage.save(filename)




#####################################################



foo = Antikaro("lemma.png")
foo.set_ins(1)
foo.set_stretch(2)
#foo.transpose()
foo.remove_lineature()
#foo.transpose()
foo.save("out.png")
