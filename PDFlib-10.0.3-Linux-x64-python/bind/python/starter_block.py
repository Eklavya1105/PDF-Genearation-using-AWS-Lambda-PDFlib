#!/usr/bin/python
# Block starter:
# Import a PDF page containing Blocks and fill text and image
# Blocks with some data. For each recipient of the simulated
# mailing a separate page with personalized information is
# generated.
#
# The Textflow Blocks are processed with variable text lengths in mind:
# if a Block doesn't fully use its vertical space or requires excess
# space, the next Block is moved up or down accordingly.
#
# Required software: PDFlib Personalization Server (PPS)
# Required data: Block PDF (template), images, fontt

from PDFlib.PDFlib import *
import sys, traceback


def printf(format, *args):
    sys.stdout.write(format % args)
    
# This is where the data files are. Adjust as necessary.
searchpath = "../data"

# By default annotations are also imported. In some cases this
# requires the Noto fonts for creating annotation appearance streams.
fontpath =  "../../resource/font"

outfile = "starter_block.pdf"
infile = "block_template.pdf"

number_of_recipients = 3

# Names and contents of text Blocks

TextBlocks = []
TextBlocks = [ 
    {
        "name": "recipient",
        # address data for each recipient
        "contents": [
            "Mr Maurizio Moroni\nStrada Provinciale 124\nReggio Emilia",
            "Ms Dominique Perrier\n25, Rue Lauriston\nParis",
            "Mr Liu Wong\n55 Grizzly Peak Rd.\nButte"
          ]
    },
    {
        "name": "announcement",
        # greeting for each recipient
        "contents": [
            "Dear Paper Planes Fan,\n\n" 
            "we are happy to present our <fillcolor=red>best price offer" 
            "<fillcolor=black> especially for you:\n",
            
            "Bonjour,\n\n" 
            "here comes your personal <fillcolor=red>best price offer:\n",
            
            "Dear Paper Folder,\n\n" 
            "here's another exciting new paper plane especially for you. " 
            "We can supply this <fillcolor=red>best price offer" 
            "<fillcolor=black> only for a limited time and in limited quantity. " 
            "Don't hesitate and order your new plane today!\n",
        ]
    },
    {
        "name": "specialoffers",
        # personalized offer for each recipient
        "contents": [
            "<fillcolor=red>Long Distance Glider<fillcolor=black>\n" 
            "With this paper rocket you can send all your " 
            "messages even when sitting in a hall or in the cinema pretty near " 
            "the back.\n",
            
            "<fillcolor=red>Giant Wing<fillcolor=black>\n" 
            "An unbelievable sailplane! It is amazingly robust and " 
            "can even do aerobatics. But it is best suited to gliding.\n" 
            "This paper arrow can be thrown with big swing. " 
            "We launched it from the roof of a hotel. It stayed in the air a " 
            "long time and covered a considerable distance.\n",
            
            "<fillcolor=red>Super Dart<fillcolor=black>\n" 
            "The super dart can fly giant loops with a radius of 4 " 
            "or 5 meters and cover very long distances. Its heavy cone point is " 
            "slightly bowed upwards to get the lift required for loops.\n"
        ]
    },
    {
        "name": "goodbye",
        # bye bye phrase for each recipient
        "contents": [
            "Visit us on our Web site at <fillcolor=blue>www.kraxi.com<fillcolor=black>!\n\n" +
            "Yours sincerely,\nVictor Kraxi",
            "Make sure to order quickly at <fillcolor=blue>www.kraxi.com<fillcolor=black> " +
            "since we will soon run out of stock!\n\n" +
            "Yours sincerely,\nVictor Kraxi",

            "Make sure to order soon at <fillcolor=blue>www.kraxi.com<fillcolor=black>!\n\n" +
            "Your friendly staff at Kraxi Systems Paper Planes",
        ]
    }
]
ImageBlocks = []
ImageBlocks = [
    {
        "name": "icon",
        # image file name for each recipient
        "contents": [
            "plane1.png",
            "plane2.png",
            "plane3.png"
        ]
    }
]

p = None

try:
    p = PDFlib()

    p.set_option("SearchPath={{" + searchpath +"}}")
    # This means we must check return values of load_font() etc.
    # Set the search path for fonts and images etc.

    p.set_option("errorpolicy=return SearchPath={{" + searchpath + "}}")
    p.set_option("SearchPath={{" + fontpath + "}}")

    if (p.begin_document(outfile,
        "destination={type=fitwindow} pagelayout=singlepage") == -1):
            raise Exception( "Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_block")

    #  Open the Block template with PDFlib Blocks
    indoc = p.open_pdi_document(infile, "")
    if (indoc == -1):
        raise Exception( "Error: " + p.get_errmsg())
        
    no_of_input_pages = p.pcos_get_number(indoc, "length:pages")
    # Preload all pages of the Block template. We assume a small
    # number of input pages and a large number of generated output
    # pages. Therefore it makes sense to keep the input pages
    # open instead of opening them again for each recipient.
    # Add 1 because we use the 1-based page number as array index.
    pagehandles = {}

    for pageno in range(1, int(no_of_input_pages)+1):
        # Open the first page and clone the page size 
        pagehandles[pageno] = p.open_pdi_page(indoc, pageno, "cloneboxes")
        if (pagehandles[pageno] == -1):
            raise Exception( "Error: " + p.get_errmsg())
   
    # For each recipient: place template page(s) and fill Blocks
    for recipient in range(0, int(number_of_recipients-1)+1):

        # Process all pages of the template document
        for pageno in range(1, int(no_of_input_pages)+1):
            # Accumulated unused or excess space in Textflow Blocks:
            # - if positive, the previous Blocks didn't use their space, so
            #   we move up the Block
            # - if negative, the previous Blocks used excess space, so
            #   we move down the Block
            accumulated_offset_y = 0

            # Start the next output page. The page size will be
            # replaced with the cloned size of the input page.
            p.begin_page_ext(0, 0, "width=a4.width height=a4.height")

            # Place the imported page on the output page, and clone all
            # page boxes which are present in the input page; this will
            # override the dummy size used in begin_page_ext().
            p.fit_pdi_page(pagehandles[pageno], 0, 0, "cloneboxes")

            # Process all Textflow Blocks
            for block in range (len(TextBlocks)):
                # The Textflow Blocks in the template use "fitmethod=nofit"
                # which means we allow the Textflow to overflow the Block.
                baseopt = ""
                optlist = baseopt

                # pCOS path for the current Block 
                blockpath = "pages[" + str(pageno-1) + "]/blocks/" + TextBlocks[block]["name"]

                # Retrieve y coordinate of the Block's lower left corner
                lly = p.pcos_get_number(indoc, blockpath + "/Rect[1]")

                # Adjust the vertical Block position by accumulated offset
                # and make sure we don't fall off the bottom page edge.
                # Similarly we could adjust the horizontal position.
                adjusted_lly = lly + accumulated_offset_y
                if (adjusted_lly < 0):
                    raise Exception("Error for recipient " + recipient + " (input page " + pageno + "): " +
                        "Too much text in Textflow Blocks");

                # The "refpoint" option overrides the Blocks's original
                # position. We use relative coordinates (suffix "r") to move
                # the Block up or down if the previous Blocks didn't use up
                # their area or exceeded the Block area.
                optlist += " refpoint={ 0r " + str(accumulated_offset_y) + "r }"

                # Create a matchbox for the Block contents, using the Block name as matchbox name
                optlist += " matchbox={name={" + TextBlocks[block]["name"] + "}}"
                
                # Fill text Block
                if (p.fill_textblock(pagehandles[pageno], TextBlocks[block]["name"] ,
                    TextBlocks[block]["contents"][recipient], optlist) == -1) :
                    print("Warning: " + p.get_errmsg())
                else:
                    # Calculate the height which wasn't used inside the Block
                    # or was used in excess outside the Block. This will be used
                    # for adjusting the position of the next Block.
                    
                    if (p.info_matchbox(TextBlocks[block]["name"], 1, "exists") == 1) :
                        # We successfully filled a Textflow Block. Retrieve the bottom edge
                        # of the matchbox which gives the vertical end position of the contents...
                        content_lly = p.info_matchbox(TextBlocks[block]["name"], 1, "y1")		# (x1, y1) = lower left corner

                        # ...and use the distance from the bottom edge of the Block as offset
                        accumulated_offset_y += (content_lly - adjusted_lly)
                    else:
                        # If the Block is empty, no corresponding matchbox exists.
                        # We use the Block height as offset to skip the whole Block,
                        # not taking into account possible space between the Blocks.
                        ury = p.pcos_get_number(indoc, blockpath + "/Rect[3]")
                        accumulated_offset_y += (ury - lly)
                    
            # Process all image Blocks
            for imageblock in ImageBlocks:
                image = p.load_image("auto", imageblock["contents"][recipient], "")
                if (image == -1):
                    raise Exception("Error: " + p.get_errmsg())

                # Fill image Block
                if (p.fill_imageblock(pagehandles[pageno], imageblock["name"], image, "") == -1):
                    print("Warning: " + p.get_errmsg())
                p.close_image(image)

            p.end_page_ext("")

    # Close the preloaded template pages
    for pageno in range(1, int(no_of_input_pages)+1):
        p.close_pdi_page(pagehandles[pageno])

    p.close_pdi_document(indoc)

    p.end_document("")

except PDFlibException as ex:
    print("PDFlib exception occurred:")
    print("[%d] %s: %s" % (ex.errnum, ex.apiname, ex.errmsg))

except Exception as ex:
    print(ex)
    traceback.print_tb()

finally:
    if p:
        p.delete()
