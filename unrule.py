#! /usr/bin/python

import sys
import itertools as it
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def moving_average(array, avlen):
    """
    array: the array that will be averaged over
    avlen: the number of elements that go into the average (window-size)
    """
    convolutor = list(it.repeat(1,avlen)) # creates a list with avlen ones
    if avlen < 1:
        avlen = 1
    return np.convolve(array, convolutor, 'valid')/avlen



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

            print("\n")
            # convolve() arbeitet nur auf 1D
            # man muss die jew. Daten erst mal extrahieren...
            print("yval:", yval)
            print("create moving average")
            print("Daten:", outpicarray[yval])
            mvaver = moving_average(outpicarray[yval], self.stretch)
            innermvav = moving_average(outpicarray[yval], self.ins)
            print(mvaver)
            print("moving average done")
            print("-----------------------------------------------")

            for xval in range(0, width - outs):
                lav = mvaver[xval]
                insav = innermvav[xval+stretch]
                rav = mvaver[xval+stretch+ins]

                #print("(yval, xval) = value: ({0:3d},{1:3d}) = {2:3d}     lav/insav/rav = {3:10.3f} / {4:10.3f} / {5:10.3f}:".format(yval, xval, outpicarray[yval][xval], lav, insav, rav))
                #print("mvaver[xval], mvaver[xval+stretch], mvaver[]", mvaver[xval], mvaver[xval+stretch], mvaver[xval+stretch+ins])
                #print("diffs", mvaver[xval] - lav, innermvav[xval+stretch] - insav, mvaver[xval+stretch+ins]-rav)

                avdiff = (lav - rav)      # for decision if newval is used
                newval =  (lav + rav) / 2 # the new value for inside, if used at all

                # Standardabweichung noch checken -> wenn zu groß, dann nicht verändern

                for idx in range(stretch + 1, stretch + ins + 1):
                    xpos = xval + idx

                    if abs(avdiff) < 10 and  -40 < insav - newval and insav - newval < 0: # copy new value to newpic
                        #print("(y,xpos) = ({0:d},{1:d}) <- {2:f}".format(yval, xpos, newval) )
                        outpicarray[yval][xpos] = newval
                    else: # just copy orig data to newpic
                            outpicarray[yval][xpos] = bwpicarray[yval][xpos]

        #self.outpicarray = outpicarray
        #return outpicarray

        print("vertikal")
        #print("ins, stretch, outs:", self.ins, self.stretch, self.outs)
        for xval in range(0, width - outs):
            for yval in range(0, height - outs):

                # keine Ahnung, wie ich aus dem outpicarray (numpy-2D-array)
                # vertikal Daten raus bekomme - irgendwas mit Axis
                data = np.transpose(outpicarray)[xval]
                print("data:", data)
                mvaver = moving_average(np.transpose(outpicarray)[xval], self.stretch) # so ist es wohl falsch

                above  = outpicarray[yval : yval + stretch, xval]
                inside = outpicarray[yval + stretch : yval + ins + stretch, xval]
                below  = outpicarray[yval + ins + stretch : yval + ins + 2 * stretch, xval]
                #print("(yval,xval) = ({0:d},{1:d}): above / inside  below = ".format(yval, xval), above, inside, below )

                aav = above.sum()/self.stretch
                insav = inside.sum()/self.ins
                bav = below.sum()/self.stretch

                #print("mvaver[yval]", mvaver[xval])

                avdiff = (aav - bav)      # for decision if newval is used
                newval =  (aav + bav) / 2 # the new value for inside, if used at all
                #newval = 0

                print("(y, x): ({0:4d},{1:4d}: insav -newval : {2:10f},   avdiff: {3:10f}".format(int(yval), int(xval), insav - newval, avdiff) )

                # Standardabweichung noch checken -> wenn zu groß, dann nicht verändern

                for idx in range(stretch + 1, stretch + ins + 1):
                    ypos = yval + idx

                    if abs(avdiff) < 10 and  -40 < insav - newval and insav - newval < 0: # copy new value to newpic
                        #print("(y,xpos) = ({0:d},{1:d}) <- {2:f}".format(ypos, xval, newval) )
                        outpicarray[ypos][xval] = newval
                    else: # just copy orig data to newpic
                            outpicarray[ypos][xval] = outpicarray[ypos][xval]
                            #outpicarray[ypos][xval] = newval - 10


        print("===============================================")
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


filelist = sys.argv[1:]

print("Try to remove lineature from these files:", filelist)

for filename in filelist:
    print("working on file:", filename)
    foo = Antikaro(filename)
    foo.set_ins(3)
    foo.set_stretch(3)
    foo.remove_lineature()
    outfilename = "linrem_{0}".format(filename)
    foo.save(outfilename)
    print("Resulting file:", outfilename)
