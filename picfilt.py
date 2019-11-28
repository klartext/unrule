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

        ins     = self.ins     # length inner part
        stretch = self.stretch # "stretching" each side of inner by stretch
        outs    = self.outs    # whole length of inner + 2 * stretched

        outpicarray = bwpicarray.copy()

        avdiff_low = -9
        avdiff_high = 2
        print("ins, stretch, outs:", self.ins, self.stretch, self.outs)


        for yval in range(0, height - outs):
            for xval in range(0, width - outs):
                left   = bwpicarray[yval,  xval : xval + stretch]
                inside = bwpicarray[yval,  xval + stretch : xval + ins + stretch]
                right  = bwpicarray[yval,  xval + ins + stretch : xval + ins + 2 * stretch]

                lav = left.sum()/self.stretch
                insav = inside.sum()/self.ins
                rav = right.sum()/self.stretch

                avdiff = (lav - rav)      # for decision if newval is used
                newval =  (lav + rav) / 2 # the new value for inside, if used at all

                print("(y, x): ({0:4d},{1:4d}: insav -newval : {2:10f},   avdiff: {3:10f}".format(int(yval), int(xval), insav - newval, avdiff) )

                # Standardabweichung noch checken -> wenn zu groß, dann nicht verändern

                for idx in range(stretch + 1, stretch + ins + 1):
                    xpos = xval + idx

                    if abs(avdiff) < 10 and  -40 < insav - newval and insav - newval < 0: # copy new value to newpic
                        print("(y,xpos) = ({0:d},{1:d}) <- {2:f}".format(yval, xpos, newval) )
                        outpicarray[yval][xpos] = newval
                    else: # just copy orig data to newpic
                            outpicarray[yval][xpos] = bwpicarray[yval][xpos]

        #self.outpicarray = outpicarray
        #return outpicarray

        print("ins, stretch, outs:", self.ins, self.stretch, self.outs)
        for xval in range(0, width - outs):
            for yval in range(0, height - outs):
                above  = outpicarray[yval : yval + stretch, xval]
                inside = outpicarray[yval + stretch : yval + ins + stretch, xval]
                below  = outpicarray[yval + ins + stretch : yval + ins + 2 * stretch, xval]
                print("(yval,xval) = ({0:d},{1:d})".format(yval, xval) )

                aav = above.sum()/self.stretch
                insav = inside.sum()/self.ins
                bav = below.sum()/self.stretch

                avdiff = (aav - bav)      # for decision if newval is used
                newval =  (aav + bav) / 2 # the new value for inside, if used at all
                #newval = 0

                print("(y, x): ({0:4d},{1:4d}: insav -newval : {2:10f},   avdiff: {3:10f}".format(int(yval), int(xval), insav - newval, avdiff) )

                # Standardabweichung noch checken -> wenn zu groß, dann nicht verändern

                for idx in range(stretch + 1, stretch + ins + 1):
                    ypos = yval + idx

                    if abs(avdiff) < 10 and  -40 < insav - newval and insav - newval < 0: # copy new value to newpic
                        print("(y,xpos) = ({0:d},{1:d}) <- {2:f}".format(ypos, xval, newval) )
                        outpicarray[ypos][xval] = newval
                    else: # just copy orig data to newpic
                            outpicarray[ypos][xval] = outpicarray[ypos][xval]
                            #outpicarray[ypos][xval] = newval - 10


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
#foo = Antikaro("small.png")
foo.set_ins(3)
foo.set_stretch(3)
#foo.transpose()
foo.remove_lineature()
#foo.transpose()
foo.save("out.png")
