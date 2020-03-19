# **unrule** - a Program to remove Rulers from your scanned Images

## Name and Functionality of **unrule**
**unrule** removes lineature from an image.

The name is coming from the opposite of rule (like hrule or vrule in TeX, which
mean horizontal rule and vertical rule) and is meant to un-rule, to remove the
rule from the paper.
But it is also a wink on _against the rules_.


## Basic Functionality

The tool uses a tripartite sliding window on the scan lines (horizontal
line of pixels) of an image to decide, if some pixels in the inner window
should be changed to the average of the left and right outer windows.

The inner window is **ins** (for inside) pixels wide.
The left and right outer windows are each **stretch** pixels wide.


# Preconditions

## Packages
numpy,
matplotlib,
PIL (PILLOW) (?)

## Image-Data
The lineature must be aligned with the image, so a rotated scan will very
likely not give useful results.

Also, the paper that was used to develop unrule, so far was white paper.
If the color is different, results may be unsatisfactory. In that case,
please let me know via Github-issues.



# Usage

Call **unrule** on the command line with the filenames as arguments.
There are also two parameters:
    **ins**
and
    **stretch**.


The **ins** parameter is the size in pixels of the inner (inside) window, as described above.
The **stretch** parameter is the size in pixels of the outer area left and right of the inside window.

The default settings are:

**stretch** = 3

**ins** = 3

This gives a complete window size of stretch + ins + stretch = 3 + 3 + 3 = 9.
So the window is 90 pixels, and the inside window-part is 3 pixels wide.

To get useful results, the number of pixels of the lineature (horizontal and/or vertical rule)
is the value that must be set as **ins** value.

If you change the **ins** value much, the **stretch** value very likely must be adapted.
