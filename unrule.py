#! /usr/bin/python

import sys
import itertools as it
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from time import perf_counter as pc

import argparse

np.set_printoptions(threshold=sys.maxsize, linewidth=200) # numpy-options
np.set_printoptions(formatter={'int': '{: 7d}'.format, 'float': '{: 6.3f}'.format})


def pdl(data, comment):
    """
    print data and length with comment
    """
    print("{:8s}:  (len = {:4d}}, data = {}".format(comment, len(data), data))


def moving_average(array, avlen):
    """
    array: the array that will be averaged over
    avlen: the number of elements that go into the average (window-size)
    """
    if avlen < 1:
        avlen = 1
    convolutor = list(it.repeat(1,avlen)) # creates a list with avlen ones
    return np.convolve(array, convolutor, 'valid')/avlen


def moving_average_with_diff(array, stretch, inner_len):
    """
    """
    if stretch < 1:
        stretch = 1

    # mean-diff-conv
    leftconv  = (np.repeat(1/stretch, stretch)) # creates a list with stretch ones
    inbetween        = (np.repeat(0, inner_len))
    rightconv = (np.repeat(-1/stretch, stretch)) # creates a list with stretch ones

    conv_avdiff = np.concatenate((leftconv, inbetween, rightconv))
    diff = np.convolve(array, conv_avdiff, 'valid') * (-1) # (-1) because left-right was used for avdiff
    print("conv_avdiff:", conv_avdiff)

    # mean-conv
    meanconv  = np.repeat(1/(2*stretch), stretch)
    conv_mean = np.concatenate((meanconv, inbetween, meanconv))
    mean = np.convolve(array, conv_mean, 'valid')
    print("conv_mean:  ", conv_mean)

    return diff, mean


def value_in_interval( value, interval ):
    low, high = interval
    if low <= value and value <= high:
        return True
    else:
        return False

class Antikaro:
    def __init__(self, filename, stretch=2, ins=2):

        self.filename = filename
        self.bwpa = readimage_as_grayval_to_array(filename)
        bwpicarray = self.bwpa
        #self.bwpicarray = bwpicarr
        self.height, self.width = bwpicarray.shape

        # set defaults
        self.ins = ins
        self.stretch = stretch
        self.calc_outs()

        if self.height < 2 * self.stretch + self.ins or self.width < 2 * self.stretch + self.ins:
            print("Image {}  too small for stretch-/ins-settings".format(filename), file=sys.stderr)
            raise ValueError

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



    # Here the main work will be done
    # ===============================
    def remove_lineature(self):

        bwpicarray = self.bwpa
        height, width = bwpicarray.shape

        ins     = self.ins     # length inner part
        stretch = self.stretch # "stretching" each side of inner by stretch
        outs    = self.outs    # whole length of inner + 2 * stretched

        outpicarray = bwpicarray.copy()

        print("SHAPE OF outpicarray:", outpicarray.shape)
        print("ELEMENT OF outpicarray:", outpicarray[0][0])

        avdiff_low = -20
        avdiff_high = 0
        print("stretch, ins, outs:", self.stretch, self.ins, self.outs)



        #print("whole linedata:\n", bwpicarray)

        # HORIZONTAL
        t0 = pc()
        for yval in range(0, height - outs):

            print("----------- Zeilenindex: {} ----------------------------".format(yval))
            linedata      = outpicarray[yval]
            dlen = len(linedata)

            # ----------------------------------------------------->>>
            linedata      = np.array([10,10,20,40,10,0,
                                  12,10,19,43,10,2,
                                  10,33,2,4,22,
                                 ])# TESTING
            # <<<-----------------------------------------------------
            mvaver    = moving_average(linedata, self.stretch) # kann spaeter weg
            innermvav = moving_average(linedata, self.ins)     # kann spaeter weg

            #pdl(linedata, "linedata")

            averdiff_arr, newval_arr = moving_average_with_diff(linedata, self.stretch, self.ins)

            #print("height, width =  {} * {}".format(height, width))
            #print("datalen: {}, mvaver-len: {}".format(len(linedata), len(mvaver)))

            print("linedata-length:   ", len(linedata))
            print("linedata:          ", linedata)
            print("mvaver-length  ", len(mvaver))
            print("mvaver:        ", mvaver)
            print()
            print("averdiff-len:", len(averdiff_arr))
            print("averdiff_arr:", averdiff_arr)
            print("newval-len:  ", len(newval_arr))
            print("newval_arr:  ", newval_arr)

            print("averdiff_arr.shape:", averdiff_arr.shape)
            print("newval_arr.shape:  ", newval_arr.shape)

            #print("len(innermvav) = {}, len(newval_arr) = {} \n".format( len(innermvav), len(newval_arr)), flush=True)
            thisline = linedata[yval,]

            subwin = linedata[stretch: -stretch]
            print("subwin:            ", subwin)
            # ISSUE WITH THE INDEXING
            #wo = np.where((averdiff_arr < 10) & (averdiff_arr > -10) &
            #              (innermvav - newval_arr > -50) & (innermvav - newval_arr < -1))
            #wo = np.where((averdiff_arr < 10) & (averdiff_arr > -10) )
            #wo = np.where((averdiff_arr > -30) & (averdiff_arr < -20) ) # TESTING with versmall.jpg
            wo = np.where( (averdiff_arr > 5) & (averdiff_arr < 10) ) # TESTING
            print("type(wo):          ", type(wo))
            print("wo[0].shape:       ", wo[0].shape)
            print("type(wo[0])        ", type(wo[0]))
            print("*** linedata.shape:", linedata.shape)
            print("*** linedata[wo].shape", linedata[wo].shape)
            print("WHERE-Indizes wo:  ", wo)
            print("linedata:          ", linedata)
            print("linedata[wo]       ", linedata[wo])

            preselect = ins
            print("linedata[sub][wo]       ", linedata[preselect:,][wo])

            #print("type of wo:", type(wo))
            #print("        wo:", wo)
            #newshape = linedata[self.stretch + self.ins - 1 : 2* self.stretch + self.ins -1]
            #print("*** newshape:", newshape)
            linedata[preselect:,][wo] = newval_arr[wo]
            print("linedata (changed):", linedata)
            #outpicarray[yval] = linedata
            print("--------------------------------------------------------".format(yval))
            exit(99)# TESTING
            continue


            for xval in range(0, width - outs):
                lav   = mvaver[xval]
                insav = innermvav[xval+stretch]
                rav   = mvaver[xval+stretch+ins]

                avdiff = (lav - rav)      # for decision if newval is used
                newval =  (lav + rav) / 2 # the new value for inside, if used at all

                print("*** Loop: avdiff / newval: {} / {}".format(avdiff, newval))

                # Standardabweichung noch checken -> wenn zu groß, dann nicht verändern
#(yval, xval) = ( 66,  59  -> avdiff = 65.666667, insav - newval: 32.833333)
#(yval, xval) = ( 66,  60  -> avdiff = 75.000000, insav - newval: 21.833333)
#(yval, xval) = ( 66,  61  -> avdiff = 75.000000, insav - newval: -3.166667)
#(yval, xval) = ( 66,  62  -> avdiff = 75.000000, insav - newval: -28.166667)
#
                #print("(yval, xval) = ({0:3d}, {1:3d}  -> avdiff = {2:f}, insav - newval: {3:f})".format(yval, xval, avdiff, insav - newval) )
                if value_in_interval(avdiff, [-10,10]) and  value_in_interval(insav - newval, [-50, -1]):
                #    print("(yval, xval) = ({0:3d}, {1:3d}  -> avdiff = {2:f}, insav - newval: {3:f})".format(yval, xval, avdiff, insav - newval) )
                    for idx in range(stretch + 1, stretch + ins + 1):
                        xpos = xval + idx - int(ins/2) # ins/2 abziehen, weil nicht nur nach vorne abziehen (???)

                        #newval = 0
                        outpicarray[yval][xpos] = newval

            # Alternative way: via Array-conditions

        t1 = pc()
        print("# HORIZONTAL: {:8.3f}".format(t1 - t0), file=sys.stderr, flush=True)

        # VERTIKAL
        for xval in range(0, width - outs):

            # welche Methode ist schneller?
            #data = np.transpose(outpicarray)[xval] # funktioniert auch
            data = outpicarray[:,xval] # funktioniert

            mvaver      = moving_average(data, self.stretch)
            innermvaver = moving_average(data, self.ins)


            for yval in range(0, height - outs):
                aav   = mvaver[yval]
                insav = innermvaver[yval + stretch]
                bav   = mvaver[yval + stretch + ins ]

                avdiff = (aav - bav)      # for decision if newval is used
                newval =  (aav + bav) / 2 # the new value for inside, if used at all

                # Standardabweichung noch checken -> wenn zu groß, dann nicht verändern

                #print("(yval, xval) = ({0:3d}, {1:3d}  -> avdiff = {2:f}, insav - newval: {3:f})".format(yval, xval, avdiff, insav - newval) )
                if value_in_interval(avdiff, [-10,10]) and  value_in_interval(insav - newval, [-50, -1]):
                    for idx in range(stretch + 1, stretch + ins + 1):
                        ypos = yval + idx - int(ins/2) # ins/2 abziehen, weil nicht nur nach vorne abziehen (???)

                        #newval = 0
                        outpicarray[ypos][xval] = newval

        t2 = pc()
        print("# VERTIKAL: {:8.3f}".format(t2 - t1), file=sys.stderr, flush=True)

        #print("===============================================")
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

# initiate the parser
programinfo = "This program removes lineature-patterns from an image."
parser = argparse.ArgumentParser( description = programinfo )

parser.add_argument("--ins", "-i", default=3, help="set inside-width in pixel")
parser.add_argument("--stretch", "-s", default=3, help="set stretch-width (pixels left and right of ins)")
parser.add_argument('filenames', metavar='infile', type=str, nargs='+', help='Filenames')


args = parser.parse_args()

print("---------------")
print(args)
print("---------------")
print("args.filenames):", args.filenames)

print("Try to remove lineature from these files:", args.filenames)


for filename in args.filenames:
    print("working on file:", filename)
    try:
        t0 = pc()
        foo = Antikaro(filename, int(args.stretch), int(args.ins))
        t1 = pc()

        foo.remove_lineature()
        outfilename = "linrem_{0}".format(filename)
        foo.save(outfilename)
        print("Resulting file:", outfilename)

    except ValueError:
        print("Error with file {}".format(filename))
        continue
