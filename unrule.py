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
    print("length of {:12s}= {}".format(comment, len(data)))
    print("{:10s}{:12s}= {}".format("", comment, data))


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
    #print("conv_avdiff:", conv_avdiff)

    # mean-conv
    meanconv  = np.repeat(1/(2*stretch), stretch)
    conv_mean = np.concatenate((meanconv, inbetween, meanconv))
    mean = np.convolve(array, conv_mean, 'valid')
    #print("conv_mean:  ", conv_mean)

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



    def patch_linedata(self, linedata):
        # for lazy typing
        ins     = self.ins     # length inner part
        stretch = self.stretch # "stretching" each side of inner by stretch

        dlen = len(linedata)

        mvaver    = moving_average(linedata, stretch) # kann spaeter weg
        innermvav = moving_average(linedata[stretch : -stretch], ins)     # kann spaeter weg

        averdiff_arr, newval_arr = moving_average_with_diff(linedata, stretch, ins)

        if False: # need to think about this rounding again
            mvaver        +=  0.5
            innermvav     +=  0.5
            averdiff_arr  +=  0.5
            newval_arr    +=  0.5

        subwin = linedata[stretch : -stretch]

        # find the indexes where changes need to be done
        # (hard coded values, I know it's bad - remove if parametrisation makes sense)
        wo = np.where((averdiff_arr < 10) & (averdiff_arr > -10) &
                      (innermvav - newval_arr > -50) & (innermvav - newval_arr < -1))

        # set new values for all ins entries
        for offset in range(ins):
            bidxa = (offset + wo[0],)
            subwin[bidxa] = newval_arr[wo] # Set the new values

        return linedata



    # Here the main work will be done
    # ===============================
    def remove_lineature(self):

        bwpicarray = self.bwpa
        height, width = bwpicarray.shape

        # for lazy typing
        ins     = self.ins     # length inner part
        stretch = self.stretch # "stretching" each side of inner by stretch
        outs    = self.outs    # whole length of inner + 2 * stretched

        outpicarray = bwpicarray.copy()

        avdiff_low = -20
        avdiff_high = 0
        print("stretch, ins, outs:", self.stretch, self.ins, self.outs)



        #print("whole linedata:\n", bwpicarray)

        # HORIZONTAL
        t0 = pc()
        for yval in range(0, height - outs):

            linedata      = outpicarray[yval]
            linedata = self.patch_linedata(linedata)
            outpicarray[yval] = linedata

        t1 = pc()
        #print("# HORIZONTAL: {:8.3f}".format(t1 - t0), file=sys.stderr, flush=True)

        # VERTIKAL
        for xval in range(0, width - outs):

            linedata      = outpicarray[:,xval]
            linedata = self.patch_linedata(linedata)
            outpicarray[:,xval] = linedata

        t2 = pc()
        #print("# VERTIKAL: {:8.3f}".format(t2 - t1), file=sys.stderr, flush=True)

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
