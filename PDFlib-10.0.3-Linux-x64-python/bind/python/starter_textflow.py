#!/usr/bin/python
#
# Textflow starter:
# Create multi-column text output which may span multiple pages.
# A Web link is inserted with Textflow options and a matchbox.
#
# Required data: font file

from PDFlib.PDFlib import *

# This is where the data files are. Adjust as necessary.
searchpath = "../data"
outfilename = "starter_textflow.pdf"
tf = -1
llx1= 50; lly1=50; urx1=250; ury1=800
llx2=300; lly2=50; urx2=500; ury2=800

# Repeat the dummy text to produce more contents
count = 50

optlist1 = "fontname=NotoSerif-Regular fontsize=10.5 " \
    "leading=125% fillcolor=black alignment=justify"
optlist2 = "fontname=NotoSerif-Regular fontsize=16 " \
    "fillcolor=red charref nounderline"

# Dummy text for filling the columns. Soft hyphens are marked with
# the character reference "&shy;" (character references are
# enabled by the charref option).

text=  \
    "Lorem ipsum dolor sit amet, consectetur adi&shy;pi&shy;sicing elit, " \
    "sed do eius&shy;mod tempor incidi&shy;dunt ut labore et dolore magna " \
    "ali&shy;qua. Ut enim ad minim ve&shy;niam, quis nostrud exer&shy;citation " \
    "ull&shy;amco la&shy;bo&shy;ris nisi ut ali&shy;quip ex ea commodo " \
    "con&shy;sequat. " \
    "Duis aute irure dolor in repre&shy;henderit in voluptate velit esse cillum " \
    "dolore " \
    "eu fugiat nulla pari&shy;atur. Excep&shy;teur sint occae&shy;cat " \
    "cupi&shy;datat " \
    "non proident, sunt in culpa qui officia dese&shy;runt mollit anim id est " \
    "laborum. "

p = None

try:
    p = PDFlib()

    p.set_option("SearchPath={{" + searchpath +"}}")

    # This means we must check return values of load_font() etc.
    p.set_option("errorpolicy=return")

    if (p.begin_document(outfilename, "") == -1):
        raise Exception("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_textflow")

    # Create dummy text and feed it to a Textflow object
    # with alternating options. 

    for i in range(count):
        i += 1
        num = repr(i) + " "

        tf = p.add_textflow(tf, num, optlist2)
        if (tf == -1):
            raise Exception("Error: " + p.get_errmsg())

        # In the first section we include a Web link with Textflow options:
        # - emit URL text and define a matchbox named "link_matchbox" around it;
        #   specify suitable Textflow options, e.g. blue text.
        # - end matchbox
        # The corresponding annotation will be created later with
        # p.create_annotation() using the matchbox name.
        #
        if (i == 1):
            tf = p.add_textflow(tf, "www.pdflib.com",
                    "save fontsize=10.5 fillcolor=blue strokecolor=blue underline " +
                    "matchbox={name=link_matchbox boxheight={ascender descender}}")

            if (tf == -1):
                raise Exception("Error: " + p.get_errmsg())

            tf = p.add_textflow(tf,  " ", "restore matchbox=end nounderline")
            if (tf == -1):
                raise Exception("Error: " + p.get_errmsg())

        tf = p.add_textflow(tf, text, optlist1)
        if (tf == -1):
            raise Exception("Error: " + p.get_errmsg())

    # Loop until all of the text is placed; create new pages
    # as long as more text needs to be placed. Two columns will
    # be created on all pages.

    result = "_boxfull"
    while (result == "_boxfull" or result == "_nextpage"):
        # Add "showborder" to visualize the fitbox borders
        optlist = "verticalalign=justify linespreadlimit=120% "

        p.begin_page_ext(0, 0, "width=a4.width height=a4.height")

        # Fill the first column
        result = p.fit_textflow(tf, llx1, lly1, urx1, ury1, optlist)

        # Fill the second column if we have more text*/
        if (result != "_stop"):
            result = p.fit_textflow(tf, llx2, lly2, urx2, ury2, optlist)

        # Create the Web link based on the named matchbox which
        # was created in the Textflow.

        # Create a "URI" action for the link annotation
        optlist = "url={https://www.pdflib.com}"
        action = p.create_action( "URI", optlist)

        # Coordinates are ignored since we use a matchbox 
        optlist = "usematchbox={link_matchbox} action={activate %d} linewidth=0" % (action)
        p.create_annotation(0, 0, 0, 0, "Link", optlist);

        p.end_page_ext("")

        # "_boxfull" means we must continue because there is more text
        # "_nextpage" is interpreted as "start new column"


    # Check for errors
    if (result != "_stop"):
        # "_boxempty" happens if the box is very small and doesn't
        # hold any text at all.

        if (result == "_boxempty"):
            raise Exception("Error: Textflow box too small")
        else:
            # Any other return value is a user exit caused by
            # the "return" option; this requires dedicated code to
            # deal with.
            raise Exception("User return '" + result + "' found in Textflow")

    p.delete_textflow(tf)

    p.end_document("")

except PDFlibException as ex:
    print("PDFlib exception occurred:")
    print("[%d] %s: %s" % (ex.errnum, ex.apiname, ex.errmsg))

except Exception as ex:
    print(ex)

finally:
    if p:
        p.delete()
