#!/usr/bin/python
# Table starter:
# Create table which may span multiple pages.
# The table cells are filled with various content types including
# Textflow, Textline, image, SVG, stamp, Web link (annotation) and
# form field.
#
# Required data: image and SVG files, font

from PDFlib.PDFlib import *

# This is where the data files are. Adjust as necessary.
searchpath = "../data"
imagefile = "nesrin.jpg"
graphicsfile = "PDFlib-logo.svg"
outfilename = "starter_table.pdf"

tf=-1; tbl=-1
rowmax = 50; colmax = 4
llx= 50; lly=50; urx=550; ury=800

headertext = "Table header (row 1)"

# Dummy text for filling a cell with multi-line Textflow
tf_text =  \
"Lorem ipsum dolor sit amet, consectetur adi&shy;pi&shy;sicing elit, sed do eius&shy;mod tempor incidi&shy;dunt ut labore et dolore magna ali&shy;qua. Ut enim ad minim ve&shy;niam, quis nostrud exer&shy;citation ull&shy;amco la&shy;bo&shy;ris nisi ut ali&shy;quip ex ea commodo con&shy;sequat. Duis aute irure dolor in repre&shy;henderit in voluptate velit esse cillum dolore eu fugiat nulla pari&shy;atur. Excep&shy;teur sint occae&shy;cat cupi&shy;datat non proident, sunt in culpa qui officia dese&shy;runt mollit anim id est laborum. "

p = None

try:
    p = PDFlib()

    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    p.set_option("SearchPath={{" + searchpath +"}}")

    if (p.begin_document(outfilename, "") == -1):
        raise Exception("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_table")

    # -------------------- Add table cells --------------------

    # ---------- row 1: table header (spans all columns)
    row = 1; col = 1
    font = p.load_font("NotoSerif-Regular", "unicode", "")
    if font == -1:
        raise Exception("Error: " + p.get_errmsg())


    optlist = "fittextline={position=center font=" + repr(font) + " fontsize=14} "+\
        "colspan=" + repr(colmax)

    tbl = p.add_table_cell(tbl, col, row, headertext, optlist)
    if tbl == -1:
        raise Exception("Error adding cell: " + p.get_errmsg())

    # ---------- row 2: various kinds of content
    row += 1; 

    # ----- Simple text cell
    col=1

    optlist = "fittextline={font=" + repr(font) + " fontsize=12 orientate=west}"

    tbl = p.add_table_cell(tbl, col, row, "vertical line", optlist)
    if tbl == -1:
        raise Exception("Error adding cell: " + p.get_errmsg())

    # ----- Colorized background
    col += 1

    optlist = "fittextline={font=" + repr(font) + " fontsize=12 fillcolor=white} " + \
        "matchbox={fillcolor=orange}"

    tbl = p.add_table_cell(tbl, col, row, "colorized cell", optlist)
    if tbl == -1:
        raise Exception("Error adding cell: " + p.get_errmsg())

    # ----- Multi-line text with Textflow
    col += 1

    optlist = "charref fontname=NotoSerif-Regular fontsize=8 alignment=justify"

    tf = p.add_textflow(tf, tf_text, optlist)
    if tf == -1:
        raise Exception("Error: " + p.get_errmsg())

    optlist = "margin=2 textflow=" + repr(tf)

    tbl = p.add_table_cell(tbl, col, row, "", optlist)
    if tbl == -1:
        raise Exception("Error adding cell: " + p.get_errmsg())

    # ----- Rotated image
    col += 1

    image = p.load_image("auto", imagefile, "")
    if (image == -1):
        raise Exception("Couldn't load image: " + p.get_errmsg())

    optlist = "image=" + repr(image) + " fitimage={orientate=west} " \
        "fittextline={fontname=NotoSerif-Regular fontsize=12 fillcolor=white}"

    tbl = p.add_table_cell(tbl, col, row, "rotated image", optlist)
    if tbl == -1:
        raise Exception("Error adding cell: " + p.get_errmsg())

    # ---------- Row 3: various kinds of content 
    row += 1

    # ----- Diagonal stamp
    col = 1

    optlist = "rowheight=50 fittextline={font=" + repr(font) + " fontsize=10 stamp=ll2ur}"

    tbl = p.add_table_cell(tbl, col, row, "diagonal stamp", optlist)
    if tbl == -1:
        raise Exception("Error adding cell: " + p.get_errmsg())

    # ----- SVG graphics 
    col += 1

    # Load the graphics 
    graphics = p.load_graphics("auto", graphicsfile, "")
    if graphics == -1:
        raise Exception("Error: " + p.get_errmsg())
    
    optlist = "margin=5 graphics=" + repr(graphics)

    tbl = p.add_table_cell(tbl, col, row, "", optlist)

    if tbl == -1:
        raise Exception("Error adding cell: " + p.get_errmsg())

    # ----- Annotation: Web link 
    col += 1
    
    action = p.create_action("URI", "url={https://www.pdflib.com}")
    
    optlist =  "margin=5 fittextline={fontname=NotoSerif-Regular fontsize=14 fillcolor=blue} " \
                "annotationtype=Link fitannotation={action={activate " + repr(action) + "} linewidth=0}"

    tbl = p.add_table_cell(tbl, col, row, "Web link", optlist);

    if tbl == -1:
        raise Exception("Error adding cell: " + p.get_errmsg());

    # ----- Form field 
    col += 1
    fieldfont = p.load_font("NotoSerif-Regular", "winansi", "simplefont nosubsetting")

    if fieldfont == -1:
        raise Exception("Error: " + p.get_errmsg());
    
    optlist = "margin=5 fieldtype=textfield fieldname={name} " \
                "fitfield={multiline linewidth=0 font=" + repr(fieldfont) + " fontsize=12 " \
                "alignment=center currentvalue={text field} scrollable=false}"

    tbl = p.add_table_cell(tbl, col, row, "", optlist)

    if tbl == -1:
        raise Exception("Error adding cell: " + p.get_errmsg());

    # ---------- Fill row 3 and above with their numbers
    row += 1
    for row in range(row, rowmax+1):
        for col in range(1, colmax+1):
            num = "Col " + repr(col) + "/Row " + repr(row)
            optlist = "colwidth=25% fittextline={font=" + repr(font) + " fontsize=10}"
            tbl = p.add_table_cell(tbl, col, row, num, optlist)
            if tbl == -1:
                raise Exception("Error adding cell: " + p.get_errmsg())

            col += 1
        row += 1

    # ---------- Place the table on one or more pages ----------

    #
    # Loop until all of the table is placed; create new pages
    # as long as more table instances need to be placed.

    result = "_boxfull"
    while (result == "_boxfull"):
        p.begin_page_ext(0, 0, "width=a4.width height=a4.height")

        # Shade every other row; draw lines for all table cells.
        # Add "showcells showborder" to visualize cell borders 
        optlist = "header=1 rowheightdefault=auto " + \
        "fill={{area=rowodd fillcolor={gray 0.9}}} stroke={{line=other}}"

        # Place the table instance
        result = p.fit_table(tbl, llx, lly, urx, ury, optlist)
        if (result ==  "_error"):
            raise Exception("Couldn't place table: " + p.get_errmsg())

        p.end_page_ext("")


    # Check the result; "_stop" means all is ok.
    if (result != "_stop"):
        if (result ==  "_error"):
            raise Exception("Error when placing table: " + p.get_errmsg())
        else:
            # Any other return value is a user exit caused by
            # the "return" option; this requires dedicated code to
            # deal with.
            raise Exception("User return found in Table")

    # This will also delete Textflow handles used in the table
    p.delete_table(tbl, "")

    p.end_document("")

except PDFlibException as ex:
    print("PDFlib exception occurred:")
    print("[%d] %s: %s" % (ex.errnum, ex.apiname, ex.errmsg))

except Exception as ex:
    print(ex)

finally:
    if p:
        p.delete()
