#!/usr/bin/python
# PDFlib Virtual File system (PVF):
# Create a PVF file which holds an image or PDF, and import the data from the
# PVF file
#
# This avoids disk access and is especially useful when the same image or PDF
# is imported multiply. For examples, images which sit in a database don't
# have to be written and re-read from disk, but can be passed to PDFlib
# directly in memory. A similar technique can be used for loading other data
# such as fonts, ICC profiles, etc.

# This is where the data files are. Adjust as necessary.
searchpath = "../data"
outfile = "starter_pvf.pdf"
# Some constant SVG data as an example for fetching input data from memory
svgdata = \
"<?xml version='1.0'?> \
<svg viewBox='0 0 100 100' version='1.1' xmlns='http://www.w3.org/2000/svg'> \
  <circle cx='50' cy='50' r='40' fill='orange'/> \
</svg>"

from PDFlib.PDFlib import *

p = None

try:
    p = PDFlib()

    p.set_option("SearchPath={{" + searchpath +"}}")

    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    # Set an output path according to the name of the topic
    if p.begin_document(outfile, "") == -1:
        raise Exception("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_pvf")

    p.create_pvf("/pvf/svg", svgdata, "")

    # Load the graphics from the PVF
    svg = p.load_graphics("svg", "/pvf/svg", "")
    if svg == -1:
        raise Exception("Error: " + p.get_errmsg())

    # Fit the graphics on page 1
    p.begin_page_ext(0,0, "width=a4.width height=a4.height")

    p.fit_graphics(svg, 350, 750, "")

    p.end_page_ext("")

    # Fit the graphics on page 2
    p.begin_page_ext(0,0, "width=a4.width height=a4.height")

    p.fit_graphics(svg, 350, 50, "")

    p.end_page_ext("")

    # Delete the virtual file to free the allocated memory
    p.delete_pvf("/pvf/svg")

    p.end_document("")

except PDFlibException as ex:
    print("PDFlib exception occurred:")
    print("[%d] %s: %s" % (ex.errnum, ex.apiname, ex.errmsg))

except Exception as ex:
    print(ex)

finally:
    if p:
        p.delete()
