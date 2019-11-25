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

save_nparray_as_pic(bwpicarr, "out.png")
