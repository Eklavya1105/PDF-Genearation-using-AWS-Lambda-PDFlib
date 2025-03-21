#!/usr/bin/python
#
# PDF/A-1b starter:
# Create PDF/A-1b conforming output
#
# Required data: font file, image file

from PDFlib.PDFlib import *

# This is where the data files are. Adjust as necessary.
searchpath = "../data"
imagefile = "nesrin.jpg"
outfilename = "starter_pdfa1b.pdf"

p = None

try:
    p = PDFlib()

    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    p.set_option("SearchPath={{" + searchpath +"}}")

    # PDF/A-1a requires Tagged PDF
    if (p.begin_document(outfilename, "pdfa=PDF/A-1b:2005") == -1):
        raise Exception("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_pdfa1b")

    p.begin_page_ext(0,0, "width=a4.width height=a4.height")

    p.fit_textline("PDF/A-1b:2005 starter", 50, 700, "fontname=NotoSerif-Regular fontsize=24")

    # Load an RGB image
    image = p.load_image("auto", imagefile, "")
    if (image == -1):
        raise Exception("Error: " + p.get_errmsg())

    # Place the image at the bottom of the page
    p.fit_image(image, 0.0, 0.0, "scale=0.5")

    p.end_page_ext("")
    p.close_image(image)

    p.end_document("")

except PDFlibException as ex:
    print("PDFlib exception occurred:")
    print("[%d] %s: %s" % (ex.errnum, ex.apiname, ex.errmsg))

except Exception as ex:
    print(ex)

finally:
    if p:
        p.delete()
