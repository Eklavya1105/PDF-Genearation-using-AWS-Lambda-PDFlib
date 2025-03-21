# Starter sample for fallback fonts
#
# Required data: suitable fonts

from PDFlib.PDFlib import *

# This is where the data files are. Adjust as necessary.
searchpath = "../data"
outfile = "starter_fallback.pdf"

llx = 30.0
lly = 50.0
urx = 800.0
ury = 570.0

headers = [
    "Use case",
    "Option list for the 'fallbackfonts' option",
    "Base font",
    "With fallback font"
]
    
# expects an array with 4 elements and returns a corresponding dictionary with
# the keys "usecase", "fontname", "encoding", "fallbackoptions", "text"
def make_testcase_dict(x):
  assert len(x) == 4
  return dict(zip(["usecase", "fontname", "fallbackoptions", "text"], x))

testcases = map(
    make_testcase_dict,
    [
    [
      "Add enlarged pictogram",
      "NotoSerif-Regular",
      # U+261E = WHITE RIGHT POINTING INDEX 
      "{fontname=ZapfDingbats forcechars=U+261E fontsize=150% "
      "textrise=-15%}",
      "hand symbol: &#x261E;"
    ],
    [
      "Add enlarged symbol glyph",
      "NotoSerif-Regular",
      "{fontname=Symbol forcechars=U+2663 fontsize=125%}",
       "club symbol: &#x2663;"
    ],
    [ # Greek characters missing in the font will be pulled from Symbol font
      "Add Hebrew characters to Latin font",
      "NotoSerif-Regular",
      "{fontname=NotoSerifHebrew-Regular}",
      "Hebrew: &#x05D0;"
    ],
    ]
)

p = None

try:
    p = PDFlib()

    p.set_option("SearchPath={{" + searchpath +"}}")
    p.set_option("charref=true")
    p.set_option("glyphcheck=replace")

    # This means that formatting and other errors will raise an
    # exception. This simplifies our sample code, but is not
    # recommended for production code.
    p.set_option("errorpolicy=exception")

    # Set an output path according to the name of the topic
    if (p.begin_document(outfile, "") == -1):
        raise Exception("Error: " + p.get_errmsg())

    p.set_info("Creator", "PDFlib starter sample")
    p.set_info("Title", "starter_fallback")

    # Start Page
    p.begin_page_ext(0, 0, "width=a4.height height=a4.width")

    table = -1

    # Table header
    row = 1
    col = 1
    for header in headers:
        optlist = (
         "fittextline={fontname=NotoSerif-Regular fontsize=10} "
         "margin=4")
        table = p.add_table_cell(table, col, row, header, optlist)
        col += 1

    row += 1
    
    # Create fallback samples, one use case per row
    for testcase in testcases:
        col=1

        # Column 1: description of the use case
        optlist = (
            "fittextline={fontname=NotoSerif-Regular fontsize=10} "
            "margin=4")
        table = p.add_table_cell(table, col, row, testcase["usecase"], optlist)

        col += 1
        
        # Column 2: reproduce option list literally
        optlist = (
            "fittextline={fontname=NotoSerif-Regular fontsize=10} "
            "margin=4")
        table = p.add_table_cell(table, col, row, testcase["fallbackoptions"], optlist)

        col += 1
        
        # Column 3: text with base font
        optlist = (
            "fittextline={fontname=%s fontsize=10 "
            "replacementchar=? } margin=4" % (testcase["fontname"]))
        table = p.add_table_cell(table, col, row, testcase["text"], optlist)

        col += 1
        
        # Column 4: text with base font and fallback fonts
        optlist = (
             "fittextline={fontname=%s "
             "fontsize=10 fallbackfonts={%s}} margin=4" %
                 (testcase["fontname"], testcase["fallbackoptions"]))
        table = p.add_table_cell(table, col, row, testcase["text"], optlist)
        
        row += 1

    # Place the table
    optlist = "header=1 fill={{area=rowodd fillcolor={gray 0.9}}} stroke={{line=other}}"
    result = p.fit_table(table, llx, lly, urx, ury, optlist)

    if (result == "_error"):
        raise Exception("Couldn't place table: " + p.get_errmsg())

    p.end_page_ext("")
    p.end_document("")

except PDFlibException as ex:
    print("PDFlib exception occurred:")
    print("[%d] %s: %s" % (ex.errnum, ex.apiname, ex.errmsg))

except Exception as ex:
    print(ex)

finally:
    if p:
        p.delete()
